from flask import Blueprint, render_template, request, redirect, url_for, flash
from auth_utils import role_required

from extensions import db
from models.doctor import Doctor


doctor_bp = Blueprint(
    "doctor",
    __name__,
    url_prefix="/doctors"
)


# ==================== DOCTOR LIST / SEARCH ====================

@doctor_bp.route("/")
@role_required("admin")
def doctor_list():

    search = request.args.get("search", "").strip()

    if search:

        doctors = Doctor.query.filter(
            db.or_(
                Doctor.name.ilike(f"%{search}%"),
                Doctor.specialization.ilike(f"%{search}%"),
                Doctor.phone.ilike(f"%{search}%")
            )
        ).order_by(
            Doctor.id.desc()
        ).all()

    else:

        doctors = Doctor.query.order_by(
            Doctor.id.desc()
        ).all()

    return render_template(
        "doctors.html",
        doctors=doctors,
        search=search
    )


# ==================== ADD DOCTOR ====================

@doctor_bp.route("/add", methods=["GET", "POST"])
@role_required("admin")
def add_doctor():

    if request.method == "POST":

        doctor = Doctor(
            name=request.form.get("name"),
            specialization=request.form.get("specialization"),
            phone=request.form.get("phone"),
            email=request.form.get("email"),
            consultation_fee=request.form.get("consultation_fee"),
            availability=request.form.get("availability")
        )

        db.session.add(doctor)
        db.session.commit()

        flash(
            "Doctor registered successfully.",
            "success"
        )

        return redirect(
            url_for("doctor.doctor_list")
        )

    return render_template(
        "add_doctor.html"
    )


# ==================== DOCTOR DETAILS ====================

@doctor_bp.route("/<int:doctor_id>")
@role_required("admin")
def doctor_details(doctor_id):

    doctor = Doctor.query.get_or_404(
        doctor_id
    )

    return render_template(
        "doctor_details.html",
        doctor=doctor
    )


# ==================== EDIT DOCTOR ====================

@doctor_bp.route(
    "/<int:doctor_id>/edit",
    methods=["GET", "POST"]
)
@role_required("admin")
def edit_doctor(doctor_id):

    doctor = Doctor.query.get_or_404(
        doctor_id
    )

    if request.method == "POST":

        doctor.name = request.form.get("name")
        doctor.specialization = request.form.get("specialization")
        doctor.phone = request.form.get("phone")
        doctor.email = request.form.get("email")
        doctor.consultation_fee = request.form.get(
            "consultation_fee"
        )
        doctor.availability = request.form.get(
            "availability"
        )

        db.session.commit()

        flash(
            "Doctor updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "doctor.doctor_details",
                doctor_id=doctor.id
            )
        )

    return render_template(
        "edit_doctor.html",
        doctor=doctor
    )


# ==================== DELETE DOCTOR ====================

@doctor_bp.route(
    "/<int:doctor_id>/delete",
    methods=["POST"]
)
@role_required("admin")
def delete_doctor(doctor_id):

    doctor = Doctor.query.get_or_404(
        doctor_id
    )

    db.session.delete(doctor)
    db.session.commit()

    flash(
        "Doctor deleted successfully.",
        "success"
    )

    return redirect(
        url_for("doctor.doctor_list")
    )