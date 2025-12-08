from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to InterviewShare API", "status": "running"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
