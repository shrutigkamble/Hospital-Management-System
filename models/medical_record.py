from datetime import datetime

from extensions import db


class MedicalRecord(db.Model):
    __tablename__ = "medical_records"

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
        nullable=False
    )

    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey("appointments.id"),
        nullable=True
    )

    diagnosis = db.Column(
        db.Text
    )

    treatment = db.Column(
        db.Text
    )

    prescription = db.Column(
        db.Text
    )

    allergies = db.Column(
        db.Text
    )

    medical_report = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )