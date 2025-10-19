import pytest
from playwright.sync_api import sync_playwright

# Screen sizes for testing
screen_sizes = [
    {"name": "mobile", "width": 375, "height": 667},
    {"name": "tablet", "width": 768, "height": 1024},
    {"name": "desktop", "width": 1440, "height": 900},
]

# FR-007 TC007-01: Verify the website layout adapts to different screen sizes and displays properly on mobile, tablet, and desktop

@pytest.mark.parametrize("device", screen_sizes)
def test_layout_responsive(device):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport=device)
        page = context.new_page()

        page.goto("http://localhost:5000", wait_until="networkidle")
        assert "Online Bookstore" in page.title()
        assert page.locator("nav").is_visible()
        assert page.locator(".books-section").is_visible()

        browser.close()

# FR-007 TC007-02: Verify the navigation menus remain accessible and functional on all devices
@pytest.mark.parametrize("device", screen_sizes)
def test_navigation_menu_accessible(device):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport=device)
        page = context.new_page()

        page.goto("http://localhost:5000", wait_until="networkidle")
        assert page.locator("nav a").count() >= 3

        browser.close()

# FR-007 TC007-03: Verify users can add items to the shopping cart and complete the checkout process on any device

@pytest.mark.parametrize("device", screen_sizes)
def test_add_and_checkout(device):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport=device)
        page = context.new_page()

        page.goto("http://localhost:5000", wait_until="networkidle")
        page.locator(".add-to-cart-btn").first.click()

        page.goto("http://localhost:5000/cart", wait_until="networkidle")
        page.locator(".cart-actions a.btn-primary").first.click()

        assert page.locator("form.checkout-form").is_visible()
        browser.close()

# FR-007 TC007-04: Verify users can remove items in the shopping cart on any device

@pytest.mark.parametrize("device", screen_sizes)
def test_remove_item_from_cart(device):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport=device)
        page = context.new_page()

        page.goto("http://localhost:5000", wait_until="networkidle")
        page.locator(".add-to-cart-btn").first.click()

        page.goto("http://localhost:5000/cart", wait_until="networkidle")
        page.once("dialog", lambda dialog: dialog.accept())
        page.locator("form[action='/remove-from-cart'] button").first.click()

        page.wait_for_timeout(1000)
        assert "Your cart is empty" in page.content()
        browser.close()

# FR-007 TC007-05: Verify users can change the quantity of items in the shopping cart on any device

@pytest.mark.parametrize("device", screen_sizes)
def test_change_quantity_in_cart(device):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport=device)
        page = context.new_page()

        page.goto("http://localhost:5000", wait_until="networkidle")
        page.locator(".add-to-cart-btn").first.click()

        page.goto("http://localhost:5000/cart", wait_until="networkidle")
        page.locator("form.quantity-form input[name='quantity']").first.fill("3")
        page.locator("form.quantity-form button").first.click()

        assert "Total Items: 3" in page.content()
        browser.close()

# FR-007 TC007-06: Verify users can complete the checkout process

@pytest.mark.parametrize("device", screen_sizes)
def test_complete_checkout_flow(device):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport=device)
        page = context.new_page()

        page.goto("http://localhost:5000", wait_until="networkidle")
        page.locator(".add-to-cart-btn").first.click()

        page.goto("http://localhost:5000/checkout", wait_until="networkidle")
        page.fill("#name", "Test User")
        page.fill("#email", "test@test.com")
        page.fill("#address", "123 Test Road")
        page.fill("#city", "Test City")
        page.fill("#zip_code", "12345")
        page.fill("#card_number", "1234567812345678")
        page.fill("#expiry_date", "12/25")
        page.fill("#cvv", "123")

        page.locator("button.btn-primary").click()
        page.wait_for_timeout(1000)

        assert "Order Confirmation" in page.content()
        browser.close()