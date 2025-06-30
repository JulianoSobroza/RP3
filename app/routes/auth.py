from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService, token_required, get_current_user
from app.services.llm_log_service import LLMLogService
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
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