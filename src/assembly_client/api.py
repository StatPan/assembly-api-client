import logging
import os
from typing import Any

import httpx
from pydantic import BaseModel
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from .errors import AssemblyAPIError, SpecParseError
from .parser import APISpec, SpecParser, load_service_map, load_service_metadata

# Try to import generated types, but don't fail if not generated yet
try:
    from .generated import MODEL_MAP, Service

    HAS_GENERATED_TYPES = True
except ImportError:
    HAS_GENERATED_TYPES = False
    Service = None
    MODEL_MAP = {}


# Configure logging
logger = logging.getLogger(__name__)


def _is_retryable_error(exception):
    """Check if the exception is retryable."""
    if isinstance(exception, (httpx.NetworkError, httpx.TimeoutException)):
        return True
    if isinstance(exception, httpx.HTTPStatusError):
        return exception.response.status_code in [429, 500, 502, 503, 504]
    return False


class AssemblyAPIClient:
    """Client for Korean National Assembly Open API."""

    BASE_URL = "https://open.assembly.go.kr/portal/openapi"

    def __init__(self, api_key: str | None = None, spec_parser: SpecParser | None = None):
        """
        Initialize the Assembly API Client.

        Args:
            api_key: API Key. If None, tries to read from ASSEMBLY_API_KEY env var.
            spec_parser: Instance of SpecParser. If None, creates a default one.
        """
        self.api_key = api_key or os.getenv("ASSEMBLY_API_KEY")

        if not self.api_key:
            logger.warning("ASSEMBLY_API_KEY is not set. Some APIs may fail.")

        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
        self.spec_parser = spec_parser or SpecParser()
        self.parsed_specs: dict[str, APISpec] = {}

        # Load service map (ID -> Name) for name resolution
        self.service_map = load_service_map(self.spec_parser.cache_dir)
        # Create reverse map (Name -> ID)
        self.name_to_id = {name: sid for sid, name in self.service_map.items()}

        # Load comprehensive service metadata
        self.service_metadata = load_service_metadata(self.spec_parser.cache_dir)

    def search_services(self, keyword: str) -> dict[str, str]:
        """
        Search for services by name or ID.

        Args:
            keyword: Search term (case-insensitive).

        Returns:
            Dictionary of {service_id: service_name}
        """
        results = {}
        keyword = keyword.lower()
        for sid, name in self.service_map.items():
            if keyword in sid.lower() or keyword in name.lower():
                results[sid] = name
        return results

    def _resolve_service_id(self, service_id_or_name: str) -> str:
        """Resolve a string to a Service ID."""
        # 1. Check if it's a known ID
        if service_id_or_name in self.service_map:
            return service_id_or_name

        # 2. Check if it's a known Name
        if service_id_or_name in self.name_to_id:
            return self.name_to_id[service_id_or_name]

        # 3. If it looks like an ID (alphanumeric, long), assume it's an ID
        # (Even if not in our cache, maybe it's new?)
        if len(service_id_or_name) > 10 and service_id_or_name.isalnum():
            return service_id_or_name

        raise AssemblyAPIError("INVALID_ID", f"Could not resolve service: {service_id_or_name}")

    async def close(self):
        """Close the underlying HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def get_endpoint(self, service_id: str) -> str:
        """
        Get the actual API endpoint for a service ID.

        Args:
            service_id: The service ID

        Returns:
            The endpoint string

        Raises:
            SpecParseError: If spec parsing fails
        """
        if service_id not in self.parsed_specs:
            logger.debug(f"Resolving endpoint for {service_id}")

            # We don't have the master list loaded here to check for infSeq.
            # But SpecParser defaults to infSeq=2 which works for most.
            # If we need robust infSeq handling, we might need to look it up from a master list.
            # For now, we'll stick to the default behavior of the original client
            # which tried to look it up from self.specs (which was loaded from all_apis.json).

            # TODO: Consider loading all_apis.json if it exists to get hints like infSeq.

            spec = await self.spec_parser.parse_spec(service_id)
            self.parsed_specs[service_id] = spec

        return self.parsed_specs[service_id].endpoint

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception(_is_retryable_error),
    )
    async def _fetch_raw(
        self,
        service_id: str,
        params: dict[str, Any] | None = None,
        fmt: str = "json",
    ) -> dict[str, Any] | str:
        """
        Internal: fetch raw API response as dict (JSON) or str (XML).

        Handles endpoint resolution, HTTP call, and API error checking.
        """
        try:
            endpoint = await self.get_endpoint(service_id)
        except SpecParseError as e:
            logger.error(f"Failed to get endpoint for {service_id}: {e}")
            raise

        url = f"{self.BASE_URL}/{endpoint}"
        default_params = {
            "KEY": self.api_key,
            "Type": fmt.lower(),
            "pIndex": 1,
            "pSize": 100,
        }
        merged_params = {**default_params, **(params or {})}

        try:
            response = await self.client.get(url, params=merged_params)
            response.raise_for_status()

            if fmt.lower() == "json":
                data = response.json()
                self._check_api_error(data, endpoint)
                return data
            else:
                return response.text

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise AssemblyAPIError(str(e.response.status_code), str(e)) from e
        except (AssemblyAPIError, SpecParseError):
            raise
        except Exception as e:
            logger.error(f"API request failed: {e}")
            raise AssemblyAPIError("UNKNOWN", str(e)) from e

    async def get_data(
        self,
        service_id_or_name: str | Service,
        params: dict[str, Any] | BaseModel = None,
        fmt: str = "json",
    ) -> list[BaseModel] | str:
        """
        Fetch data from the API using dynamic endpoint resolution.

        Returns a list of typed Pydantic models (for JSON) or str (for XML).
        If generated types are not available, falls back to list of raw dicts.

        Args:
            service_id_or_name: The API service ID, Service Name, or Service Enum member.
            params: Query parameters.
            fmt: Response format ('json' or 'xml').

        Returns:
            list[BaseModel] for JSON responses (or list[dict] without generated types),
            str for XML. Empty list [] when API returns no data (INFO-200).

        Raises:
            SpecParseError: If endpoint resolution fails
            AssemblyAPIError: If API returns an error or model parsing fails
        """
        # Resolve ID
        if HAS_GENERATED_TYPES and isinstance(service_id_or_name, Service):
            service_id = service_id_or_name.value
        else:
            service_id = self._resolve_service_id(service_id_or_name)

        # Handle Pydantic Params
        if isinstance(params, BaseModel):
            params = params.model_dump(by_alias=True, exclude_none=True)

        data = await self._fetch_raw(service_id, params, fmt)

        if isinstance(data, str):
            return data

        return self._parse_response(data, service_id)

    def _parse_response(
        self, data: dict[str, Any], service_id: str
    ) -> list[BaseModel] | list[dict[str, Any]]:
        """
        Parse API JSON response into a list of Pydantic models.

        Falls back to list of raw dicts if generated types are unavailable.
        Returns [] for empty/no-data responses.
        Raises AssemblyAPIError on parse failure (no silent fallback).
        """
        # Find the response key containing rows
        target_key = service_id
        if service_id not in data:
            for key, val in data.items():
                if isinstance(val, list) and len(val) >= 2 and "row" in val[1]:
                    target_key = key
                    break

        if target_key not in data:
            return []

        items = data[target_key][1].get("row", [])
        if not items:
            return []

        # If no generated types, return raw dicts
        if not HAS_GENERATED_TYPES or service_id not in MODEL_MAP:
            return items

        model_cls = MODEL_MAP[service_id]
        try:
            return [model_cls(**row) for row in items]
        except Exception as e:
            raise AssemblyAPIError(
                "MODEL_PARSE_ERROR",
                f"Failed to parse response into {model_cls.__name__}: {e}",
            ) from e

    async def get_all_data(
        self,
        service_id_or_name: str | Service,
        params: dict[str, Any] | BaseModel = None,
        p_size: int = 100,
    ):
        """
        Fetch all pages of data from the API with automatic pagination.

        Yields a list of Pydantic models (or raw dicts) per page.
        For INFO-200 (no data) responses, yields nothing and exits cleanly.

        Args:
            service_id_or_name: The API service ID, Service Name, or Service Enum member.
            params: Query parameters (pIndex/pSize will be managed internally).
            p_size: Page size for pagination (default: 100).

        Yields:
            list[BaseModel]: Models from each page (or list[dict] without generated types).

        Example:
            async for rows in client.get_all_data("ServiceName"):
                for row in rows:
                    process(row)
        """
        # Resolve ID once
        if HAS_GENERATED_TYPES and isinstance(service_id_or_name, Service):
            service_id = service_id_or_name.value
        else:
            service_id = self._resolve_service_id(service_id_or_name)

        # Handle Pydantic Params once
        if isinstance(params, BaseModel):
            params = params.model_dump(by_alias=True, exclude_none=True)
        else:
            params = dict(params) if params else {}

        p_index = 1

        while True:
            try:
                page_params = {**params, "pIndex": p_index, "pSize": p_size}
                data = await self._fetch_raw(service_id, page_params)

                if not isinstance(data, dict):
                    logger.warning(f"Unexpected response type: {type(data)}")
                    break

                # Get root key (endpoint name or "RESULT")
                root_key = next(iter(data.keys()), None)
                if not root_key:
                    break

                # Handle RESULT-only response (INFO-200: no data)
                if root_key == "RESULT":
                    logger.debug(f"RESULT-only response: {data.get('RESULT', {})}")
                    break

                res_content = data.get(root_key)

                # Validate response structure: should be list with [head, row]
                if not isinstance(res_content, list) or len(res_content) < 2:
                    logger.warning(f"Unexpected response structure for {root_key}")
                    break

                # Extract total count from head
                total_count = 0
                try:
                    head = res_content[0].get("head", [])
                    for h in head:
                        if "list_total_count" in h:
                            total_count = int(h["list_total_count"])
                            break
                except (KeyError, IndexError, ValueError, TypeError) as e:
                    logger.debug(f"Could not extract total_count: {e}")

                # Parse rows into models
                rows = self._parse_response(data, service_id)
                if not rows:
                    break

                yield rows

                # Check if we've fetched all data
                fetched_count = p_index * p_size
                if total_count and fetched_count >= total_count:
                    break

                if len(rows) < p_size:
                    break

                p_index += 1

            except (KeyError, IndexError, ValueError, TypeError) as e:
                logger.error(f"Pagination parsing error at page {p_index}: {e}")
                break

    def _check_api_error(self, data: dict[str, Any], endpoint: str):
        """Check for API specific error codes."""
        # The response key is usually the endpoint name (e.g. "nzmimeepazxkubdpn")

        if endpoint in data:
            items = data[endpoint]
            for item in items:
                if "head" in item:
                    for head_item in item["head"]:
                        if "RESULT" in head_item:
                            result = head_item["RESULT"]
                            code = result.get("CODE")
                            message = result.get("MESSAGE")

                            # Check for specific error codes
                            if code in ["INFO-200", "INFO-290", "INFO-300", "INFO-337"]:
                                logger.info(f"API Result: {code} - {message}")
                                if code == "INFO-200":
                                    return  # No data is valid result
                                raise AssemblyAPIError(code, message)

                            if code != "INFO-000":
                                raise AssemblyAPIError(code, message)
