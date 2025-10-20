import timeit
import csv
from app import app, session

# get_book_by_title

setup_lookup = '''
from app import get_book_by_title, BOOKS
titles = [book.title for book in BOOKS] * 1000
'''

exec_lookup = timeit.timeit("get_book_by_title(titles[0])", setup=setup_lookup, number=100)
print(f"get_book_by_title: {exec_lookup:.7f} seconds over 100 runs")

exec_lookup = timeit.timeit("get_book_by_title(titles[0])", setup=setup_lookup, number=1000)
print(f"get_book_by_title: {exec_lookup:.7f} seconds over 1000 runs")

exec_lookup = timeit.timeit("get_book_by_title(titles[0])", setup=setup_lookup, number=10000)
print(f"get_book_by_title: {exec_lookup:.7f} seconds over 10000 runs")


# cart.add_book

setup_add = '''
from app import cart, BOOKS
cart.clear()
'''

exec_add = timeit.timeit("cart.add_book(BOOKS[0], 1)", setup=setup_add, number=100)
print(f"cart.add_book: {exec_add:.7f} seconds over 100 runs")

exec_add = timeit.timeit("cart.add_book(BOOKS[0], 1)", setup=setup_add, number=1000)
print(f"cart.add_book: {exec_add:.7f} seconds over 1000 runs")

exec_add = timeit.timeit("cart.add_book(BOOKS[0], 1)", setup=setup_add, number=10000)
print(f"cart.add_book: {exec_add:.7f} seconds over 10000 runs")


# cart.update_quantity

setup_update = '''
from app import cart, BOOKS
cart.clear()
cart.add_book(BOOKS[0], 1)
'''

exec_update = timeit.timeit("cart.update_quantity(BOOKS[0].title, 3)", setup=setup_update, number=100)
print(f"cart.update_quantity: {exec_update:.7f} seconds over 100 runs")

exec_update = timeit.timeit("cart.update_quantity(BOOKS[0].title, 3)", setup=setup_update, number=1000)
print(f"cart.update_quantity: {exec_update:.7f} seconds over 1000 runs")

exec_update = timeit.timeit("cart.update_quantity(BOOKS[0].title, 3)", setup=setup_update, number=10000)
print(f"cart.update_quantity: {exec_update:.7f} seconds over 10000 runs")


# cart.remove_book

setup_remove = '''
from app import cart, BOOKS
cart.clear()
cart.add_book(BOOKS[0], 1)
'''

exec_remove = timeit.timeit("cart.remove_book(BOOKS[0].title)", setup=setup_remove, number=100)
print(f"cart.remove_book: {exec_remove:.7f} seconds over 100 runs")

exec_remove = timeit.timeit("cart.remove_book(BOOKS[0].title)", setup=setup_remove, number=1000)
print(f"cart.remove_book: {exec_remove:.7f} seconds over 1000 runs")

exec_remove = timeit.timeit("cart.remove_book(BOOKS[0].title)", setup=setup_remove, number=10000)
print(f"cart.remove_book: {exec_remove:.7f} seconds over 10000 runs")

# cart.get_total_price

setup_total = '''
from app import cart, BOOKS
cart.clear()
cart.add_book(BOOKS[0], 2)
'''

exec_total = timeit.timeit("cart.get_total_price()", setup=setup_total, number=100)
print(f"cart.get_total_price: {exec_total:.7f} seconds over 100 runs")

exec_total = timeit.timeit("cart.get_total_price()", setup=setup_total, number=1000)
print(f"cart.get_total_price: {exec_total:.7f} seconds over 1000 runs")

exec_total = timeit.timeit("cart.get_total_price()", setup=setup_total, number=10000)
print(f"cart.get_total_price: {exec_total:.7f} seconds over 10000 runs")

# cart.clear

setup_clear_cart = '''
from app import cart, BOOKS
cart.add_book(BOOKS[0], 1)
'''

exec_clear_cart = timeit.timeit("cart.clear()", setup=setup_clear_cart, number=100)
print(f"cart.clear: {exec_clear_cart:.7f} seconds over 100 runs")

exec_clear_cart = timeit.timeit("cart.clear()", setup=setup_clear_cart, number=1000)
print(f"cart.clear: {exec_clear_cart:.7f} seconds over 1000 runs")

exec_clear_cart = timeit.timeit("cart.clear()", setup=setup_clear_cart, number=10000)
print(f"cart.clear: {exec_clear_cart:.7f} seconds over 10000 runs")


