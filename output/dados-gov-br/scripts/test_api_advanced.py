#!/usr/bin/env python3
"""
Advanced API testing with multiple authentication strategies
"""
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv('../../../.env')
API_KEY = os.getenv('GOVBR_API_KEY')

print("="*80)
print("ADVANCED API AUTHENTICATION TEST")
print("="*80)
print(f"API Key loaded: {API_KEY[:40]}...\n")

BASE_URL = "https://dados.gov.br/dados/api/publico/conjuntos-dados"
params = {"pagina": 1, "tamanhoPagina": 3}

def test_strategy(name, session, base_url=BASE_URL, params_override=None):
    """Test a specific authentication strategy"""
    print(f"\n{'='*80}")
    print(f"STRATEGY: {name}")
    print('='*80)
    
    test_params = params_override if params_override else params
    
    try:
        response = session.get(base_url, params=test_params, timeout=30, allow_redirects=False)
        
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 302:
            print(f"❌ Redirect to: {response.headers.get('Location', 'N/A')}")
            return False
        elif response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                print("✅ SUCCESS! JSON response received")
                data = response.json()
                print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                print(f"Sample data:\n{json.dumps(data, indent=2, ensure_ascii=False)[:800]}")
                
                # Save successful response
                with open('../references/api-responses/successful_auth.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print("\n💾 Response saved to: ../references/api-responses/successful_auth.json")
                
                return True
            else:
                print(f"⚠️  HTML response (length: {len(response.text)})")
                return False
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Strategy 1: Bearer Token (já testado, mas incluir para completude)
print("\n" + "="*80)
print("Strategy 1: Bearer Token in Authorization header")
print("="*80)
session1 = requests.Session()
session1.headers.update({
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})
result1 = test_strategy("Bearer Token", session1)

# Strategy 2: API Key as Cookie
print("\n" + "="*80)
print("Strategy 2: API Key as Cookie")
print("="*80)
session2 = requests.Session()
session2.cookies.set('api_key', API_KEY, domain='dados.gov.br')
session2.cookies.set('GOVBR_API_KEY', API_KEY, domain='dados.gov.br')
session2.headers.update({
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})
result2 = test_strategy("API Key Cookie", session2)

# Strategy 3: API Key as Query Parameter
print("\n" + "="*80)
print("Strategy 3: API Key as Query Parameter")
print("="*80)
session3 = requests.Session()
session3.headers.update({
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})
params_with_key = {**params, 'api_key': API_KEY}
result3 = test_strategy("Query Parameter", session3, params_override=params_with_key)

# Strategy 4: X-API-Key header
print("\n" + "="*80)
print("Strategy 4: X-API-Key header")
print("="*80)
session4 = requests.Session()
session4.headers.update({
    'X-API-Key': API_KEY,
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})
result4 = test_strategy("X-API-Key Header", session4)

# Strategy 5: X-Auth-Token header
print("\n" + "="*80)
print("Strategy 5: X-Auth-Token header")
print("="*80)
session5 = requests.Session()
session5.headers.update({
    'X-Auth-Token': API_KEY,
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})
result5 = test_strategy("X-Auth-Token Header", session5)

# Strategy 6: Try with access_token in query
print("\n" + "="*80)
print("Strategy 6: access_token Query Parameter")
print("="*80)
session6 = requests.Session()
session6.headers.update({
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})
params_with_token = {**params, 'access_token': API_KEY}
result6 = test_strategy("access_token Parameter", session6, params_override=params_with_token)

# Strategy 7: Try old CKAN API endpoint
print("\n" + "="*80)
print("Strategy 7: CKAN API v3 with Bearer Token")
print("="*80)
session7 = requests.Session()
session7.headers.update({
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})
ckan_url = "https://dados.gov.br/api/3/action/package_search"
ckan_params = {"rows": 3}
result7 = test_strategy("CKAN API v3", session7, base_url=ckan_url, params_override=ckan_params)

# Summary
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)
results = [
    ("Bearer Token", result1),
    ("API Key Cookie", result2),
    ("Query Parameter", result3),
    ("X-API-Key Header", result4),
    ("X-Auth-Token Header", result5),
    ("access_token Parameter", result6),
    ("CKAN API v3", result7),
]

success_count = sum(1 for _, result in results if result)
total_count = len(results)

print(f"\n✅ Successful: {success_count}/{total_count}")
print(f"❌ Failed: {total_count - success_count}/{total_count}\n")

for name, result in results:
    status = "✅" if result else "❌"
    print(f"  {status} {name}")

if success_count > 0:
    print("\n🎉 SUCCESS! At least one authentication method worked!")
    print("Check ../references/api-responses/successful_auth.json for the response")
else:
    print("\n⚠️  No authentication method worked with the API key.")
    print("Next step: Browser automation with Selenium is required.")
    print("\nRun: python test_api_selenium.py")

