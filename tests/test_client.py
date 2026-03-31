from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import BaseModel, Field

from assembly_client.api import AssemblyAPIClient
from assembly_client.errors import AssemblyAPIError

SAMPLE_SPEC = {"OPENSRVAPI": [{"row": [{"INF_ID": "TEST_ID", "INF_NM": "Test Service"}]}]}


class FakeModel(BaseModel):
    """Fake model for testing."""

    HG_NM: str | None = Field(None)
    AGE: str | None = Field(None)


FAKE_MODEL_MAP = {"TEST_SVC_ID": FakeModel}


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"ASSEMBLY_API_KEY": "test_key"}):
        yield


def _make_client_with_mock(mock_env, json_return_value, service_id="TEST_SVC_ID"):
    """Helper: create client with mocked HTTP response."""
    client = AssemblyAPIClient()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = json_return_value
    mock_response.raise_for_status = MagicMock()

    client.get_endpoint = AsyncMock(return_value="test_endpoint")
    client._resolve_service_id = MagicMock(side_effect=lambda x: x)
    client.client.get = AsyncMock(return_value=mock_response)
    return client


# --- Basic tests ---


@pytest.mark.asyncio
async def test_client_init(mock_env):
    client = AssemblyAPIClient()
    assert client.api_key == "test_key"
    assert client.spec_parser is not None


@pytest.mark.asyncio
async def test_get_data_error(mock_env):
    client = _make_client_with_mock(
        mock_env,
        {"test_endpoint": [{"head": [{"RESULT": {"CODE": "INFO-300", "MESSAGE": "Error"}}]}]},
    )

    with pytest.raises(AssemblyAPIError) as exc:
        await client.get_data("TEST_SVC_ID")
    assert "INFO-300" in str(exc.value)


# --- get_data returns list[Model] ---


@pytest.mark.asyncio
async def test_get_data_returns_models(mock_env):
    """get_data() returns list[BaseModel] when generated types available."""
    client = _make_client_with_mock(
        mock_env,
        {
            "test_endpoint": [
                {"head": [{"RESULT": {"CODE": "INFO-000", "MESSAGE": "Success"}}]},
                {"row": [{"HG_NM": "김민석", "AGE": "30"}, {"HG_NM": "이영희", "AGE": "25"}]},
            ]
        },
    )

    with patch("assembly_client.api.HAS_GENERATED_TYPES", True), \
         patch("assembly_client.api.MODEL_MAP", FAKE_MODEL_MAP):
        result = await client.get_data("TEST_SVC_ID")

    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], FakeModel)
    assert result[0].HG_NM == "김민석"
    assert result[1].AGE == "25"


@pytest.mark.asyncio
async def test_get_data_empty_returns_empty_list(mock_env):
    """INFO-200 (no data) returns []."""
    client = _make_client_with_mock(
        mock_env,
        {"RESULT": {"CODE": "INFO-200", "MESSAGE": "해당하는 데이터가 없습니다."}},
    )

    with patch("assembly_client.api.HAS_GENERATED_TYPES", True), \
         patch("assembly_client.api.MODEL_MAP", FAKE_MODEL_MAP):
        result = await client.get_data("TEST_SVC_ID")

    assert result == []


@pytest.mark.asyncio
async def test_get_data_parse_failure_raises(mock_env):
    """Model parsing failure raises AssemblyAPIError, not silent fallback."""

    class StrictModel(BaseModel):
        REQUIRED_FIELD: str  # no default → will fail on missing key

    client = _make_client_with_mock(
        mock_env,
        {
            "test_endpoint": [
                {"head": [{"RESULT": {"CODE": "INFO-000", "MESSAGE": "Success"}}]},
                {"row": [{"WRONG_FIELD": "value"}]},
            ]
        },
    )

    with patch("assembly_client.api.HAS_GENERATED_TYPES", True), \
         patch("assembly_client.api.MODEL_MAP", {"TEST_SVC_ID": StrictModel}):
        with pytest.raises(AssemblyAPIError) as exc:
            await client.get_data("TEST_SVC_ID")
        assert "MODEL_PARSE_ERROR" in str(exc.value)


@pytest.mark.asyncio
async def test_get_data_without_generated_types_returns_dicts(mock_env):
    """Without generated types, get_data() returns list[dict] as fallback."""
    client = _make_client_with_mock(
        mock_env,
        {
            "test_endpoint": [
                {"head": [{"RESULT": {"CODE": "INFO-000", "MESSAGE": "Success"}}]},
                {"row": [{"data": "value"}]},
            ]
        },
    )

    with patch("assembly_client.api.HAS_GENERATED_TYPES", False):
        result = await client.get_data("TEST_SVC_ID")

    assert isinstance(result, list)
    assert result[0] == {"data": "value"}
