---
name: dados-gov-br
description: Access Brazilian government open data through the dados.gov.br REST API. Search, list, and retrieve public datasets, organizations, groups, and tags. Includes token authentication, JSON responses, and integration patterns for federal government data.
---

## When to Use This Skill

Use this skill when you need to work with the Brazilian Open Data Portal API (dados.gov.br), including:
- Searching and retrieving Brazilian government datasets
- Accessing public data from federal organizations
- Building applications that consume open government data
- Integrating Brazilian federal data into systems and dashboards
- Exploring available datasets, organizations, groups, and tags
- Implementing data-driven applications using government sources

## Overview

The **Portal Brasileiro de Dados Abertos** (Brazilian Open Data Portal) provides a REST API for accessing information about public datasets available from the Brazilian federal government. The API follows REST standards and returns data in JSON format.

**Legal Framework:**
- Law No. 12,527/2011 (Access to Information Law)
- Decree No. 8,777/2016 (Open Data Policy for Federal Public Administration)

**Key Resources:**
- Production API: https://dados.gov.br/swagger-ui/index.html
- Homologation API: https://hmg.dados.gov.br/swagger-ui/index.html
- API Catalog: https://www.gov.br/conecta/catalogo/apis/api-portal-de-dados-abertos
- Main Portal: https://dados.gov.br
- GitHub: https://github.com/dadosgovbr

## Installation

### Prerequisites

- No installation required - this is a REST API
- HTTP client library (requests, axios, fetch, etc.)
- API token (generated through dados.gov.br portal)
- Python 3.6+ (for Python examples) or any language with HTTP support

### Python Setup

```bash
# Install requests library for HTTP calls
pip install requests

# Optional: Install for async support
pip install aiohttp
```

### JavaScript/Node.js Setup

```bash
# Install axios for HTTP calls
npm install axios

# Or use built-in fetch (Node.js 18+)
```

## Quick Start

### Getting an API Token

1. Access https://dados.gov.br
2. Register or log in to your account
3. Navigate to API settings
4. Generate your authentication token
5. Store the token securely (environment variable recommended)

### Basic Python Example

```python
import requests

# Configuration
API_BASE_URL = "https://dados.gov.br/api/3/action"
API_TOKEN = "your-token-here"  # Get from dados.gov.br

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Search for datasets
def search_datasets(query, rows=10):
    endpoint = f"{API_BASE_URL}/package_search"
    params = {
        "q": query,
        "rows": rows
    }

    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()

    return response.json()

# Example: Search for health datasets
results = search_datasets("saúde")
print(f"Found {results['result']['count']} datasets")

for dataset in results['result']['results']:
    print(f"- {dataset['title']}")
```

### Basic JavaScript Example

```javascript
const axios = require('axios');

const API_BASE_URL = 'https://dados.gov.br/api/3/action';
const API_TOKEN = process.env.DADOS_GOV_TOKEN;

const headers = {
    'Authorization': `Bearer ${API_TOKEN}`,
    'Content-Type': 'application/json'
};

// Search for datasets
async function searchDatasets(query, rows = 10) {
    const endpoint = `${API_BASE_URL}/package_search`;

    const response = await axios.get(endpoint, {
        headers,
        params: { q: query, rows }
    });

    return response.data;
}

// Example: Search for education datasets
searchDatasets('educação')
    .then(data => {
        console.log(`Found ${data.result.count} datasets`);
        data.result.results.forEach(dataset => {
            console.log(`- ${dataset.title}`);
        });
    })
    .catch(error => console.error('Error:', error));
```

## Core Concepts

### Architecture

The dados.gov.br API is built on CKAN (Comprehensive Knowledge Archive Network), an open-source data portal platform. It follows RESTful architecture principles with JSON responses.

**Base URLs:**
- Production: `https://dados.gov.br/api/3/action`
- Homologation: `https://hmg.dados.gov.br/api/3/action`

### Key Entities

1. **Datasets (Packages)**: Collections of data resources with metadata
   - Title, description, tags, organization
   - Creation/modification dates
   - License information
   - Resources (data files, APIs, etc.)

2. **Organizations**: Government entities that publish datasets
   - Federal ministries and agencies
   - Public institutions
   - Government departments

3. **Groups**: Thematic categorization of datasets
   - Health, Education, Transportation, etc.
   - Cross-organization topic areas

4. **Tags**: Keywords for dataset discovery
   - Searchable metadata
   - Helps with dataset classification

5. **Resources**: Actual data files or endpoints
   - CSV, JSON, XML files
   - APIs, web services
   - Documentation links

### API Endpoints

The API provides several action endpoints:

**Search & Discovery:**
- `package_search` - Search datasets
- `package_list` - List all dataset names
- `package_show` - Get dataset details
- `current_package_list_with_resources` - List datasets with resources

**Organizations:**
- `organization_list` - List all organizations
- `organization_show` - Get organization details

**Groups:**
- `group_list` - List all groups
- `group_show` - Get group details

**Tags:**
- `tag_list` - List all tags
- `tag_show` - Get tag details

**Resources:**
- `resource_show` - Get resource details
- `resource_search` - Search resources

## Configuration

