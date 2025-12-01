import asyncio
import logging
from typing import Any, Dict, Optional, Union

import httpx

from .exceptions import AssemblyAPIError, SpecParseError
from .models import APISpec
from .spec_parser import SpecParser

logger = logging.getLogger("assembly_client.client")


class AssemblyAPIClient:
    """Client for Korean National Assembly Open API."""

    BASE_URL = "https://open.assembly.go.kr/portal/openapi"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

        if not self.api_key:
            # Warning only, as some APIs might work without key or for testing
            logger.warning("ASSEMBLY_API_KEY is not provided.")

        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
        self.spec_parser = SpecParser()
        self.parsed_specs: Dict[str, APISpec] = {}

    async def close(self):
        await self.client.aclose()

    async def get_endpoint(self, service_id: str) -> str:
        """
        Get the actual API endpoint for a service ID.
        """
        if service_id not in self.parsed_specs:
            logger.info("Parsing spec", extra={"service_id": service_id})
            # Default inf_seq to 2 as per original logic
            spec = await self.spec_parser.parse_spec(service_id, inf_seq=2)
            self.parsed_specs[service_id] = spec

        return self.parsed_specs[service_id].endpoint

    async def get_data(
        self,
        service_id: str,
        params: Optional[Dict[str, Any]] = None,
        fmt: str = "json",
    ) -> Union[Dict[str, Any], str]:
        """
        Fetch data from the API using dynamic endpoint resolution.

        Args:
            service_id: The API service ID (e.g., 'OK7XM1000938DS17215').
            params: Query parameters.
            fmt: Response format ('json' or 'xml').

        Returns:
            Parsed JSON dict or raw XML string.
        """
        # Get actual endpoint from Excel spec
        try:
            endpoint = await self.get_endpoint(service_id)
        except SpecParseError as e:
            logger.error(f"Failed to get endpoint for {service_id}: {e}")
            raise

        # Build URL with actual endpoint
        url = f"{self.BASE_URL}/{endpoint}"

        # Add format parameter using Type param
        default_params = {
            "Type": fmt.lower(),
            "pIndex": 1,
            "pSize": 100,
        }
        if self.api_key:
            default_params["KEY"] = self.api_key

        merged_params = {**default_params, **(params or {})}

        # Retry logic (simple loop)
        max_attempts = 3
        last_exception = None

        for attempt in range(1, max_attempts + 1):
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
                logger.warning(
                    f"HTTP error (attempt {attempt}/{max_attempts}): {e.response.status_code}"
                )
                last_exception = e
                if e.response.status_code in [429, 500, 502, 503, 504]:
                    await asyncio.sleep(2 ** (attempt - 1))
                    continue
                raise
            except (httpx.NetworkError, httpx.TimeoutException) as e:
                logger.warning(f"Network error (attempt {attempt}/{max_attempts}): {e}")
                last_exception = e
                await asyncio.sleep(2 ** (attempt - 1))
                continue
            except AssemblyAPIError as e:
                # API logic error, do not retry unless specific codes (not implemented here)
                raise e
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise e

        raise last_exception or Exception("Max retry attempts reached")

    def _check_api_error(self, data: Dict[str, Any], service_id: str):
        """Check for API specific error codes."""
        # Expected structure: { service_id: [ { "head": [ ... { "RESULT": ... } ] }, ... ] }
        if service_id in data:
            items = data[service_id]
            # Items is a list. Usually item 0 is head, item 1 is row.
            # But sometimes it might be different.
            # We iterate to find "head".
            for item in items:
                if "head" in item:
                    for head_item in item["head"]:
                        if "RESULT" in head_item:
                            result = head_item["RESULT"]
                            code = result.get("CODE")
                            message = result.get("MESSAGE")

                            if code in ["INFO-200", "INFO-290", "INFO-300", "INFO-337"]:
                                logger.info(f"API Info: {code} - {message}")
                                if code == "INFO-200":
                                    return  # No data is valid result
                                raise AssemblyAPIError(code, message)

                            if code != "INFO-000":
                                raise AssemblyAPIError(code, message)
