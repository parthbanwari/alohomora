from flask import Flask
from db import init_db
from feedback import feedback_bp

def create_app():
    app = Flask(__name__)
    # Load env already done before this

    # Initialize DB connection
    conn = init_db()
    app.config['DB_CONN'] = conn

    # Register blueprint
    app.register_blueprint(feedback_bp)

    return app
