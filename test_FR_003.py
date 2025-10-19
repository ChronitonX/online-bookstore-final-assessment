import pytest
from app import app, cart, BOOKS

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# FR-003 TC003-01: Verify checkout page’s order summary displays the cart’s contents and details

def test_checkout_order_summary_displays_cart(client):
    cart.clear()
    cart.add_book(BOOKS[0], 2)  # The Great Gatsby
    cart.add_book(BOOKS[1], 1)  # 1984

    response = client.get('/checkout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Checkout' in response.data
    assert b'Order Summary' in response.data
    assert b'The Great Gatsby' in response.data
    assert b'1984' in response.data
    assert b'Quantity: 2' in response.data
    assert b'Quantity: 1' in response.data

# FR-003 TC003-02: Verify order summary shows no items if cart is empty

def test_checkout_order_summary_empty_cart(client):
    cart.clear()
    response = client.get('/checkout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Your cart is empty' in response.data or b'No items in cart' in response.data

# FR-003 TC003-03: Verify shipping detail fields accept input

def test_shipping_fields_accept_input(client):
    cart.clear()
    cart.add_book(BOOKS[0], 1)

    response = client.post('/process-checkout', data={
        'name': 'Test User',
        'address': '123 Test Road',
        'email': 'test@test.com',
        'city': 'Test City',
        'zip_code': '12345',
        'payment_method': 'credit_card'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Complete Purchase' in response.data or b'Order Confirmed' in response.data

# FR-003 TC003-04: Verify shipping details ‘name’ field has been filled

def test_shipping_name_required(client):
    cart.clear()
    cart.add_book(BOOKS[0], 1)

    response = client.post('/process-checkout', data={
        'name': '',
        'address': '123 Test Road',
        'email': 'test@test.com',
        'city': 'Test City',
        'zip_code': '12345',
        'payment_method': 'credit_card'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Full Name *' in response.data
    assert b'Please fill in the name field' in response.data

# FR-003 TC003-05: Verify shipping details ‘address’ field has been filled

def test_shipping_address_required(client):
    cart.clear()
    cart.add_book(BOOKS[0], 1)

    response = client.post('/process-checkout', data={
        'name': 'Test User',
        'address': '',
        'email': 'test@etest.com',
        'city': 'Test City',
        'zip_code': '12345',
        'payment_method': 'credit_card'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Street Address *' in response.data
    assert b'Please fill in the address field' in response.data

# FR-003 TC003-06: Verify shipping details ‘email address’ field has been filled

def test_shipping_email_required(client):
    cart.clear()
    cart.add_book(BOOKS[0], 1)

    response = client.post('/process-checkout', data={
        'name': 'Test User',
        'address': '123 Test Road',
        'email': '',
        'city': 'Test City',
        'zip_code': '12345',
        'payment_method': 'credit_card'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Email Address *' in response.data
    assert b'Please fill in the email field' in response.data

# FR-003 TC003-07: Verify PayPal payment method can be selected - not working

def test_paypal_selection(client):
    cart.clear()
    cart.add_book(BOOKS[0], 1)

    response = client.post('/process-checkout', data={
        'name': 'Test User',
        'address': '123 Test Road',
        'email': 'test@test.com',
        'city': 'Test City',
        'zip_code': '12345',
        'payment_method': 'paypal'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'PayPal' in response.data
    assert b'You will be redirected to PayPal to complete your payment.' in response.data

# FR-003 TC003-08: Verify discount code

def test_discount_code_applied(client):
    cart.clear()
    cart.add_book(BOOKS[0], 1)

    response = client.post('/process-checkout', data={
        'name': 'Test User',
        'address': '123 Test Road',
        'email': 'test@test.com',
        'city': 'Test City',
        'zip_code': '12345',
        'payment_method': 'credit_card',
        'discount_code': 'SAVE10'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Discount Code:' in response.data
    assert b'Discount applied' in response.data # Check this

# FR-003 TC003-09: Verify payment method has been selected - not working

def test_payment_method_selected(client):
    cart.clear()
    cart.add_book(BOOKS[0], 1)

    response = client.post('/process-checkout', data={
        'name': 'Test User',
        'address': '123 Test Road',
        'email': 'test@test.com',
        'city': 'Test City',
        'zip_code': '12345',
        'payment_method': ''
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Payment Information' in response.data
    assert b'Payment method is required' in response.data
