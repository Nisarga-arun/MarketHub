"""
Staff routes: dashboard, store details, products, orders.
Only users with role "staff" can access. Staff see only their assigned store's data.
"""
import os
from decimal import Decimal
from uuid import uuid4

from flask import current_app, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from extensions import db
from models import Category, Order, OrderItem, Product, StoreStaff
from utils.role_helpers import role_required


def allowed_file(filename):
    """Check if file extension is allowed for upload."""
    if not filename or "." not in filename:
        return False
    return filename.rsplit(".", 1)[-1].lower() in current_app.config.get("ALLOWED_EXTENSIONS", set())


def save_product_image(file):
    """Save uploaded file to static/uploads/products/. Returns relative path or None."""
    if not file or not allowed_file(file.filename):
        return None
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    ext = file.filename.rsplit(".", 1)[-1].lower()
    filename = "{}.{}".format(uuid4().hex, ext)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    return os.path.join("uploads", "products", filename).replace("\\", "/")


def get_staff_store():
    """Return the (store, store_staff) for the current user, or (None, None) if no assignment."""
    user_id = __import__("flask").session.get("user_id")
    if not user_id:
        return None, None
    store_staff = StoreStaff.query.filter_by(user_id=user_id, is_active=True).first()
    if not store_staff:
        return None, None
    return store_staff.store, store_staff


