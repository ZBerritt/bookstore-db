import os
from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
from database import get_db, user_login, user_register, user_delete, get_user_info, start_transaction, admin_get_books, admin_get_users, admin_get_transactions

app = Flask(__name__)
app.secret_key = os.environ["APP_SECRET"]


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
            session["role"] = user["Role"]
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
            session["user_id"] = user["ID"]
            session["username"] = user["Username"]
            session["role"] = user["Role"]
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
    print(session)
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
    # Read filters
    q         = request.args.get("q", "").strip()
    genre     = request.args.get("genre", "")
    min_price = request.args.get("min_price", "")
    max_price = request.args.get("max_price", "")

    # Build WHERE clauses
    conditions = []
    params     = []
    if q:
        conditions.append("(b.Title LIKE %s OR a.Name LIKE %s)")
        like_q = f"%{q}%"
        params += [like_q, like_q]
    if genre:
        conditions.append("b.Genre = %s")
        params.append(genre)
    if min_price:
        conditions.append("b.Price >= %s")
        params.append(min_price)
    if max_price:
        conditions.append("b.Price <= %s")
        params.append(max_price)

    where = " AND ".join(conditions)

    # Query with JOIN + GROUP_CONCAT for authors
    sql = """
    SELECT
      b.ISBN,
      b.Title,
      GROUP_CONCAT(a.Name SEPARATOR ', ') AS Authors,
      b.Genre,
      b.Price
    FROM Book b
    LEFT JOIN Book_Author ba ON ba.ISBN = b.ISBN
    LEFT JOIN Author a       ON a.Email = ba.Author_Email
    """
    if where:
        sql += " WHERE " + where
    sql += " GROUP BY b.ISBN;"

    db     = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql, tuple(params))
    books  = cursor.fetchall()

    # Find distinct genres for the filter dropdown
    cursor.execute("SELECT DISTINCT Genre FROM Book;")
    genres = [r["Genre"] for r in cursor.fetchall()]

    cursor.close()
    db.close()

    return render_template(
        "shop.html",
        books=books,
        genres=genres,
        filters={
            "q": q,
            "genre": genre,
            "min_price": min_price,
            "max_price": max_price
        }
    )


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

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart_items = session.get("cart", [])
    if request.method == "POST":
        if "user_id" not in session:
            return jsonify({"status": "error", "message": "Not authenticated"}), 401
        if len(cart_items) == 0:
            return jsonify({"status": "error", "message": "Empty cart"}), 400
        start_transaction(session["user_id"], cart_items)
        session.pop("cart", None)
        flash('Purchase Successful!', 'success')
        return redirect(url_for("dashboard"))
    else:
        if "user_id" not in session:
            return redirect(url_for("login"))
        if len(cart_items) == 0:
            return redirect(url_for("shop"))
        user_info = get_user_info(id=session["user_id"])
        return render_template("checkout.html", cart=cart_items, user=user_info)
        
@app.route("/admin")
def admin():
    if "user_id" not in session:
        return redirect(url_for("login"))
    info = get_user_info(session["user_id"])
    if info["Role"] != "admin":
        return redirect(url_for("shop"))
    return render_template("admin.html", books=admin_get_books(), users=admin_get_users(), transactions=admin_get_transactions())

@app.route("/logout")
def logout():
    cart = session.get("cart", [])
    session.clear()
    session["cart"] = cart
    return redirect(url_for("login"))
