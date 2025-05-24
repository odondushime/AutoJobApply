"""
Core Package
Contains core application configuration and setup.
"""

from flask import Flask
from flask_cors import CORS

def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    from ..api import resume_bp
    app.register_blueprint(resume_bp)
    
    return app

__all__ = ['create_app']
