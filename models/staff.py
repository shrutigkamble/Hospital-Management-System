from datetime import datetime

from extensions import db


class Staff(db.Model):
    __tablename__ = "staff"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    role = db.Column(
        db.String(50),
        nullable=False
    )

    department = db.Column(
        db.String(100)
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    email = db.Column(
        db.String(100)
    )

    address = db.Column(
        db.Text
    )

    salary = db.Column(
        db.Float,
        default=0
    )

    joining_date = db.Column(
        db.Date
    )

    status = db.Column(
        db.String(30),
        default="Active",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )