#!/usr/bin/env python3
"""
OAuth2 Brasil Cidadão login automation
"""
import os
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

USERNAME = "06035782680"
PASSWORD = "t@Deu31!"

print("="*80)
print("OAUTH2 GOV.BR LOGIN - dados.gov.br API")
print("="*80)

def setup_driver():
    print("\n🔧 Setting up Chrome...")
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1600,1000')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("✅ Chrome ready\n")
    return driver

def oauth_login(driver):
    print("="*80)
    print("STEP 1: Navigate and click OAuth button")
    print("="*80)
    
    driver.get("https://dados.gov.br")
    print("✅ Loaded dados.gov.br")
    time.sleep(3)
    
    # Click OAuth2 login button
    print("\n🔍 Looking for OAuth2 gov.br login button...")
    try:
        # Try direct href
        oauth_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/oauth2/authorization/brasil-cidadao"]'))
        )
        print("✅ Found OAuth button!")
        oauth_link.click()
        print("✅ Clicked OAuth button")
        time.sleep(5)
        print(f"   Current URL: {driver.current_url}\n")
    except Exception as e:
        print(f"⚠️  Could not find OAuth button: {e}")
        print("   Trying alternative selectors...")
        try:
            # Try by class
            oauth_link = driver.find_element(By.CLASS_NAME, "login-button")
            oauth_link.click()
            print("✅ Clicked login button")
            time.sleep(5)
        except:
            print("❌ Could not find login button")
            return False
    
    print("="*80)
    print("STEP 2: Login on gov.br OAuth page")
    print("="*80)
    
    try:
        # Wait for CPF field on gov.br
        print("🔍 Waiting for CPF field...")
        cpf_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "accountId"))
        )
        print("✅ Found CPF field")
        
        # Enter CPF
        cpf_field.clear()
        cpf_field.send_keys(USERNAME)
        print(f"📝 Entered CPF: {USERNAME}")
        time.sleep(1)
        
        # Click continue
        print("🔍 Looking for continue button...")
        continue_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        continue_btn.click()
        print("✅ Clicked continue")
        time.sleep(4)
        
        # Wait for password field
        print("\n🔍 Waiting for password field...")
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        print("✅ Found password field")
        
        # Enter password
        password_field.clear()
        password_field.send_keys(PASSWORD)
        print("📝 Entered password")
        time.sleep(1)
        
        # Click login
        login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_btn.click()
        print("✅ Clicked login")
        time.sleep(6)
        
        # Check result
        current_url = driver.current_url
        print(f"\n📍 After login URL: {current_url}")
        
        if 'dados.gov.br' in current_url and 'signin' not in current_url:
            print("✅ LOGIN SUCCESSFUL!")
            return True
        else:
            print("⚠️  Login may require additional steps")
            return False
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        import traceback
        traceback.print_exc()
        return False

def capture_and_test(driver):
    print("\n" + "="*80)
    print("STEP 3: Capture cookies")
    print("="*80)
    
    cookies = driver.get_cookies()
    print(f"\n🍪 Captured {len(cookies)} cookies:")
    
    for cookie in cookies:
        name = cookie['name']
        value_preview = cookie['value'][:40]
        print(f"   - {name}: {value_preview}...")
        if 'JSESSIONID' in name:
            print(f"     ⭐⭐⭐ JSESSIONID FOUND! ⭐⭐⭐")
    
    # Save cookies
    os.makedirs('../references/api-responses', exist_ok=True)
    with open('../references/api-responses/oauth_cookies.json', 'w') as f:
        json.dump([{
            'name': c['name'],
            'value': c['value'],
            'domain': c.get('domain', ''),
            'path': c.get('path', '/')
        } for c in cookies], f, indent=2)
    print("\n💾 Cookies saved\n")
    
    print("="*80)
    print("STEP 4: Test API with cookies")
    print("="*80)
    
    # Create session with cookies
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
    
    # Test endpoint
    url = "https://dados.gov.br/dados/api/publico/conjuntos-dados"
    params = {"pagina": 1, "tamanhoPagina": 5}
    
    print(f"\n🔄 Request: {url}")
    print(f"   Params: {params}")
    
    response = session.get(url, params=params, timeout=30, allow_redirects=False)
    print(f"\n   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            print("\n   ✅✅✅ SUCCESS! JSON RESPONSE! ✅✅✅\n")
            
            data = response.json()
            
            # Show summary
            if isinstance(data, dict):
                print(f"   Response keys: {list(data.keys())}")
                if 'count' in data:
                    print(f"   Total datasets: {data['count']}")
                if 'results' in data and isinstance(data['results'], list):
                    print(f"   Datasets returned: {len(data['results'])}")
                    if data['results']:
                        print(f"\n   First dataset title: {data['results'][0].get('title', 'N/A')}")
            
            # Save
            with open('../references/api-responses/API_SUCCESS.json', 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n   💾 SAVED TO: API_SUCCESS.json")
            
            return True
        else:
            print(f"\n   ⚠️  HTML response (length: {len(response.text)})")
    elif response.status_code == 302:
        print(f"\n   ❌ Redirect to: {response.headers.get('Location')}")
    
    return False

driver = None
try:
    driver = setup_driver()
    
    # OAuth login
    login_ok = oauth_login(driver)
    
    if not login_ok:
        print("\n⚠️  Automated login failed. Please complete manually...")
        print("   Waiting 30 seconds for manual intervention...")
        time.sleep(30)
    
    # Capture and test
    success = capture_and_test(driver)
    
    print("\n" + "="*80)
    print("FINAL RESULT")
    print("="*80)
    
    if success:
        print("\n🎉🎉🎉 API ACCESS SUCCESSFUL! 🎉🎉🎉")
        print("\nCookies saved and working!")
        print("Check: ../references/api-responses/API_SUCCESS.json")
    else:
        print("\n❌ API access still blocked")
    
    print("\nBrowser stays open for 15 seconds...")
    time.sleep(15)
    
except KeyboardInterrupt:
    print("\n\n⚠️  Interrupted")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    if driver:
        driver.quit()
        print("\n✅ Browser closed\n")
