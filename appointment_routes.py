from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from auth_utils import role_required

from extensions import db
from models.appointment import Appointment
from models.patient import Patient
from models.doctor import Doctor


appointment_bp = Blueprint(
    "appointment",
    __name__,
    url_prefix="/appointments"
)


# ==================== APPOINTMENT LIST / SEARCH ====================

@appointment_bp.route("/")
@role_required("admin", "reception", "doctor")
def appointment_list():

    search = request.args.get("search", "").strip()

    query = Appointment.query

    if search:

        query = query.join(
            Patient,
            Appointment.patient_id == Patient.id
        ).join(
            Doctor,
            Appointment.doctor_id == Doctor.id
        ).filter(
            db.or_(
                Patient.name.ilike(f"%{search}%"),
                Doctor.name.ilike(f"%{search}%"),
                Appointment.status.ilike(f"%{search}%")
            )
        )

    appointments = query.order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()

    return render_template(
        "appointments.html",
        appointments=appointments,
        search=search
    )


# ==================== ADD APPOINTMENT ====================

@appointment_bp.route("/add", methods=["GET", "POST"])
@role_required("admin", "reception", "doctor")
def add_appointment():

    patients = Patient.query.order_by(
        Patient.name.asc()
    ).all()

    doctors = Doctor.query.order_by(
        Doctor.name.asc()
    ).all()

    if request.method == "POST":

        appointment_date = request.form.get(
            "appointment_date"
        )

        appointment_time = request.form.get(
            "appointment_time"
        )

        appointment = Appointment(
            patient_id=request.form.get("patient_id"),
            doctor_id=request.form.get("doctor_id"),
            appointment_date=datetime.strptime(
                appointment_date,
                "%Y-%m-%d"
            ).date(),
            appointment_time=datetime.strptime(
                appointment_time,
                "%H:%M"
            ).time(),
            reason=request.form.get("reason"),
            status=request.form.get("status") or "Scheduled"
        )

        db.session.add(appointment)
        db.session.commit()

        flash(
            "Appointment scheduled successfully.",
            "success"
        )

        return redirect(
            url_for("appointment.appointment_list")
        )

    return render_template(
        "add_appointment.html",
        patients=patients,
        doctors=doctors
    )


# ==================== APPOINTMENT DETAILS ====================

@appointment_bp.route("/<int:appointment_id>")
@role_required("admin", "reception", "doctor")
def appointment_details(appointment_id):

    appointment = Appointment.query.get_or_404(
        appointment_id
    )

    patient = Patient.query.get(
        appointment.patient_id
    )

    doctor = Doctor.query.get(
        appointment.doctor_id
    )

    return render_template(
        "appointment_details.html",
        appointment=appointment,
        patient=patient,
        doctor=doctor
    )


# ==================== EDIT APPOINTMENT ====================

@appointment_bp.route(
    "/<int:appointment_id>/edit",
    methods=["GET", "POST"]
)
@role_required("admin", "reception", "doctor")
def edit_appointment(appointment_id):

    appointment = Appointment.query.get_or_404(
        appointment_id
    )

    patients = Patient.query.order_by(
        Patient.name.asc()
    ).all()

    doctors = Doctor.query.order_by(
        Doctor.name.asc()
    ).all()

    if request.method == "POST":

        appointment.appointment_date = datetime.strptime(
            request.form.get("appointment_date"),
            "%Y-%m-%d"
        ).date()

        appointment.appointment_time = datetime.strptime(
            request.form.get("appointment_time"),
            "%H:%M"
        ).time()

        appointment.patient_id = request.form.get(
            "patient_id"
        )

        appointment.doctor_id = request.form.get(
            "doctor_id"
        )

        appointment.reason = request.form.get(
            "reason"
        )

        appointment.status = request.form.get(
            "status"
        )

        db.session.commit()

        flash(
            "Appointment updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "appointment.appointment_details",
                appointment_id=appointment.id
            )
        )

    return render_template(
        "edit_appointment.html",
        appointment=appointment,
        patients=patients,
        doctors=doctors
    )


# ==================== DELETE APPOINTMENT ====================

@appointment_bp.route(
    "/<int:appointment_id>/delete",
    methods=["POST"]
)
@role_required("admin", "reception", "doctor")
def delete_appointment(appointment_id):

    appointment = Appointment.query.get_or_404(
        appointment_id
    )

    db.session.delete(appointment)
    db.session.commit()

    flash(
        "Appointment deleted successfully.",
        "success"
    )

    return redirect(
        url_for("appointment.appointment_list")
    )