# Assembly API Client

A Python client for the [Korean National Assembly Open API](https://open.assembly.go.kr/).

## Features

- **Automatic Spec Parsing**: Automatically downloads and parses Excel specifications from the Open API portal to determine endpoints and parameters.
- **Dynamic Endpoint Resolution**: Handles the mapping between Service IDs (e.g., `OK7XM1000938DS17215`) and actual API endpoints.
- **Async Support**: Built with `httpx` for high-performance asynchronous HTTP requests.
- **Caching**: Caches parsed specifications locally to minimize overhead.

## Installation

```bash
pip install assembly-api-client
```

## Usage

```python
import asyncio
from assembly_client import AssemblyAPIClient

async def main():
    # Initialize client (API key is optional for some endpoints but recommended)
    client = AssemblyAPIClient(api_key="YOUR_API_KEY")

    try:
        # Fetch data using Service ID
        # Example: National Assembly Bill Information
        service_id = "OK7XM1000938DS17215" 
        data = await client.get_data(service_id, params={"pSize": 5})
        print(data)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## License

MIT
