from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_bootstrap import Bootstrap5
from database import get_db, user_login

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

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))