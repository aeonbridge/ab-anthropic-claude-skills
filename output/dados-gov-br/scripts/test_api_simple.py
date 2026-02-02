#!/usr/bin/env python3
"""
Simple API test with the provided token
"""
import requests
import json

API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJPaEx6RktTZWNUR1c0V25KT1NLbjFuYU5NTWxTSWxEX29RUGxpZHk5NXN3OUYtT2Zadm9sZnVjX0UtdlZyTzRNT2FTcGNHUGNOMzN4VXNpNiIsImlhdCI6MTc0MjI0Njk4N30.LOboeht1ujLjjS3Qsyn3nlGXbguCN4sb2xIsIenK52s"

# Test 1: Simple GET without auth
print("="*70)
print("Test 1: Public endpoint without auth")
print("="*70)
url = "https://dados.gov.br/dados/api/publico/conjuntos-dados"
params = {"pagina": 1, "tamanhoPagina": 2}
headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, params=params, headers=headers, timeout=30)
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Response length: {len(response.text)}")
print(f"First 500 chars:\n{response.text[:500]}")

# Test 2: With Bearer token
print("\n" + "="*70)
print("Test 2: With Bearer token")
print("="*70)
headers["Authorization"] = f"Bearer {API_TOKEN}"

response = requests.get(url, params=params, headers=headers, timeout=30)
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Response length: {len(response.text)}")
print(f"First 500 chars:\n{response.text[:500]}")

# Test 3: Check if it's a redirect
print("\n" + "="*70)
print("Test 3: Check response details")
print("="*70)
print(f"URL final: {response.url}")
print(f"History: {response.history}")
print(f"Headers recebidos:")
for key, value in list(response.headers.items())[:10]:
    print(f"  {key}: {value}")
