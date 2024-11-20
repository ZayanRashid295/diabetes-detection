import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # MongoDB settings
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGODB_URI', 'mongodb://localhost:27017/diabetes_detection')
    }