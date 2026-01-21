import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = 'https://opensource-demo.orangehrmlive.com/web/index.php/auth/login'
USERNAME = 'Admin'
PASSWORD = 'admin123'
USERNAME_XPATH = "//input[@name='username']"
PASSWORD_XPATH = "//input[@name='password']"
LOGIN_BUTTON_XPATH = "//button[@type='submit']"
DASHBOARD_URL_FRAGMENT = '/dashboard'

@pytest.fixture(scope='function')
def driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    yield driver
    driver.quit()

def test_login_orangehrm(driver):
    """
    Jira Ticket: KAN-15
    Summary: Automate login functionality for OrangeHRM
    Description: Verify that a valid user can successfully log in to the application.
    Steps:
        1. Navigate to the login page
        2. Enter valid username
        3. Enter valid password
        4. Click on Login button
    Expected Result:
        User should be redirected to the dashboard page.
    """
    try:
        driver.get(LOGIN_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, USERNAME_XPATH)))
        username_input = driver.find_element(By.XPATH, USERNAME_XPATH)
        password_input = driver.find_element(By.XPATH, PASSWORD_XPATH)
        login_button = driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH)
        username_input.clear()
        username_input.send_keys(USERNAME)
        password_input.clear()
        password_input.send_keys(PASSWORD)
        login_button.click()
        WebDriverWait(driver, 15).until(
            lambda d: DASHBOARD_URL_FRAGMENT in d.current_url or
                      EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))(d)
        )
        # Assertion: Validate redirection to dashboard
        current_url = driver.current_url
        dashboard_header_present = False
        try:
            dashboard_header_present = driver.find_element(By.XPATH, "//h6[text()='Dashboard']") is not None
        except Exception:
            dashboard_header_present = False
        assert DASHBOARD_URL_FRAGMENT in current_url or dashboard_header_present, (
            f"Login failed. Current URL: {current_url}. Dashboard header present: {dashboard_header_present}"
        )
    except Exception as e:
        pytest.fail(f"Test failed due to unexpected error: {str(e)}")
