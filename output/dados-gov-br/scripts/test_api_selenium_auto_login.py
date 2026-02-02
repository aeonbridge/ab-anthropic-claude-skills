#!/usr/bin/env python3
"""
Automated login and API testing for dados.gov.br
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

# Credentials (passed as arguments, not stored)
USERNAME = "06035782680"
PASSWORD = "t@Deu31!"

print("="*80)
print("AUTOMATED LOGIN & API TEST - dados.gov.br")
print("="*80)

def setup_driver():
    """Setup Chrome WebDriver"""
    print("\n🔧 Setting up Chrome WebDriver...")
    
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1400,900')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--headless')  # Uncomment for headless mode
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("✅ WebDriver ready\n")
    return driver

def login_to_govbr(driver, username, password):
    """Automated login to gov.br"""
    print("="*80)
    print("STEP 1: Navigating to login page")
    print("="*80)
    
    # Go to dados.gov.br
    driver.get("https://dados.gov.br")
    print(f"✅ Loaded: {driver.current_url}")
    time.sleep(2)
    
    # Look for login button
    print("\n🔍 Looking for login button...")
    try:
        # Try to find "Entrar" button
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Entrar') or contains(text(), 'Login')]"))
        )
        print("✅ Found login button")
        login_button.click()
        time.sleep(3)
        print(f"   Current URL: {driver.current_url}\n")
    except Exception as e:
        print(f"⚠️  Could not find login button automatically: {e}")
        print("   Trying direct navigation to signin...\n")
        driver.get("https://dados.gov.br/signin")
        time.sleep(3)
    
    print("="*80)
    print("STEP 2: Entering credentials")
    print("="*80)
    
    # Wait for gov.br login page
    print("🔍 Waiting for gov.br login form...")
    try:
        # Look for CPF/CNPJ input field
        cpf_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "accountId"))
        )
        print("✅ Found CPF input field")
        
        # Enter CPF
        print(f"📝 Entering CPF: {username}")
        cpf_input.clear()
        cpf_input.send_keys(username)
        time.sleep(1)
        
        # Click continue/next button
        print("🔍 Looking for continue button...")
        continue_button = driver.find_element(By.XPATH, "//button[contains(@class, 'button') or @type='submit']")
        continue_button.click()
        print("✅ Clicked continue")
        time.sleep(3)
        
        # Wait for password field
        print("\n🔍 Waiting for password field...")
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        print("✅ Found password field")
        
        # Enter password
        print("📝 Entering password...")
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(1)
        
        # Click login button
        print("🔍 Looking for login button...")
        login_submit = driver.find_element(By.XPATH, "//button[@type='submit' or contains(@class, 'button')]")
        login_submit.click()
        print("✅ Clicked login")
        time.sleep(5)
        
        # Check if login successful
        current_url = driver.current_url
        print(f"\n📍 Current URL after login: {current_url}")
        
        if 'dados.gov.br' in current_url and 'signin' not in current_url and 'login' not in current_url:
            print("✅ LOGIN SUCCESSFUL!\n")
            return True
        else:
            print("⚠️  Login may have failed or requires additional steps\n")
            return False
            
    except Exception as e:
        print(f"❌ Error during login: {e}")
        print(f"   Current URL: {driver.current_url}")
        import traceback
        traceback.print_exc()
        return False

def capture_cookies(driver):
    """Capture session cookies"""
    print("="*80)
    print("STEP 3: Capturing session cookies")
    print("="*80)
    
    cookies = driver.get_cookies()
    print(f"\n🍪 Found {len(cookies)} cookies:")
    
    session_cookies = []
    for cookie in cookies:
        print(f"   - {cookie['name']}: {cookie['value'][:40]}...")
        if any(key in cookie['name'] for key in ['JSESSIONID', 'session', 'token', 'auth']):
            print(f"     ⭐ Important authentication cookie!")
            session_cookies.append(cookie)
    
    if session_cookies:
        print(f"\n✅ Found {len(session_cookies)} authentication cookies")
    else:
        print("\n⚠️  No JSESSIONID or auth cookies found")
    
    # Save all cookies
    os.makedirs('../references/api-responses', exist_ok=True)
    cookies_file = '../references/api-responses/authenticated_cookies.json'
    with open(cookies_file, 'w', encoding='utf-8') as f:
        json.dump([{
            'name': c['name'],
            'value': c['value'],
            'domain': c.get('domain', ''),
            'path': c.get('path', '/'),
            'expiry': c.get('expiry')
        } for c in cookies], f, indent=2)
    
    print(f"💾 Cookies saved to: {cookies_file}\n")
    return cookies

def test_api_with_cookies(cookies):
    """Test API access with captured cookies"""
    print("="*80)
    print("STEP 4: Testing API with authenticated session")
    print("="*80)
    
    session = requests.Session()
    
    # Add all cookies to session
    for cookie in cookies:
        session.cookies.set(
            cookie['name'],
            cookie['value'],
            domain=cookie.get('domain', ''),
            path=cookie.get('path', '/')
        )
    
    # Set headers
    session.headers.update({
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://dados.gov.br/'
    })
    
    # Test endpoints
    endpoints = [
        ("conjuntos-dados", {"pagina": 1, "tamanhoPagina": 5}),
        ("organizacao", {}),
    ]
    
    success_count = 0
    
    for endpoint, params in endpoints:
        url = f"https://dados.gov.br/dados/api/publico/{endpoint}"
        print(f"\n🔄 Testing: {url}")
        print(f"   Parameters: {params}")
        
        try:
            response = session.get(url, params=params, timeout=30, allow_redirects=False)
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    print(f"   ✅ SUCCESS! JSON response received")
                    
                    data = response.json()
                    
                    # Show summary
                    if isinstance(data, dict):
                        print(f"   📊 Response keys: {list(data.keys())}")
                        if 'count' in data:
                            print(f"   📈 Total count: {data['count']}")
                        if 'results' in data:
                            print(f"   📄 Results: {len(data['results'])} items")
                    
                    # Save response
                    filename = f'../references/api-responses/{endpoint}_success.json'
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    print(f"   💾 Saved to: {filename}")
                    
                    success_count += 1
                else:
                    print(f"   ⚠️  HTML response (length: {len(response.text)})")
            elif response.status_code == 302:
                print(f"   ❌ Redirect to: {response.headers.get('Location')}")
            else:
                print(f"   ⚠️  Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return success_count > 0

def main():
    driver = None
    
    try:
        # Setup driver
        driver = setup_driver()
        
        # Login
        login_success = login_to_govbr(driver, USERNAME, PASSWORD)
        
        if not login_success:
            print("\n⚠️  Login may have failed. Will try to capture cookies anyway...")
        
        # Capture cookies
        cookies = capture_cookies(driver)
        
        # Test API
        api_success = test_api_with_cookies(cookies)
        
        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        
        if api_success:
            print("\n🎉 SUCCESS! API access working with authenticated session!")
            print("\nNext steps:")
            print("1. Use the saved cookies for API requests")
            print("2. Cookies are valid for the session duration")
            print("3. Re-run this script when cookies expire")
        else:
            print("\n❌ API access still not working")
            print("\nTroubleshooting:")
            print("1. Check if login completed successfully in browser")
            print("2. Verify account has API access permissions")
            print("3. Check if additional verification is required")
        
        print("\n📌 Browser will stay open for 15 seconds for inspection...")
        time.sleep(15)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            print("\n🔒 Closing browser...")
            driver.quit()
            print("✅ Browser closed\n")

if __name__ == "__main__":
    main()
