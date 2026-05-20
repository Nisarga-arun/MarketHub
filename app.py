"""
E-Commerce Web Application.
Flask application entry point.
"""
from datetime import datetime

from flask import Flask, render_template

from config import config_by_name
from extensions import db
from routes.admin_routes import register_admin_routes
from routes.auth import register_auth_routes
from routes.customer_routes import register_customer_routes
from routes.staff_routes import register_staff_routes


def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = "default"

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)

    # Import models so db.create_all knows about them
    import models  # noqa: F401

    with app.app_context():
        db.create_all()

    @app.context_processor
    def inject_current_year():
        """Make current_year available in all templates."""
        return {"current_year": datetime.now().year}

    @app.route("/")
    def index():
        """Home page."""
        return render_template("base.html")

    register_auth_routes(app)
    register_admin_routes(app)
    register_staff_routes(app)
    register_customer_routes(app)

    return app


app = create_app()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", True))
