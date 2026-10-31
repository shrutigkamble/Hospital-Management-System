from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from auth_utils import role_required

from extensions import db
from models.billing import Bill
from models.patient import Patient


billing_bp = Blueprint(
    "billing",
    __name__,
    url_prefix="/billing"
)


# ==================== BILLING LIST / SEARCH ====================

@billing_bp.route("/")
@role_required("admin", "billing")
def billing_list():

    search = request.args.get("search", "").strip()

    query = Bill.query

    if search:

        query = query.join(
            Patient,
            Bill.patient_id == Patient.id
        ).filter(
            db.or_(
                Patient.name.ilike(f"%{search}%"),
                Patient.patient_code.ilike(f"%{search}%"),
                Bill.payment_status.ilike(f"%{search}%")
            )
        )

    bills = query.order_by(
        Bill.id.desc()
    ).all()

    return render_template(
        "billing.html",
        bills=bills,
        search=search
    )


# ==================== ADD BILL ====================

@billing_bp.route("/add", methods=["GET", "POST"])
@role_required("admin", "billing")
def add_bill():

    patients = Patient.query.order_by(
        Patient.name.asc()
    ).all()

    if request.method == "POST":

        bill_date = request.form.get(
            "bill_date"
        )

        consultation_charge = float(
            request.form.get("consultation_charge") or 0
        )

        laboratory_charge = float(
            request.form.get("laboratory_charge") or 0
        )

        pharmacy_charge = float(
            request.form.get("pharmacy_charge") or 0
        )

        room_charge = float(
            request.form.get("room_charge") or 0
        )

        other_charge = float(
            request.form.get("other_charge") or 0
        )

        total_amount = (
            consultation_charge
            + laboratory_charge
            + pharmacy_charge
            + room_charge
            + other_charge
        )

        bill = Bill(
            patient_id=request.form.get("patient_id"),
            bill_date=datetime.strptime(
                bill_date,
                "%Y-%m-%d"
            ).date(),
            consultation_charge=consultation_charge,
            laboratory_charge=laboratory_charge,
            pharmacy_charge=pharmacy_charge,
            room_charge=room_charge,
            other_charge=other_charge,
            total_amount=total_amount,
            payment_status=request.form.get(
                "payment_status"
            ) or "Pending",
            payment_method=request.form.get(
                "payment_method"
            ),
            notes=request.form.get(
                "notes"
            )
        )

        db.session.add(bill)
        db.session.commit()

        flash(
            "Bill created successfully.",
            "success"
        )

        return redirect(
            url_for("billing.billing_list")
        )

    return render_template(
        "add_bill.html",
        patients=patients
    )


# ==================== BILL DETAILS ====================

@billing_bp.route("/<int:bill_id>")
@role_required("admin", "billing")
def bill_details(bill_id):

    bill = Bill.query.get_or_404(
        bill_id
    )

    patient = Patient.query.get(
        bill.patient_id
    )

    return render_template(
        "bill_details.html",
        bill=bill,
        patient=patient
    )


# ==================== EDIT BILL ====================

@billing_bp.route(
    "/<int:bill_id>/edit",
    methods=["GET", "POST"]
)
@role_required("admin", "billing")
def edit_bill(bill_id):

    bill = Bill.query.get_or_404(
        bill_id
    )

    patients = Patient.query.order_by(
        Patient.name.asc()
    ).all()

    if request.method == "POST":

        bill.patient_id = request.form.get(
            "patient_id"
        )

        bill.bill_date = datetime.strptime(
            request.form.get("bill_date"),
            "%Y-%m-%d"
        ).date()

        bill.consultation_charge = float(
            request.form.get("consultation_charge") or 0
        )

        bill.laboratory_charge = float(
            request.form.get("laboratory_charge") or 0
        )

        bill.pharmacy_charge = float(
            request.form.get("pharmacy_charge") or 0
        )

        bill.room_charge = float(
            request.form.get("room_charge") or 0
        )

        bill.other_charge = float(
            request.form.get("other_charge") or 0
        )

        bill.total_amount = (
            bill.consultation_charge
            + bill.laboratory_charge
            + bill.pharmacy_charge
            + bill.room_charge
            + bill.other_charge
        )

        bill.payment_status = request.form.get(
            "payment_status"
        )

        bill.payment_method = request.form.get(
            "payment_method"
        )

        bill.notes = request.form.get(
            "notes"
        )

        db.session.commit()

        flash(
            "Bill updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "billing.bill_details",
                bill_id=bill.id
            )
        )

    return render_template(
        "edit_bill.html",
        bill=bill,
        patients=patients
    )


# ==================== DELETE BILL ====================

@billing_bp.route(
    "/<int:bill_id>/delete",
    methods=["POST"]
)
@role_required("admin", "billing")
def delete_bill(bill_id):

    bill = Bill.query.get_or_404(
        bill_id
    )

    db.session.delete(bill)
    db.session.commit()

    flash(
        "Bill deleted successfully.",
        "success"
    )

    return redirect(
        url_for("billing.billing_list")
    )