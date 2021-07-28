from flask import Flask

from flask_bootstrap import Bootstrap
# from flask_session import Session

# Globally accessible libraries
bootstrap = Bootstrap()


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    bootstrap = Bootstrap(app)  # noqa: F841

    with app.app_context():
        # Include our Routes
        from . import routes  # noqa: F401

        # # Register Blueprints
        # app.register_blueprint(auth.auth_bp)
        # app.register_blueprint(admin.admin_bp)

        return app
