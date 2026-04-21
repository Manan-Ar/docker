from flask_sqlalchemy import SQLAlchemy

# Create a single shared SQLAlchemy instance.
# Imported by both app.py and models.py to avoid circular imports.
db = SQLAlchemy()
