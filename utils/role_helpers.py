"""
Role helper utilities for session-based role identification.
"""
from functools import wraps

from flask import session, redirect, url_for, flash


def get_current_user_role():
    """Return the current user's role from session, or None if not logged in."""
    return session.get("user_role")


def is_admin():
    """Return True if the current user has admin role."""
    return get_current_user_role() == "admin"


def is_staff():
    """Return True if the current user has staff role."""
    return get_current_user_role() == "staff"


def is_customer():
    """Return True if the current user has customer role."""
    return get_current_user_role() == "customer"


def login_required(f):
    """Decorator: redirect to login if user is not in session."""

    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to access this page.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return wrapped


def role_required(*allowed_roles):
    """Decorator: require user to be logged in and have one of the allowed roles."""

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not session.get("user_id"):
                flash("Please log in to access this page.", "error")
                return redirect(url_for("login"))
            role = get_current_user_role()
            if role not in allowed_roles:
                flash("You do not have permission to access this page.", "error")
                return redirect(url_for("index"))
            return f(*args, **kwargs)

        return wrapped

    return decorator
