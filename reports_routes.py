from flask import Blueprint, render_template, request
from auth_utils import role_required

from extensions import db
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.laboratory import LaboratoryTest
from models.billing import Bill
from models.staff import Staff


reports_bp = Blueprint(
    "reports",
    __name__,
    url_prefix="/reports"
)


@reports_bp.route("/")
@role_required("admin")
def reports_dashboard():

    report_type = request.args.get(
        "type",
        "overview"
    )

    data = {}

    # ==================== OVERVIEW ====================

    if report_type == "overview":

        data["total_patients"] = Patient.query.count()

        data["total_doctors"] = Doctor.query.count()

        data["total_appointments"] = Appointment.query.count()

        data["total_staff"] = Staff.query.count()

        data["total_lab_tests"] = LaboratoryTest.query.count()

        data["total_bills"] = Bill.query.count()

        data["total_revenue"] = db.session.query(
            db.func.coalesce(
                db.func.sum(Bill.total_amount),
                0
            )
        ).scalar()


    # ==================== PATIENT REPORT ====================

    elif report_type == "patients":

        data["patients"] = Patient.query.order_by(
            Patient.id.desc()
        ).all()


    # ==================== APPOINTMENT REPORT ====================

    elif report_type == "appointments":

        data["appointments"] = Appointment.query.order_by(
            Appointment.appointment_date.desc(),
            Appointment.appointment_time.desc()
        ).all()


    # ==================== LABORATORY REPORT ====================

    elif report_type == "laboratory":

        data["tests"] = LaboratoryTest.query.order_by(
            LaboratoryTest.id.desc()
        ).all()


    # ==================== BILLING REPORT ====================

    elif report_type == "billing":

        data["bills"] = Bill.query.order_by(
            Bill.id.desc()
        ).all()

        data["total_revenue"] = db.session.query(
            db.func.coalesce(
                db.func.sum(Bill.total_amount),
                0
            )
        ).scalar()


    # ==================== STAFF REPORT ====================

    elif report_type == "staff":

        data["staff_members"] = Staff.query.order_by(
            Staff.id.desc()
        ).all()


    return render_template(
        "reports.html",
        report_type=report_type,
        data=data
    )