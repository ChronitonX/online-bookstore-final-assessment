import pytest
from app import app, cart, BOOKS

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# FR-004 TC004-01: Verify user can input payment information

def test_user_can_input_payment_information(client):
    cart.clear()
    cart.add_book(BOOKS[0], 1)  # Add one book to cart

    response = client.post('/process-checkout', data={
        'name': 'Test User',
        'email': 'test@test.com',
        'address': '123 Test Road',
        'city': 'Test City',
        'zip_code': '12345',
        'payment_method': 'credit_card',
        'card_number': '1234567812345678',
        'expiry_date': '12/25',
        'cvv': '123',
        'discount_code': ''
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Payment Method: Credit Card' in response.data
    assert b'Order Confirmed!' in response.data
    assert b'Thank you for your purchase' in response.data

# FR-004 TC004-02: Verify successful transaction redirects to confirmation page

def test_successful_transaction_redirects_to_confirmation(client):
    cart.clear()
    cart.add_book(BOOKS[0], 1)

    response = client.post('/process-checkout', data={
        'name': 'Test User',
        'email': 'test@test.com',
        'address': '123 Test Road',
        'city': 'Test City',
        'zip_code': '12345',
        'payment_method': 'credit_card',
        'card_number': '1234567812345678',
        'expiry_date': '12/25',
        'cvv': '123',
        'discount_code': ''
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Order Confirmed!' in response.data
    assert b'Thank you for your purchase' in response.data
    assert b'Payment Method: Credit Card' in response.data

# FR-004 TC004-03: Verify unsuccessful transaction displays error message with incorrect card number

def test_unsuccessful_transaction_shows_error_message(client):
    cart.clear()
    cart.add_book(BOOKS[0], 1)

    response = client.post('/process-checkout', data={
        'name': 'Test User',
        'email': 'test@test.com',
        'address': '123 Test Road',
        'city': 'Test City',
        'zip_code': '12345',
        'payment_method': 'credit_card',
        'card_number': '1234567812341111',  # triggers mock failure
        'expiry_date': '12/25',
        'cvv': '123',
        'discount_code': ''
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Payment failed: Invalid card number' in response.data
    assert b'Order Confirmed!' not in response.data
    assert b'Thank you for your purchase' not in response.data

# FR-004 TC004-04: Verify unsuccessful transaction displays error message with incorrect expiration date

def test_unsuccessful_transaction_invalid_expiry_date(client):
    cart.clear()
    cart.add_book(BOOKS[0], 1)

    response = client.post('/process-checkout', data={
        'name': 'Test User',
        'email': 'test@test.com',
        'address': '123 Test Road',
        'city': 'Test City',
        'zip_code': '12345',
        'payment_method': 'credit_card',
        'card_number': '1234567812345678',
        'expiry_date': '',  # Invalid / missing
        'cvv': '123',
        'discount_code': ''
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Please fill in all credit card details' in response.data
    assert b'Order Confirmed!' not in response.data
    assert b'Thank you for your purchase' not in response.data

# FR-004 TC004-05: Verify unsuccessful transaction displays error message with incorrect security code

def test_unsuccessful_transaction_invalid_cvv(client):
    cart.clear()
    cart.add_book(BOOKS[0], 1)

    response = client.post('/process-checkout', data={
        'name': 'Test User',
        'email': 'test@test.com',
        'address': '123 Test Road',
        'city': 'Test City',
        'zip_code': '12345',
        'payment_method': 'credit_card',
        'card_number': '1234567812345678',
        'expiry_date': '12/25',
        'cvv': '',  # Missing or invalid CVV
        'discount_code': ''
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Please fill in all credit card details' in response.data
    assert b'Order Confirmed!' not in response.data
    assert b'Thank you for your purchase' not in response.data

# FR-004 TC004-06: Verify payment gateway processes payment using encrypted connection - can't do this