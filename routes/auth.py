"""
Authentication routes: register, login, logout.
"""
from flask import flash, redirect, render_template, request, session, url_for

from extensions import db
from models import User


def register_auth_routes(app):
    """Register authentication routes on the Flask app."""

    @app.route("/register", methods=["GET", "POST"])
    def register():
        """User registration."""
        if request.method == "GET":
            return render_template("auth/register.html")

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        # Validate required fields
        if not name:
            flash("Name is required.", "error")
            return render_template("auth/register.html", name=name, email=email)
        if not email:
            flash("Email is required.", "error")
            return render_template("auth/register.html", name=name, email=email)
        if not password:
            flash("Password is required.", "error")
            return render_template("auth/register.html", name=name, email=email)
        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("auth/register.html", name=name, email=email)
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("auth/register.html", name=name, email=email)

        # Prevent duplicate email
        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please login.", "error")
            return render_template("auth/register.html", name=name, email=email)

        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        """User login."""
        if request.method == "GET":
            return render_template("auth/login.html")

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("auth/login.html", email=email)

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid email or password.", "error")
            return render_template("auth/login.html", email=email)

        session.clear()
        session["user_id"] = user.id
        session["user_email"] = user.email
        session["user_name"] = user.name
        session["user_role"] = user.role

        flash("Welcome, {}!".format(user.name), "success")

        # Role-based redirection after login
        if user.role == "admin":
            return redirect(url_for("admin_dashboard"))
        if user.role == "staff":
            return redirect(url_for("staff_dashboard"))
        return redirect(url_for("customer_dashboard"))

    @app.route("/logout")
    def logout():
        """User logout - clear session and redirect to login."""
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for("login"))
