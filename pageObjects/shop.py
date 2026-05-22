from selenium.webdriver.common.by import By

from pageObjects.checkout import CheckoutPage


class shopPage():
    def __init__(self, driver):

        self.driver = driver
        self.shoplink= (By.CSS_SELECTOR, "a[href*='shop']")
        #self.shoplink = (By.CSS_SELECTOR, "//a[normalize-space()='Shop']")
        self.productCards = (By.XPATH, "//div[@class='card h-100']")
        self.checkoutBtn = (By.CSS_SELECTOR, "a[class*='btn-primary']")

    def add_products_to_cart(self, product_names):
        self.driver.find_element(*self.shoplink).click()
        products = self.driver.find_elements(*self.productCards)

        # If single product passed as string → convert to list
        #isinstance() — Type Checking
        if isinstance(product_names, str):
            product_names = [product_names]

        for product_name in product_names:
            for product in products:
                name = product.find_element(By.XPATH, "div/h4/a").text
                if name == product_name:
                    product.find_element(By.XPATH, "div/button").click()
                    break

    def get_checkout_count(self) -> int:
        text = self.driver.find_element(*self.checkoutBtn).text
        count = int(text.split("(")[1].split(")")[0])
        return count

    def go_to_cart(self):
        self.driver.find_element(*self.checkoutBtn).click()
        checkout_page = CheckoutPage(self.driver)
        return checkout_page


