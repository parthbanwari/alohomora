from flask import Blueprint

# Create blueprint with correct template folder
feedback_bp = Blueprint('feedback_bp', __name__, template_folder='templates')

# Import routes
from . import routes

# Make sure it's importable
__all__ = ['feedback_bp']
