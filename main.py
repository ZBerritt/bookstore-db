# Run python ./scripts/setup.py to setup or reset database with updated schema
from dotenv import load_dotenv
load_dotenv()
from router import app

if __name__ == "__main__":
    """
    Create a .env file in the main directory with the following lines (remove {}):
    DATABASE_USER={user}
    DATABASE_PASSWORD={password}
    APP_SECRET={secret}
    """
    
    app.run(debug=True)