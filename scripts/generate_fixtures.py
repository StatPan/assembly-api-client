import asyncio
import json
import os
import logging
from pathlib import Path
from assembly_client.api import AssemblyAPIClient, AssemblyAPIError
from assembly_client.generated import Service, PARAM_MAP

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load key from env
API_KEY = os.getenv("ASSEMBLY_API_KEY")
if not API_KEY:
    try:
        with open(".env") as f:
            for line in f:
                if line.startswith("ASSEMBLY_API_KEY="):
                    API_KEY = line.strip().split("=")[1]
                    break
    except FileNotFoundError:
        pass

if not API_KEY:
    raise ValueError("ASSEMBLY_API_KEY not found")

FIXTURE_DIR = Path("tests/fixtures")
FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

async def fetch_fixture(client: AssemblyAPIClient, service: Service):
    filename = f"{service.name}.json"
    filepath = FIXTURE_DIR / filename
    
    if filepath.exists():
        logger.info(f"Skipping {service.name} (already exists)")
        return

    logger.info(f"Fetching {service.name}...")
    
    # Default params that might work for many services
    params = {
        "pSize": 1,
        "AGE": "21", # 21st Assembly
        "UNIT_CD": "100021", # Sometimes needed
    }
    
    # Try to be smarter? 
    # We could check PARAM_MAP[service.value] to see required fields.
    # But for now, let's just try with defaults and see what sticks.
    
    try:
        # Use internal client to get raw JSON
        endpoint = await client.get_endpoint(service.value)
        url = f"{client.BASE_URL}/{endpoint}"
        
        request_params = {
            "KEY": client.api_key,
            "Type": "json",
            "pIndex": 1,
        }
        request_params.update(params)
        
        response = await client.client.get(url, params=request_params)
        response.raise_for_status()
        data = response.json()
        
        # Check for API error in response body (INFO-xxx is usually success or no data)
        # But if it's an ERROR code, we might want to know.
        # The API returns errors in <head> usually.
        
        # Save to file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {filename}")
        
    except Exception as e:
        logger.error(f"Failed to fetch {service.name}: {e}")

async def main():
    async with AssemblyAPIClient(api_key=API_KEY) as client:
        # Iterate over all services
        tasks = []
        sem = asyncio.Semaphore(5) # Limit concurrency to avoid rate limits
        
        async def bound_fetch(s):
            async with sem:
                await fetch_fixture(client, s)
                await asyncio.sleep(0.1) # Be nice to the server

        for service in Service:
            tasks.append(bound_fetch(service))
            
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
