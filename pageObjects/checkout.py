import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageObjects.confirmation import ConfirmationPage


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.checkoutBtn = (By.XPATH, "//button[@class='btn btn-success']")
        self.cart_product_names = (By.CSS_SELECTOR, "h4.media-heading a")
        self.grand_total = (By.CSS_SELECTOR, "h3 strong")

    def checkout(self):
        self.driver.find_element(*self.checkoutBtn).click()
        confirmation_page = ConfirmationPage(self.driver)
        return confirmation_page

    def get_cart_product_names(self):

        elements = self.driver.find_elements(*self.cart_product_names)
        return [e.text.strip() for e in elements]


    def _digits(self, text: str) -> int:
        digits_only = "".join(ch for ch in text if ch.isdigit())
        return int(digits_only) if digits_only else 0

    def get_grand_total_value(self) -> int:
        el = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.grand_total)
        )
        return self._digits(el.text.strip())

    def get_line_total_for_product(self, product_name: str) -> int:
        # Total column (4th td) for that product row
        locator = (
            By.XPATH,
            f"//h4/a[normalize-space()='{product_name}']/ancestor::tr/td[4]"
        )
        el = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(locator))
        return self._digits(el.text.strip())

    def get_line_totals_map(self) -> dict:
        """
        Returns dict of {product_name: line_total} for current cart.
        """
        names = self.get_cart_product_names()
        return {name: self.get_line_total_for_product(name) for name in names}

    def remove_product_by_name(self, product_name: str):
        remove_btn = (
            By.XPATH,
            f"//h4/a[normalize-space()='{product_name}']/ancestor::tr//button[contains(@class,'btn-danger')]"
        )
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(remove_btn)).click()

        # Wait until product is removed from DOM/cart list
        WebDriverWait(self.driver, 5).until(
            lambda d: product_name not in self.get_cart_product_names()
        )

    def remove_products(self, products_to_remove):
        """
        Remove multiple products safely, one by one.
        """
        for p in products_to_remove:
            if p in self.get_cart_product_names():
                self.remove_product_by_name(p)

    def _row_for_product(self, product_name: str):
        row = (
            By.XPATH,
            f"//h4/a[normalize-space()='{product_name}']/ancestor::tr"
        )
        return WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(row))

    # ---------- Locators (product specific) ----------

    def _row(self, product_name):
        return (
            By.XPATH,
            f"//a[text()='{product_name}']/ancestor::tr"
        )

    def _quantity_input(self, product_name):
        return (
            By.XPATH,
            f"//a[text()='{product_name}']/ancestor::tr//input[@type='number']"
        )

    def _line_total(self, product_name):
        return (
            By.XPATH,
            f"//a[text()='{product_name}']/ancestor::tr/td[4]"
        )

    # ---------- Quantity Methods ----------

    def set_quantity(self, product_name: str, qty: int):
        """
        Sets quantity directly (reliable alternative to spinner arrows)
        """
        inp = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self._quantity_input(product_name))
        )
        inp.click()
        inp.send_keys(Keys.CONTROL + "a")
        inp.send_keys(str(qty))
        inp.send_keys(Keys.TAB)  # triggers recalculation

    def get_quantity(self, product_name: str) -> int:
        inp = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self._quantity_input(product_name))
        )
        return int(inp.get_attribute("value"))

