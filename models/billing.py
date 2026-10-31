from datetime import datetime

from extensions import db


class Bill(db.Model):
    __tablename__ = "bills"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    bill_date = db.Column(
        db.Date,
        nullable=False
    )

    consultation_charge = db.Column(
        db.Float,
        default=0
    )

    laboratory_charge = db.Column(
        db.Float,
        default=0
    )

    pharmacy_charge = db.Column(
        db.Float,
        default=0
    )

    room_charge = db.Column(
        db.Float,
        default=0
    )

    other_charge = db.Column(
        db.Float,
        default=0
    )

    total_amount = db.Column(
        db.Float,
        default=0
    )

    payment_status = db.Column(
        db.String(30),
        default="Pending",
        nullable=False
    )

    payment_method = db.Column(
        db.String(30)
    )

    notes = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )