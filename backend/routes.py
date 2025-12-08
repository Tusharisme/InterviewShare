from flask import Blueprint, request, jsonify
from extensions import db
from models import Experience, User

api = Blueprint('api', __name__)

@api.route('/experiences', methods=['GET'])
def get_experiences():
    experiences = Experience.query.order_by(Experience.created_at.desc()).all()
    return jsonify([exp.to_dict() for exp in experiences]), 200

from flask_security import auth_token_required, current_user

# ... imports ...

@api.route('/experiences', methods=['POST'])
@auth_token_required
def create_experience():
    data = request.get_json()
    
    # Validation (Basic)
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'message': 'Missing required fields'}), 400

    new_experience = Experience(
        title=data['title'],
        company=data['company'],
        role_title=data['role_title'],
        content=data['content'],
        user_id=current_user.id
    )

    db.session.add(new_experience)
    db.session.commit()

    return jsonify(new_experience.to_dict()), 201

@api.route('/experiences/<int:id>', methods=['DELETE'])
@auth_token_required
def delete_experience(id):
    experience = Experience.query.get_or_404(id)
    
    if experience.user_id != current_user.id:
        return jsonify({'message': 'Permission denied'}), 403

    db.session.delete(experience)
    db.session.commit()

    return jsonify({'message': 'Experience deleted'}), 200

