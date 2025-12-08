from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from extensions import db
from models import User, Role

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from routes import api
    app.register_blueprint(api, url_prefix='/api')

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to InterviewShare API", "status": "running"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
