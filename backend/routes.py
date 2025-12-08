from flask import Blueprint, request, jsonify
from extensions import db
from models import Experience, User

api = Blueprint('api', __name__)

@api.route('/experiences', methods=['GET'])
def get_experiences():
    experiences = Experience.query.order_by(Experience.created_at.desc()).all()
    return jsonify([exp.to_dict() for exp in experiences]), 200

@api.route('/experiences', methods=['POST'])
def create_experience():
    data = request.get_json()
    
    # Validation (Basic)
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'message': 'Missing required fields'}), 400

    # TODO: Replace with actual logged-in user once Auth is implemented
    # For now, we'll create a dummy user or use the first user if exists
    user = User.query.first()
    if not user:
        # Create a temporary dummy user for development testing
        import uuid
        user = User(email=f'test_{uuid.uuid4().hex[:8]}@example.com', fs_uniquifier=uuid.uuid4().hex)
        db.session.add(user)
        db.session.commit()

    new_experience = Experience(
        title=data['title'],
        company=data['company'],
        role_title=data['role_title'],
        content=data['content'],
        user_id=user.id
    )

    db.session.add(new_experience)
    db.session.commit()

    return jsonify(new_experience.to_dict()), 201
