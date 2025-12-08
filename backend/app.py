from flask import Flask, jsonify
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from config import Config
from extensions import db
from models import User, Role

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    with app.app_context():
        db.create_all()
        # Create a test user if none exists
        if not user_datastore.find_user(email="test@example.com"):
            user_datastore.create_user(email="test@example.com", password=hash_password("password"))
            db.session.commit()

    from routes import api
    app.register_blueprint(api, url_prefix='/api')

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to InterviewShare API", "status": "running"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
