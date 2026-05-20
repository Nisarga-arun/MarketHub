"""
Admin routes: dashboard, user management, and category management.
Only users with role "admin" can access these routes.
"""
from flask import flash, redirect, render_template, request, url_for

from extensions import db
from models import Category, Store, StoreStaff, User
from utils.role_helpers import role_required


def register_admin_routes(app):
    """Register admin-only routes on the Flask app."""

    @app.route("/admin/dashboard")
    @role_required("admin")
    def admin_dashboard():
        """Admin dashboard with navigation options."""
        return render_template("admin/dashboard.html")

    @app.route("/admin/users")
    @role_required("admin")
    def admin_users_list():
        """View all users in the system."""
        users = User.query.order_by(User.created_at.desc()).all()
        return render_template("admin/users_list.html", users=users)

    @app.route("/admin/staff")
    @role_required("admin")
    def admin_staff_list():
        """View all users with role staff."""
        staff = User.query.filter_by(role="staff").order_by(User.created_at.desc()).all()
        return render_template("admin/staff_list.html", staff=staff)

    @app.route("/admin/customers")
    @role_required("admin")
    def admin_customers_list():
        """View all users with role customer."""
        customers = User.query.filter_by(role="customer").order_by(User.created_at.desc()).all()
        return render_template("admin/customers_list.html", customers=customers)

    # Category management
    @app.route("/admin/categories")
    @role_required("admin")
    def admin_category_list():
        """List all categories."""
        categories = Category.query.order_by(Category.name).all()
        return render_template("admin/categories/category_list.html", categories=categories)

    @app.route("/admin/categories/add", methods=["GET", "POST"])
    @role_required("admin")
    def admin_category_add():
        """Add a new category."""
        if request.method == "GET":
            return render_template("admin/categories/add_category.html")
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        if not name:
            flash("Category name is required.", "error")
            return render_template("admin/categories/add_category.html", name=name, description=description)
        if Category.query.filter_by(name=name).first():
            flash("A category with this name already exists.", "error")
            return render_template("admin/categories/add_category.html", name=name, description=description)
        category = Category(name=name, description=description or None)
        db.session.add(category)
        db.session.commit()
        flash("Category added successfully.", "success")
        return redirect(url_for("admin_category_list"))

    @app.route("/admin/categories/<int:category_id>")
    @role_required("admin")
    def admin_category_view(category_id):
        """View a single category."""
        category = Category.query.get_or_404(category_id)
        return render_template("admin/categories/view_category.html", category=category)

    @app.route("/admin/categories/<int:category_id>/edit", methods=["GET", "POST"])
    @role_required("admin")
    def admin_category_edit(category_id):
        """Edit a category."""
        category = Category.query.get_or_404(category_id)
        if request.method == "GET":
            return render_template("admin/categories/edit_category.html", category=category)
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        if not name:
            flash("Category name is required.", "error")
            return render_template("admin/categories/edit_category.html", category=category, name=name, description=description)
        existing = Category.query.filter_by(name=name).first()
        if existing and existing.id != category_id:
            flash("A category with this name already exists.", "error")
            return render_template("admin/categories/edit_category.html", category=category, name=name, description=description)
        category.name = name
        category.description = description or None
        db.session.commit()
        flash("Category updated successfully.", "success")
        return redirect(url_for("admin_category_view", category_id=category.id))

    # Store management
    @app.route("/admin/stores")
    @role_required("admin")
    def admin_store_list():
        """List all stores."""
        stores = Store.query.order_by(Store.name).all()
        return render_template("admin/stores/store_list.html", stores=stores)

    @app.route("/admin/stores/add", methods=["GET", "POST"])
    @role_required("admin")
    def admin_store_add():
        """Add a new store."""
        if request.method == "GET":
            return render_template("admin/stores/add_store.html")
        name = request.form.get("name", "").strip()
        location = request.form.get("location", "").strip()
        if not name:
            flash("Store name is required.", "error")
            return render_template("admin/stores/add_store.html", name=name, location=location)
        store = Store(name=name, location=location or None)
        db.session.add(store)
        db.session.commit()
        flash("Store added successfully.", "success")
        return redirect(url_for("admin_store_list"))

    @app.route("/admin/stores/<int:store_id>")
    @role_required("admin")
    def admin_store_view(store_id):
        """View a single store."""
        store = Store.query.get_or_404(store_id)
        return render_template("admin/stores/view_store.html", store=store)

    @app.route("/admin/stores/<int:store_id>/edit", methods=["GET", "POST"])
    @role_required("admin")
    def admin_store_edit(store_id):
        """Edit a store."""
        store = Store.query.get_or_404(store_id)
        if request.method == "GET":
            return render_template("admin/stores/edit_store.html", store=store)
        name = request.form.get("name", "").strip()
        location = request.form.get("location", "").strip()
        if not name:
            flash("Store name is required.", "error")
            return render_template("admin/stores/edit_store.html", store=store)
        store.name = name
        store.location = location or None
        db.session.commit()
        flash("Store updated successfully.", "success")
        return redirect(url_for("admin_store_view", store_id=store.id))

    # Store staff management (StoreStaff: user + store + category access)
    @app.route("/admin/store-staff")
    @role_required("admin")
    def admin_store_staff_list():
        """List all store staff assignments."""
        staff_list = StoreStaff.query.order_by(StoreStaff.id.desc()).all()
        return render_template("admin/staff/staff_list.html", staff_list=staff_list)

    @app.route("/admin/store-staff/add", methods=["GET", "POST"])
    @role_required("admin")
    def admin_store_staff_add():
        """Add store staff: create User (staff) + StoreStaff with store and category access."""
        if request.method == "GET":
            stores = Store.query.order_by(Store.name).all()
            categories = Category.query.order_by(Category.name).all()
            return render_template("admin/staff/add_staff.html", stores=stores, categories=categories)
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        store_id = request.form.get("store_id", type=int)
        category_ids = request.form.getlist("category_ids", type=int)
        if not name:
            flash("Name is required.", "error")
            return redirect(url_for("admin_store_staff_add"))
        if not email:
            flash("Email is required.", "error")
            return redirect(url_for("admin_store_staff_add"))
        if not password:
            flash("Password is required.", "error")
            return redirect(url_for("admin_store_staff_add"))
        if password != confirm:
            flash("Passwords do not match.", "error")
            return redirect(url_for("admin_store_staff_add"))
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return redirect(url_for("admin_store_staff_add"))
        if not store_id or not Store.query.get(store_id):
            flash("Please select a store.", "error")
            return redirect(url_for("admin_store_staff_add"))
        if User.query.filter_by(email=email).first():
            flash("A user with this email already exists.", "error")
            return redirect(url_for("admin_store_staff_add"))
        user = User(name=name, email=email, role="staff")
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        store_staff = StoreStaff(user_id=user.id, store_id=store_id, is_active=True)
        db.session.add(store_staff)
        db.session.flush()
        if category_ids:
            for cid in category_ids:
                if Category.query.get(cid):
                    store_staff.categories.append(Category.query.get(cid))
        db.session.commit()
        flash("Store staff added successfully.", "success")
        return redirect(url_for("admin_store_staff_list"))

    @app.route("/admin/store-staff/<int:store_staff_id>")
    @role_required("admin")
    def admin_store_staff_view(store_staff_id):
        """View a store staff record."""
        store_staff = StoreStaff.query.get_or_404(store_staff_id)
        return render_template("admin/staff/view_staff.html", store_staff=store_staff)

    @app.route("/admin/store-staff/<int:store_staff_id>/edit", methods=["GET", "POST"])
    @role_required("admin")
    def admin_store_staff_edit(store_staff_id):
        """Edit store staff (no email/password)."""
        store_staff = StoreStaff.query.get_or_404(store_staff_id)
        if request.method == "GET":
            stores = Store.query.order_by(Store.name).all()
            categories = Category.query.order_by(Category.name).all()
            return render_template("admin/staff/edit_staff.html", store_staff=store_staff, stores=stores, categories=categories)
        name = request.form.get("name", "").strip()
        store_id = request.form.get("store_id", type=int)
        category_ids = request.form.getlist("category_ids", type=int)
        is_active = request.form.get("is_active") == "1"
        if not name:
            flash("Name is required.", "error")
            return redirect(url_for("admin_store_staff_edit", store_staff_id=store_staff_id))
        if not store_id or not Store.query.get(store_id):
            flash("Please select a store.", "error")
            return redirect(url_for("admin_store_staff_edit", store_staff_id=store_staff_id))
        store_staff.user.name = name
        store_staff.store_id = store_id
        store_staff.is_active = is_active
        store_staff.categories = []
        if category_ids:
            for cid in category_ids:
                cat = Category.query.get(cid)
                if cat:
                    store_staff.categories.append(cat)
        db.session.commit()
        flash("Store staff updated successfully.", "success")
        return redirect(url_for("admin_store_staff_view", store_staff_id=store_staff.id))

    @app.route("/admin/store-staff/<int:store_staff_id>/toggle-active", methods=["POST"])
    @role_required("admin")
    def admin_store_staff_toggle_active(store_staff_id):
        """Activate or deactivate store staff."""
        store_staff = StoreStaff.query.get_or_404(store_staff_id)
        store_staff.is_active = not store_staff.is_active
        db.session.commit()
        status = "activated" if store_staff.is_active else "deactivated"
        flash("Staff {} successfully.".format(status), "success")
        return redirect(url_for("admin_store_staff_list"))
