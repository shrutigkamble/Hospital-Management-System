from werkzeug.security import generate_password_hash

from app import app
from extensions import db
from models.user import User


users = [
    {
        "username": "reception",
        "password": "reception123",
        "role": "reception"
    },
    {
        "username": "doctor",
        "password": "doctor123",
        "role": "doctor"
    },
    {
        "username": "laboratory",
        "password": "lab123",
        "role": "laboratory"
    },
    {
        "username": "billing",
        "password": "billing123",
        "role": "billing"
    },
    {
        "username": "staff",
        "password": "staff123",
        "role": "staff"
    }
]


with app.app_context():

    for user_data in users:

        existing_user = User.query.filter_by(
            username=user_data["username"]
        ).first()

        if existing_user:

            print(
                f"User already exists: {user_data['username']}"
            )

        else:

            user = User(
                username=user_data["username"],
                password_hash=generate_password_hash(
                    user_data["password"]
                ),
                role=user_data["role"]
            )

            db.session.add(user)

            print(
                f"User created: {user_data['username']}"
            )

    db.session.commit()

    print("Role-based users setup completed.")