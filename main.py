from flask import Flask
from db import init_db
from feedback import feedback_bp
from main_app.routes import main_bp  # ✅ New import

def create_app():
    app = Flask(__name__, template_folder="main_app/templates")  # ✅ Optional: sets default template folder for main app

    # Initialize DB connection
    conn = init_db()
    app.config['DB_CONN'] = conn
    app.secret_key = "supersecretkey"  # ✅ Needed for sessions, flash messages, etc.

    # Register main homepage blueprint
    app.register_blueprint(main_bp)

    # Register feedback blueprint (already has its own templates folder)
    app.register_blueprint(feedback_bp, url_prefix="/feedback")


    return app


# ✅ Needed by Gunicorn
app = create_app()
