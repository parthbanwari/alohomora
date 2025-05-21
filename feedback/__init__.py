from flask import Blueprint

feedback_bp = Blueprint('feedback_bp', __name__, template_folder='templates')

from feedback import routes  # This attaches routes to the blueprint
