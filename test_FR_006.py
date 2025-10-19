import pytest
from app import app
from models import Book, Cart, Order
from app import get_current_user

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# FR-006 TC006-01: Verify user can create an account using their email address and a password

def test_user_can_create_account(client):
    response = client.post('/register', data={
        'name': 'Test User',
        'email': 'testuser@test.com',
        'password': 'TestUser123',
        'confirm_password': 'TestUser123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Account created successfully' in response.data or b'Login to Your Account' in response.data
    assert b'Hello, Test User!' in response.data

# FR-006 TC006-02: Verify users can log in to view their past orders

def test_demo_user_places_order_and_sees_it_as_past_order(client):
    response = client.post('/login', data={
        'email': 'demo@bookstore.com',
        'password': 'demo123'
    }, follow_redirects=True)
    assert response.status_code == 200

    demo_user = get_current_user()
    cart = Cart()
    book1 = Book("1984", "Dystopia", 8.99, "1984.jpg")
    book2 = Book("Moby Dick", "Adventure", 12.49, "moby_dick.jpg")
    cart.add_book(book1, quantity=2)
    cart.add_book(book2, quantity=1)

    shipping_info = {'address': demo_user.address}
    payment_info = {'card_number': '1234567812345678', 'payment_method': 'credit_card'}
    total = cart.get_total_price()
    order = Order(order_id="ORDER123", user_email=demo_user.email, items=cart.get_items(),
                  shipping_info=shipping_info, payment_info=payment_info, total_amount=total)
    demo_user.add_order(order)

    response = client.get('/account')
    assert response.status_code == 200
    assert b'Order History' in response.data
    assert b'ORDER123' in response.data
    assert b'1984' in response.data
    assert b'Moby Dick' in response.data
    assert b'Quantity: 2' in response.data
    assert b'Quantity: 1' in response.data

# FR-006 TC006-03: Verify users can update their name in their registered account

def test_user_can_update_name_only(client):
    response = client.post('/login', data={
        'email': 'demo@bookstore.com',
        'password': 'demo123'
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.post('/update-profile', data={
        'name': 'New Name',
        'address': '',
        'new_password': ''
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'New Name' in response.data

# FR-006 TC006-04: Verify that user can update their address in their registered account

def test_user_can_update_address_only(client):
    response = client.post('/login', data={
        'email': 'demo@bookstore.com',
        'password': 'demo123'
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.post('/update-profile', data={
        'name': '',
        'address': '123 New Test Road',
        'new_password': ''
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'123 New Test Road' in response.data

# FR-006 TC006-05: Verify that user can update their password in their registered account

def test_user_can_update_password_only(client):
    response = client.post('/login', data={
        'email': 'demo@bookstore.com',
        'password': 'demo123'
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.post('/update-profile', data={
        'name': '',
        'address': '',
        'new_password': 'NewPassword123'
    }, follow_redirects=True)
    assert response.status_code == 200

    client.get('/logout', follow_redirects=True)
    response = client.post('/login', data={
        'email': 'demo@bookstore.com',
        'password': 'NewPassword123'
    }, follow_redirects=True)
    assert response.status_code == 200

# FR-006 TC006-06: Verify that the user can't change their email address

def test_user_cannot_change_email_address(client):
    response = client.post('/login', data={
        'email': 'demo@bookstore.com',
        'password': 'demo123'
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.post('/update-profile', data={
        'name': 'Demo User',
        'address': '123 Demo Street',
        'email': 'newtest@test.com',
    }, follow_redirects=True)
    assert response.status_code == 200

    assert b'demo@bookstore.com' in response.data
    assert b'newtest@test.com' not in response.data

# FR-006 TC006-07: Verify that user can log out of the website

def test_user_can_log_out(client):
    response = client.post('/login', data={
        'email': 'demo@bookstore.com',
        'password': 'demo123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Account' in response.data

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data or b'Sign In' in response.data
    assert b'Account' not in response.data
