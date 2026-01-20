#!/usr/bin/env python3
"""
Test script for dados.gov.br API (CORRECT VERSION)
Uses the actual API structure discovered from Swagger UI
"""

import requests
import json
import os
from typing import Dict, Any, Optional

# API Configuration - CORRECT URLS
API_BASE_URL = "https://dados.gov.br/dados/api"
API_PUBLIC_BASE = f"{API_BASE_URL}/publico"
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJPaEx6RktTZWNUR1c0V25KT1NLbjFuYU5NTWxTSWxEX29RUGxpZHk5NXN3OUYtT2Zadm9sZnVjX0UtdlZyTzRNT2FTcGNHUGNOMzN4VXNpNiIsImlhdCI6MTc0MjI0Njk4N30.LOboeht1ujLjjS3Qsyn3nlGXbguCN4sb2xIsIenK52s"

def make_request(
    endpoint: str,
    params: Dict[str, Any] = None,
    use_auth: bool = False,
    auth_type: str = "bearer"
) -> Dict:
    """Make API request and return parsed JSON"""

    url = f"{API_PUBLIC_BASE}/{endpoint}"

    headers = {
        "Accept": "application/json",
        "User-Agent": "DadosGovBR-TestClient/1.0"
    }

    if use_auth:
        if auth_type == "bearer":
            headers["Authorization"] = f"Bearer {API_TOKEN}"
        elif auth_type == "apikey":
            headers["X-API-Key"] = API_TOKEN

    try:
        print(f"\n🔄 Request: GET {url}")
        if params:
            print(f"   Parameters: {params}")
        if use_auth:
            print(f"   Auth: {auth_type} (token: {API_TOKEN[:30]}...)")

        response = requests.get(url, headers=headers, params=params, timeout=30)

        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")

        # Check if response is JSON
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            data = response.json()
            print(f"   Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            return {"success": True, "status_code": response.status_code, "data": data}
        else:
            print(f"   ⚠️  Non-JSON response (length: {len(response.text)})")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": "Non-JSON response",
                "content_type": content_type,
                "text_preview": response.text[:500]
            }

    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error: {e}")
        return {"success": False, "error": str(e)}
    except json.JSONDecodeError as e:
        print(f"   ❌ JSON decode error: {e}")
        return {"success": False, "error": f"JSON decode error: {e}", "status_code": response.status_code}

def save_response(endpoint: str, data: Dict, filename: str = None):
    """Save API response to file"""
    if filename is None:
        endpoint_safe = endpoint.replace('/', '_').replace('{', '').replace('}', '')
        filename = f"{endpoint_safe}_response.json"

    output_dir = "../references/api-responses"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"   💾 Saved to {filepath}")

def test_list_datasets():
    """Test list datasets endpoint - PUBLIC"""
    print("\n" + "="*70)
    print("TEST 1: List Datasets (PUBLIC)")
    print("="*70)

    # Test without auth
    result = make_request("conjuntos-dados", params={"pagina": 1, "tamanhoPagina": 10})

    if result["success"]:
        save_response("conjuntos-dados", result, "list_datasets.json")

        # Try to analyze response structure
        if isinstance(result.get("data"), dict):
            print("\n   📊 Response analysis:")
            for key, value in result["data"].items():
                print(f"      - {key}: {type(value).__name__}")

    return result

def test_list_organizations():
    """Test list organizations endpoint - PUBLIC"""
    print("\n" + "="*70)
    print("TEST 2: List Organizations (PUBLIC)")
    print("="*70)

    result = make_request("organizacao")

    if result["success"]:
        save_response("organizacao", result, "list_organizations.json")

    return result

def test_list_themes():
    """Test list themes endpoint"""
    print("\n" + "="*70)
    print("TEST 3: List Themes")
    print("="*70)

    # Note: This endpoint might be at /dados/api/temas instead of /publico/temas
    result = make_request("../temas")  # Go up one level from /publico

    if result["success"]:
        save_response("temas", result, "list_themes.json")

    return result

def test_list_tags():
    """Test list tags endpoint"""
    print("\n" + "="*70)
    print("TEST 4: List Tags")
    print("="*70)

    result = make_request("../tags")  # Go up one level from /publico

    if result["success"]:
        save_response("tags", result, "list_tags.json")

    return result

def test_with_auth_bearer():
    """Test authenticated endpoint with Bearer token"""
    print("\n" + "="*70)
    print("TEST 5: List Datasets with Bearer Auth")
    print("="*70)

    result = make_request(
        "conjuntos-dados",
        params={"pagina": 1, "tamanhoPagina": 5},
        use_auth=True,
        auth_type="bearer"
    )

    if result["success"]:
        save_response("conjuntos-dados", result, "list_datasets_auth_bearer.json")

    return result

def test_with_auth_apikey():
    """Test authenticated endpoint with X-API-Key header"""
    print("\n" + "="*70)
    print("TEST 6: List Datasets with X-API-Key Auth")
    print("="*70)

    result = make_request(
        "conjuntos-dados",
        params={"pagina": 1, "tamanhoPagina": 5},
        use_auth=True,
        auth_type="apikey"
    )

    if result["success"]:
        save_response("conjuntos-dados", result, "list_datasets_auth_apikey.json")

    return result

def test_dataset_filters():
    """Test dataset filtering"""
    print("\n" + "="*70)
    print("TEST 7: Filter Datasets (Open Data Only)")
    print("="*70)

    result = make_request(
        "conjuntos-dados",
        params={
            "pagina": 1,
            "tamanhoPagina": 10,
            "dadosAbertos": True,
            "isPrivado": "false"
        }
    )

    if result["success"]:
        save_response("conjuntos-dados", result, "list_datasets_filtered.json")

    return result

def test_list_reusos():
    """Test list reuses endpoint"""
    print("\n" + "="*70)
    print("TEST 8: List Reuses (Dataset Reuses)")
    print("="*70)

    result = make_request("reusos")

    if result["success"]:
        save_response("reusos", result, "list_reusos.json")

    return result

def main():
    """Run all tests"""
    print("="*70)
    print("DADOS.GOV.BR API TEST SUITE")
    print("Correct API Structure (Discovered from Swagger UI)")
    print("="*70)
    print(f"\nBase URL: {API_PUBLIC_BASE}")
    print(f"Token: {API_TOKEN[:40]}...\n")

    results = {}

    # Run tests
    results["list_datasets"] = test_list_datasets()
    results["list_organizations"] = test_list_organizations()
    results["list_themes"] = test_list_themes()
    results["list_tags"] = test_list_tags()
    results["auth_bearer"] = test_with_auth_bearer()
    results["auth_apikey"] = test_with_auth_apikey()
    results["dataset_filters"] = test_dataset_filters()
    results["list_reusos"] = test_list_reusos()

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    success_count = sum(1 for r in results.values() if r.get("success"))
    total_count = len(results)

    print(f"\n✅ Successful: {success_count}/{total_count}")
    print(f"❌ Failed: {total_count - success_count}/{total_count}\n")

    print("Detailed Results:")
    for test_name, result in results.items():
        status = "✅" if result.get("success") else "❌"
        status_code = result.get("status_code", "N/A")
        print(f"  {status} {test_name}: HTTP {status_code}")

    print("\n" + "="*70)
    print("All response files saved to: ../references/api-responses/")
    print("="*70)

if __name__ == "__main__":
    main()