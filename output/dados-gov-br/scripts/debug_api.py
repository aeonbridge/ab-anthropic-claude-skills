#!/usr/bin/env python3
"""
Debug script to test dados.gov.br API authentication and responses
"""

import requests
import json

# API Configuration
API_BASE_URL = "https://dados.gov.br/api/3/action"
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJPaEx6RktTZWNUR1c0V25KT1NLbjFuYU5NTWxTSWxEX29RUGxpZHk5NXN3OUYtT2Zadm9sZnVjX0UtdlZyTzRNT2FTcGNHUGNOMzN4VXNpNiIsImlhdCI6MTc0MjI0Njk4N30.LOboeht1ujLjjS3Qsyn3nlGXbguCN4sb2xIsIenK52s"

print("="*60)
print("DADOS.GOV.BR API DEBUG")
print("="*60)

# Test 1: No authentication
print("\n1. Testing without authentication:")
url = f"{API_BASE_URL}/package_list"
response = requests.get(url, timeout=30)
print(f"   Status Code: {response.status_code}")
print(f"   Content-Type: {response.headers.get('Content-Type')}")
print(f"   Response Length: {len(response.text)}")
print(f"   First 500 chars: {response.text[:500]}")

# Test 2: With Bearer token
print("\n2. Testing with Bearer token in header:")
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}
response = requests.get(url, headers=headers, timeout=30)
print(f"   Status Code: {response.status_code}")
print(f"   Content-Type: {response.headers.get('Content-Type')}")
print(f"   Response Length: {len(response.text)}")
print(f"   First 500 chars: {response.text[:500]}")

# Test 3: With X-CKAN-API-Key header (CKAN standard)
print("\n3. Testing with X-CKAN-API-Key header:")
headers = {
    "X-CKAN-API-Key": API_TOKEN
}
response = requests.get(url, headers=headers, timeout=30)
print(f"   Status Code: {response.status_code}")
print(f"   Content-Type: {response.headers.get('Content-Type')}")
print(f"   Response Length: {len(response.text)}")
print(f"   First 500 chars: {response.text[:500]}")

# Test 4: Try a simple search
print("\n4. Testing package_search endpoint:")
url = f"{API_BASE_URL}/package_search"
params = {"q": "*:*", "rows": 1}
response = requests.get(url, params=params, timeout=30)
print(f"   Status Code: {response.status_code}")
print(f"   Content-Type: {response.headers.get('Content-Type')}")
print(f"   Response Length: {len(response.text)}")
print(f"   First 1000 chars: {response.text[:1000]}")

# Try to parse JSON
try:
    data = response.json()
    print(f"\n   ✅ JSON parsed successfully!")
    print(f"   Success: {data.get('success')}")
    if data.get('result'):
        print(f"   Result keys: {list(data['result'].keys())}")
except json.JSONDecodeError as e:
    print(f"\n   ❌ JSON decode error: {e}")

# Test 5: Check if it's HTML (JavaScript required page)
if "<!DOCTYPE" in response.text or "<html" in response.text.lower():
    print("\n   ⚠️  Response is HTML, not JSON - might need JavaScript")

# Test 6: Check headers
print("\n5. Response Headers:")
for key, value in response.headers.items():
    print(f"   {key}: {value}")