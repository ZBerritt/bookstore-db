import mysql.connector
import hashlib

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='CoolPassword',
        port='3306',
        database='Bookstore'
    )
    
def init_db():
    with get_db() as db, db.cursor() as cursor:
            with open('scripts/setup.sql', 'r') as f:
                cursor.execute(f.read())
    
    # Add sample data
    with get_db() as db, db.cursor() as cursor:
            with open('scripts/sample-data.sql', 'r') as f:
                cursor.execute(f.read())
                
def user_login(username, password):
    password_hash = hashlib.sha256(password)
    with get_db() as db, db.cursor() as cursor:
        cursor.execute("SELECT * FROM User WHERE Username = %s and Password = %s", (username, password_hash))
            
        
def user_register():
    pass