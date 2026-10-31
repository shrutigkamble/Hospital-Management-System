from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from auth_utils import role_required

from extensions import db
from models.laboratory import LaboratoryTest
from models.patient import Patient
from models.doctor import Doctor


laboratory_bp = Blueprint(
    "laboratory",
    __name__,
    url_prefix="/laboratory"
)


# ==================== LABORATORY LIST / SEARCH ====================

@laboratory_bp.route("/")
@role_required("admin", "laboratory")
def laboratory_list():

    search = request.args.get("search", "").strip()

    query = LaboratoryTest.query

    if search:

        query = query.join(
            Patient,
            LaboratoryTest.patient_id == Patient.id
        ).join(
            Doctor,
            LaboratoryTest.doctor_id == Doctor.id,
            isouter=True
        ).filter(
            db.or_(
                Patient.name.ilike(f"%{search}%"),
                LaboratoryTest.test_name.ilike(f"%{search}%"),
                LaboratoryTest.status.ilike(f"%{search}%")
            )
        )

    tests = query.order_by(
        LaboratoryTest.id.desc()
    ).all()

    return render_template(
        "laboratory.html",
        tests=tests,
        search=search
    )


# ==================== ADD LABORATORY TEST ====================

@laboratory_bp.route("/add", methods=["GET", "POST"])
@role_required("admin", "laboratory")
def add_laboratory_test():

    patients = Patient.query.order_by(
        Patient.name.asc()
    ).all()

    doctors = Doctor.query.order_by(
        Doctor.name.asc()
    ).all()

    if request.method == "POST":

        test_date = request.form.get("test_date")

        laboratory_test = LaboratoryTest(
            patient_id=request.form.get("patient_id"),
            doctor_id=request.form.get("doctor_id") or None,
            test_name=request.form.get("test_name"),
            test_date=datetime.strptime(
                test_date,
                "%Y-%m-%d"
            ).date(),
            status=request.form.get("status") or "Requested",
            result=request.form.get("result"),
            report=request.form.get("report"),
            remarks=request.form.get("remarks")
        )

        db.session.add(laboratory_test)
        db.session.commit()

        flash(
            "Laboratory test added successfully.",
            "success"
        )

        return redirect(
            url_for("laboratory.laboratory_list")
        )

    return render_template(
        "add_laboratory.html",
        patients=patients,
        doctors=doctors
    )


# ==================== LABORATORY DETAILS ====================

@laboratory_bp.route("/<int:test_id>")
@role_required("admin", "laboratory")
def laboratory_details(test_id):

    test = LaboratoryTest.query.get_or_404(
        test_id
    )

    patient = Patient.query.get(
        test.patient_id
    )

    doctor = None

    if test.doctor_id:

        doctor = Doctor.query.get(
            test.doctor_id
        )

    return render_template(
        "laboratory_details.html",
        test=test,
        patient=patient,
        doctor=doctor
    )


# ==================== EDIT LABORATORY TEST ====================

@laboratory_bp.route(
    "/<int:test_id>/edit",
    methods=["GET", "POST"]
)
@role_required("admin", "laboratory")
def edit_laboratory_test(test_id):

    test = LaboratoryTest.query.get_or_404(
        test_id
    )

    patients = Patient.query.order_by(
        Patient.name.asc()
    ).all()

    doctors = Doctor.query.order_by(
        Doctor.name.asc()
    ).all()

    if request.method == "POST":

        test.patient_id = request.form.get(
            "patient_id"
        )

        test.doctor_id = request.form.get(
            "doctor_id"
        ) or None

        test.test_name = request.form.get(
            "test_name"
        )

        test.test_date = datetime.strptime(
            request.form.get("test_date"),
            "%Y-%m-%d"
        ).date()

        test.status = request.form.get(
            "status"
        )

        test.result = request.form.get(
            "result"
        )

        test.report = request.form.get(
            "report"
        )

        test.remarks = request.form.get(
            "remarks"
        )

        db.session.commit()

        flash(
            "Laboratory test updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "laboratory.laboratory_details",
                test_id=test.id
            )
        )

    return render_template(
        "edit_laboratory.html",
        test=test,
        patients=patients,
        doctors=doctors
    )


# ==================== DELETE LABORATORY TEST ====================

@laboratory_bp.route(
    "/<int:test_id>/delete",
    methods=["POST"]
)
@role_required("admin", "laboratory")
def delete_laboratory_test(test_id):

    test = LaboratoryTest.query.get_or_404(
        test_id
    )

    db.session.delete(test)
    db.session.commit()

    flash(
        "Laboratory test deleted successfully.",
        "success"
    )

    return redirect(
        url_for("laboratory.laboratory_list")
    )