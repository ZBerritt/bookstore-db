import os
import mysql.connector
import hashlib
from datetime import datetime

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user=os.environ["DATABASE_USER"],
        password=os.environ["DATABASE_PASSWORD"],
        port='3306',
        database='bookstore'
    )
                
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
    
def get_user_info(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT Username, Email, Address, Phone_Number FROM User WHERE ID = %s;", (id,))
    return cursor.fetchone()

def start_transaction(user_id, cart):
    total_price = sum(n["price"] for n in cart)
    books = [ (n["isbn"], n["quantity"]) for n in cart ]
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT MAX(ID) FROM Transaction")
    max_id = cursor.fetchone()[0]
    new_id = max_id + 1 if max_id is not None else 1
    cursor.execute("""
            INSERT INTO Transaction (ID, Date, Price, UserID)
            VALUES (%s, %s, %s, %s)
        """, (new_id, datetime.now(), total_price, user_id))
    for book in books:
        cursor.execute("""
                INSERT INTO Book_Transaction (ISBN, Transaction_ID, Quantity)
                VALUES (%s, %s, %s)
            """, (book[0], new_id, book[1]))
    db.commit()