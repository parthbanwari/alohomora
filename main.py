from flask import Flask
from db import init_db
import os
import sys

# Add the current directory to the path to ensure imports work
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"  # Make sure this matches in both places

    # Initialize DB connection
    conn = init_db()
    app.config['DB_CONN'] = conn

    # Import and register blueprints
    from main_app import main_bp
    from feedback import feedback_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(feedback_bp, url_prefix="/feedback")

    # Session security configs
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    # 🔧 Ensure the DB table is created within the app context
    with app.app_context():
        from feedback.routes import create_table
        create_table()

    # For debugging - print all registered routes
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

    return app

# Create the application instance (needed by Gunicorn)
app = create_app()

# For local development
if __name__ == "__main__":
    app.run(debug=True)
