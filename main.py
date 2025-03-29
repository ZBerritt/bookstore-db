from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap5
import mysql.connector

app = Flask(__name__)
bootstrap = Bootstrap5(app)
def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='CoolPassword',
        port='3306',
        database='Bookstore'
    )


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

if __name__ == "__main__":
    # Initialize database schema
    with get_db() as db: 
        with db.cursor() as cursor:
            with open('scripts/setup.sql', 'r') as f:
                cursor.execute(f.read())
    
    # Add sample data
    with get_db() as db: 
        with db.cursor() as cursor:
            with open('scripts/sample-data.sql', 'r') as f:
                cursor.execute(f.read())
    app.run(debug=True)