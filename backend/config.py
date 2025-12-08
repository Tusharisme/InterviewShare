import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///interviewshare.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Security
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'super-secret-salt')
    SECURITY_PASSWORD_HASH = 'argon2'
    
    # Flask-Security Config for SPA/API
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    WTF_CSRF_ENABLED = False 
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_PASSWORD_LENGTH_MIN = 6  # Allow shorter passwords for development

