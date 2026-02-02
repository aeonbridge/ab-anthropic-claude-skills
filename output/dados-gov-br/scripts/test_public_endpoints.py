#!/usr/bin/env python3
"""
Test truly public endpoints without authentication
"""
import requests
import json

def test_endpoint(name, url, params=None):
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print('='*70)
    
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30, allow_redirects=False)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 302:
            print(f"Redirect to: {response.headers.get('Location', 'N/A')}")
        elif 'application/json' in response.headers.get('Content-Type', ''):
            print("✅ JSON response received!")
            data = response.json()
            print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
            print(f"Sample: {json.dumps(data, indent=2)[:500]}")
            return True
        else:
            print(f"Response length: {len(response.text)}")
            print(f"First 200 chars: {response.text[:200]}")
        
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Try different base URLs and endpoints
base_urls = [
    "https://dados.gov.br/api/3/action",  # CKAN API
    "https://dados.gov.br/dados/api",      # New API
    "https://dados.gov.br/dados/api/publico",  # Public API
]

endpoints = [
    ("package_search", {"rows": 2}),  # CKAN-style
    ("package_list", None),            # CKAN-style
    ("conjuntos-dados", {"pagina": 1, "tamanhoPagina": 2}),  # New API
    ("organizacao", None),              # New API
]

print("Testing different API bases and endpoints...")

for base_url in base_urls:
    for endpoint, params in endpoints:
        url = f"{base_url}/{endpoint}"
        test_endpoint(f"{base_url} → {endpoint}", url, params)

# Also try the root API documentation
test_endpoint("API Root", "https://dados.gov.br/api", None)
test_endpoint("API v3", "https://dados.gov.br/api/3", None)
