import mysql.connector

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='CoolPassword',
        port='3306',
        database='Bookstore'
    )
    
def init_db():
    with get_db() as db: 
        with db.cursor() as cursor:
            with open('scripts/setup.sql', 'r') as f:
                cursor.execute(f.read())
    
    # Add sample data
    with get_db() as db: 
        with db.cursor() as cursor:
            with open('scripts/sample-data.sql', 'r') as f:
                cursor.execute(f.read())