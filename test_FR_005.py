import pytest
from app import app, cart, BOOKS
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# FR-005 TC005-01: Verify user receives email with order details following successful payment

def test_email_sent_after_successful_payment(client):
    cart.clear()
    cart.add_book(BOOKS[0], 1)

    with patch('models.EmailService.send_order_confirmation') as mock_send_email:
        response = client.post('/process-checkout', data={
            'name': 'Test User',
            'email': 'test@test.com',
            'address': '123 Test Road',
            'city': 'Test City',
            'zip_code': '12345',
            'payment_method': 'credit_card',
            'card_number': '4242424242424242',
            'expiry_date': '12/25',
            'cvv': '123',
            'discount_code': ''
        }, follow_redirects=True)

        assert response.status_code == 200
        assert mock_send_email.called
        args, kwargs = mock_send_email.call_args
        assert args[0] == 'test@test.com'
        assert hasattr(args[1], 'order_id')
        assert b'Confirmation Email Sent' in response.data
        assert b'test@test.com' in response.data

# FR-005 TC005-02: Verify user can view order details on webpage following successful payment

def test_user_can_view_order_details_after_payment(client):
    cart.clear()
    cart.add_book(BOOKS[0], 2)

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
    assert b'Order Number:' in response.data
    assert b'test@test.com' in response.data
    assert b'Total Amount:' in response.data
    assert BOOKS[0].title.encode() in response.data
    assert b'Quantity: 2' in response.data