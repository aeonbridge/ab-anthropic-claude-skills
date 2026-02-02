#!/usr/bin/env python3
"""
Browser automation with Selenium to access dados.gov.br API
Handles session-based authentication
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
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../../../.env')
API_KEY = os.getenv('GOVBR_API_KEY')

print("="*80)
print("SELENIUM BROWSER AUTOMATION - dados.gov.br API")
print("="*80)
print(f"API Key: {API_KEY[:40]}...\n")

def setup_driver():
    """Configure and return Chrome WebDriver"""
    print("🔧 Setting up Chrome WebDriver...")
    
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Uncomment for headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
    
    # Auto-install ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print("✅ WebDriver ready\n")
    return driver

def navigate_to_api_docs(driver):
    """Navigate to Swagger UI"""
    print("🌐 Navigating to Swagger UI...")
    driver.get("https://dados.gov.br/swagger-ui/index.html")
    time.sleep(3)
    print(f"✅ Current URL: {driver.current_url}")
    print(f"   Page title: {driver.title}\n")
    return driver.current_url

def check_authentication_status(driver):
    """Check if user is authenticated"""
    print("🔍 Checking authentication status...")
    
    # Check current URL
    current_url = driver.current_url
    print(f"   Current URL: {current_url}")
    
    # Check if redirected to login
    if 'signin' in current_url or 'login' in current_url:
        print("   ❌ Not authenticated - Redirected to login page\n")
        return False
    
    # Check page title
    title = driver.title
    print(f"   Page title: {title}")
    
    if 'Swagger' in title or 'API' in title:
        print("   ✅ Appears to be on API documentation page\n")
        return True
    
    print("   ⚠️  Uncertain authentication state\n")
    return False

def capture_cookies(driver):
    """Capture all cookies from browser"""
    print("🍪 Capturing session cookies...")
    cookies = driver.get_cookies()
    
    print(f"   Found {len(cookies)} cookies:")
    for cookie in cookies:
        print(f"   - {cookie['name']}: {cookie['value'][:30]}...")
    
    print()
    return cookies

def test_api_with_cookies(cookies):
    """Test API access using captured cookies"""
    print("="*80)
    print("TESTING API WITH CAPTURED COOKIES")
    print("="*80)
    
    # Create session with cookies
    session = requests.Session()
    
    for cookie in cookies:
        session.cookies.set(
            cookie['name'],
            cookie['value'],
            domain=cookie.get('domain', ''),
            path=cookie.get('path', '/')
        )
    
    # Add headers
    session.headers.update({
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://dados.gov.br/swagger-ui/index.html'
    })
    
    # Test endpoint
    url = "https://dados.gov.br/dados/api/publico/conjuntos-dados"
    params = {"pagina": 1, "tamanhoPagina": 5}
    
    print(f"\n🔄 Making request to: {url}")
    print(f"   Parameters: {params}\n")
    
    try:
        response = session.get(url, params=params, timeout=30, allow_redirects=False)
        
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 302:
            print(f"❌ Still redirecting to: {response.headers.get('Location', 'N/A')}")
            print("   Cookies may not be sufficient\n")
            return False
            
        elif response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            
            if 'application/json' in content_type:
                print("✅ SUCCESS! JSON response received!\n")
                data = response.json()
                
                # Display response info
                print("Response structure:")
                if isinstance(data, dict):
                    print(f"  Top-level keys: {list(data.keys())}")
                    if 'result' in data:
                        result = data['result']
                        if isinstance(result, dict):
                            print(f"  Result keys: {list(result.keys())}")
                            if 'count' in result:
                                print(f"  Total datasets: {result['count']}")
                            if 'results' in result and isinstance(result['results'], list):
                                print(f"  Datasets in page: {len(result['results'])}")
                
                # Save response
                os.makedirs('../references/api-responses', exist_ok=True)
                output_file = '../references/api-responses/selenium_success.json'
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"\n💾 Full response saved to: {output_file}")
                
                # Save cookies for reuse
                cookies_file = '../references/api-responses/session_cookies.json'
                with open(cookies_file, 'w', encoding='utf-8') as f:
                    json.dump([
                        {
                            'name': c['name'],
                            'value': c['value'],
                            'domain': c.get('domain', ''),
                            'path': c.get('path', '/')
                        }
                        for c in cookies
                    ], f, indent=2)
                
                print(f"🍪 Cookies saved to: {cookies_file}")
                print("\n✅ You can now reuse these cookies for API access!")
                
                return True
            else:
                print(f"⚠️  HTML response received (length: {len(response.text)})")
                return False
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main execution"""
    driver = None
    
    try:
        # Setup browser
        driver = setup_driver()
        
        # Navigate to API docs
        navigate_to_api_docs(driver)
        
        # Check authentication
        is_authenticated = check_authentication_status(driver)
        
        if not is_authenticated:
            print("="*80)
            print("MANUAL LOGIN REQUIRED")
            print("="*80)
            print("\nThe browser is open but not authenticated.")
            print("\nPLEASE:")
            print("1. Complete the login process in the browser window")
            print("2. Navigate to the Swagger UI or any authenticated page")
            print("3. Press ENTER here when you're logged in")
            print()
            input("Press ENTER after logging in... ")
            
            # Re-check after manual login
            print("\n🔍 Re-checking authentication...")
            time.sleep(2)
            is_authenticated = check_authentication_status(driver)
        
        # Capture cookies
        cookies = capture_cookies(driver)
        
        # Test API with cookies
        success = test_api_with_cookies(cookies)
        
        if success:
            print("\n" + "="*80)
            print("🎉 SUCCESS! API access established with browser session")
            print("="*80)
        else:
            print("\n" + "="*80)
            print("⚠️  API access still blocked")
            print("="*80)
            print("\nPossible reasons:")
            print("- Account may not have API access enabled")
            print("- Additional authentication steps required")
            print("- API may require manual interaction in Swagger UI")
        
        # Keep browser open for inspection
        print("\n📌 Browser will stay open for 10 seconds for inspection...")
        time.sleep(10)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            print("\n🔒 Closing browser...")
            driver.quit()
            print("✅ Browser closed\n")

if __name__ == "__main__":
    main()
