import cProfile
import pstats

def profile_get_book_by_title():
    from app import get_book_by_title, BOOKS
    titles = [book.title for book in BOOKS] * 1000
    for _ in range(10000):
        get_book_by_title(titles[0])

def profile_cart_add_book():
    from app import cart, BOOKS
    cart.clear()
    for _ in range(10000):
        cart.add_book(BOOKS[0], 1)

def profile_cart_update_quantity():
    from app import cart, BOOKS
    cart.clear()
    cart.add_book(BOOKS[0], 1)
    for _ in range(10000):
        cart.update_quantity(BOOKS[0].title, 3)

def profile_cart_remove_book():
    from app import cart, BOOKS
    cart.clear()
    cart.add_book(BOOKS[0], 1)
    for _ in range(10000):
        cart.remove_book(BOOKS[0].title)

def profile_cart_get_total_price():
    from app import cart, BOOKS
    cart.clear()
    cart.add_book(BOOKS[0], 2)
    for _ in range(10000):
        cart.get_total_price()

def profile_user_login():
    from app import users
    email = "demo@bookstore.com"
    password = "demo123"
    user = users.get(email)
    for _ in range(10000):
        user and user.password == password

def profile_user_logout():
    from app import app, session
    with app.test_request_context():
        session['user_email'] = "demo@bookstore.com"
        for _ in range(10000):
            session.pop('user_email', None)
            session['user_email'] = "demo@bookstore.com"

def profile_update_profile():
    from app import users
    user = users["demo@bookstore.com"]
    new_name = "Updated Name"
    new_address = "123 New Test Road"
    for _ in range(10000):
        user.name = new_name
        user.address = new_address

def profile_update_password():
    from app import users
    user = users["demo@bookstore.com"]
    new_password = "NewPassword123"
    for _ in range(10000):
        user.password = new_password

def profile_cart_operations():
    from app import Cart, BOOKS
    cart = Cart()
    book = BOOKS[0]
    for _ in range(1000):
        cart.add_book(book, quantity=1)
        cart.update_quantity(book.title, 2)
        cart.get_total_price()
        cart.get_total_items()
        cart.is_empty()
        cart.get_items()
        cart.remove_book(book.title)
        cart.clear()

def profile_order_to_dict():
    from app import Order, Cart, BOOKS
    cart = Cart()
    cart.add_book(BOOKS[0], 2)
    order = Order("ORD001", "user@example.com", cart.get_items(), {"address": "123 Test Street"}, {"card_number": "4242"}, cart.get_total_price())
    for _ in range(1000):
        order.to_dict()

def profile_user_add_order():
    from app import User, Order, Cart, BOOKS
    cart = Cart()
    cart.add_book(BOOKS[0], 2)
    order = Order("ORD001", "user@example.com", cart.get_items(), {"address": "123 Test Street"}, {"card_number": "4242"}, cart.get_total_price())
    user = User("user@example.com", "securepass", "Test User", "123 Test Street")
    for _ in range(1000):
        user.add_order(order)
        user.get_order_history()

def profile_payment_gateway():
    from app import PaymentGateway
    payment_info = {"card_number": "4242424242424242", "payment_method": "credit"}
    for _ in range(100):
        PaymentGateway.process_payment(payment_info)

def profile_email_service():
    from app import EmailService, Order, Cart, BOOKS
    cart = Cart()
    cart.add_book(BOOKS[0], 2)
    order = Order("ORD001", "user@example.com", cart.get_items(), {"address": "123 Test Street"}, {"card_number": "4242"}, cart.get_total_price())
    for _ in range(10):
        EmailService.send_order_confirmation("user@example.com", order)

def run_profile(func, label):
    profiler = cProfile.Profile()
    profiler.enable()
    func()
    profiler.disable()

    with open(f"profile_{label}.txt", "w") as f:
        stats = pstats.Stats(profiler, stream=f)
        stats.strip_dirs().sort_stats("cumtime").print_stats()

    profiler.dump_stats(f"profile_{label}.prof")

# from app.py

if __name__ == "__main__":
    run_profile(profile_get_book_by_title, "get_book_by_title")
    run_profile(profile_cart_add_book, "cart_add_book")
    run_profile(profile_cart_update_quantity, "cart_update_quantity")
    run_profile(profile_cart_remove_book, "cart_remove_book")
    run_profile(profile_cart_get_total_price, "cart_get_total_price")
    run_profile(profile_user_login, "user_login")
    run_profile(profile_user_logout, "user_logout")
    run_profile(profile_update_profile, "update_profile")
    run_profile(profile_update_password, "update_password")

# from models.py

    run_profile(profile_cart_operations, "cart_operations")
    run_profile(profile_order_to_dict, "order_to_dict")
    run_profile(profile_user_add_order, "user_add_order")
    run_profile(profile_payment_gateway, "payment_gateway")
    run_profile(profile_email_service, "email_service")