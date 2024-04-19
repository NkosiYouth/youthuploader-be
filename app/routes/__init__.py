from flask import Blueprint

# Import blueprints from route modules
from app.routes.user_routes import user_bp
from app.routes.file_routes import file_bp
from app.routes.host_routes import host_bp
from app.routes.host_address_routes import host_address_bp
from app.routes.supervisor_routes import supervisor_bp

# Expose blueprints
__all__ = ['user_bp', 'host_bp', 'host_address_bp', 'supervisor_bp', 'file_bp']
