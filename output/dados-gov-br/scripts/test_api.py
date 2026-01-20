#!/usr/bin/env python3
"""
Test script for dados.gov.br API
Explores all endpoints and documents real responses
"""

import requests
import json
import os
from typing import Dict, Any

# API Configuration
API_BASE_URL = "https://dados.gov.br/api/3/action"
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJPaEx6RktTZWNUR1c0V25KT1NLbjFuYU5NTWxTSWxEX29RUGxpZHk5NXN3OUYtT2Zadm9sZnVjX0UtdlZyTzRNT2FTcGNHUGNOMzN4VXNpNiIsImlhdCI6MTc0MjI0Njk4N30.LOboeht1ujLjjS3Qsyn3nlGXbguCN4sb2xIsIenK52s"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def make_request(endpoint: str, params: Dict[str, Any] = None) -> Dict:
    """Make API request and return parsed JSON"""
    url = f"{API_BASE_URL}/{endpoint}"

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling {endpoint}: {e}")
        return {"success": False, "error": str(e)}

def save_response(endpoint: str, data: Dict, filename: str = None):
    """Save API response to file"""
    if filename is None:
        filename = f"{endpoint.replace('/', '_')}_response.json"

    output_dir = "../references"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved response to {filepath}")

def test_package_search():
    """Test package_search endpoint"""
    print("\n" + "="*60)
    print("Testing: package_search")
    print("="*60)

    # Test 1: Basic search
    print("\n1. Basic search (COVID-19):")
    data = make_request("package_search", {"q": "COVID-19", "rows": 5})

    if data.get("success"):
        result = data["result"]
        print(f"   Total datasets found: {result['count']}")
        print(f"   Datasets returned: {len(result['results'])}")

        if result['results']:
            first_ds = result['results'][0]
            print(f"   First dataset: {first_ds['title']}")
            print(f"   Organization: {first_ds['organization']['title']}")
            print(f"   Resources: {len(first_ds['resources'])}")

        save_response("package_search", data, "package_search_covid.json")
    else:
        print(f"   ❌ Error: {data.get('error')}")

    # Test 2: Search with organization filter
    print("\n2. Search with organization filter:")
    data = make_request("package_search", {
        "q": "*:*",
        "fq": "organization:ministerio-da-saude",
        "rows": 5
    })

    if data.get("success"):
        result = data["result"]
        print(f"   Datasets from Ministério da Saúde: {result['count']}")
        save_response("package_search", data, "package_search_org_filter.json")

    # Test 3: Sort by recent
    print("\n3. Sort by recently modified:")
    data = make_request("package_search", {
        "q": "*:*",
        "sort": "metadata_modified desc",
        "rows": 5
    })

    if data.get("success"):
        result = data["result"]
        print(f"   Total datasets: {result['count']}")
        if result['results']:
            print(f"   Most recent: {result['results'][0]['title']}")
            print(f"   Modified: {result['results'][0]['metadata_modified']}")

        save_response("package_search", data, "package_search_recent.json")

def test_package_list():
    """Test package_list endpoint"""
    print("\n" + "="*60)
    print("Testing: package_list")
    print("="*60)

    data = make_request("package_list")

    if data.get("success"):
        result = data["result"]
        print(f"   Total packages: {len(result)}")
        print(f"   First 5 packages: {result[:5]}")

        save_response("package_list", data)
    else:
        print(f"   ❌ Error: {data.get('error')}")

def test_package_show():
    """Test package_show endpoint"""
    print("\n" + "="*60)
    print("Testing: package_show")
    print("="*60)

    # First get a dataset ID from package_search
    search_data = make_request("package_search", {"q": "*:*", "rows": 1})

    if search_data.get("success") and search_data["result"]["results"]:
        dataset_id = search_data["result"]["results"][0]["id"]
        dataset_name = search_data["result"]["results"][0]["name"]

        print(f"\n   Testing with dataset: {dataset_name}")

        data = make_request("package_show", {"id": dataset_id})

        if data.get("success"):
            result = data["result"]
            print(f"   ✅ Dataset title: {result['title']}")
            print(f"   Organization: {result['organization']['title']}")
            print(f"   Resources: {len(result['resources'])}")
            print(f"   Tags: {[t['name'] for t in result.get('tags', [])]}")

            save_response("package_show", data)
        else:
            print(f"   ❌ Error: {data.get('error')}")

def test_organization_list():
    """Test organization_list endpoint"""
    print("\n" + "="*60)
    print("Testing: organization_list")
    print("="*60)

    # Test 1: Simple list
    print("\n1. Simple organization list:")
    data = make_request("organization_list")

    if data.get("success"):
        result = data["result"]
        print(f"   Total organizations: {len(result)}")
        print(f"   First 5: {result[:5]}")

    # Test 2: Full details
    print("\n2. Organization list with full details:")
    data = make_request("organization_list", {"all_fields": "true"})

    if data.get("success"):
        result = data["result"]
        print(f"   Total organizations: {len(result)}")

        if result:
            # Sort by package count
            sorted_orgs = sorted(result, key=lambda x: x.get('package_count', 0), reverse=True)
            print("\n   Top 5 organizations by dataset count:")
            for i, org in enumerate(sorted_orgs[:5], 1):
                print(f"   {i}. {org['title']}: {org.get('package_count', 0)} datasets")

        save_response("organization_list", data, "organization_list_full.json")
    else:
        print(f"   ❌ Error: {data.get('error')}")

