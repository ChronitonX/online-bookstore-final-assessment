import pytest
from app import app, BOOKS

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# FR-001: Test that books are visible for browsing

def test_book_browsing(client):
    response = client.get('/')
    assert response.status_code == 200

    for book in BOOKS:
        assert book.title.encode() in response.data

# FR-002 TC002-15: Verify dynamic pricing calculations on homepage - wrong test case

def test_homepage_dynamic_pricing(client):
    """Verify that book prices are correctly displayed on the homepage."""
    response = client.get('/')
    assert response.status_code == 200

    # Check that each book's price appears in the rendered HTML
    for book in BOOKS:
        price_str = f"${book.price:.2f}".encode()
        assert price_str in response.data

