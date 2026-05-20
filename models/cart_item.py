"""
CartItem model for shopping cart.
"""
from extensions import db


class CartItem(db.Model):
    """CartItem links a user to a product with quantity."""

    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref=db.backref("cart_items", lazy="dynamic"))
    product = db.relationship("Product", backref=db.backref("cart_items", lazy="dynamic"))
