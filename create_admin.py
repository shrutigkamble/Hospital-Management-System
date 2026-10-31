from werkzeug.security import generate_password_hash

from app import app
from extensions import db
from models.user import User


with app.app_context():

    existing_user = User.query.filter_by(username="admin").first()

    if existing_user:
        print("Admin user already exists.")

    else:
        admin = User(
            username="admin",
            password_hash=generate_password_hash("admin123"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")