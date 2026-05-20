"""
Store model.
"""
from extensions import db


class Store(db.Model):
    """Store model mapped to stores table."""

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    store_staff = db.relationship("StoreStaff", back_populates="store", lazy="dynamic")


# Association table for StoreStaff <-> Category (many-to-many)
store_staff_categories = db.Table(
    "store_staff_categories",
    db.Column("store_staff_id", db.Integer, db.ForeignKey("store_staff.id", ondelete="CASCADE"), primary_key=True),
    db.Column("category_id", db.Integer, db.ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)


class StoreStaff(db.Model):
    """StoreStaff links a user (staff) to a store and category access."""

    __tablename__ = "store_staff"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref=db.backref("store_staff_assignments", lazy="dynamic"))
    store = db.relationship("Store", back_populates="store_staff")
    categories = db.relationship(
        "Category",
        secondary=store_staff_categories,
        backref=db.backref("store_staff_with_access", lazy="dynamic"),
        lazy="joined",
    )
