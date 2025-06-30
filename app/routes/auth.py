from flask import Blueprint, render_template, redirect, url_for, request,flash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from app.services import user_services

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')

        if user_services.get_user_by_email(email):
            flash('Email ja cadastrado.', 'danger')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        user_services.create_user(email=email, password=hashed_password, username=username)
        flash('Cadastro realizado com sucesso! Realize o login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = user_services.get_user_by_username(username)

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard.dashboard"))
        flash("Credenciais invalidas", "danger")

    return render_template("login.html")


@login_required
@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('dashboard.index'))