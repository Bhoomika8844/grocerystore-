from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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
            return '''<script>alert("✅ Login Successful!"); window.location.href="/dashboard";</script>'''
        else:
            return '''<script>alert("❌ Invalid Login! Try Again."); window.location.href="/";</script>'''

    return render_template("login.html")

# Route for Dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Route for Product Categories
@app.route("/products/<category>")
def show_products(category):
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM products WHERE category = ?", (category,))
    products = cursor.fetchall()
    conn.close()
    
    return render_template("products.html", category=category, products=products)

if __name__ == "__main__":
    app.run(debug=True)
