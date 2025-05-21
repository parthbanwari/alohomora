from flask import Flask
from db import init_db
from feedback import feedback_bp

def create_app():
    app = Flask(__name__)
    conn = init_db()
    app.config['DB_CONN'] = conn
    app.register_blueprint(feedback_bp)
    return app

# 👇 Add this line to expose the app object
app = create_app()