### Basic Configuration

```python
# config.py
import os

class DadosGovBRConfig:
    """Configuration for dados.gov.br API"""

    # API Settings
    BASE_URL = "https://dados.gov.br/api/3/action"
    HOMOLOG_URL = "https://hmg.dados.gov.br/api/3/action"

    # Authentication
    API_TOKEN = os.getenv("DADOS_GOV_TOKEN")

    # Request Settings
    TIMEOUT = 30  # seconds
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds

    # Pagination
    DEFAULT_ROWS = 10
    MAX_ROWS = 1000

    # Headers
    HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "DadosGovBR-Client/1.0"
    }

    @classmethod
    def get_headers(cls):
        headers = cls.HEADERS.copy()
        if cls.API_TOKEN:
            headers["Authorization"] = f"Bearer {cls.API_TOKEN}"
        return headers
```

### Environment Variables

Recommended environment variables:

```bash
# .env file
DADOS_GOV_TOKEN=your-api-token-here
DADOS_GOV_BASE_URL=https://dados.gov.br/api/3/action
DADOS_GOV_TIMEOUT=30
DADOS_GOV_MAX_RETRIES=3
```

Load with python-dotenv:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Common Patterns

### Pattern 1: Dataset Search with Filtering

```python
import requests
from typing import Dict, List, Optional

class DadosGovBRClient:
    def __init__(self, token: Optional[str] = None):
        self.base_url = "https://dados.gov.br/api/3/action"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}" if token else None
        }

    def search_datasets(
        self,
        query: str = "*:*",
        organization: Optional[str] = None,
        tags: Optional[List[str]] = None,
        rows: int = 10,
        start: int = 0
    ) -> Dict:
        """Search datasets with filters"""

        # Build filter query
        fq_parts = []
        if organization:
            fq_parts.append(f"organization:{organization}")
        if tags:
            for tag in tags:
                fq_parts.append(f"tags:{tag}")

        params = {
            "q": query,
            "rows": rows,
            "start": start
        }

        if fq_parts:
            params["fq"] = " AND ".join(fq_parts)

        response = requests.get(
            f"{self.base_url}/package_search",
            headers=self.headers,
            params=params,
            timeout=30
        )
        response.raise_for_status()

        return response.json()["result"]

# Usage
client = DadosGovBRClient(token="your-token")

# Search health datasets from Ministry of Health
results = client.search_datasets(
    query="COVID-19",
    organization="ministerio-da-saude",
    tags=["saúde", "epidemiologia"],
    rows=20
)

print(f"Found {results['count']} datasets")
for dataset in results['results']:
    print(f"- {dataset['title']}")
    print(f"  Organization: {dataset['organization']['title']}")
    print(f"  Resources: {len(dataset['resources'])}")
```

### Pattern 2: Paginated Dataset Retrieval

```python
def get_all_datasets(client: DadosGovBRClient, query: str = "*:*", page_size: int = 100):
    """Retrieve all datasets matching query with pagination"""

    all_datasets = []
    start = 0

    while True:
        results = client.search_datasets(
            query=query,
            rows=page_size,
            start=start
        )

        datasets = results['results']
        all_datasets.extend(datasets)

        # Check if we have more pages
        if start + page_size >= results['count']:
            break

        start += page_size
        print(f"Retrieved {len(all_datasets)}/{results['count']} datasets...")

    return all_datasets

# Usage
all_education_datasets = get_all_datasets(client, query="educação")
print(f"Total datasets retrieved: {len(all_education_datasets)}")
```

### Pattern 3: Resource Download

```python
import os
from urllib.parse import urlparse

def download_resource(resource_url: str, save_dir: str = "./data"):
    """Download a dataset resource file"""

    os.makedirs(save_dir, exist_ok=True)

    # Get filename from URL
    filename = os.path.basename(urlparse(resource_url).path)
    filepath = os.path.join(save_dir, filename)

    # Download with progress
    response = requests.get(resource_url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0

    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    percent = (downloaded / total_size) * 100
                    print(f"\rDownloading: {percent:.1f}%", end='')

    print(f"\nSaved to: {filepath}")
    return filepath

# Usage: Download all CSV resources from a dataset
dataset = client.search_datasets(query="população", rows=1)['results'][0]

for resource in dataset['resources']:
    if resource['format'].lower() == 'csv':
        print(f"Downloading: {resource['name']}")
        download_resource(resource['url'])
```

### Pattern 4: Organization and Group Discovery

```python
def explore_organizations(client: DadosGovBRClient):
    """List all organizations with dataset counts"""

    response = requests.get(
        f"{client.base_url}/organization_list",
        headers=client.headers,
        params={"all_fields": "true"}
    )
    response.raise_for_status()

    orgs = response.json()["result"]

    # Sort by package count
    orgs_sorted = sorted(
        orgs,
        key=lambda x: x.get('package_count', 0),
        reverse=True
    )

    print("Top Organizations by Dataset Count:")
    for org in orgs_sorted[:10]:
        print(f"- {org['title']}: {org.get('package_count', 0)} datasets")

    return orgs_sorted

# Usage
organizations = explore_organizations(client)
```

## API Reference

### Core API Endpoints

