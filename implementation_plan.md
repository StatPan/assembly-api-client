# Assembly API Client Implementation Plan

## Objective
Create a standalone, robust Python library (`assembly-api-client`) for the Korean National Assembly Open API. This library will:
1.  **Core Client**: Provide a generic `AssemblyAPIClient` that handles authentication, dynamic spec parsing, and request execution.
2.  **Spec Management**: Include logic to automatically download, parse (from Excel), and cache API specifications (`SpecParser`).
3.  **Sync Capability**: Provide tools (CLI/Module) to synchronize local spec caches with the latest versions from the Assembly portal.
4.  **Reusability**: Be easily installable and usable in other projects (e.g., Airflow data collectors, MCP servers).

## Repository Structure
We will restructure the code into a proper Python package layout.

```text
assembly-api-client/
├── pyproject.toml          # Build configuration (Hatchling) and dependencies
├── README.md               # Documentation
├── src/
│   └── assembly_client/    # Main package
│       ├── __init__.py     # Exports AssemblyAPIClient
│       ├── api.py          # Core client logic (refactored from client.py)
│       ├── parser.py       # Spec parsing logic (refactored from spec_parser.py)
│       ├── sync.py         # Spec synchronization logic (refactored from sync_specs.py)
│       ├── models.py       # Pydantic models for common data types (Bill, Committee)
│       └── cli.py          # CLI entry point (e.g., `assembly-client sync`)
└── tests/                  # Unit tests
```

## Implementation Steps

### Phase 1: Project Initialization
1.  **Setup `pyproject.toml`**: Define the project metadata, dependencies (`httpx`, `openpyxl`, `pydantic`, `tenacity`, `typer`, `platformdirs`), and build system (`hatchling`).
2.  **Create Directory Structure**: Set up `src/assembly_client` and `tests`.

### Phase 2: Core Logic Migration & Refactoring
1.  **Port `SpecParser` (`parser.py`)**:
    *   Move `SpecParser` logic from `AssemblyMCP`.
    *   **Improvement**: Use `platformdirs` to determine the default cache directory (e.g., `~/.cache/assembly-api-client/specs`) instead of a hardcoded path or temp dir.
    *   **Improvement**: Ensure `SpecParseError` is exported and well-defined.
    *   Keep the Excel parsing logic using `openpyxl` as documented in `SPEC_PARSER.md`.
2.  **Port `AssemblyAPIClient` (`api.py`)**:
    *   Move `AssemblyAPIClient` logic.
    *   Refactor to accept a `SpecParser` instance or configuration.
    *   **Improvement**: Ensure `AssemblyAPIError` captures the specific error codes (INFO-200, etc.) mentioned in `client.py`.
    *   Maintain the `get_data` method signature but ensure it returns typed data if possible (or raw dicts/strings as it currently does).
3.  **Port Sync Logic (`sync.py`)**:
    *   Convert `sync_specs.py` into a reusable module `sync.py`.
    *   Allow syncing specific services or the master list programmatically.
    *   Ensure it uses the same `SpecParser` configuration.

### Phase 3: Models & CLI
1.  **Expose Models (`models.py`)**:
    *   Port `models.py` to provide standard Pydantic models (`Bill`, `Member`, `Committee`, `MeetingRecord`) for consumers.
    *   These models will serve as the "data contract" for the library.
2.  **Create CLI (`cli.py`)**:
    *   Implement a simple CLI using `typer`.
    *   Commands:
        *   `sync`: Download/update specs (wraps `sync.py`).
        *   `list`: Show available APIs (from master list).
        *   `info [service_id]`: Show spec details for a service.
        *   `search [keyword]`: Search for APIs by name.

### Phase 4: Verification
1.  **Unit Tests**: Port existing tests from `AssemblyMCP/tests` and ensure they pass in the new structure.
2.  **Integration Test**: Create a script to install the package locally and verify it can fetch data (e.g., a simple "Hello World" fetching a bill).

## Phase 2: Type-Safety & Code Generation (Current Focus)

To maximize developer experience (DX) and robustness, we will move from dynamic runtime parsing to **ahead-of-time code generation**.

### 1. Code Generation Strategy
We will create a `codegen` module that:
1.  **Reads Specs**: Iterates over all cached JSON specs (or downloads them).
2.  **Generates `services.py`**: A massive `StrEnum` containing all available services.
    ```python
    class Service(StrEnum):
        BILL_INFO = "OK7XM1000938DS17215"  # 국회의원발의법률안
        MEETING_RECORD = "..."
    ```
3.  **Generates Pydantic Models**:
    *   For each service, generate a Pydantic model representing its response structure.
    *   Use the "output fields" from the Excel spec (if available) or infer from sample data.
    *   Store in `src/assembly_client/generated/models.py` or separate files.

### 2. Client Refactoring
*   Update `AssemblyAPIClient` to accept `Service` enum members.
*   `get_data` should automatically return the correct Pydantic model instance based on the service.

### 3. Robust Testing
*   **Fixtures**: Capture real API responses (sanitized) and store them as JSON fixtures.
*   **Tests**: Verify that the generated models correctly parse these real-world fixtures.

### 4. Typed Request Parameters
*   **Generate `Params_...` Models**: Similar to response models, generate Pydantic models for request arguments.
    *   Required params -> Required fields.
    *   Optional params -> Optional fields.
*   **Usage**:
    ```python
    params = Params_BILL_INFO(AGE="21")
    client.get_data(Service.BILL_INFO, params=params)
    ```

## Future Usage
*   **Airflow**: Install this package in the Airflow environment. Use `AssemblyAPIClient` in PythonOperators to fetch data.
*   **MCP Server**: Create a separate project (or sub-package) that imports `assembly_client` and wraps it in an MCP server, exposing the dynamic tools.

## Dependencies
*   `httpx`: Async HTTP client.
*   `openpyxl`: For parsing Excel specs.
*   `pydantic`: For data validation and models.
*   `tenacity`: For retry logic.
*   `typer`: For the CLI.
*   `platformdirs`: For determining standard cache directories (optional but recommended).
