from flask import Blueprint, current_app, render_template, request, redirect, url_for, session, flash
import json
from functools import wraps

feedback_bp = Blueprint('feedback_bp', __name__,template_folder='templates')

# Helper function to get DB connection and cursor
def get_db_cursor():
    conn = current_app.config.get('DB_CONN')
    if not conn:
        raise RuntimeError("Database connection not initialized")
    return conn.cursor(), conn


# Create table if not exists - you can call this once when app starts
def create_table():
    cursor, conn = get_db_cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS form_responses (
            id SERIAL PRIMARY KEY,
            selected_class TEXT,
            response JSONB,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


# Load questions JSON once (you can also load this in app factory and pass via config if you want)
import os
json_path = os.path.join(os.path.dirname(__file__), 'form-data.json')
with open(json_path, encoding='utf-8') as f:
    questions_data = json.load(f)

@feedback_bp.route("/", methods=["GET", "POST"])
def form():
    selected_class = request.args.get("class", None)
    cursor, conn = get_db_cursor()

    if request.method == "POST":
        responses = request.form.to_dict(flat=False)
        cleaned_responses = {k: v if len(v) > 1 else v[0] for k, v in responses.items()}

        cursor.execute("""
            INSERT INTO form_responses (selected_class, response)
            VALUES (%s, %s)
        """, (selected_class, json.dumps(cleaned_responses)))
        conn.commit()

        return render_template("thank-you.html")

    common_questions = questions_data["common"]
    grade_specific_questions = []

    if selected_class and selected_class in questions_data["grade_specific"]:
        grade_specific_questions = questions_data["grade_specific"][selected_class]

    return render_template("form.html",
                           common_questions=common_questions,
                           grade_specific_questions=grade_specific_questions,
                           selected_class=selected_class)
