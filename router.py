from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_bootstrap import Bootstrap5
from database import get_db, user_login, user_register, user_delete

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = 'key'


@app.route("/")
def root():
    # If the user is authenticated, redirect them to the shop page.
    if "user_id" in session:
        return redirect(url_for("shop"))
    # Otherwise, show the default landing page.
    return render_template("index.html")


@app.route("/status")
def status():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        db.close()
        return jsonify({'status': 'success', 'tables': tables})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = user_login(username, password)
        if user:
            session["user_id"] = user["ID"]  
            session["username"] = user["Username"]
            return redirect(url_for("shop"))  
        
        return render_template("login.html", error="Invalid credentials")
    elif "user_id" in session:
        return redirect(url_for("shop"))
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            address = request.form["address"]
            phone = request.form["phone"]
            
            # Register in DB
            user = user_register(username, password, email, address, phone)
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("shop"))
        except Exception as err:
            return render_template("register.html", error=err)
    elif "user_id" in session:
        return redirect(url_for("shop"))
    else:
        return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if "user_id" not in session:
        return redirect(url_for("login"))
    elif request.method == "POST":
        user_delete(session["user_id"])
        session.clear()
        return redirect(url_for("login"))
    else:
        return render_template("delete.html")
    
@app.route("/shop")
def shop():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Book")
    books = cursor.fetchall()
    print(books)
    db.close()
    return render_template("books.html", books=books)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if "user_id" not in session:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({'status': 'error', 'message': 'Not authenticated'}), 401
        return redirect(url_for("login"))
    
    isbn = request.form.get("isbn")
    try:
        quantity = int(request.form.get("quantity", 1))
    except ValueError:
        quantity = 1

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT ISBN, Title, Price FROM Book WHERE ISBN = %s", (isbn,))
    book = cursor.fetchone()
    cursor.close()
    db.close()
    
    if not book:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({'status': 'error', 'message': 'Book not found'}), 404
        return "Book not found", 404

    cart_item = {
         "isbn": book["ISBN"],
         "title": book["Title"],
         "quantity": quantity,
         "price": float(book["Price"])
    }
    
    if "cart" not in session:
        session["cart"] = []
    
    found = False
    for item in session["cart"]:
        if item.get("isbn") == cart_item["isbn"]:
            item["quantity"] += quantity
            found = True
            break
    if not found:
        session["cart"].append(cart_item)
    
    session.modified = True
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({'status': 'success', 'message': 'Item added to cart'})
    else:
        return redirect(url_for("shop"))

@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Not authenticated"}), 401
    
    isbn = request.form.get("isbn")
    if not isbn:
        return jsonify({"status": "error", "message": "ISBN missing"}), 400

    cart = session.get("cart", [])
    for i, item in enumerate(cart):
        if item.get("isbn") == isbn:
            # If the quantity is greater than 1, reduce it by one.
            if item.get("quantity", 1) > 1:
                item["quantity"] -= 1
            else:
                # If quantity is 1, remove the item entirely
                del cart[i]
            break
    
    session["cart"] = cart
    session.modified = True
    return jsonify({"status": "success", "message": "Item modified in cart"})

@app.route("/cart")
def cart():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    cart_items = session.get("cart", [])
    return render_template("cart.html", cart=cart_items)

# Temporary
@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("cart"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))