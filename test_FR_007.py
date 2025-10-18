import pytest
from app import app, BOOKS

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# FR-007 TC007-01: Verify the website layout adapts to different screen sizes and displays properly on mobile, tablet, and desktop

# FR-007 TC007-02: Verify the navigation menus remain accessible and functional on all devices

# FR-007 TC007-03: Users should be able to add items to the shopping cart and complete the checkout process on any device

# FR-007 TC007-04: Users should be able to remove items in the shopping cart on any device

# FR-007 TC007-05: Users should be able to change the quantity of items in the shopping cart on any device