import os
import mysql.connector
import hashlib

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user=os.environ["DATABASE_USER"],
        password=os.environ["DATABASE_PASSWORD"],
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
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT ID, Username FROM User WHERE Username = %s AND Password = %s", (username, hashed_password))
    user = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    return user
            
        
def user_register(username, password, email, address, phone_number):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM User WHERE Username = %s", (username,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Username already exists.")
    
    # Check if the email already exists
    cursor.execute("SELECT COUNT(*) FROM User WHERE Email = %s", (email,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Email already registered.")
    
    cursor.execute("SELECT MAX(ID) FROM User")
    max_id = cursor.fetchone()[0]
    new_id = max_id + 1 if max_id is not None else 1
    
    # Insert the new user
    cursor.execute("""
            INSERT INTO User (ID, Username, Password, Email, Address, Phone_Number)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (new_id, username, hashed_password, email, address, phone_number))
    
    db.commit()
    
    cursor.execute("SELECT ID, Username FROM User WHERE Username = %s", (username,))
    return cursor.fetchone()

def user_delete(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM User WHERE ID = %s;", (id,))
    db.commit()