import os
import json
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "test_cart_remove_items.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    test_data = json.load(f)["data"]


@pytest.mark.parametrize("item", test_data, ids=lambda d: d["name"])
def test_remove_items_updates_cart_and_total(logged_in_shop_page, item):
    shop_page = logged_in_shop_page

    products_to_add = item["products_to_add"]
    products_to_remove = item["products_to_remove"]

    # Add N products
    shop_page.add_products_to_cart(products_to_add)

    # Go to cart
    checkout_page = shop_page.go_to_cart()

    # Verify all added products are present initially
    cart_before = checkout_page.get_cart_product_names()
    for p in products_to_add:
        assert p in cart_before, f"Expected '{p}' in cart before removal, got: {cart_before}"

    # Snapshot line totals before removal (for reliable expected calculation)
    line_totals_before = checkout_page.get_line_totals_map()

    # Remove M products
    checkout_page.remove_products(products_to_remove)

    # Expected remaining products
    expected_remaining = [p for p in products_to_add if p not in products_to_remove]

    # Verify remaining products and count
    cart_after = checkout_page.get_cart_product_names()
    assert len(cart_after) == len(expected_remaining), (
        f"Expected cart count {len(expected_remaining)} after removal, got {len(cart_after)}. Cart: {cart_after}"
    )

    for p in expected_remaining:
        assert p in cart_after, f"Expected remaining product '{p}' missing. Cart: {cart_after}"

    for p in products_to_remove:
        assert p not in cart_after, f"Removed product '{p}' still present. Cart: {cart_after}"

    # Verify total recalculated = sum of remaining line totals (from before snapshot)
    #Expected total = sum of line totals of remaining products
    expected_total = sum(line_totals_before[p] for p in expected_remaining)
    actual_total = checkout_page.get_grand_total_value()

    assert actual_total == expected_total, (
        f"Grand total mismatch. Expected {expected_total}, got {actual_total}. "
        f"Remaining: {expected_remaining}"
    )
