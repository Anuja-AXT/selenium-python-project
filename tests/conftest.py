import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from pageObjects.login import LoginPage
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "data", "test_config.json")
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name",  # The name of the custom option
        action="store",  # How the option behaves (e.g., store a value)
        default="chrome",  # Default value if the option is not provided
        help="browser selection"  # Help text for the option
    )

@pytest.fixture(scope="session")
def valid_creds():
    with open(CONFIG_PATH) as f:
        data = json.load(f)
    return data["valid_login"]


@pytest.fixture(scope="function")
def browserInstance(request):

    browser_name = request.config.getoption("browser_name")  # "--" will be added by default

    if browser_name == "chrome":

        options = ChromeOptions()
        service = ChromeService()
        driver = webdriver.Chrome(service=service, options=options)


    elif browser_name == "firefox":

        options = FirefoxOptions()
        # OPTIONAL but safe for Windows machines
        import os
        firefox_binary = os.getenv("FIREFOX_BINARY")
        if firefox_binary:
            options.binary_location = firefox_binary
        service = FirefoxService()
        driver = webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser_name: {browser_name}")
    driver.implicitly_wait(5)
    driver.get("https://rahulshettyacademy.com/loginpagePractise")
    yield driver
    driver.quit()



@pytest.fixture(scope="function")
def logged_in_shop_page(browserInstance, valid_creds):
    driver = browserInstance

    login_page = LoginPage(driver)

    # If you need User role popup, uncomment:
    # login_page.select_user_role()

    shop_page = login_page.login(
        valid_creds["username"],
        valid_creds["password"]
    )

    return shop_page
