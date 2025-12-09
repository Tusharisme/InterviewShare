from flask import Blueprint, request, jsonify
from extensions import db
from models import Experience, User
from flask_security import auth_token_required, current_user

api = Blueprint('api', __name__)
# We've globally disabled CSRF in config, but explicitly ensures no issues for this BP

@api.route('/health', methods=['GET'])
def health_check():
    db_status = "ok"
    db_info = "unknown"
    try:
        # Check DB connection
        db.session.execute(db.text("SELECT 1"))
        uri = str(db.engine.url)
        if "sqlite" in uri:
            db_info = "sqlite (fallback active - dangerous on vercel)"
        elif "postgres" in uri:
            db_info = "postgres (correct)"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return jsonify({
        "status": "online",
        "db_status": db_status,
        "db_type": db_info
    }), 200

@api.route('/experiences', methods=['GET'])
def get_experiences():
    try:
        query = request.args.get('q')
        if query:
            # Simple search implementation
            experiences = Experience.query.filter(
                (Experience.company.ilike(f'%{query}%')) | 
                (Experience.role_title.ilike(f'%{query}%'))
            ).order_by(Experience.created_at.desc()).all()
        else:
            experiences = Experience.query.order_by(Experience.created_at.desc()).all()
            
        return jsonify([e.to_dict() for e in experiences])
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@api.route('/experiences/me', methods=['GET'])
@auth_token_required
def get_my_experiences():
    experiences = Experience.query.filter_by(user_id=current_user.id).order_by(Experience.created_at.desc()).all()
    return jsonify([exp.to_dict() for exp in experiences]), 200

@api.route('/experiences/<int:id>/like', methods=['POST'])
@auth_token_required
def toggle_like(id):
    experience = Experience.query.get_or_404(id)
    
    if current_user in experience.liked_by:
        experience.liked_by.remove(current_user)
        action = 'unliked'
    else:
        experience.liked_by.append(current_user)
        action = 'liked'
    
    db.session.commit()
    
    return jsonify({
        'message': f'Experience {action}',
        'likes_count': len(experience.liked_by),
        'action': action
    }), 200




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

@api.route('/experiences/<int:id>', methods=['GET'])
def get_experience(id):
    experience = Experience.query.get_or_404(id)
    return jsonify(experience.to_dict()), 200

@api.route('/experiences/<int:id>', methods=['PUT'])
@auth_token_required
def update_experience(id):
    experience = Experience.query.get_or_404(id)
    
    if experience.user_id != current_user.id:
        return jsonify({'message': 'Permission denied'}), 403

    data = request.get_json()
    
    if 'title' in data:
        experience.title = data['title']
    if 'company' in data:
        experience.company = data['company']
    if 'role_title' in data:
        experience.role_title = data['role_title']
    if 'content' in data:
        experience.content = data['content']

    db.session.commit()

    return jsonify(experience.to_dict()), 200