# cart.is_empty, and cart.get_total_price

setup_checkout = '''
from app import cart, BOOKS
cart.clear()
cart.add_book(BOOKS[0], 2)
'''

exec_checkout = timeit.timeit("cart.is_empty(); cart.get_total_price()", setup=setup_checkout, number=100)
print(f"checkout logic: {exec_checkout:.7f} seconds over 100 runs")

exec_checkout = timeit.timeit("cart.is_empty(); cart.get_total_price()", setup=setup_checkout, number=1000)
print(f"checkout logic: {exec_checkout:.7f} seconds over 1000 runs")

exec_checkout = timeit.timeit("cart.is_empty(); cart.get_total_price()", setup=setup_checkout, number=10000)
print(f"checkout logic: {exec_checkout:.7f} seconds over 10000 runs")


# Discount

setup_discount = '''
from app import cart, BOOKS
cart.clear()
cart.add_book(BOOKS[0], 2)
discount_code = 'SAVE10'
total_amount = cart.get_total_price()
'''

exec_discount = timeit.timeit("""
discount_applied = 0
if discount_code == 'SAVE10':
    discount_applied = total_amount * 0.10
    total_amount -= discount_applied
""", setup=setup_discount, number=100)
print(f"discount logic (SAVE10): {exec_discount:.7f} seconds over 100 runs")

exec_discount = timeit.timeit("""
discount_applied = 0
if discount_code == 'SAVE10':
    discount_applied = total_amount * 0.10
    total_amount -= discount_applied
""", setup=setup_discount, number=1000)
print(f"discount logic (SAVE10): {exec_discount:.7f} seconds over 1000 runs")

exec_discount = timeit.timeit("""
discount_applied = 0
if discount_code == 'SAVE10':
    discount_applied = total_amount * 0.10
    total_amount -= discount_applied
""", setup=setup_discount, number=10000)
print(f"discount logic (SAVE10): {exec_discount:.7f} seconds over 10000 runs")

# Store orders in orders dictionary

setup_store_order = '''
from app import orders, Order
order = Order("ABC123", "demo@bookstore.com", [], {}, {}, 99.99)
order_id = "ABC123"
'''

exec_store_order = timeit.timeit("orders[order_id] = order", setup=setup_store_order, number=100)
print(f"orders[order_id] = order: {exec_store_order:.7f} seconds over 100 runs")

exec_store_order = timeit.timeit("orders[order_id] = order", setup=setup_store_order, number=1000)
print(f"orders[order_id] = order: {exec_store_order:.7f} seconds over 1000 runs")

exec_store_order = timeit.timeit("orders[order_id] = order", setup=setup_store_order, number=10000)
print(f"orders[order_id] = order: {exec_store_order:.7f} seconds over 10000 runs")


# Add order to user

setup_add_order = '''
from app import users, Order
order = Order("ABC123", "demo@bookstore.com", [], {}, {}, 99.99)
user = users["demo@bookstore.com"]
'''

exec_add_order = timeit.timeit("user.add_order(order)", setup=setup_add_order, number=100)
print(f"user.add_order(order): {exec_add_order:.7f} seconds over 100 runs")

exec_add_order = timeit.timeit("user.add_order(order)", setup=setup_add_order, number=1000)
print(f"user.add_order(order): {exec_add_order:.7f} seconds over 1000 runs")

exec_add_order = timeit.timeit("user.add_order(order)", setup=setup_add_order, number=10000)
print(f"user.add_order(order): {exec_add_order:.7f} seconds over 10000 runs")


# Send confirmation email

setup_email = '''
from app import EmailService, Order
order = Order("ABC123", "demo@bookstore.com", [], {}, {}, 99.99)
'''

exec_email = timeit.timeit("EmailService.send_order_confirmation('demo@bookstore.com', order)", setup=setup_email, number=10)
print(f"send_order_confirmation: {exec_email:.7f} seconds over 10 runs")

exec_email = timeit.timeit("EmailService.send_order_confirmation('demo@bookstore.com', order)", setup=setup_email, number=20)
print(f"send_order_confirmation: {exec_email:.7f} seconds over 20 runs")

exec_email = timeit.timeit("EmailService.send_order_confirmation('demo@bookstore.com', order)", setup=setup_email, number=30)
print(f"send_order_confirmation: {exec_email:.7f} seconds over 30 runs")