All endpoints follow the pattern: `{BASE_URL}/{action}`

#### Dataset Endpoints

**`package_search`** - Search for datasets

Parameters:
- `q` (string): Search query (use `*:*` for all)
- `fq` (string): Filter query (e.g., `organization:ministry-name`)
- `rows` (int): Number of results (default: 10, max: 1000)
- `start` (int): Offset for pagination
- `sort` (string): Sort field and order (e.g., `metadata_modified desc`)

Example:
```
GET /api/3/action/package_search?q=saúde&rows=20&start=0
```

**`package_show`** - Get dataset details

Parameters:
- `id` (string, required): Dataset ID or name

Example:
```
GET /api/3/action/package_show?id=covid-19-brasil
```

**`package_list`** - List all dataset names

Returns: Array of dataset name strings

**`current_package_list_with_resources`** - List datasets with resources

Parameters:
- `limit` (int): Number of datasets
- `offset` (int): Pagination offset

#### Organization Endpoints

**`organization_list`** - List organizations

Parameters:
- `all_fields` (bool): Return full details (default: false)
- `limit` (int): Number of results

**`organization_show`** - Get organization details

Parameters:
- `id` (string, required): Organization ID or name
- `include_datasets` (bool): Include datasets list

#### Group Endpoints

**`group_list`** - List groups (thematic categories)

Parameters:
- `all_fields` (bool): Return full details

**`group_show`** - Get group details

Parameters:
- `id` (string, required): Group ID or name
- `include_datasets` (bool): Include datasets

#### Tag Endpoints

**`tag_list`** - List all tags

Parameters:
- `vocabulary_id` (string): Filter by vocabulary

**`tag_show`** - Get tag details

Parameters:
- `id` (string, required): Tag name

#### Resource Endpoints

**`resource_show`** - Get resource details

Parameters:
- `id` (string, required): Resource ID

**`resource_search`** - Search resources

Parameters:
- `query` (string): Search terms
- `fields` (dict): Field-specific searches

### Response Format

All successful API responses follow this structure:

```json
{
  "help": "API endpoint URL",
  "success": true,
  "result": {
    // Endpoint-specific data
  }
}
```

Error responses:

```json
{
  "help": "API endpoint URL",
  "success": false,
  "error": {
    "message": "Error description",
    "__type": "Error Type"
  }
}
```

### Authentication

Include token in request headers:

```
Authorization: Bearer YOUR_API_TOKEN
```

The API supports both authenticated and unauthenticated requests. Authentication is required for:
- Creating/updating datasets (admin only)
- Accessing private datasets
- Higher rate limits

### Rate Limits

While official rate limits are not publicly documented, follow these best practices:
- Implement exponential backoff for retries
- Cache responses when possible
- Use pagination instead of large single requests
- Monitor 429 (Too Many Requests) responses

Reference: The Portal da Transparência (related service) allows 90 requests/minute during business hours (6 AM - 11:59 PM) and 300 requests/minute during off-hours (midnight - 5:59 AM).

Official documentation:
- Swagger UI: https://dados.gov.br/swagger-ui/index.html
- API Catalog: https://www.gov.br/conecta/catalogo/apis/api-portal-de-dados-abertos

## Integration Examples

### Example 1: COVID-19 Data Dashboard

Build a dashboard that tracks COVID-19 datasets and downloads daily updates.

```python
import requests
import pandas as pd
from datetime import datetime
import schedule
import time

class COVID19DataMonitor:
    def __init__(self, token: str):
        self.client = DadosGovBRClient(token)
        self.base_dir = "./covid_data"

    def fetch_latest_covid_datasets(self):
        """Fetch and download latest COVID-19 datasets"""

        # Search for COVID datasets
        results = self.client.search_datasets(
            query="COVID-19 OR coronavirus",
            tags=["saúde", "epidemiologia"],
            rows=50,
            sort="metadata_modified desc"
        )

        print(f"Found {results['count']} COVID-19 datasets")

        # Download CSV resources from top 5 most recent
        for dataset in results['results'][:5]:
            print(f"\nDataset: {dataset['title']}")
            print(f"Modified: {dataset['metadata_modified']}")

            for resource in dataset['resources']:
                if resource['format'].lower() in ['csv', 'json']:
                    try:
                        filepath = download_resource(
                            resource['url'],
                            save_dir=f"{self.base_dir}/{dataset['name']}"
                        )
                        print(f"Downloaded: {filepath}")
                    except Exception as e:
                        print(f"Error downloading {resource['name']}: {e}")

    def schedule_updates(self):
        """Schedule daily updates"""
        schedule.every().day.at("08:00").do(self.fetch_latest_covid_datasets)

        print("Scheduler started. Checking for updates daily at 08:00")
        while True:
            schedule.run_pending()
            time.sleep(3600)  # Check every hour

# Usage
monitor = COVID19DataMonitor(token="your-token")
monitor.fetch_latest_covid_datasets()
# monitor.schedule_updates()  # Run continuously
```

### Example 2: Multi-Organization Data Aggregator

Aggregate datasets from multiple government organizations into a searchable database.

