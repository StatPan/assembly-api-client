"""Tests for get_all_data async generator method."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from pydantic import BaseModel, Field

from assembly_client.api import AssemblyAPIClient


@pytest.fixture
def client():
    """Create a test client with mocked dependencies."""
    with patch.object(AssemblyAPIClient, "__init__", lambda self, *args, **kwargs: None):
        c = AssemblyAPIClient.__new__(AssemblyAPIClient)
        c.api_key = "test_key"
        c.service_map = {}
        c.name_to_id = {}
        c.parsed_specs = {}
        c._resolve_service_id = MagicMock(side_effect=lambda x: x)
        return c


@pytest.mark.asyncio
async def test_get_all_data_result_only_response(client):
    """Test that RESULT-only responses (INFO-200) return empty result."""
    client._fetch_raw = AsyncMock(return_value={
        "RESULT": {
            "CODE": "INFO-200",
            "MESSAGE": "해당하는 데이터가 없습니다."
        }
    })

    rows_collected = []
    async for rows in client.get_all_data("test_service"):
        rows_collected.extend(rows)

    assert rows_collected == []
    client._fetch_raw.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_data_normal_response_single_page(client):
    """Test normal response with single page of data."""
    client._fetch_raw = AsyncMock(return_value={
        "test_endpoint": [
            {"head": [{"list_total_count": 2}]},
            {"row": [{"id": 1}, {"id": 2}]}
        ]
    })

    rows_collected = []
    with patch("assembly_client.api.HAS_GENERATED_TYPES", False):
        async for rows in client.get_all_data("test_service"):
            rows_collected.extend(rows)

    assert len(rows_collected) == 2
    assert rows_collected[0]["id"] == 1
    assert rows_collected[1]["id"] == 2


@pytest.mark.asyncio
async def test_get_all_data_multiple_pages(client):
    """Test pagination across multiple pages."""
    call_count = 0

    async def mock_fetch_raw(service_id, params, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "test_endpoint": [
                    {"head": [{"list_total_count": 150}]},
                    {"row": [{"id": i} for i in range(100)]}
                ]
            }
        else:
            return {
                "test_endpoint": [
                    {"head": [{"list_total_count": 150}]},
                    {"row": [{"id": i} for i in range(100, 150)]}
                ]
            }

    client._fetch_raw = mock_fetch_raw

    rows_collected = []
    with patch("assembly_client.api.HAS_GENERATED_TYPES", False):
        async for rows in client.get_all_data("test_service", p_size=100):
            rows_collected.extend(rows)

    assert len(rows_collected) == 150
    assert call_count == 2


@pytest.mark.asyncio
async def test_get_all_data_empty_rows(client):
    """Test that empty rows stops iteration."""
    client._fetch_raw = AsyncMock(return_value={
        "test_endpoint": [
            {"head": [{"list_total_count": 0}]},
            {"row": []}
        ]
    })

    rows_collected = []
    with patch("assembly_client.api.HAS_GENERATED_TYPES", False):
        async for rows in client.get_all_data("test_service"):
            rows_collected.extend(rows)

    assert rows_collected == []


@pytest.mark.asyncio
async def test_get_all_data_non_list_content(client):
    """Test that non-list content stops iteration gracefully."""
    client._fetch_raw = AsyncMock(return_value={
        "strange_endpoint": "not a list"
    })

    rows_collected = []
    with patch("assembly_client.api.HAS_GENERATED_TYPES", False):
        async for rows in client.get_all_data("test_service"):
            rows_collected.extend(rows)

    assert rows_collected == []


@pytest.mark.asyncio
async def test_get_all_data_missing_head(client):
    """Test graceful handling when head is missing list_total_count."""
    client._fetch_raw = AsyncMock(return_value={
        "test_endpoint": [
            {"head": []},  # No list_total_count
            {"row": [{"id": 1}]}
        ]
    })

    rows_collected = []
    with patch("assembly_client.api.HAS_GENERATED_TYPES", False):
        async for rows in client.get_all_data("test_service"):
            rows_collected.extend(rows)

    # Should still return the row, just can't paginate intelligently
    assert len(rows_collected) == 1


# --- Pydantic model parsing in get_all_data ---


class PaginationModel(BaseModel):
    """Model for pagination Pydantic tests."""
    id: int | None = Field(None)
    name: str | None = Field(None)


PAGINATION_MODEL_MAP = {"TEST_SVC": PaginationModel}


@pytest.mark.asyncio
async def test_get_all_data_returns_pydantic_models(client):
    """get_all_data yields list[BaseModel] when generated types available."""
    client._fetch_raw = AsyncMock(return_value={
        "test_endpoint": [
            {"head": [{"list_total_count": 2}]},
            {"row": [{"id": 1, "name": "김민석"}, {"id": 2, "name": "이영희"}]}
        ]
    })

    rows_collected = []
    with patch("assembly_client.api.HAS_GENERATED_TYPES", True), \
         patch("assembly_client.api.MODEL_MAP", PAGINATION_MODEL_MAP):
        async for rows in client.get_all_data("TEST_SVC"):
            rows_collected.extend(rows)

    assert len(rows_collected) == 2
    assert isinstance(rows_collected[0], PaginationModel)
    assert rows_collected[0].name == "김민석"
    assert rows_collected[1].id == 2


@pytest.mark.asyncio
async def test_get_all_data_pydantic_multiple_pages(client):
    """get_all_data yields Pydantic models across multiple pages."""
    call_count = 0

    async def mock_fetch_raw(service_id, params, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "test_endpoint": [
                    {"head": [{"list_total_count": 3}]},
                    {"row": [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]}
                ]
            }
        else:
            return {
                "test_endpoint": [
                    {"head": [{"list_total_count": 3}]},
                    {"row": [{"id": 3, "name": "C"}]}
                ]
            }

    client._fetch_raw = mock_fetch_raw

    rows_collected = []
    with patch("assembly_client.api.HAS_GENERATED_TYPES", True), \
         patch("assembly_client.api.MODEL_MAP", PAGINATION_MODEL_MAP):
        async for rows in client.get_all_data("TEST_SVC", p_size=2):
            rows_collected.extend(rows)

    assert len(rows_collected) == 3
    assert all(isinstance(r, PaginationModel) for r in rows_collected)
    assert call_count == 2
