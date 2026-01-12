"""
Authentication Blueprint
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db
from app.models.user import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__, template_folder='../../templates/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash('계정이 비활성화되었습니다. (Account is deactivated)', 'danger')
                return redirect(url_for('auth.login'))

            # Update login info
            user.last_login = datetime.utcnow()
            user.login_count += 1
            user.failed_login_attempts = 0
            db.session.commit()

            login_user(user, remember=remember)
            flash('로그인 성공! (Login successful!)', 'success')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
        else:
            if user:
                user.failed_login_attempts += 1
                db.session.commit()

            flash('잘못된 사용자명 또는 비밀번호입니다. (Invalid username or password)', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('로그아웃되었습니다. (Logged out successfully)', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        full_name = request.form.get('full_name')

        # Validation
        if password != password_confirm:
            flash('비밀번호가 일치하지 않습니다. (Passwords do not match)', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash('이미 존재하는 사용자명입니다. (Username already exists)', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('이미 존재하는 이메일입니다. (Email already exists)', 'danger')
            return redirect(url_for('auth.register'))

        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=full_name
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('회원가입이 완료되었습니다! 로그인해주세요. (Registration successful! Please login)', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('profile.html')


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password"""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_user.check_password(current_password):
            flash('현재 비밀번호가 올바르지 않습니다. (Current password is incorrect)', 'danger')
            return redirect(url_for('auth.change_password'))

        if new_password != confirm_password:
            flash('새 비밀번호가 일치하지 않습니다. (New passwords do not match)', 'danger')
            return redirect(url_for('auth.change_password'))

        current_user.set_password(new_password)
        db.session.commit()

        flash('비밀번호가 변경되었습니다. (Password changed successfully)', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('change_password.html')
