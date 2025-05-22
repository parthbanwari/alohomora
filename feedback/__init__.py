from flask import Blueprint

# Create blueprint with correct template folder
feedback_bp = Blueprint('feedback_bp', __name__, template_folder='templates')

