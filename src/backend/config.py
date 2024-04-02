from pathlib import Path


class Config:
    DEBUG = True
    SECRET_KEY = "d1542bd969ae4edabfdf34e750c624a5"
    
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAX_CONTENT_LENGTH = 1024 * 1024 * 5 # MAX 5MB
    UPLOAD_EXTENSIONS = ['.jpg', '.JPG']
    UPLOAD_PATH = Path('static/uploads')
    