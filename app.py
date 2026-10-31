from flask import Flask, redirect, url_for, render_template, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from config import Config
from extensions import db
from auth_utils import role_required


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


# ==================== IMPORT MODELS ====================

from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.medical_record import MedicalRecord
from models.laboratory import LaboratoryTest
from models.billing import Bill
from models.staff import Staff
from reports_routes import reports_bp


# ==================== IMPORT ROUTES ====================

from patient_routes import patient_bp
from doctor_routes import doctor_bp
from appointment_routes import appointment_bp
from medical_record_routes import medical_record_bp
from laboratory_routes import laboratory_bp
from billing_routes import billing_bp
from staff_routes import staff_bp


# ==================== REGISTER BLUEPRINTS ====================

app.register_blueprint(patient_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(medical_record_bp)
app.register_blueprint(laboratory_bp)
app.register_blueprint(billing_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(reports_bp)


# ==================== LOGIN MANAGER ====================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


# ==================== HOME ====================

@app.route("/")
def home():

    return "Hospital Management System is running!"


# ==================== LOGIN ====================

@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        if current_user.role == "admin":
            return redirect(url_for("dashboard"))

        elif current_user.role == "reception":
            return redirect(url_for("patient.patient_list"))

        elif current_user.role == "doctor":
            return redirect(url_for("appointment.appointment_list"))

        elif current_user.role == "laboratory":
            return redirect(url_for("laboratory.laboratory_list"))

        elif current_user.role == "billing":
            return redirect(url_for("billing.billing_list"))

        elif current_user.role == "staff":
            return redirect(url_for("staff.staff_list"))

        else:
            return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password_hash,
            password
        ):

            login_user(user)

            # ==================== ROLE-BASED REDIRECT ====================

            if user.role == "admin":

                return redirect(
                    url_for("dashboard")
                )

            elif user.role == "reception":

                return redirect(
                    url_for("patient.patient_list")
                )

            elif user.role == "doctor":

                return redirect(
                    url_for("appointment.appointment_list")
                )

            elif user.role == "laboratory":

                return redirect(
                    url_for("laboratory.laboratory_list")
                )

            elif user.role == "billing":

                return redirect(
                    url_for("billing.billing_list")
                )

            elif user.role == "staff":

                return redirect(
                    url_for("staff.staff_list")
                )

            else:

                return redirect(
                    url_for("dashboard")
                )

        flash(
            "Invalid username or password.",
            "danger"
        )

    return render_template(
        "login.html"
    )


# ==================== DASHBOARD ====================

@app.route("/dashboard")
@role_required("admin")
def dashboard():

    total_patients = Patient.query.count()

    total_doctors = Doctor.query.count()

    total_appointments = Appointment.query.count()

    total_staff = Staff.query.count()

    total_lab_tests = LaboratoryTest.query.count()

    total_revenue = db.session.query(
        db.func.coalesce(
            db.func.sum(Bill.total_amount),
            0
        )
    ).scalar()

    return render_template(
        "dashboard.html",
        total_patients=total_patients,
        total_doctors=total_doctors,
        total_appointments=total_appointments,
        total_staff=total_staff,
        total_lab_tests=total_lab_tests,
        total_revenue=total_revenue
    )


# ==================== CUSTOM 403 ERROR ====================

@app.errorhandler(403)
def access_denied(error):

    return render_template(
        "403.html"
    ), 403


# ==================== LOGOUT ====================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("login")
    )


# ==================== RUN APPLICATION ====================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(debug=True)