```python
from sqlalchemy import create_engine, Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Dataset(Base):
    __tablename__ = 'datasets'

    id = Column(String, primary_key=True)
    name = Column(String)
    title = Column(String)
    organization = Column(String)
    metadata = Column(JSON)
    resources_count = Column(Integer)
    created = Column(DateTime)
    modified = Column(DateTime)
    last_synced = Column(DateTime)

class DataAggregator:
    def __init__(self, token: str, db_url: str = "sqlite:///dados_gov.db"):
        self.client = DadosGovBRClient(token)
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def sync_organization(self, org_name: str):
        """Sync all datasets from an organization"""

        print(f"Syncing datasets from: {org_name}")

        # Get all datasets from organization
        datasets = self.client.search_datasets(
            query="*:*",
            organization=org_name,
            rows=1000
        )

        synced_count = 0

        for ds in datasets['results']:
            # Check if dataset exists
            existing = self.session.query(Dataset).filter_by(id=ds['id']).first()

            dataset_obj = Dataset(
                id=ds['id'],
                name=ds['name'],
                title=ds['title'],
                organization=ds['organization']['name'],
                metadata=ds,
                resources_count=len(ds['resources']),
                created=datetime.fromisoformat(ds['metadata_created'].replace('Z', '+00:00')),
                modified=datetime.fromisoformat(ds['metadata_modified'].replace('Z', '+00:00')),
                last_synced=datetime.now()
            )

            if existing:
                # Update existing
                for key, value in dataset_obj.__dict__.items():
                    if key != '_sa_instance_state':
                        setattr(existing, key, value)
            else:
                # Add new
                self.session.add(dataset_obj)

            synced_count += 1

        self.session.commit()
        print(f"Synced {synced_count} datasets from {org_name}")

    def sync_all_organizations(self):
        """Sync datasets from all organizations"""

        response = requests.get(
            f"{self.client.base_url}/organization_list",
            headers=self.client.headers,
            params={"all_fields": "true"}
        )
        orgs = response.json()["result"]

        for org in orgs:
            if org.get('package_count', 0) > 0:
                try:
                    self.sync_organization(org['name'])
                except Exception as e:
                    print(f"Error syncing {org['name']}: {e}")

        print(f"\nTotal datasets in database: {self.session.query(Dataset).count()}")

    def search_local(self, query: str):
        """Search synced datasets locally"""
        results = self.session.query(Dataset).filter(
            Dataset.title.contains(query) | Dataset.name.contains(query)
        ).all()

        return results

# Usage
aggregator = DataAggregator(token="your-token")
aggregator.sync_organization("ministerio-da-saude")
aggregator.sync_organization("ministerio-da-educacao")

# Local search (much faster)
results = aggregator.search_local("COVID")
for ds in results:
    print(f"- {ds.title} ({ds.organization})")
```

### Example 3: FastAPI Service

Create a REST API service that proxies dados.gov.br with caching.

```python
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import redis
import json
from datetime import timedelta

app = FastAPI(title="Dados.gov.br API Proxy")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis cache
cache = redis.Redis(host='localhost', port=6379, db=0)
CACHE_TTL = timedelta(hours=1)

class DatasetSummary(BaseModel):
    id: str
    name: str
    title: str
    organization: str
    resources_count: int
    tags: List[str]

@app.get("/datasets/search", response_model=List[DatasetSummary])
async def search_datasets(
    q: str = Query("*:*", description="Search query"),
    organization: Optional[str] = None,
    rows: int = Query(10, le=100),
    start: int = 0
):
    """Search datasets with caching"""

    # Create cache key
    cache_key = f"search:{q}:{organization}:{rows}:{start}"

    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)

    # Fetch from API
    client = DadosGovBRClient(token=os.getenv("DADOS_GOV_TOKEN"))

    try:
        results = client.search_datasets(
            query=q,
            organization=organization,
            rows=rows,
            start=start
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Transform to response model
    datasets = [
        DatasetSummary(
            id=ds['id'],
            name=ds['name'],
            title=ds['title'],
            organization=ds['organization']['title'],
            resources_count=len(ds['resources']),
            tags=[tag['name'] for tag in ds.get('tags', [])]
        )
        for ds in results['results']
    ]

    # Cache results
    cache.setex(
        cache_key,
        CACHE_TTL,
        json.dumps([ds.dict() for ds in datasets])
    )

    return datasets

@app.get("/datasets/{dataset_id}")
async def get_dataset(dataset_id: str):
    """Get dataset details"""

    cache_key = f"dataset:{dataset_id}"

    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)

    # Fetch from API
    client = DadosGovBRClient(token=os.getenv("DADOS_GOV_TOKEN"))

    response = requests.get(
        f"{client.base_url}/package_show",
        headers=client.headers,
        params={"id": dataset_id}
    )

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Dataset not found")

    dataset = response.json()["result"]

    # Cache
    cache.setex(cache_key, CACHE_TTL, json.dumps(dataset))

    return dataset

# Run with: uvicorn main:app --reload
```

## Best Practices

### Development

1. **Use Environment Variables for Tokens**
   ```python
   import os
   token = os.getenv("DADOS_GOV_TOKEN")  # Never hardcode tokens
   ```

