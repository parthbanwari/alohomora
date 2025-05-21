from flask import Blueprint

# Create a blueprint for the main app
main_bp = Blueprint('main_bp', __name__, 
                    template_folder='templates')

# Import routes after creating the blueprint
from . import routes