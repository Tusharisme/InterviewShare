import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-secret-key'
    # Check for both standard naming conventions
    _db_url = os.environ.get('SQLALCHEMY_DATABASE_URI') or os.environ.get('DATABASE_URL')
    if _db_url and _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql+pg8000://")
    elif _db_url and _db_url.startswith("postgresql://"):
        _db_url = _db_url.replace("postgresql://", "postgresql+pg8000://")
        
    SQLALCHEMY_DATABASE_URI = _db_url or 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Security
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'super-secret-salt')
    # SECURITY_PASSWORD_HASH = 'bcrypt' # Removed to use default (standard lib)
    
    # Flask-Security Config for SPA/API
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_UNAUTHORIZED_VIEW = None
    WTF_CSRF_ENABLED = False 
    WTF_CSRF_CHECK_DEFAULT = False # Strict CSRF protection can block API calls
    SECURITY_CSRF_PROTECT_MECHANISMS = [] # Disable CSRF mechanisms for API
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_PASSWORD_LENGTH_MIN = 6  # Allow shorter passwords for development

