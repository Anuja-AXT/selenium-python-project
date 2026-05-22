from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class ConfirmationPage:
    def __init__(self, driver):
        self.driver = driver
        self.countryInput=(By.ID, "country")
        self.country_suggestions = (By.CSS_SELECTOR, ".suggestions ul li a")
        self.checkbox =(By.XPATH, "//div[@class='checkbox checkbox-primary']")
        self.submitbtn = (By.CSS_SELECTOR, "[type='submit']")
        self.success_msg = (By.XPATH, "//div[@class='alert alert-success alert-dismissible']")

    def enter_address(self, partialCountryName, expectedCountryName):
        self.driver.find_element(*self.countryInput).send_keys(partialCountryName)
        wait = WebDriverWait(self.driver, 10)
        wait.until(expected_conditions.presence_of_element_located(self.country_suggestions))

        countries = self.driver.find_elements(*self.country_suggestions)

        for country in countries:
            if country.text.strip() == expectedCountryName:
                country.click()
                break


        wait.until(expected_conditions.element_to_be_clickable(self.checkbox))
        self.driver.find_element(*self.checkbox).click()
        self.driver.find_element(*self.submitbtn).click()

    def validateOrder(self):

        message = self.driver.find_element(*self.success_msg).text
        assert "Success" in message