def register_staff_routes(app):
    """Register staff-only routes on the Flask app."""

    @app.route("/staff/dashboard")
    @role_required("staff")
    def staff_dashboard():
        """Staff dashboard with welcome and navigation."""
        store, _ = get_staff_store()
        return render_template("staff/dashboard.html", store=store)

    @app.route("/staff/store")
    @role_required("staff")
    def staff_store_details():
        """View assigned store details."""
        store, _ = get_staff_store()
        if not store:
            flash("You are not assigned to a store. Contact admin.", "error")
            return redirect(url_for("staff_dashboard"))
        return render_template("staff/store_details.html", store=store)

    @app.route("/staff/products")
    @role_required("staff")
    def staff_product_list():
        """View products belonging to the staff's assigned store."""
        store, _ = get_staff_store()
        if not store:
            flash("You are not assigned to a store. Contact admin.", "error")
            return redirect(url_for("staff_dashboard"))
        products = Product.query.filter_by(store_id=store.id).order_by(Product.name).all()
        return render_template("staff/products/product_list.html", store=store, products=products)

    @app.route("/staff/products/add", methods=["GET", "POST"])
    @role_required("staff")
    def staff_product_add():
        """Create a product for the staff's assigned store."""
        store, _ = get_staff_store()
        if not store:
            flash("You are not assigned to a store. Contact admin.", "error")
            return redirect(url_for("staff_dashboard"))
        categories = Category.query.order_by(Category.name).all()
        if request.method == "GET":
            return render_template("staff/products/add_product.html", store=store, categories=categories)
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        try:
            price = Decimal(request.form.get("price", "0"))
        except Exception:
            price = Decimal("0")
        try:
            quantity = int(request.form.get("quantity", "0"))
        except Exception:
            quantity = 0
        category_id = request.form.get("category_id") or None
        if category_id:
            try:
                category_id = int(category_id)
                if not Category.query.get(category_id):
                    category_id = None
            except Exception:
                category_id = None
        if not name:
            flash("Product name is required.", "error")
            return render_template("staff/products/add_product.html", store=store, categories=categories)
        image_path = save_product_image(request.files.get("image"))
        product = Product(
            store_id=store.id,
            category_id=category_id,
            name=name,
            description=description or None,
            price=price,
            quantity=max(0, quantity),
            image_path=image_path,
        )
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully.", "success")
        return redirect(url_for("staff_product_list"))

    @app.route("/staff/products/<int:product_id>")
    @role_required("staff")
    def staff_product_view(product_id):
        """View a product (must belong to staff's store)."""
        store, _ = get_staff_store()
        if not store:
            flash("You are not assigned to a store. Contact admin.", "error")
            return redirect(url_for("staff_dashboard"))
        product = Product.query.get_or_404(product_id)
        if product.store_id != store.id:
            flash("You cannot view this product.", "error")
            return redirect(url_for("staff_product_list"))
        return render_template("staff/products/view_product.html", store=store, product=product)

    @app.route("/staff/products/<int:product_id>/edit", methods=["GET", "POST"])
    @role_required("staff")
    def staff_product_edit(product_id):
        """Edit a product (must belong to staff's store)."""
        store, _ = get_staff_store()
        if not store:
            flash("You are not assigned to a store. Contact admin.", "error")
            return redirect(url_for("staff_dashboard"))
        product = Product.query.get_or_404(product_id)
        if product.store_id != store.id:
            flash("You cannot edit this product.", "error")
            return redirect(url_for("staff_product_list"))
        categories = Category.query.order_by(Category.name).all()
        if request.method == "GET":
            return render_template("staff/products/edit_product.html", store=store, product=product, categories=categories)
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        try:
            price = Decimal(request.form.get("price", "0"))
        except Exception:
            price = product.price
        try:
            quantity = int(request.form.get("quantity", "0"))
        except Exception:
            quantity = product.quantity
        category_id = request.form.get("category_id") or None
        if category_id:
            try:
                category_id = int(category_id)
                if not Category.query.get(category_id):
                    category_id = None
            except Exception:
                category_id = None
        if not name:
            flash("Product name is required.", "error")
            return render_template("staff/products/edit_product.html", store=store, product=product, categories=categories)
        new_image = save_product_image(request.files.get("image"))
        product.name = name
        product.description = description or None
        product.price = price
        product.quantity = max(0, quantity)
        product.category_id = category_id
        if new_image:
            product.image_path = new_image
        db.session.commit()
        flash("Product updated successfully.", "success")
        return redirect(url_for("staff_product_view", product_id=product.id))

    # Staff order management: view orders with store products only, update status (forward only)
    STATUS_FLOW = ("placed", "packed", "shipped", "delivered")
    STATUS_CANCELLED = "cancelled"

    def _get_allowed_next_statuses(current_status):
        """Return statuses that are valid next steps. Forward only, or Cancelled."""
        if current_status == STATUS_CANCELLED or current_status == "delivered":
            return []
        idx = STATUS_FLOW.index(current_status) if current_status in STATUS_FLOW else -1
        allowed = []
        if idx >= 0 and idx < len(STATUS_FLOW) - 1:
            allowed.append(STATUS_FLOW[idx + 1])
        if current_status in STATUS_FLOW:
            allowed.append(STATUS_CANCELLED)
        return allowed

    @app.route("/staff/orders")
    @role_required("staff")
    def staff_order_list():
        """List orders that contain products from the staff's store."""
        store, _ = get_staff_store()
        if not store:
            flash("You are not assigned to a store. Contact admin.", "error")
            return redirect(url_for("staff_dashboard"))
        order_ids = (
            db.session.query(OrderItem.order_id)
            .join(Product)
            .filter(Product.store_id == store.id)
            .distinct()
            .all()
        )
        order_ids = [r[0] for r in order_ids]
        if not order_ids:
            orders = []
        else:
            orders = (
                Order.query.options(db.joinedload(Order.user), db.joinedload(Order.items))
                .filter(Order.id.in_(order_ids))
                .order_by(Order.created_at.desc())
                .all()
            )
        order_totals = {o.id: sum((oi.price * oi.quantity) for oi in o.items) for o in orders}
        return render_template(
            "staff/orders/order_list.html",
            store=store,
            orders=orders,
            order_totals=order_totals,
        )

    @app.route("/staff/orders/<int:order_id>")
    @role_required("staff")
    def staff_order_details(order_id):
        """View order details (items from staff's store)."""
        store, _ = get_staff_store()
        if not store:
            flash("You are not assigned to a store. Contact admin.", "error")
            return redirect(url_for("staff_dashboard"))
        order = (
            Order.query.options(
                db.joinedload(Order.user),
                db.joinedload(Order.items).joinedload(OrderItem.product).joinedload(Product.store),
            )
            .get_or_404(order_id)
        )
        store_product_ids = {p.id for p in store.products}
        order_items = [oi for oi in order.items if oi.product_id in store_product_ids]
        if not order_items:
            flash("This order has no items from your store.", "error")
            return redirect(url_for("staff_order_list"))
        items_total = sum((oi.price * oi.quantity) for oi in order_items)
        return render_template(
            "staff/orders/order_details.html",
            store=store,
            order=order,
            order_items=order_items,
            items_total=items_total,
        )

    @app.route("/staff/orders/<int:order_id>/update-status", methods=["GET", "POST"])
    @role_required("staff")
    def staff_order_update_status(order_id):
        """Update order status. Forward only: Placed→Packed→Shipped→Delivered, or Cancelled."""
        store, _ = get_staff_store()
        if not store:
            flash("You are not assigned to a store. Contact admin.", "error")
            return redirect(url_for("staff_dashboard"))
        order = Order.query.get_or_404(order_id)
        store_product_ids = {p.id for p in store.products}
        order_product_ids = {oi.product_id for oi in order.items}
        if not (store_product_ids & order_product_ids):
            flash("This order has no items from your store.", "error")
            return redirect(url_for("staff_order_list"))
        allowed_statuses = _get_allowed_next_statuses(order.status)
        if request.method == "POST":
            new_status = (request.form.get("status") or "").strip().lower()
            if new_status in allowed_statuses:
                order.status = new_status
                db.session.commit()
                flash("Order status updated to {}.".format(new_status.capitalize()), "success")
                return redirect(url_for("staff_order_details", order_id=order_id))
            flash("Invalid status transition. Status cannot move backward.", "error")
        return render_template(
            "staff/orders/update_status.html",
            store=store,
            order=order,
            allowed_statuses=allowed_statuses,
        )
