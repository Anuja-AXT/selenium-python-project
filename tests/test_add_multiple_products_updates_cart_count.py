import os
import json
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "test_add_multiple_products_updates_cart_count.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    test_data = json.load(f)["data"]


@pytest.mark.parametrize("item", test_data, ids=lambda d: d["name"])
def test_add_products_verify_count_and_cart(logged_in_shop_page, item):
    shop_page = logged_in_shop_page

    products_to_add = item["products"]

    # Add products (your single method supports list input)
    shop_page.add_products_to_cart(products_to_add)

    # Verify checkout count equals number of products added
    assert shop_page.get_checkout_count() == len(products_to_add)

    # Go to cart and verify each product is present
    checkout_page = shop_page.go_to_cart()
    cart_products = checkout_page.get_cart_product_names()


    for p in products_to_add:
        assert p in cart_products
