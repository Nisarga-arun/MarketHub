"""
Product and Order models.
"""
from extensions import db


class Product(db.Model):
    """Product model - belongs to a store and optional category."""

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    image_path = db.Column(db.String(512), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    store = db.relationship("Store", backref=db.backref("products", lazy="dynamic"))
    category = db.relationship("Category", backref=db.backref("products", lazy="dynamic"))


class Order(db.Model):
    """Order model - placed by a customer (user)."""

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="placed")
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref=db.backref("orders", lazy="dynamic"))
    items = db.relationship("OrderItem", back_populates="order", lazy="joined", cascade="all, delete-orphan")


class OrderItem(db.Model):
    """OrderItem links an order to a product with quantity and price snapshot."""

    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0)

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", backref=db.backref("order_items", lazy="dynamic"))
