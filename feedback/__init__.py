from flask import Blueprint

# Create the blueprint with the template folder
feedback_bp = Blueprint('feedback_bp', __name__, 
                        template_folder='templates')

# Import routes after creating the blueprint to avoid circular imports
from . import routes