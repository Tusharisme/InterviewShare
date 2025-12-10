from flask import Blueprint, request, jsonify
from extensions import db
from models import Experience, User
from flask_security import auth_token_required, current_user

api = Blueprint('api', __name__)
# We've globally disabled CSRF in config, but explicitly ensures no issues for this BP

@api.route('/health', methods=['GET'])
def health_check():
    status_report = {
        "status": "online",
        "db_connection": "unknown",
        "tables": [],
        "errors": []
    }
    
    try:
        # 1. Basic Connection
        db.session.execute(db.text("SELECT 1"))
        status_report['db_connection'] = "success"
        
        # 2. Check Tables (Introspection)
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        status_report['tables'] = tables
        
        # 3. Check Data Access
        if 'experience' in tables:
            count = db.session.query(Experience).count()
            status_report['experience_count'] = count
            
            # Try fetching one to test serialization
            if count > 0:
                exp = db.session.query(Experience).first()
                try:
                    status_report['sample_serialization'] = "success"
                except Exception as e:
                    status_report['sample_serialization'] = str(e)
                    
    except Exception as e:
        status_report['db_connection'] = "failed"
        status_report['errors'].append(str(e))
        import traceback
        status_report['trace'] = traceback.format_exc()

    return jsonify(status_report), 200

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

@api.route('/stats/heatmap', methods=['GET'])
def get_heatmap_stats():
    try:
        # Aggregate experiences by date
        # func.date() extracts the date part from datetime
        try:
            results = db.session.query(
                func.date(Experience.created_at).label('date'), 
                func.count(Experience.id).label('count')
            ).group_by(func.date(Experience.created_at)).all()
        except:
             # Fallback for some DBs if func.date fails (sqlite sometimes behaves differently)
             results = []
             
        # Format for frontend (list of objects)
        heatmap_data = []
        for r in results:
            heatmap_data.append({
                'date': str(r.date),
                'count': r.count
            })
            
        return jsonify(heatmap_data), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

from flask_security.utils import verify_password, login_user
@api.route('/login', methods=['POST'])
def login_custom():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'meta': {'code': 400}, 'response': {'errors': ['Missing credentials']}}), 400
        
    user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        return jsonify({'meta': {'code': 400}, 'response': {'errors': ['Invalid email or password']}}), 400
        
    if not verify_password(data['password'], user.password):
        return jsonify({'meta': {'code': 400}, 'response': {'errors': ['Invalid email or password']}}), 400
        
    # Login the user
    login_user(user)
    
    return jsonify({
        'meta': {'code': 200},
        'response': {
            'user': user.to_dict(include_token=True)
        }
    })

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
