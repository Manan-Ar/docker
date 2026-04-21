import os
from flask import Flask, jsonify
from extensions import db
from config import config_map
from routes import api


def create_app():
    """Application factory — creates and configures the Flask app."""

    app = Flask(__name__)

    # Load config based on FLASK_ENV (defaults to development)
    env = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_map.get(env, "development"))

    # Initialise extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(api, url_prefix="/api")

    # Create all tables if they don't already exist
    with app.app_context():
        db.create_all()

    # Health check endpoint
    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "environment": env}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
