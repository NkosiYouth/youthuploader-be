# app/__init__.py

from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from config import Config
from app.routes.user_routes import user_bp
from app.routes.file_routes import file_bp

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

CORS(app, origins='*', methods=['GET', 'POST', 'PUT', 'DELETE'])

# Initialize PyMongo extension
mongo = PyMongo(app)

# Import routes and register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(file_bp, url_prefix='/api')

# @app.route('/')
# def index():
#     return jsonify({"message": "Welcome to the API!"})

