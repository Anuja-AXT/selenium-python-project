import os, json, pytest
from pageObjects.login import LoginPage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "test_end_to_end_checkout.json")

with open(DATA_FILE) as f:
    test_data = json.load(f)
    test_list = test_data["data"]
@pytest.mark.parametrize("test_list_item", test_list)
@pytest.mark.smoke
def test_e2e_purchase_flow(browserInstance,test_list_item ):
    driver= browserInstance
    loginpage = LoginPage(driver)
    shop_page = loginpage.login(test_list_item["userEmail"],test_list_item["userPassword"] )
    shop_page.add_products_to_cart(test_list_item["productName"])
    checkout_page = shop_page.go_to_cart()
    confirmation_page =checkout_page.checkout()
    confirmation_page.enter_address(test_list_item["partialCountryName"],test_list_item["expectedCountryName"] )
    confirmation_page.validateOrder()