def test_organization_show():
    """Test organization_show endpoint"""
    print("\n" + "="*60)
    print("Testing: organization_show")
    print("="*60)

    # Get an organization ID first
    list_data = make_request("organization_list")

    if list_data.get("success") and list_data["result"]:
        org_id = list_data["result"][0]
        print(f"\n   Testing with organization: {org_id}")

        data = make_request("organization_show", {
            "id": org_id,
            "include_datasets": "false"
        })

        if data.get("success"):
            result = data["result"]
            print(f"   ✅ Organization: {result['title']}")
            print(f"   Display name: {result['display_name']}")
            print(f"   Package count: {result.get('package_count', 0)}")
            print(f"   Description: {result.get('description', 'N/A')[:100]}...")

            save_response("organization_show", data)
        else:
            print(f"   ❌ Error: {data.get('error')}")

def test_group_list():
    """Test group_list endpoint"""
    print("\n" + "="*60)
    print("Testing: group_list")
    print("="*60)

    # Test 1: Simple list
    print("\n1. Simple group list:")
    data = make_request("group_list")

    if data.get("success"):
        result = data["result"]
        print(f"   Total groups: {len(result)}")
        print(f"   Groups: {result}")

    # Test 2: Full details
    print("\n2. Group list with full details:")
    data = make_request("group_list", {"all_fields": "true"})

    if data.get("success"):
        result = data["result"]
        print(f"   Total groups: {len(result)}")

        if result:
            print("\n   Groups with package counts:")
            for group in result[:10]:
                print(f"   - {group['title']}: {group.get('package_count', 0)} datasets")

        save_response("group_list", data, "group_list_full.json")
    else:
        print(f"   ❌ Error: {data.get('error')}")

def test_group_show():
    """Test group_show endpoint"""
    print("\n" + "="*60)
    print("Testing: group_show")
    print("="*60)

    # Get a group ID first
    list_data = make_request("group_list")

    if list_data.get("success") and list_data["result"]:
        group_id = list_data["result"][0] if list_data["result"] else None

        if group_id:
            print(f"\n   Testing with group: {group_id}")

            data = make_request("group_show", {
                "id": group_id,
                "include_datasets": "false"
            })

            if data.get("success"):
                result = data["result"]
                print(f"   ✅ Group: {result['title']}")
                print(f"   Display name: {result['display_name']}")
                print(f"   Package count: {result.get('package_count', 0)}")

                save_response("group_show", data)
            else:
                print(f"   ❌ Error: {data.get('error')}")

def test_tag_list():
    """Test tag_list endpoint"""
    print("\n" + "="*60)
    print("Testing: tag_list")
    print("="*60)

    data = make_request("tag_list")

    if data.get("success"):
        result = data["result"]
        print(f"   Total tags: {len(result)}")
        print(f"   Sample tags: {result[:20]}")

        save_response("tag_list", data)
    else:
        print(f"   ❌ Error: {data.get('error')}")

def test_resource_search():
    """Test resource_search endpoint"""
    print("\n" + "="*60)
    print("Testing: resource_search")
    print("="*60)

    data = make_request("resource_search", {
        "query": "name:csv"
    })

    if data.get("success"):
        result = data["result"]
        print(f"   Total resources found: {result.get('count', 0)}")

        if result.get('results'):
            print(f"   Resources returned: {len(result['results'])}")
            first_resource = result['results'][0]
            print(f"   First resource: {first_resource.get('name', 'N/A')}")
            print(f"   Format: {first_resource.get('format', 'N/A')}")

        save_response("resource_search", data)
    else:
        print(f"   ❌ Error: {data.get('error')}")

def test_current_package_list_with_resources():
    """Test current_package_list_with_resources endpoint"""
    print("\n" + "="*60)
    print("Testing: current_package_list_with_resources")
    print("="*60)

    data = make_request("current_package_list_with_resources", {
        "limit": 5
    })

    if data.get("success"):
        result = data["result"]
        print(f"   Packages returned: {len(result)}")

        if result:
            first_pkg = result[0]
            print(f"   First package: {first_pkg.get('title', 'N/A')}")
            print(f"   Resources: {len(first_pkg.get('resources', []))}")

        save_response("current_package_list_with_resources", data)
    else:
        print(f"   ❌ Error: {data.get('error')}")

def main():
    """Run all endpoint tests"""
    print("="*60)
    print("DADOS.GOV.BR API ENDPOINT EXPLORER")
    print("="*60)
    print(f"\nAPI Base URL: {API_BASE_URL}")
    print(f"Token: {API_TOKEN[:30]}...")
    print("\nStarting endpoint exploration...\n")

    # Test all endpoints
    test_package_search()
    test_package_list()
    test_package_show()
    test_organization_list()
    test_organization_show()
    test_group_list()
    test_group_show()
    test_tag_list()
    test_resource_search()
    test_current_package_list_with_resources()

    print("\n" + "="*60)
    print("✅ API EXPLORATION COMPLETE")
    print("="*60)
    print("\nAll responses saved to ../references/ directory")

if __name__ == "__main__":
    main()