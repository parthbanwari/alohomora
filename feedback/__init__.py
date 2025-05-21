from flask import Blueprint

feedback_bp = Blueprint('feedback_bp', __name__, template_folder='templates')

from . import routes  # This attaches routes to the blueprint
