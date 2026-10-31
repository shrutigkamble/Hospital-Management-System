from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from auth_utils import role_required

from extensions import db
from models.staff import Staff


staff_bp = Blueprint(
    "staff",
    __name__,
    url_prefix="/staff"
)


# ==================== STAFF LIST / SEARCH ====================

@staff_bp.route("/")
@role_required("admin", "staff")
def staff_list():

    search = request.args.get("search", "").strip()

    query = Staff.query

    if search:

        query = query.filter(
            db.or_(
                Staff.name.ilike(f"%{search}%"),
                Staff.role.ilike(f"%{search}%"),
                Staff.department.ilike(f"%{search}%"),
                Staff.phone.ilike(f"%{search}%")
            )
        )

    staff_members = query.order_by(
        Staff.id.desc()
    ).all()

    return render_template(
        "staff.html",
        staff_members=staff_members,
        search=search
    )


# ==================== ADD STAFF ====================

@staff_bp.route("/add", methods=["GET", "POST"])
@role_required("admin", "staff")
def add_staff():

    if request.method == "POST":

        joining_date = request.form.get(
            "joining_date"
        )

        staff = Staff(
            name=request.form.get("name"),
            role=request.form.get("role"),
            department=request.form.get("department"),
            phone=request.form.get("phone"),
            email=request.form.get("email"),
            address=request.form.get("address"),
            salary=float(
                request.form.get("salary") or 0
            ),
            joining_date=datetime.strptime(
                joining_date,
                "%Y-%m-%d"
            ).date() if joining_date else None,
            status=request.form.get("status") or "Active"
        )

        db.session.add(staff)
        db.session.commit()

        flash(
            "Staff member added successfully.",
            "success"
        )

        return redirect(
            url_for("staff.staff_list")
        )

    return render_template(
        "add_staff.html"
    )


# ==================== STAFF DETAILS ====================

@staff_bp.route("/<int:staff_id>")
@role_required("admin", "staff")
def staff_details(staff_id):

    staff = Staff.query.get_or_404(
        staff_id
    )

    return render_template(
        "staff_details.html",
        staff=staff
    )


# ==================== EDIT STAFF ====================

@staff_bp.route(
    "/<int:staff_id>/edit",
    methods=["GET", "POST"]
)
@role_required("admin", "staff")
def edit_staff(staff_id):

    staff = Staff.query.get_or_404(
        staff_id
    )

    if request.method == "POST":

        staff.name = request.form.get(
            "name"
        )

        staff.role = request.form.get(
            "role"
        )

        staff.department = request.form.get(
            "department"
        )

        staff.phone = request.form.get(
            "phone"
        )

        staff.email = request.form.get(
            "email"
        )

        staff.address = request.form.get(
            "address"
        )

        staff.salary = float(
            request.form.get("salary") or 0
        )

        joining_date = request.form.get(
            "joining_date"
        )

        staff.joining_date = (
            datetime.strptime(
                joining_date,
                "%Y-%m-%d"
            ).date()
            if joining_date
            else None
        )

        staff.status = request.form.get(
            "status"
        )

        db.session.commit()

        flash(
            "Staff member updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "staff.staff_details",
                staff_id=staff.id
            )
        )

    return render_template(
        "edit_staff.html",
        staff=staff
    )


# ==================== DELETE STAFF ====================

@staff_bp.route(
    "/<int:staff_id>/delete",
    methods=["POST"]
)
@role_required("admin", "staff")
def delete_staff(staff_id):

    staff = Staff.query.get_or_404(
        staff_id
    )

    db.session.delete(staff)
    db.session.commit()

    flash(
        "Staff member deleted successfully.",
        "success"
    )

    return redirect(
        url_for("staff.staff_list")
    )