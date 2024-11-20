from flask_mongoengine import MongoEngine
from mongoengine.connection import ConnectionFailure

db = MongoEngine()

def init_db(app):
    try:
        db.init_app(app)
        db.get_db()
        print("Successfully connected to MongoDB!")
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB. Error: {e}")
        raise
    except Exception as e:
        print(f"An error occurred while initializing the database: {e}")
        raise