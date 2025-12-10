from extensions import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime

# Association table for User-Role many-to-many relationship
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False) # Required by newer Flask-Security
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    experiences = db.relationship('Experience', backref='author', lazy=True)
    liked_experiences = db.relationship('Experience', secondary='experience_likes', backref='liked_by', lazy='dynamic')

    def to_dict(self, include_token=False):
        data = {
            'id': self.id,
            'email': self.email,
            'active': self.active
        }
        if include_token:
            data['authentication_token'] = self.get_auth_token()
        return data

# Association table for Likes
experience_likes = db.Table('experience_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('experience_id', db.Integer, db.ForeignKey('experience.id'))
)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    role_title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'role_title': self.role_title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'author': self.author.email,
            'likes_count': len(self.liked_by),
            # We can't easily check 'is_liked' here without context of current user, 
            # so we'll handle that on the frontend or a separate field if needed.
            # For simplicity, we'll return the list of liker IDs or just the count.
            'liker_ids': [user.id for user in self.liked_by]
        }
