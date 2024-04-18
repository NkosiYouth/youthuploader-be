from flask import Blueprint

# Import blueprints from route modules
from app.routes.user_routes import user_bp
from app.routes.file_routes import file_bp

# Expose blueprints
__all__ = ['user_bp', 'file_bp']
