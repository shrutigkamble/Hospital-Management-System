from datetime import datetime

from extensions import db


class LaboratoryTest(db.Model):
    __tablename__ = "laboratory_tests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctors.id"),
        nullable=True
    )

    test_name = db.Column(
        db.String(150),
        nullable=False
    )

    test_date = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Requested",
        nullable=False
    )

    result = db.Column(
        db.Text
    )

    report = db.Column(
        db.Text
    )

    remarks = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )