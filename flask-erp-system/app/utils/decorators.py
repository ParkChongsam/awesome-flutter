"""
Custom decorators for access control
"""
from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('로그인이 필요합니다. (Login required)', 'warning')
            return redirect(url_for('auth.login'))

        if not current_user.has_role('admin'):
            flash('관리자 권한이 필요합니다. (Admin access required)', 'danger')
            abort(403)

        return f(*args, **kwargs)

    return decorated_function


def manager_required(f):
    """Decorator to require manager or admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('로그인이 필요합니다. (Login required)', 'warning')
            return redirect(url_for('auth.login'))

        if not (current_user.has_role('admin') or current_user.has_role('manager')):
            flash('관리자 또는 매니저 권한이 필요합니다. (Manager access required)', 'danger')
            abort(403)

        return f(*args, **kwargs)

    return decorated_function


def role_required(role_name):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('로그인이 필요합니다. (Login required)', 'warning')
                return redirect(url_for('auth.login'))

            if not current_user.has_role(role_name):
                flash(f'{role_name} 권한이 필요합니다. ({role_name} access required)', 'danger')
                abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator
