from flask import Blueprint, render_template, request, redirect, url_for, flash
from auth_utils import role_required

from extensions import db
from models.medical_record import MedicalRecord
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment


medical_record_bp = Blueprint(
    "medical_record",
    __name__,
    url_prefix="/medical-records"
)


# ==================== MEDICAL RECORD LIST / SEARCH ====================

@medical_record_bp.route("/")
@role_required("admin", "doctor")
def medical_record_list():

    search = request.args.get("search", "").strip()

    query = MedicalRecord.query

    if search:

        query = query.join(
            Patient,
            MedicalRecord.patient_id == Patient.id
        ).join(
            Doctor,
            MedicalRecord.doctor_id == Doctor.id
        ).filter(
            db.or_(
                Patient.name.ilike(f"%{search}%"),
                Doctor.name.ilike(f"%{search}%"),
                MedicalRecord.diagnosis.ilike(f"%{search}%")
            )
        )

    records = query.order_by(
        MedicalRecord.id.desc()
    ).all()

    return render_template(
        "medical_records.html",
        records=records,
        search=search
    )


# ==================== ADD MEDICAL RECORD ====================

@medical_record_bp.route("/add", methods=["GET", "POST"])
@role_required("admin", "doctor")
def add_medical_record():

    patients = Patient.query.order_by(
        Patient.name.asc()
    ).all()

    doctors = Doctor.query.order_by(
        Doctor.name.asc()
    ).all()

    appointments = Appointment.query.order_by(
        Appointment.id.desc()
    ).all()

    if request.method == "POST":

        medical_record = MedicalRecord(
            patient_id=request.form.get("patient_id"),
            doctor_id=request.form.get("doctor_id"),
            appointment_id=request.form.get("appointment_id") or None,
            diagnosis=request.form.get("diagnosis"),
            treatment=request.form.get("treatment"),
            prescription=request.form.get("prescription"),
            allergies=request.form.get("allergies"),
            medical_report=request.form.get("medical_report")
        )

        db.session.add(medical_record)
        db.session.commit()

        flash(
            "Medical record added successfully.",
            "success"
        )

        return redirect(
            url_for("medical_record.medical_record_list")
        )

    return render_template(
        "add_medical_record.html",
        patients=patients,
        doctors=doctors,
        appointments=appointments
    )


# ==================== MEDICAL RECORD DETAILS ====================

@medical_record_bp.route("/<int:record_id>")
@role_required("admin", "doctor")
def medical_record_details(record_id):

    record = MedicalRecord.query.get_or_404(
        record_id
    )

    patient = Patient.query.get(
        record.patient_id
    )

    doctor = Doctor.query.get(
        record.doctor_id
    )

    appointment = None

    if record.appointment_id:

        appointment = Appointment.query.get(
            record.appointment_id
        )

    return render_template(
        "medical_record_details.html",
        record=record,
        patient=patient,
        doctor=doctor,
        appointment=appointment
    )


# ==================== EDIT MEDICAL RECORD ====================

@medical_record_bp.route(
    "/<int:record_id>/edit",
    methods=["GET", "POST"]
)
@role_required("admin", "doctor")
def edit_medical_record(record_id):

    record = MedicalRecord.query.get_or_404(
        record_id
    )

    patients = Patient.query.order_by(
        Patient.name.asc()
    ).all()

    doctors = Doctor.query.order_by(
        Doctor.name.asc()
    ).all()

    appointments = Appointment.query.order_by(
        Appointment.id.desc()
    ).all()

    if request.method == "POST":

        record.patient_id = request.form.get(
            "patient_id"
        )

        record.doctor_id = request.form.get(
            "doctor_id"
        )

        record.appointment_id = request.form.get(
            "appointment_id"
        ) or None

        record.diagnosis = request.form.get(
            "diagnosis"
        )

        record.treatment = request.form.get(
            "treatment"
        )

        record.prescription = request.form.get(
            "prescription"
        )

        record.allergies = request.form.get(
            "allergies"
        )

        record.medical_report = request.form.get(
            "medical_report"
        )

        db.session.commit()

        flash(
            "Medical record updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "medical_record.medical_record_details",
                record_id=record.id
            )
        )

    return render_template(
        "edit_medical_record.html",
        record=record,
        patients=patients,
        doctors=doctors,
        appointments=appointments
    )


# ==================== DELETE MEDICAL RECORD ====================

@medical_record_bp.route(
    "/<int:record_id>/delete",
    methods=["POST"]
)
@role_required("admin", "doctor")
def delete_medical_record(record_id):

    record = MedicalRecord.query.get_or_404(
        record_id
    )

    db.session.delete(record)
    db.session.commit()

    flash(
        "Medical record deleted successfully.",
        "success"
    )

    return redirect(
        url_for("medical_record.medical_record_list")
    )