# cart.clear

setup_clear = '''
from app import cart, BOOKS
cart.add_book(BOOKS[0], 1)
'''

exec_clear = timeit.timeit("cart.clear()", setup=setup_clear, number=100)
print(f"cart.clear: {exec_clear:.7f} seconds over 100 runs")

exec_clear = timeit.timeit("cart.clear()", setup=setup_clear, number=1000)
print(f"cart.clear: {exec_clear:.7f} seconds over 1000 runs")

exec_clear = timeit.timeit("cart.clear()", setup=setup_clear, number=10000)
print(f"cart.clear: {exec_clear:.7f} seconds over 10000 runs")

# Register new user

setup_register = '''
from app import User, users
email = "newuser@example.com"
password = "Password123"
name = "New User"
address = "123 New Test Road"
'''

exec_register = timeit.timeit("users[email] = User(email, password, name, address)", setup=setup_register, number=100)
print(f"users[email] = User(...): {exec_register:.7f} seconds over 100 runs")

exec_register = timeit.timeit("users[email] = User(email, password, name, address)", setup=setup_register, number=1000)
print(f"users[email] = User(...): {exec_register:.7f} seconds over 1000 runs")

exec_register = timeit.timeit("users[email] = User(email, password, name, address)", setup=setup_register, number=10000)
print(f"users[email] = User(...): {exec_register:.7f} seconds over 10000 runs")

# User login

setup_login = '''
from app import users
email = "demo@bookstore.com"
password = "demo123"
user = users.get(email)
'''

exec_login = timeit.timeit("user and user.password == password", setup=setup_login, number=100)
print(f"user login check: {exec_login:.7f} seconds over 100 runs")

exec_login = timeit.timeit("user and user.password == password", setup=setup_login, number=1000)
print(f"user login check: {exec_login:.7f} seconds over 1000 runs")

exec_login = timeit.timeit("user and user.password == password", setup=setup_login, number=10000)
print(f"user login check: {exec_login:.7f} seconds over 10000 runs")


# User logout

setup_logout = '''
from app import session
session['user_email'] = "demo@bookstore.com"
'''

with app.test_request_context():
    session['user_email'] = "demo@bookstore.com"
    order_id = "ORD123"

    exec_logout = timeit.timeit("session.pop('user_email', None)", globals=globals(), number=100)
    print(f"session.pop('user_email'): {exec_logout:.7f} seconds over 100 runs")

    exec_logout = timeit.timeit("session.pop('user_email', None)", globals=globals(), number=1000)
    print(f"session.pop('user_email'): {exec_logout:.7f} seconds over 1000 runs")

    exec_logout = timeit.timeit("session.pop('user_email', None)", globals=globals(), number=10000)
    print(f"session.pop('user_email'): {exec_logout:.7f} seconds over 10000 runs")


# Update user account details

setup_update_profile = '''
from app import users
user = users["demo@bookstore.com"]
new_name = "Updated Name"
new_address = "123 New Test Road"
'''

exec_update_profile = timeit.timeit("""
user.name = new_name
user.address = new_address
""", setup=setup_update_profile, number=100)
print(f"user profile update: {exec_update_profile:.7f} seconds over 100 runs")

exec_update_profile = timeit.timeit("""
user.name = new_name
user.address = new_address
""", setup=setup_update_profile, number=1000)
print(f"user profile update: {exec_update_profile:.7f} seconds over 1000 runs")

exec_update_profile = timeit.timeit("""
user.name = new_name
user.address = new_address
""", setup=setup_update_profile, number=10000)
print(f"user profile update: {exec_update_profile:.7f} seconds over 10000 runs")


# Update password

setup_update_password = '''
from app import users
user = users["demo@bookstore.com"]
new_password = "NewPassword123"
'''

exec_update_password = timeit.timeit("user.password = new_password", setup=setup_update_password, number=100)
print(f"user password update: {exec_update_password:.7f} seconds over 100 runs")

exec_update_password = timeit.timeit("user.password = new_password", setup=setup_update_password, number=1000)
print(f"user password update: {exec_update_password:.7f} seconds over 1000 runs")

exec_update_password = timeit.timeit("user.password = new_password", setup=setup_update_password, number=10000)
print(f"user password update: {exec_update_password:.7f} seconds over 10000 runs")

# Export as a .CSV file

