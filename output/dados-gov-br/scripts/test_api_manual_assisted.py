#!/usr/bin/env python3
"""
Manual-assisted browser automation
Opens browser, waits for manual login, then captures cookies
"""
import os
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

print("="*80)
print("MANUAL-ASSISTED API TEST - dados.gov.br")
print("="*80)

def setup_driver():
    print("\n🔧 Setting up Chrome...")
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1400,900')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("✅ Chrome ready\n")
    return driver

def test_api_with_cookies(cookies):
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'], 
                          domain=cookie.get('domain', ''), 
                          path=cookie.get('path', '/'))
    
    session.headers.update({
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://dados.gov.br/'
    })
    
    url = "https://dados.gov.br/dados/api/publico/conjuntos-dados"
    params = {"pagina": 1, "tamanhoPagina": 5}
    
    print(f"\n🔄 Testing API: {url}")
    response = session.get(url, params=params, timeout=30, allow_redirects=False)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type', ''):
        print("   ✅ SUCCESS! JSON response")
        data = response.json()
        
        # Save response
        os.makedirs('../references/api-responses', exist_ok=True)
        with open('../references/api-responses/authenticated_success.json', 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("   💾 Saved to: authenticated_success.json")
        return True
    elif response.status_code == 302:
        print(f"   ❌ Still redirecting to: {response.headers.get('Location')}")
    else:
        print(f"   ⚠️  Status {response.status_code}, Content-Type: {response.headers.get('Content-Type')}")
    
    return False

driver = None
try:
    driver = setup_driver()
    
    print("="*80)
    print("STEP 1: Opening dados.gov.br")
    print("="*80)
    driver.get("https://dados.gov.br/signin")
    print("✅ Page loaded\n")
    time.sleep(3)
    
    print("="*80)
    print("PLEASE LOGIN MANUALLY NOW")
    print("="*80)
    print("\nIn the Chrome window:")
    print("1. Enter CPF: 06035782680")
    print("2. Enter password: t@Deu31!")
    print("3. Complete login")
    print("4. Wait until you see the main page (NOT signin)")
    print("\nI'll check every 10 seconds...\n")
    
    # Check periodically for login
    for i in range(30):  # Check for 5 minutes
        time.sleep(10)
        url = driver.current_url
        print(f"⏱️  [{i+1}/30] Current URL: {url}")
        
        if 'signin' not in url and 'login' not in url:
            print("\n✅ Detected: Not on signin page anymore!\n")
            break
    
    print("="*80)
    print("STEP 2: Capturing cookies")
    print("="*80)
    
    cookies = driver.get_cookies()
    print(f"\n🍪 Captured {len(cookies)} cookies")
    
    for cookie in cookies:
        name = cookie['name']
        value = cookie['value'][:40]
        print(f"   - {name}: {value}...")
        if 'JSESSIONID' in name or 'session' in name.lower():
            print(f"     ⭐ AUTHENTICATION COOKIE!")
    
    # Save cookies
    os.makedirs('../references/api-responses', exist_ok=True)
    with open('../references/api-responses/session_cookies.json', 'w') as f:
        json.dump([{
            'name': c['name'],
            'value': c['value'],
            'domain': c.get('domain', ''),
            'path': c.get('path', '/')
        } for c in cookies], f, indent=2)
    print("\n💾 Cookies saved\n")
    
    print("="*80)
    print("STEP 3: Testing API")
    print("="*80)
    
    success = test_api_with_cookies(cookies)
    
    print("\n" + "="*80)
    if success:
        print("🎉 SUCCESS! API WORKING!")
    else:
        print("❌ API still not accessible")
        print("\nThis may mean:")
        print("- API requires additional permissions")
        print("- Account doesn't have API access")
        print("- Need to use Swagger UI directly")
    print("="*80)
    
    print("\nKeeping browser open for 20 seconds...")
    time.sleep(20)
    
except KeyboardInterrupt:
    print("\n\n⚠️  Interrupted")
finally:
    if driver:
        driver.quit()
        print("\n✅ Browser closed\n")
