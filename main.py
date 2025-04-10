from database import init_db
from dotenv import load_dotenv
from router import app

'''
Create a .env file in the main directory with the following lines:
DATABASE_USER={user}
DATABASE_PASSWORD={password}
'''
load_dotenv()

if __name__ == "__main__":
    # Initialize database schema
    # init_db()
    app.run(debug=True)