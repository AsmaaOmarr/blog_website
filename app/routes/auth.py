from flask import Blueprint, render_template, redirect, url_for
from flask_injector import inject
from app.services.user import UserService
from flask_login import login_required
from app.forms.auth.login_form import LoginForm
from app.forms.auth.signup_form import SignupForm

from flask import Blueprint
from app import db
import uuid
from app.models.user import User
from werkzeug.security import generate_password_hash



auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
@inject
def login(user_service: UserService):
    login_form = LoginForm()

    error_message = ""

    if login_form.validate_on_submit():
        if user_service.login(login_form.email.data, login_form.password.data):
            return redirect(url_for("user.profile"))

    error_message = "incorrect email or password"

    return render_template("/auth/login.html", form=login_form, error_message=error_message)

@auth.route("/signup", methods=["GET", "POST"])
@inject
def signup(user_service: UserService):
    signup_form = SignupForm()

    if signup_form.validate_on_submit():
        if not user_service.get_by_email(email=signup_form.email.data):
            user_service.signup(
                signup_form.username.data,
                signup_form.email.data,
                signup_form.password.data
            )

        return redirect(url_for("auth.login"))

    return render_template("/auth/signup.html", form=signup_form)


@auth.route('/admin-login', methods=['GET', 'POST'])
@inject
def admin_login(user_service: UserService):
    form = LoginForm()
    error_message=" "
    if form.validate_on_submit():
        if user_service.loginAdmin(form.email.data, form.password.data):
            return redirect(url_for('admin.admin_home'))
        
        error_message = "incorrect email or password"
    
    return render_template("/auth/admin_login.html", form=form, error_message=error_message)



@auth.route("/logout")
@login_required
@inject
def logout(user_service: UserService):
    user_service.logout()
    
    return redirect(url_for("dashboard.home"))

# Create a temporary route
@auth.route('/create-admin', methods=['GET'])
@inject
def create_admin():
    # Generate hashed password
    hashed_password = generate_password_hash('Adminasmaa')
    public_id = str(uuid.uuid4())

    # Create admin user
    admin_user = User(
        public_id=public_id,
        username='admin_asmaa',
        email='admin@example.com',
        password=hashed_password,
        role='admin'
    )

    # Add user to the database
    db.session.add(admin_user)
    db.session.commit()

    return "Admin user created successfully!"