from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_bootstrap import Bootstrap5
from database import get_db, user_login, user_register, user_delete

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = 'key'


@app.route("/")
def root():
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
            return redirect(url_for("dashboard"))  # Redirect to dashboard
        
        return render_template("login.html", error="Invalid credentials")
    elif "user_id" in session:
        return redirect(url_for("dashboard"))
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
            return redirect(url_for("dashboard"))
        except Exception as err:
            return render_template("register.html", error=err)
    elif "user_id" in session:
        return redirect(url_for("dashboard"))
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
    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()
    print(books)
    db.close()
    return render_template("books.html", books=books)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))