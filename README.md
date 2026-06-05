# Selenium Python Automation Framework

A modular, data-driven UI test automation framework built with **Python**, **Selenium WebDriver**, and **pytest** — following the **Page Object Model (POM)** design pattern for maintainability and scalability.

Tests cover an end-to-end e-commerce flow including login, product selection, cart management, checkout, and order confirmation on a live practice site.

---

## Framework Architecture

```
selenium-python-project/
│
├── pageObjects/               # Page Object Model classes
│   ├── login.py               # Login page — auth, error handling, role selection
│   ├── shop.py                # Shop page — product search and cart actions
│   ├── checkout.py            # Checkout page — quantity, removal, totals
│   └── confirmation.py        # Confirmation page — address entry, order validation
│
├── tests/                     # Test suites
│   ├── conftest.py            # Fixtures: browser setup, teardown, session login
│   ├── test_end_to_end_checkout.py
│   ├── test_login_negative.py
│   ├── test_cart_remove_items.py
│   ├── test_cart_quantity_update.py
│   ├── test_add_multiple_products_updates_cart_count.py
│   └── test_user_role_ui.py
│
├── data/                      # External JSON test data (data-driven testing)
│   ├── test_config.json       # Credentials config
│   ├── test_login_negative.json
│   ├── test_end_to_end_checkout.json
│   ├── test_cart_remove_items.json
│   ├── test_cart_quantity_update.json
│   └── test_add_multiple_products_updates_cart_count.json
│
└── pytest.ini                 # Pytest configuration
```

---

## Key Features

- **Page Object Model (POM)** — UI locators and interactions are fully separated from test logic, making tests easy to maintain when the UI changes
- **Data-Driven Testing** — all test inputs are externalized into JSON files; no hardcoded test data inside test methods
- **Explicit Waits** — `WebDriverWait` with `expected_conditions` used throughout, replacing fragile `time.sleep()` calls
- **Multi-browser support** — runs on Chrome or Firefox via `--browser_name` CLI flag
- **Parameterized tests** — `@pytest.mark.parametrize` drives multiple scenarios from a single test function


---

## Test Coverage

| Test File | What It Validates |
|---|---|
| `test_end_to_end_checkout.py` | Full purchase flow: login → add product → checkout → confirm order |
| `test_login_negative.py` | 4 negative login scenarios: empty fields, invalid credentials |
| `test_cart_remove_items.py` | Remove 1 or more products; verify cart count and grand total recalculate correctly |
| `test_cart_quantity_update.py` | Increase and decrease quantity; assert line total and grand total update accurately |
| `test_add_multiple_products_updates_cart_count.py` | Add 1, 2, and 3 products; verify cart badge count and cart contents |
| `test_user_role_ui.py` | User role radio button selection and popup handling |

**Total: 14+ parameterized test cases across 6 test modules**

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| Browser Automation | Selenium WebDriver 4.x |
| Test Runner | pytest |
| Design Pattern | Page Object Model (POM) |
| Test Data | JSON (data-driven) |
| Browser Support | Chrome, Firefox |
| IDE | PyCharm |

---

## Getting Started

### Prerequisites

- Python 3.8+
- Google Chrome or Firefox installed
- ChromeDriver / GeckoDriver (auto-managed via Selenium Manager in Selenium 4.x)

### Installation

```bash
git clone https://github.com/Anuja-AXT/selenium-python-project.git
cd selenium-python-project
pip install selenium pytest
```

### Run All Tests

```bash
pytest tests/
```

### Run on a Specific Browser

```bash
pytest tests/ --browser_name=chrome
pytest tests/ --browser_name=firefox
```

### Run by Marker (Selective Execution)

```bash
# Smoke tests only
pytest tests/ -m smoke

# Regression suite only
pytest tests/ -m regression
```

### Run a Single Test File

```bash
pytest tests/test_end_to_end_checkout.py -v
```

### Run with Verbose Output

```bash
pytest tests/ -v
```

---

## Design Decisions

**Why Page Object Model?**
Locators and page interactions live in one place. When the UI changes, you update one file — not every test that touches that element.

**Why external JSON for test data?**
Test logic stays clean and readable. New test scenarios can be added by editing a JSON file without touching any Python code.

**Why explicit waits over implicit waits?**
`WebDriverWait` with `expected_conditions` waits for a specific condition on a specific element. It's more reliable than blanket `implicitly_wait` or `time.sleep()` because it doesn't slow down tests that load quickly and doesn't fail tests that occasionally load slowly.

**Why pytest fixtures scoped at `session` vs `function`?**
`valid_creds` is `session`-scoped because credentials don't change. `browserInstance` is `function`-scoped to give each test a clean browser state and prevent test pollution.

---

## Application Under Test

[Rahul Shetty Academy — Login Practice](https://rahulshettyacademy.com/loginpagePractise)

A publicly available practice site for automation engineers — suitable for demonstrating real framework capabilities without proprietary dependencies.

---

## Author

**Anuja Taywade**
Senior QA Automation Engineer | 6+ years in test automation
[LinkedIn](https://www.linkedin.com/in/anuja-taywade)
