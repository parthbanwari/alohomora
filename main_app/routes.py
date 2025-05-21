from flask import Blueprint, render_template

main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/")
def homepage():
    return render_template("index.html")  # Should be in main_app/templates/index.html