2. **Implement Retry Logic with Exponential Backoff**
   ```python
   from tenacity import retry, stop_after_attempt, wait_exponential

   @retry(
       stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=2, max=10)
   )
   def fetch_dataset(dataset_id):
       return client.search_datasets(query=dataset_id)
   ```

3. **Cache API Responses**
   - Use Redis, Memcached, or file-based caching
   - Set appropriate TTL (1-24 hours for metadata)
   - Cache dataset lists longer than individual datasets

4. **Use Pagination for Large Datasets**
   ```python
   # Bad: Fetching all at once
   results = client.search_datasets(query="*:*", rows=10000)  # May fail

   # Good: Paginate
   for offset in range(0, total_count, 100):
       results = client.search_datasets(query="*:*", rows=100, start=offset)
   ```

5. **Validate Data Before Processing**
   - Check `success` field in responses
   - Handle missing fields gracefully
   - Verify resource URLs before downloading

### Production

1. **Security**
   - Store tokens in secure vaults (AWS Secrets Manager, HashiCorp Vault)
   - Use HTTPS for all requests
   - Implement rate limiting on your proxy endpoints
   - Sanitize user input for search queries (prevent injection)

2. **Performance**
   - Use connection pooling: `requests.Session()`
   - Implement async requests for bulk operations (aiohttp)
   - Compress responses if possible
   - Use CDN for frequently accessed datasets

3. **Monitoring**
   ```python
   import logging
   from prometheus_client import Counter, Histogram

   # Metrics
   api_requests = Counter('dados_gov_api_requests_total', 'Total API requests')
   api_latency = Histogram('dados_gov_api_latency_seconds', 'API latency')

   # Logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   def monitored_request(endpoint, params):
       api_requests.inc()
       with api_latency.time():
           logger.info(f"Requesting {endpoint} with params {params}")
           response = requests.get(endpoint, params=params)
           logger.info(f"Response status: {response.status_code}")
           return response
   ```

4. **Error Handling**
   ```python
   from requests.exceptions import Timeout, ConnectionError, HTTPError

   try:
       results = client.search_datasets(query="test")
   except Timeout:
       logger.error("Request timed out")
       # Retry or return cached data
   except ConnectionError:
       logger.error("Connection failed")
       # Check network or use fallback
   except HTTPError as e:
       if e.response.status_code == 429:
           logger.warning("Rate limited, backing off")
           time.sleep(60)
       elif e.response.status_code == 404:
           logger.error("Resource not found")
       else:
           logger.error(f"HTTP error: {e}")
   ```

### Common Pitfalls

1. **Issue**: Forgetting to check the `success` field in responses
   - **Solution**: Always validate `response.json()['success']` before accessing `result`

2. **Issue**: Hardcoding API tokens in source code
   - **Solution**: Use environment variables or secret management systems

3. **Issue**: Not handling pagination for large result sets
   - **Solution**: Implement proper pagination logic; API limits results per request

4. **Issue**: Assuming all datasets have resources
   - **Solution**: Check `if dataset['resources']:` before iterating

5. **Issue**: Not setting request timeouts
   - **Solution**: Always set timeout: `requests.get(url, timeout=30)`

6. **Issue**: Ignoring rate limits
   - **Solution**: Implement exponential backoff and monitor 429 responses

7. **Issue**: Downloading large files synchronously
   - **Solution**: Use streaming downloads and async processing

## Troubleshooting

### Common Issues

#### Issue 1: 401 Unauthorized Error

**Symptoms:**
- `{"success": false, "error": {"__type": "Authorization Error", "message": "Access denied"}}`
- HTTP 401 status code

**Solution:**
```python
# Verify token is set correctly
import os
print("Token:", os.getenv("DADOS_GOV_TOKEN"))

# Check header format
headers = {
    "Authorization": f"Bearer {token}"  # Note: "Bearer" prefix
}

# Some endpoints may not require auth - try without token first
response = requests.get(endpoint)  # Public endpoints
```

#### Issue 2: Rate Limiting (429 Too Many Requests)

**Symptoms:**
- HTTP 429 status code
- `{"error": "Too many requests"}`
- Intermittent failures during bulk operations

**Solution:**
```python
import time
from requests.exceptions import HTTPError

def api_call_with_backoff(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except HTTPError as e:
            if e.response.status_code == 429:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")

# Usage
result = api_call_with_backoff(
    lambda: client.search_datasets(query="test")
)
```

#### Issue 3: Empty Result Set for Valid Query

**Symptoms:**
- `{"result": {"count": 0, "results": []}}`
- Expected datasets not returned

**Solution:**
1. Check query syntax - use `*:*` for all datasets
2. Verify organization/tag names are exact matches
3. Check if datasets are private (require authentication)
4. Try homologation environment to test

```python
# Debug search
print("Query:", query)
print("Organization filter:", organization)

# Try without filters first
results = client.search_datasets(query="*:*", rows=5)
print("Total datasets:", results['count'])

# Then add filters one by one
results = client.search_datasets(
    query="*:*",
    organization="ministerio-da-saude",
    rows=5
)
print("Filtered results:", results['count'])
```

#### Issue 4: Timeout Errors

