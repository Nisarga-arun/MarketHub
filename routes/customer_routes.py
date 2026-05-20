"""
Customer routes: dashboard, profile, categories, product browsing, cart, and orders.
Only users with role "customer" can access these routes.
"""
from flask import flash, redirect, render_template, request, session, url_for
from sqlalchemy.orm import joinedload

from extensions import db
from models import CartItem, Category, Order, OrderItem, Product, User
from utils.role_helpers import role_required


def register_customer_routes(app):
    """Register customer-only routes on the Flask app."""

    ACTIVE_STATUSES = ("placed", "packed", "shipped")
    DELIVERED_STATUS = "delivered"

    @app.route("/customer/dashboard")
    @role_required("customer")
    def customer_dashboard():
        """Customer dashboard with welcome, navigation, and order summary."""
        user_id = session.get("user_id")
        active_count = (
            Order.query.filter_by(user_id=user_id)
            .filter(Order.status.in_(ACTIVE_STATUSES))
            .count()
        )
        delivered_count = Order.query.filter_by(user_id=user_id, status=DELIVERED_STATUS).count()
        return render_template(
            "customer/dashboard.html",
            active_orders_count=active_count,
            delivered_orders_count=delivered_count,
        )

    @app.route("/customer/profile")
    @role_required("customer")
    def customer_profile():
        """View customer profile details."""
        user_id = session.get("user_id")
        user = User.query.get_or_404(user_id)
        return render_template("customer/profile.html", user=user)

    @app.route("/customer/categories")
    @role_required("customer")
    def customer_category_list():
        """List all product categories (created by admin)."""
        categories = Category.query.order_by(Category.name).all()
        return render_template("customer/category_list.html", categories=categories)

    @app.route("/customer/categories/<int:category_id>/products")
    @role_required("customer")
    def customer_product_list(category_id):
        """View products within a selected category."""
        category = Category.query.get_or_404(category_id)
        products = (
            Product.query.options(joinedload(Product.category), joinedload(Product.store))
            .filter(Product.category_id == category_id)
            .order_by(Product.name)
            .all()
        )
        return render_template(
            "customer/product_list.html",
            category=category,
            products=products,
        )

    @app.route("/customer/products/<int:product_id>")
    @role_required("customer")
    def customer_product_view(product_id):
        """View a single product (read-only) with Add to Cart."""
        product = (
            Product.query.options(joinedload(Product.category), joinedload(Product.store))
            .get_or_404(product_id)
        )
        return render_template("customer/product_view.html", product=product)

    @app.route("/customer/cart")
    @role_required("customer")
    def customer_cart():
        """View cart with products, quantity, price, subtotal."""
        user_id = session.get("user_id")
        items = (
            CartItem.query.filter_by(user_id=user_id)
            .options(joinedload(CartItem.product))
            .order_by(CartItem.id)
            .all()
        )
        total = sum((ci.product.price * ci.quantity) for ci in items)
        return render_template("customer/cart.html", cart_items=items, total=total)

    @app.route("/customer/cart/add", methods=["POST"])
    @role_required("customer")
    def customer_cart_add():
        """Add product to cart."""
        user_id = session.get("user_id")
        try:
            product_id = int(request.form.get("product_id", 0))
        except (TypeError, ValueError):
            flash("Invalid product.", "error")
            return redirect(url_for("customer_category_list"))
        quantity = int(request.form.get("quantity", 1) or 1)
        if quantity < 1:
            flash("Quantity must be at least 1.", "error")
            next_url = request.form.get("next") or url_for("customer_category_list")
            return redirect(next_url)
        product = Product.query.get_or_404(product_id)
        if product.quantity < quantity:
            flash("Not enough stock. Available: {}.".format(product.quantity), "error")
            return redirect(url_for("customer_product_view", product_id=product_id))
        existing = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing:
            new_qty = existing.quantity + quantity
            if product.quantity < new_qty:
                flash("Not enough stock. Available: {}.".format(product.quantity), "error")
                return redirect(url_for("customer_product_view", product_id=product_id))
            existing.quantity = new_qty
        else:
            db.session.add(CartItem(user_id=user_id, product_id=product_id, quantity=quantity))
        db.session.commit()
        flash("Added to cart.", "success")
        next_url = request.form.get("next") or url_for("customer_product_view", product_id=product_id)
        return redirect(next_url)

    @app.route("/customer/cart/update/<int:cart_item_id>", methods=["POST"])
    @role_required("customer")
    def customer_cart_update(cart_item_id):
        """Update cart item quantity."""
        user_id = session.get("user_id")
        item = CartItem.query.filter_by(id=cart_item_id, user_id=user_id).first_or_404()
        try:
            quantity = int(request.form.get("quantity", 1) or 1)
        except (TypeError, ValueError):
            quantity = 1
        if quantity < 1:
            db.session.delete(item)
            db.session.commit()
            flash("Item removed from cart.", "info")
            return redirect(url_for("customer_cart"))
        if item.product.quantity < quantity:
            flash("Not enough stock. Available: {}.".format(item.product.quantity), "error")
            return redirect(url_for("customer_cart"))
        item.quantity = quantity
        db.session.commit()
        flash("Cart updated.", "success")
        return redirect(url_for("customer_cart"))

    @app.route("/customer/cart/remove/<int:cart_item_id>", methods=["POST"])
    @role_required("customer")
    def customer_cart_remove(cart_item_id):
        """Remove product from cart."""
        user_id = session.get("user_id")
        item = CartItem.query.filter_by(id=cart_item_id, user_id=user_id).first_or_404()
        db.session.delete(item)
        db.session.commit()
        flash("Item removed from cart.", "info")
        return redirect(url_for("customer_cart"))

    @app.route("/customer/cart/place-order", methods=["POST"])
    @role_required("customer")
    def customer_cart_place_order():
        """Place order from cart: create order, order items, clear cart."""
        user_id = session.get("user_id")
        items = CartItem.query.filter_by(user_id=user_id).options(joinedload(CartItem.product)).all()
        if not items:
            flash("Your cart is empty.", "error")
            return redirect(url_for("customer_cart"))
        errors = []
        for item in items:
            if item.product.quantity < item.quantity:
                errors.append("{}: only {} available.".format(item.product.name, item.product.quantity))
        if errors:
            flash("Insufficient stock: " + " ".join(errors), "error")
            return redirect(url_for("customer_cart"))
        order = Order(user_id=user_id, status="placed")
        db.session.add(order)
        db.session.flush()
        for item in items:
            db.session.add(
                OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.product.price,
                )
            )
            item.product.quantity -= item.quantity
        CartItem.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        flash("Order placed successfully.", "success")
        return redirect(url_for("customer_order_details", order_id=order.id))

    @app.route("/customer/orders")
    @role_required("customer")
    def customer_order_list():
        """List customer orders with optional status filter."""
        user_id = session.get("user_id")
        status_filter = request.args.get("status", "").strip().lower()
        query = Order.query.filter_by(user_id=user_id).options(
            joinedload(Order.items).joinedload(OrderItem.product)
        )
        if status_filter and status_filter in ("placed", "packed", "shipped", "delivered", "cancelled"):
            query = query.filter(Order.status == status_filter)
        orders = query.order_by(Order.created_at.desc()).all()
        order_totals = {o.id: sum((oi.price * oi.quantity) for oi in o.items) for o in orders}
        return render_template(
            "customer/orders/order_list.html",
            orders=orders,
            order_totals=order_totals,
            status_filter=status_filter,
        )

    @app.route("/customer/orders/history")
    @role_required("customer")
    def customer_order_history():
        """Order history: delivered and cancelled orders."""
        user_id = session.get("user_id")
        orders = (
            Order.query.filter_by(user_id=user_id)
            .filter(Order.status.in_(("delivered", "cancelled")))
            .options(joinedload(Order.items).joinedload(OrderItem.product))
            .order_by(Order.created_at.desc())
            .all()
        )
        order_totals = {o.id: sum((oi.price * oi.quantity) for oi in o.items) for o in orders}
        return render_template(
            "customer/orders/order_history.html",
            orders=orders,
            order_totals=order_totals,
        )

    @app.route("/customer/orders/<int:order_id>")
    @role_required("customer")
    def customer_order_details(order_id):
        """View full order details."""
        user_id = session.get("user_id")
        order = (
            Order.query.filter_by(id=order_id, user_id=user_id)
            .options(joinedload(Order.items).joinedload(OrderItem.product))
            .first_or_404()
        )
        order_total = sum((oi.price * oi.quantity) for oi in order.items)
        return render_template(
            "customer/orders/order_details.html",
            order=order,
            order_total=order_total,
        )
