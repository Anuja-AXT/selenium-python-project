import os
import json
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "test_cart_quantity_update.json")

with open(DATA_FILE) as f:
    test_data = json.load(f)["data"]


@pytest.mark.parametrize("item", test_data, ids=lambda d: d["name"])
@pytest.mark.regression
def test_quantity_plus_minus_updates_totals(logged_in_shop_page, item):

    shop_page = logged_in_shop_page

    product = item["product"]
    increase_to = item["increase_to"]
    decrease_to = item["decrease_to"]

    # Step 1: Add product and open cart
    shop_page.add_products_to_cart(product)
    checkout_page = shop_page.go_to_cart()

    # Step 2: Capture baseline values
    qty_before = checkout_page.get_quantity(product)
    line_total_before = checkout_page.get_line_total_for_product(product)
    grand_total_before = checkout_page.get_grand_total_value()

    # Validate baseline (single product cart)
    assert line_total_before == grand_total_before

    # Step 3: Increase quantity
    checkout_page.set_quantity(product, increase_to)

    qty_after_increase = checkout_page.get_quantity(product)
    line_total_after_increase = checkout_page.get_line_total_for_product(product)
    grand_total_after_increase = checkout_page.get_grand_total_value()

    assert qty_after_increase == increase_to
    assert line_total_after_increase == line_total_before * increase_to
    assert grand_total_after_increase == line_total_after_increase

    # Step 4: Decrease quantity back
    checkout_page.set_quantity(product, decrease_to)

    qty_after_decrease = checkout_page.get_quantity(product)
    line_total_after_decrease = checkout_page.get_line_total_for_product(product)
    grand_total_after_decrease = checkout_page.get_grand_total_value()

    assert qty_after_decrease == decrease_to
    assert line_total_after_decrease == line_total_before
    assert grand_total_after_decrease == grand_total_before