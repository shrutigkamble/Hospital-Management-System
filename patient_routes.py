from flask import Blueprint, render_template, request, redirect, url_for, flash
from auth_utils import role_required

from extensions import db
from models.patient import Patient


patient_bp = Blueprint(
    "patient",
    __name__,
    url_prefix="/patients"
)


# ==================== PATIENT LIST / SEARCH ====================

@patient_bp.route("/")
@role_required("admin", "reception")
def patient_list():

    search = request.args.get("search", "").strip()

    if search:

        patients = Patient.query.filter(
            db.or_(
                Patient.name.ilike(f"%{search}%"),
                Patient.patient_code.ilike(f"%{search}%"),
                Patient.phone.ilike(f"%{search}%")
            )
        ).order_by(
            Patient.id.desc()
        ).all()

    else:

        patients = Patient.query.order_by(
            Patient.id.desc()
        ).all()

    return render_template(
        "patients.html",
        patients=patients,
        search=search
    )


# ==================== ADD PATIENT ====================

@patient_bp.route("/add", methods=["GET", "POST"])
@role_required("admin", "reception")
def add_patient():

    if request.method == "POST":

        last_patient = Patient.query.order_by(
            Patient.id.desc()
        ).first()

        if last_patient:
            next_number = last_patient.id + 1
        else:
            next_number = 1

        patient_code = f"P{next_number:04d}"

        patient = Patient(
            patient_code=patient_code,
            name=request.form.get("name"),
            age=request.form.get("age"),
            gender=request.form.get("gender"),
            phone=request.form.get("phone"),
            email=request.form.get("email"),
            address=request.form.get("address"),
            blood_group=request.form.get("blood_group"),
            allergies=request.form.get("allergies"),
            medical_history=request.form.get("medical_history")
        )

        db.session.add(patient)
        db.session.commit()

        flash(
            "Patient registered successfully.",
            "success"
        )

        return redirect(
            url_for("patient.patient_list")
        )

    return render_template(
        "add_patient.html"
    )


# ==================== PATIENT DETAILS ====================

@patient_bp.route("/<int:patient_id>")
@role_required("admin", "reception")
def patient_details(patient_id):

    patient = Patient.query.get_or_404(
        patient_id
    )

    return render_template(
        "patient_details.html",
        patient=patient
    )


# ==================== EDIT PATIENT ====================

@patient_bp.route(
    "/<int:patient_id>/edit",
    methods=["GET", "POST"]
)
@role_required("admin", "reception")
def edit_patient(patient_id):

    patient = Patient.query.get_or_404(
        patient_id
    )

    if request.method == "POST":

        patient.name = request.form.get("name")
        patient.age = request.form.get("age")
        patient.gender = request.form.get("gender")
        patient.phone = request.form.get("phone")
        patient.email = request.form.get("email")
        patient.address = request.form.get("address")
        patient.blood_group = request.form.get("blood_group")
        patient.allergies = request.form.get("allergies")
        patient.medical_history = request.form.get(
            "medical_history"
        )

        db.session.commit()

        flash(
            "Patient updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "patient.patient_details",
                patient_id=patient.id
            )
        )

    return render_template(
        "edit_patient.html",
        patient=patient
    )


# ==================== DELETE PATIENT ====================

@patient_bp.route(
    "/<int:patient_id>/delete",
    methods=["POST"]
)
@role_required("admin", "reception")
def delete_patient(patient_id):

    patient = Patient.query.get_or_404(
        patient_id
    )

    db.session.delete(patient)
    db.session.commit()

    flash(
        "Patient deleted successfully.",
        "success"
    )

    return redirect(
        url_for("patient.patient_list")
    )