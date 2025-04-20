import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

# Dummy login credentials
VALID_USERNAME = "admin"
VALID_PASSWORD = "kjc"

# Route for Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["user"] = username  # Store user session
            return '''<script>
                        alert("✅ Login Successful!");0
                        window.location.href="/dashboard";
                      </script>'''
        else:
            return '''<script>
                        alert("❌ Invalid Login! Try Again.");
                        window.location.href="/";
                      </script>'''

    return render_template("login.html")

# Route for Dashboard (Login Required)
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))  # Redirect to login if not logged in
    return render_template("dashboard.html")

# Route to show products based on category (Login Required)
@app.route("/products/<category>")
def show_products(category):
    if "user" not in session:
        return redirect(url_for("login"))  # Redirect to login if not logged in

    conn = sqlite3.connect("products.db")  # Updated to 'products.db'
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM products WHERE category = ?", (category,))
    products = cursor.fetchall()
    conn.close()

    return render_template("products.html", category=category, products=products)


# Function to insert cart items into the checkout table
def insert_into_checkout(product_name, quantity, total_price):
    conn = sqlite3.connect('products.db')  # Use your actual database file name
    cursor = conn.cursor()

    # Insert product into checkout table
    cursor.execute('''INSERT INTO checkout (product_name, quantity, total_price)
                      VALUES (?, ?, ?)''', (product_name, quantity, total_price))

    conn.commit()
    conn.close()

# Route to add products to the cart
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    product_name = data['product']
    quantity = data['quantity']

    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("SELECT price, stock FROM products WHERE name = ?", (product_name,))
    result = cursor.fetchone()

    if result:
        product_price, stock = result

        if stock < quantity:
            conn.close()
            return jsonify({"message": "❌ Out of Stock!"}), 400

        total_price = product_price * quantity

        # Update stock
        cursor.execute("UPDATE products SET stock = stock - ? WHERE name = ?", (quantity, product_name))

        # Insert into checkout here (same connection)
        cursor.execute('''
            INSERT INTO checkout (product_name, quantity, total_price)
            VALUES (?, ?, ?)
        ''', (product_name, quantity, total_price))

        conn.commit()
        conn.close()

        return jsonify({"message": "✅ Product added to cart successfully!"})
    else:
        conn.close()
        return jsonify({"message": "❌ Product not found!"}), 404
# Route for Cart Page
@app.route("/cart")
def view_cart():
    total_price = 0
    product_price = {}

    # Get prices for all products in the cart from the checkout table
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    # Retrieve all products in the checkout table (since they're already stored there)
    cursor.execute("SELECT product_name, quantity, total_price FROM checkout")
    cart_items = cursor.fetchall()

    for item in cart_items:
        product_name, quantity, total_price_item = item
        product_price[product_name] = total_price_item / quantity  # Calculate per item price
        total_price += total_price_item

    conn.close()

    return render_template("cart.html", cart=cart_items, product_price=product_price, total_price=total_price)

# Route to remove items from the cart
@app.route("/remove_from_cart/<product>", methods=["POST"])
def remove_from_cart(product):
    # Remove product from the checkout table
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM checkout WHERE product_name = ?", (product,))
    conn.commit()
    conn.close()

    return redirect(url_for("view_cart"))
@app.route("/checkout")
def checkout():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("customer.html")

# Save customer route - stores data without viewing capability
@app.route("/save_customer", methods=["POST"])
def save_customer():
    if "user" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    try:
        data = request.get_json()
        
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO customers (
                full_name, email, phone, address, 
                payment_method, card_number, card_name, 
                expiry_date, cvv
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['fullName'],
            data['email'],
            data['phone'],
            data['address'],
            data['paymentMethod'],
            data['cardNumber'] if data['paymentMethod'] != 'Cash' else None,
            data['cardName'] if data['paymentMethod'] != 'Cash' else None,
            data['expiryDate'] if data['paymentMethod'] != 'Cash' else None,
            data['cvv'] if data['paymentMethod'] != 'Cash' else None
        ))
        
        conn.commit()
        conn.close()
        
        # Clear the cart after successful checkout
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM checkout")
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Order placed successfully!',
            'redirect': url_for('dashboard')
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
@app.route("/logout")
def logout():
    session.pop("user", None)  # Remove user session
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)