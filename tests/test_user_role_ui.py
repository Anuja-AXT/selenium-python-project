from pageObjects.login import LoginPage


def test_user_role_popup_and_selection(browserInstance):
    driver = browserInstance
    login_page = LoginPage(driver)
    # Select User role (should trigger popup and handle it)
    login_page.select_user_role()

    # Verify User radio is selected
    assert login_page.is_user_role_selected()