benchmarks = [

    ("get_book_by_title", "get_book_by_title(titles[0])", '''
from app import get_book_by_title, BOOKS
titles = [book.title for book in BOOKS] * 1000
''', [100, 1000, 10000]),

    ("cart.add_book", "cart.add_book(BOOKS[0], 1)", '''
from app import cart, BOOKS
cart.clear()
''', [100, 1000, 10000]),

    ("cart.update_quantity", "cart.update_quantity(BOOKS[0].title, 3)", '''
from app import cart, BOOKS
cart.clear()
cart.add_book(BOOKS[0], 1)
''', [100, 1000, 10000]),

    ("cart.remove_book", "cart.remove_book(BOOKS[0].title)", '''
from app import cart, BOOKS
cart.clear()
cart.add_book(BOOKS[0], 1)
''', [100, 1000, 10000]),

    ("cart.get_total_price", "cart.get_total_price()", '''
from app import cart, BOOKS
cart.clear()
cart.add_book(BOOKS[0], 2)
''', [100, 1000, 10000]),

    ("cart.clear", "cart.clear()", '''
from app import cart, BOOKS
cart.add_book(BOOKS[0], 1)
''', [100, 1000, 10000]),

    ("checkout logic", "cart.is_empty(); cart.get_total_price()", '''
from app import cart, BOOKS
cart.clear()
cart.add_book(BOOKS[0], 2)
''', [100, 1000, 10000]),

    ("discount logic (SAVE10)", '''
discount_applied = 0
if discount_code == 'SAVE10':
    discount_applied = total_amount * 0.10
    total_amount -= discount_applied
''', '''
from app import cart, BOOKS
cart.clear()
cart.add_book(BOOKS[0], 2)
discount_code = 'SAVE10'
total_amount = cart.get_total_price()
''', [100, 1000, 10000]),

    ("orders[order_id] = order", "orders[order_id] = order", '''
from app import orders, Order
order = Order("ABC123", "demo@bookstore.com", [], {}, {}, 99.99)
order_id = "ABC123"
''', [100, 1000, 10000]),

    ("user.add_order(order)", "user.add_order(order)", '''
from app import users, Order
order = Order("ABC123", "demo@bookstore.com", [], {}, {}, 99.99)
user = users["demo@bookstore.com"]
''', [100, 1000, 10000]),

    ("send_order_confirmation", "EmailService.send_order_confirmation('demo@bookstore.com', order)", '''
from app import EmailService, Order
order = Order("ABC123", "demo@bookstore.com", [], {}, {}, 99.99)
''', [10, 20, 30]),

    ("register new user", "users[email] = User(email, password, name, address)", '''
from app import User, users
email = "newuser@example.com"
password = "Password123"
name = "New User"
address = "123 New Test Road"
''', [100, 1000, 10000]),

    ("user login check", "user and user.password == password", '''
from app import users
email = "demo@bookstore.com"
password = "demo123"
user = users.get(email)
''', [100, 1000, 10000]),

    ("user profile update", '''
user.name = new_name
user.address = new_address
''', '''
from app import users
user = users["demo@bookstore.com"]
new_name = "Updated Name"
new_address = "123 New Test Road"
''', [100, 1000, 10000]),

    ("user password update", "user.password = new_password", '''
from app import users
user = users["demo@bookstore.com"]
new_password = "NewPassword123"
''', [100, 1000, 10000]),
]
session_benchmarks = [
    ("session.pop('user_email')", "session.pop('user_email', None)", [100, 1000, 10000])
]

with open("timeit_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Function", "Runs", "Total Time (s)", "Avg Time (ms)"])

    for label, stmt, setup, runs_list in benchmarks:
        for n in runs_list:
            try:
                exec_time = timeit.timeit(stmt=stmt, setup=setup, number=n)
                avg_time = (exec_time / n) * 1000
                writer.writerow([label, n, f"{exec_time:.6f}", f"{avg_time:.6f}"])
            except Exception as e:
                writer.writerow([label, n, "ERROR", str(e)])

    with app.test_request_context():
        session['user_email'] = "demo@bookstore.com"
        for label, stmt, runs_list in session_benchmarks:
            for n in runs_list:
                try:
                    exec_time = timeit.timeit(stmt=stmt, globals=globals(), number=n)
                    avg_time = (exec_time / n) * 1000
                    writer.writerow([label, n, f"{exec_time:.6f}", f"{avg_time:.6f}"])
                except Exception as e:
                    writer.writerow([label, n, "ERROR", str(e)])