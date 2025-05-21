from flask import Flask
import sys,os

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def create_app():
    app = Flask(__name__)
    app.secret_key = "your-secret-key"

    from main_app.routes import main_bp
    from ..feedback import feedback_bp  # ← import blueprint

    app.register_blueprint(main_bp)
    app.register_blueprint(feedback_bp, url_prefix="/feedback")  # ← attach at /feedback

    return app
