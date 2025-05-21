from flask import Blueprint, render_template, url_for

# Get the blueprint from __init__.py
from main_app import main_bp

@main_bp.route("/")
def homepage():
    # Render the main homepage
    return render_template("index.html")

# If you need any additional routes for your main app, add them here