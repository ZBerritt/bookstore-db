from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap5
from database import get_db

app = Flask(__name__)
bootstrap = Bootstrap5(app)


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