**Symptoms:**
- `requests.exceptions.Timeout`
- `ReadTimeout` errors
- Slow API responses

**Solution:**
```python
# Increase timeout
response = requests.get(endpoint, timeout=60)  # 60 seconds

# Use session with retry adapter
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

response = session.get(endpoint, timeout=30)
```

#### Issue 5: Dataset Resources Have Broken URLs

**Symptoms:**
- 404 errors when downloading resources
- Resource URLs return errors

**Solution:**
```python
def verify_resource_url(url):
    """Check if resource URL is accessible"""
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

# Filter valid resources
valid_resources = [
    res for res in dataset['resources']
    if verify_resource_url(res['url'])
]

print(f"Valid: {len(valid_resources)}/{len(dataset['resources'])}")
```

### Debugging Tips

1. **Enable Debug Logging**
   ```python
   import logging
   import http.client as http_client

   http_client.HTTPConnection.debuglevel = 1
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Inspect Raw Response**
   ```python
   response = requests.get(endpoint)
   print("Status:", response.status_code)
   print("Headers:", response.headers)
   print("Body:", response.text[:500])  # First 500 chars
   ```

3. **Test in Homologation Environment**
   ```python
   # Switch to test environment
   BASE_URL = "https://hmg.dados.gov.br/api/3/action"
   ```

4. **Validate JSON Structure**
   ```python
   import json
   try:
       data = response.json()
       if not data.get('success'):
           print("API Error:", data.get('error'))
   except json.JSONDecodeError:
       print("Invalid JSON response")
       print(response.text)
   ```

5. **Monitor API Health**
   - Check https://dados.gov.br status
   - Verify network connectivity
   - Test with curl: `curl -X GET "https://dados.gov.br/api/3/action/package_list"`

## Advanced Topics

### Topic 1: Async Batch Processing with aiohttp

Process multiple datasets concurrently for improved performance.

```python
import aiohttp
import asyncio
from typing import List, Dict

class AsyncDadosGovBRClient:
    def __init__(self, token: str):
        self.base_url = "https://dados.gov.br/api/3/action"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    async def fetch_dataset(self, session: aiohttp.ClientSession, dataset_id: str) -> Dict:
        """Fetch single dataset asynchronously"""
        url = f"{self.base_url}/package_show"
        params = {"id": dataset_id}

        async with session.get(url, params=params, headers=self.headers) as response:
            data = await response.json()
            return data['result']

    async def fetch_multiple_datasets(self, dataset_ids: List[str]) -> List[Dict]:
        """Fetch multiple datasets concurrently"""

        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_dataset(session, dataset_id)
                for dataset_id in dataset_ids
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Filter out errors
            valid_results = [
                r for r in results
                if not isinstance(r, Exception)
            ]

            return valid_results

# Usage
async def main():
    client = AsyncDadosGovBRClient(token="your-token")

    dataset_ids = [
        "covid-19-brasil",
        "dados-epidemiologicos",
        "vacinacao-covid19"
    ]

    datasets = await client.fetch_multiple_datasets(dataset_ids)
    print(f"Fetched {len(datasets)} datasets")

# Run
asyncio.run(main())
```

### Topic 2: Data Pipeline with Apache Airflow

Automate daily dataset synchronization using Airflow DAGs.

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dados_gov_br_sync',
    default_args=default_args,
    description='Sync dados.gov.br datasets daily',
    schedule_interval='0 2 * * *',  # 2 AM daily
    catchup=False
)

def extract_datasets(**context):
    """Extract datasets from dados.gov.br"""
    client = DadosGovBRClient(token=os.getenv("DADOS_GOV_TOKEN"))

    datasets = client.search_datasets(
        query="saúde",
        rows=1000
    )

    # Save to XCom for next task
    return datasets['results']

def transform_datasets(**context):
    """Transform dataset metadata"""
    ti = context['task_instance']
    datasets = ti.xcom_pull(task_ids='extract')

    # Transform to DataFrame
    df = pd.DataFrame([
        {
            'id': ds['id'],
            'title': ds['title'],
            'organization': ds['organization']['name'],
            'resources_count': len(ds['resources']),
            'modified': ds['metadata_modified']
        }
        for ds in datasets
    ])

    # Save to CSV
    output_path = f"/data/dados_gov_{context['ds']}.csv"
    df.to_csv(output_path, index=False)

    return output_path

def load_to_database(**context):
    """Load data to warehouse"""
    ti = context['task_instance']
    csv_path = ti.xcom_pull(task_ids='transform')

    # Load to database
    df = pd.read_csv(csv_path)

    # Example: Load to PostgreSQL
    from sqlalchemy import create_engine
    engine = create_engine(os.getenv("DATABASE_URL"))
    df.to_sql('dados_gov_datasets', engine, if_exists='replace')

    print(f"Loaded {len(df)} datasets to database")

# Define tasks
extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract_datasets,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform_datasets,
    dag=dag
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load_to_database,
    dag=dag
)

# Set dependencies
extract_task >> transform_task >> load_task
```

### Topic 3: Real-Time Dataset Monitoring

Monitor dataset updates and send notifications.

