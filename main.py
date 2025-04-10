from database import init_db
from router import app

if __name__ == "__main__":
    # Initialize database schema
    # init_db()
    app.run(debug=True)