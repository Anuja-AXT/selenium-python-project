import os
# from selenium.webdriver.chrome import webdriver
import time
import json

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from pageObjects.checkout import CheckoutPage
from pageObjects.login import LoginPage
from pageObjects.shop import shopPage
from pageObjects.confirmation import ConfirmationPage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "test_end_to_end_checkout.json")

with open(DATA_FILE) as f:
    test_data = json.load(f)
    test_list = test_data["data"]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "test_login_negative.json")

with open(DATA_FILE) as f:
    test_data = json.load(f)["data"]


@pytest.mark.regression
@pytest.mark.parametrize("item", test_data, ids=lambda d: d["name"])
def test_login_negative_cases(browserInstance, item):
    driver = browserInstance
    login_page = LoginPage(driver)

    # 🔑 calling function written in LoginPage
    login_page.submit_login(
        username=item["username"],
        password=item["password"]
    )
    assert login_page.is_error_displayed()
    actual_error = login_page.get_error_text()
    assert item["expected_error"] in actual_error