```python
import time
from datetime import datetime
from typing import Set
import smtplib
from email.mime.text import MIMEText

class DatasetMonitor:
    def __init__(self, token: str, check_interval: int = 3600):
        self.client = DadosGovBRClient(token)
        self.check_interval = check_interval  # seconds
        self.known_datasets: Set[str] = set()

    def get_recent_datasets(self, hours: int = 24):
        """Get datasets modified in last N hours"""
        results = self.client.search_datasets(
            query="*:*",
            sort="metadata_modified desc",
            rows=100
        )

        recent = []
        cutoff = datetime.now() - timedelta(hours=hours)

        for ds in results['results']:
            modified = datetime.fromisoformat(
                ds['metadata_modified'].replace('Z', '+00:00')
            )
            if modified > cutoff:
                recent.append(ds)

        return recent

    def send_notification(self, datasets: List[Dict]):
        """Send email notification about new/updated datasets"""

        if not datasets:
            return

        message = "New/Updated Datasets on dados.gov.br:\n\n"
        for ds in datasets:
            message += f"- {ds['title']}\n"
            message += f"  Organization: {ds['organization']['title']}\n"
            message += f"  Modified: {ds['metadata_modified']}\n"
            message += f"  URL: https://dados.gov.br/dataset/{ds['name']}\n\n"

        # Send email (configure SMTP settings)
        msg = MIMEText(message)
        msg['Subject'] = f'dados.gov.br: {len(datasets)} Dataset Updates'
        msg['From'] = os.getenv('EMAIL_FROM')
        msg['To'] = os.getenv('EMAIL_TO')

        # Send via SMTP
        # ... SMTP configuration ...

        print(f"Notification sent for {len(datasets)} datasets")

    def monitor(self):
        """Continuous monitoring loop"""
        print("Starting dataset monitor...")

        while True:
            try:
                recent = self.get_recent_datasets(hours=1)

                # Check for new datasets
                new_datasets = [
                    ds for ds in recent
                    if ds['id'] not in self.known_datasets
                ]

                if new_datasets:
                    print(f"Found {len(new_datasets)} new/updated datasets")
                    self.send_notification(new_datasets)

                    # Update known datasets
                    for ds in new_datasets:
                        self.known_datasets.add(ds['id'])

                else:
                    print("No new datasets")

            except Exception as e:
                print(f"Error during monitoring: {e}")

            time.sleep(self.check_interval)

# Usage
monitor = DatasetMonitor(token="your-token", check_interval=3600)
monitor.monitor()  # Run continuously
```

### Topic 4: GraphQL Proxy Layer

Create a GraphQL API on top of the REST API for flexible queries.

```python
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional

@strawberry.type
class Resource:
    id: str
    name: str
    url: str
    format: str
    description: Optional[str]

@strawberry.type
class Dataset:
    id: str
    name: str
    title: str
    notes: Optional[str]
    organization: str
    resources: List[Resource]
    tags: List[str]

@strawberry.type
class Query:
    @strawberry.field
    def datasets(
        self,
        query: str = "*:*",
        organization: Optional[str] = None,
        limit: int = 10
    ) -> List[Dataset]:
        """Search datasets"""

        client = DadosGovBRClient(token=os.getenv("DADOS_GOV_TOKEN"))
        results = client.search_datasets(
            query=query,
            organization=organization,
            rows=limit
        )

        return [
            Dataset(
                id=ds['id'],
                name=ds['name'],
                title=ds['title'],
                notes=ds.get('notes'),
                organization=ds['organization']['title'],
                resources=[
                    Resource(
                        id=r['id'],
                        name=r['name'],
                        url=r['url'],
                        format=r['format'],
                        description=r.get('description')
                    )
                    for r in ds['resources']
                ],
                tags=[t['name'] for t in ds.get('tags', [])]
            )
            for ds in results['results']
        ]

    @strawberry.field
    def dataset(self, id: str) -> Optional[Dataset]:
        """Get dataset by ID"""

        client = DadosGovBRClient(token=os.getenv("DADOS_GOV_TOKEN"))
        response = requests.get(
            f"{client.base_url}/package_show",
            headers=client.headers,
            params={"id": id}
        )

        if response.status_code != 200:
            return None

        ds = response.json()['result']

        return Dataset(
            id=ds['id'],
            name=ds['name'],
            title=ds['title'],
            notes=ds.get('notes'),
            organization=ds['organization']['title'],
            resources=[
                Resource(
                    id=r['id'],
                    name=r['name'],
                    url=r['url'],
                    format=r['format'],
                    description=r.get('description')
                )
                for r in ds['resources']
            ],
            tags=[t['name'] for t in ds.get('tags', [])]
        )

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

# Add to FastAPI
app.include_router(graphql_app, prefix="/graphql")

# Query with:
# query {
#   datasets(query: "COVID", limit: 5) {
#     title
#     organization
#     resources {
#       name
#       format
#     }
#   }
# }
```

## Resources

### Official Documentation

**API Documentation:**
- Production Swagger UI: https://dados.gov.br/swagger-ui/index.html
- Homologation Swagger UI: https://hmg.dados.gov.br/swagger-ui/index.html
- API Catalog: https://www.gov.br/conecta/catalogo/apis/api-portal-de-dados-abertos
- Main Portal: https://dados.gov.br

