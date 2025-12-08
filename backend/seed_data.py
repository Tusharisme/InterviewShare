from app import create_app
from extensions import db
from models import User, Experience
from flask_security import hash_password

app = create_app()

with app.app_context():
    print("Seeding database...")
    
    # Create Users
    users_data = [
        {"email": "alice@example.com", "password": "password"},
        {"email": "bob@example.com", "password": "password"},
        {"email": "charlie@example.com", "password": "password"}
    ]
    
    users = []
    for u_data in users_data:
        if not User.query.filter_by(email=u_data['email']).first():
            user = app.extensions['security'].datastore.create_user(
                email=u_data['email'],
                password=hash_password(u_data['password']),
                active=True
            )
            users.append(user)
            print(f"Created user: {u_data['email']}")
        else:
            users.append(User.query.filter_by(email=u_data['email']).first())
            print(f"User already exists: {u_data['email']}")
            
    db.session.commit()
    
    # Create Experiences
    experiences_data = [
        {
            "title": "Software Engineer at Google",
            "company": "Google",
            "role_title": "Software Engineer",
            "content": "The interview process consisted of 5 rounds. 1 screening, 3 technical coding rounds (LeetCode Hard/Medium), and 1 Googleyness round. Focus on graphs and DP.",
            "author_email": "alice@example.com"
        },
        {
            "title": "Frontend Developer at Amazon",
            "company": "Amazon",
            "role_title": "Frontend Engineer II",
            "content": "Lots of questions about CSS, React internals, and performance optimization. Also standard LP questions.",
            "author_email": "bob@example.com"
        },
        {
            "title": "Data Scientist at Netflix",
            "company": "Netflix",
            "role_title": "Senior Data Scientist",
            "content": "Deep dive into A/B testing methodologies, statistics, and machine learning models for recommendation systems. Culture fit is huge here.",
            "author_email": "charlie@example.com"
        },
         {
            "title": "Intern at Microsoft",
            "company": "Microsoft",
            "role_title": "SDE Intern",
            "content": "3 rounds. First round was online assessment. Second round asked about linked lists. Final round was system design (URL shortener) adapted for an intern.",
            "author_email": "alice@example.com"
        }
    ]
    
    for exp_data in experiences_data:
        author = User.query.filter_by(email=exp_data['author_email']).first()
        if author:
            # Check if exists to avoid duplicates (simple check by title)
            if not Experience.query.filter_by(title=exp_data['title'], user_id=author.id).first():
                exp = Experience(
                    title=exp_data['title'],
                    company=exp_data['company'],
                    role_title=exp_data['role_title'],
                    content=exp_data['content'],
                    user_id=author.id
                )
                db.session.add(exp)
                print(f"Created experience: {exp_data['title']}")
    
    db.session.commit()
    print("Database seeded successfully!")
