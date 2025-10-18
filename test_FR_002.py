import pytest
from app import app, cart, BOOKS
from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# FR-002 TC002-01: Verify adding an item to the cart

def test_add_book_to_cart(client):
    cart.clear()

    response = client.post('/add-to-cart', data={
        'title': '1984',
        'quantity': '2'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert any(item.book.title == '1984' for item in cart.get_items())

    item = next((i for i in cart.get_items() if i.book.title == '1984'), None)
    assert item is not None
    assert item.quantity == 2

# FR-002 TC002-02: Verify adding item to cart when quantity is set to '0'

def test_add_zero_quantity_to_cart(client):
    cart.clear()

    response = client.post('/add-to-cart', data={
        'title': '1984',
        'quantity': '0'
    }, follow_redirects=True)

    assert response.status_code == 200

    assert '1984' not in cart.get_items()

# FR-002 TC002-03: Verify adding multiple copies of the same book to the cart

def test_add_multiple_copies_to_cart(client):
    cart.clear()

    # First add 1 copy
    response1 = client.post('/add-to-cart', data={
        'title': '1984',
        'quantity': '1'
    }, follow_redirects=True)

    assert response1.status_code == 200

    # Add 2 more copies
    response2 = client.post('/add-to-cart', data={
        'title': '1984',
        'quantity': '2'
    }, follow_redirects=True)

    assert response2.status_code == 200

    # Verify total quantity is now 3
    item = next((i for i in cart.get_items() if i.book.title == '1984'), None)
    assert item is not None
    assert item.quantity == 3


# FR-002 TC002-04: Verify adding multiple books with different titles to the cart

def test_add_multiple_books_to_cart(client):
    cart.clear()  # Start with an empty cart

    # Add first book
    response1 = client.post('/add-to-cart', data={
        'title': '1984',
        'quantity': '1'
    }, follow_redirects=True)

    assert response1.status_code == 200

    # Add second book
    response2 = client.post('/add-to-cart', data={
        'title': 'The Great Gatsby',
        'quantity': '2'
    }, follow_redirects=True)

    assert response2.status_code == 200

    # Verify both books are in the cart with correct quantities
    items = cart.get_items()
    titles = [item.book.title for item in items]
    assert '1984' in titles
    assert 'The Great Gatsby' in titles

    item_1984 = next((i for i in items if i.book.title == '1984'), None)
    item_gatsby = next((i for i in items if i.book.title == 'The Great Gatsby'), None)

    assert item_1984 is not None and item_1984.quantity == 1
    assert item_gatsby is not None and item_gatsby.quantity == 2

    # Final cart check
    assert len(items) == 2


# FR-002 TC002-05: Verify adding the maximum quantity of a book

def test_add_maximum_dropdown_quantity_to_cart(client):
    cart.clear()  # Start with an empty cart

    response = client.post('/add-to-cart', data={
        'title': 'Moby Dick',
        'quantity': '10'
    }, follow_redirects=True)

    assert response.status_code == 200

    # Verify the item is in the cart and has correct quantity
    item = next((i for i in cart.get_items() if i.book.title == 'Moby Dick'), None)
    assert item is not None
    assert item.quantity == 10


# FR-002 TC002-06: Verify adding an item to the cart which is out of stock - can't do this

# FR-002 TC002-07: Verify viewing the cart when there are items added

def test_view_cart_with_items(client):
    """Verify that the cart page displays items after books are added."""
    cart.clear()  # Start with an empty cart

    # Add two books to the cart
    cart.add_book(BOOKS[0], 1)  # The Great Gatsby
    cart.add_book(BOOKS[1], 2)  # 1984

    response = client.get('/cart')
    assert response.status_code == 200

    # Check that both book titles appear in the cart page
    assert b'The Great Gatsby' in response.data
    assert b'1984' in response.data

# FR-002 TC002-08: Verify viewing the cart when there are no items added

def test_view_empty_cart(client):

    cart.clear()  # Ensure cart is empty before test

    response = client.get('/cart')
    assert response.status_code == 200

    # Check for empty cart message — adjust if your template uses different wording
    assert b'Your cart is empty' in response.data


    # Optionally confirm no book titles are present
    for book in BOOKS:
        assert book.title.encode() not in response.data


# FR-002 TC002-09: Verify updating item quantities in the cart

def test_update_cart_item_quantity(client):
    cart.clear()  # Start with an empty cart

    # Add initial quantity
    cart.add_book(BOOKS[0], 1)  # The Great Gatsby

    # Update quantity to 3
    response = client.post('/update-cart', data={
        'title': 'The Great Gatsby',
        'quantity': '3'
    }, follow_redirects=True)

    assert response.status_code == 200

    # Find the updated item
    item = next((i for i in cart.get_items() if i.book.title == 'The Great Gatsby'), None)
    assert item is not None
    assert item.quantity == 3

# FR-002 TC002-10: Verify updating item quantities to “0”

def test_update_cart_quantity_to_zero(client):

    cart.clear()  # Start with an empty cart

    # Add a book to the cart
    cart.add_book(BOOKS[0], 2)  # The Great Gatsby

    # Update quantity to 0
    response = client.post('/update-cart', data={
        'title': 'The Great Gatsby',
        'quantity': '0'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'The Great Gatsby' not in cart.get_items()

# FR-002 TC002-11: Verify removing an item from the cart when it is the only item in the cart

def test_remove_only_item_from_cart(client):

    cart.clear()  # Ensure cart starts empty

    # Add one book to the cart
    cart.add_book(BOOKS[1], 1)  # 1984

    # Remove the book
    response = client.post('/remove-from-cart', data={
        'title': '1984'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert cart.is_empty()


# FR-002 TC002-12: Verify removing an item from the cart while there are other items in the cart

def test_remove_item_from_multi_item_cart(client):
    cart.clear()  # Start with an empty cart

    # Add two books to the cart
    cart.add_book(BOOKS[0], 1)  # The Great Gatsby
    cart.add_book(BOOKS[1], 2)  # 1984

    # Remove one of them
    response = client.post('/remove-from-cart', data={
        'title': '1984'
    }, follow_redirects=True)

    assert response.status_code == 200

    # Verify 1984 is gone, but Gatsby remains
    items = cart.get_items()
    titles = [item.book.title for item in items]
    assert '1984' not in titles
    assert 'The Great Gatsby' in titles

    gatsby = next((i for i in items if i.book.title == 'The Great Gatsby'), None)
    assert gatsby is not None
    assert gatsby.quantity == 1

# FR-002 TC002-13: Verify clearing the cart of all items

def test_clear_cart_all_items(client):

    cart.clear()  # Start fresh

    # Add multiple books to the cart
    cart.add_book(BOOKS[0], 1)  # The Great Gatsby
    cart.add_book(BOOKS[1], 2)  # 1984
    cart.add_book(BOOKS[2], 1)  # I Ching

    # Clear the cart
    response = client.post('/clear-cart', follow_redirects=True)

    assert response.status_code == 200
    assert b'Cart cleared!' in response.data
    assert cart.is_empty()


# FR-002 TC002-14: Verify dynamic pricing calculations in cart

def test_cart_dynamic_pricing(client):

    cart.clear()  # Start with an empty cart

    # Add books with different quantities
    cart.add_book(BOOKS[0], 2)  # The Great Gatsby — 2 × 10.99
    cart.add_book(BOOKS[1], 1)  # 1984 — 1 × 8.99
    cart.add_book(BOOKS[3], 3)  # Moby Dick — 3 × 12.49

    expected_total = (
        2 * BOOKS[0].price +
        1 * BOOKS[1].price +
        3 * BOOKS[3].price
    )

    # Get cart page
    response = client.get('/cart')
    assert response.status_code == 200

    # Check that total price is rendered correctly
    assert f'Total Price: ${expected_total:.2f}'.encode() in response.data



# FR-002 TC002-16: Verify book cover images display in cart

def test_cart_book_image_render(client):
    """Verify that book cover image is rendered in the cart."""
    cart.clear()
    cart.add_book(BOOKS[0], 1)  # The Great Gatsby

    response = client.get('/cart')
    assert response.status_code == 200

    with app.test_request_context():
        image_url = url_for('static', filename=BOOKS[0].image).encode()
        assert image_url in response.data

# FR-002 TC002-17: Verify adding item to cart when quantity is set to '-1'

def test_add_negative_quantity_to_cart(client):
    cart.clear()

    response = client.post('/add-to-cart', data={
        'title': '1984',
        'quantity': '-1'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert '1984' not in cart.get_items()        