**Legal Framework:**
- Law No. 12,527/2011 (Access to Information Law): http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm
- Decree No. 8,777/2016 (Open Data Policy): http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/decreto/d8777.htm

### Community Resources

**GitHub:**
- Official Organization: https://github.com/dadosgovbr
- CKAN (underlying platform): https://github.com/ckan/ckan
- Example integrations and tools

**Developer Guides:**
- W3C Brazil - Manual dos Dados Abertos (Developers): https://www.w3c.br/pub/Materiais/PublicacoesW3C/manual_dados_abertos_desenvolvedores_web.pdf
- Open Data Guide: https://ceweb.br/guias/dados-abertos/

**Related Government APIs:**
- Portal da Transparência API: https://portaldatransparencia.gov.br/api-de-dados
- Ministry of Health Open Data: https://apidadosabertos.saude.gov.br/
- Superior Court of Justice Data: https://dadosabertos.web.stj.jus.br/

### Related Tools and Libraries

**Python Libraries:**
- `requests`: HTTP client for API calls
- `aiohttp`: Async HTTP client for concurrent requests
- `pandas`: Data manipulation and analysis
- `sqlalchemy`: Database ORM for data storage
- `fastapi`: Build API proxies and services
- `apache-airflow`: Data pipeline orchestration
- `tenacity`: Retry logic with exponential backoff

**Data Processing:**
- `dask`: Parallel computing for large datasets
- `polars`: Fast DataFrame library
- `apache-beam`: Batch and streaming data pipelines

**Monitoring & Observability:**
- `prometheus-client`: Metrics collection
- `sentry-sdk`: Error tracking
- `structlog`: Structured logging

**Similar Platforms:**
- CKAN: https://ckan.org/ (underlying platform)
- data.gov (US): https://www.data.gov/
- data.gov.uk (UK): https://www.data.gov.uk/
- European Data Portal: https://data.europa.eu/

### Example Projects

Build inspiration from these use cases:
- COVID-19 dashboards using dados.gov.br
- Education statistics aggregation
- Health data analysis and visualization
- Environmental monitoring systems
- Public spending transparency tools
- Open data portals for municipalities

## Data Quality and Usage Notes

### Data Quality Considerations

1. **Metadata Quality**: Varies by organization
   - Some datasets have comprehensive metadata
   - Others may have minimal descriptions
   - Validate before use in production

2. **Update Frequency**: Inconsistent across datasets
   - Check `metadata_modified` field
   - Some datasets updated daily, others annually
   - Set up monitoring for critical datasets

3. **Data Formats**: Multiple formats available
   - Prefer CSV/JSON for machine-readable data
   - PDF/DOC files may require OCR
   - Check resource format before downloading

4. **Data Completeness**: May contain gaps
   - Historical data availability varies
   - Some datasets are incomplete
   - Verify data coverage for your use case

### Attribution and Licensing

**Attribution Requirements:**
- Most datasets require attribution to the source organization
- Check individual dataset license field
- Common licenses: Creative Commons, Open Data Commons

**Example Attribution:**
```
Data source: [Dataset Title], [Organization Name]
Available at: dados.gov.br
License: [License Type]
Accessed: [Date]
```

### Responsible Use

1. **Respect Rate Limits**: Don't overwhelm the API
2. **Cache Appropriately**: Reduce unnecessary requests
3. **Report Issues**: Help improve data quality by reporting problems
4. **Give Back**: Share insights and visualizations with the community
5. **Privacy**: Be mindful of any personal data (rare, but check)

## Contributing

The dados.gov.br platform welcomes contributions from the community:

**Ways to Contribute:**
1. **Report Data Issues**: Contact dataset publishers about errors or omissions
2. **Suggest Improvements**: Feedback on API functionality and documentation
3. **Share Integrations**: Publish your tools and libraries
4. **Publish Data**: Government agencies can publish new datasets

**Contact:**
- Official Portal: https://dados.gov.br
- GitHub: https://github.com/dadosgovbr
- API Catalog: https://www.gov.br/conecta

## Version Information

**Skill Version**: 1.0.0
**Last Updated**: 2026-01-20
**API Version**: CKAN API v3
**Author**: Claude Code Skill

**Changelog:**
- v1.0.0 (2026-01-20): Initial comprehensive skill release
  - Complete API reference with all endpoints
  - Authentication and configuration guides
  - Python and JavaScript code examples
  - Integration patterns (FastAPI, Airflow, async)
  - Advanced topics (GraphQL, monitoring, batch processing)
  - Troubleshooting and best practices
  - Real-world usage examples

---

**Legal Notice**: This skill is created for educational and development purposes. Always refer to the official dados.gov.br documentation and comply with Brazilian data protection and access laws (LGPD - Law No. 13,709/2018) when using government data.

**Disclaimer**: This skill provides technical guidance for integrating with the dados.gov.br API. Data quality, availability, and licensing vary by dataset. Always verify data sources and comply with individual dataset licenses.

*For the most up-to-date API documentation, visit: https://dados.gov.br/swagger-ui/index.html*
