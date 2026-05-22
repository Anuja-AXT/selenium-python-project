import time


from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageObjects.shop import shopPage

class LoginPage:
    def __init__(self, driver):


        self.driver= driver
        self.error_msg = (By.CSS_SELECTOR, "div.alert.alert-danger")
        self.username_input = (By.ID, "username")
        self.password_input = (By.NAME, "password")
        self.signIn = (By.ID, "signInBtn")
        self.okay_button= ((By.ID, "okayBtn"))
        self.user_role = (By.XPATH, "//input[@value='user']")
    def login(self, username , password):

        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.signIn).click()
        shop_page = shopPage(self.driver)
        return shop_page

    def submit_login(self, username="", password=""):

        self.driver.find_element(*self.username_input).clear()
        if username:
            self.driver.find_element(*self.username_input).send_keys(username)

        self.driver.find_element(*self.password_input).clear()
        if password:
            self.driver.find_element(*self.password_input).send_keys(password)

        self.driver.find_element(*self.signIn).click()

    def is_error_displayed(self, timeout=3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.error_msg)
            )
            return True
        except TimeoutException:
            return False

    def get_error_text(self) -> str:
        el = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.error_msg)
        )
        return el.text.strip()

    def select_user_role(self):
        self.driver.find_element(*self.user_role).click()
        self.handle_user_role_popup()

    def handle_user_role_popup(self, timeout=5):
        """
        Handles the popup that appears when 'User' role is selected.
        Clicks 'Okay' if popup appears.
        """

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.okay_button)
            )
            self.driver.find_element(*self.okay_button).click()
        except TimeoutException:
            # Popup did not appear (safe to continue)
            pass

    def is_user_role_selected(self) -> bool:
        return self.driver.find_element(*self.user_role).is_selected()