from flask import Blueprint, current_app, render_template, request, redirect, url_for, session, flash
import json
from functools import wraps

feedback_bp = Blueprint('feedback_bp', __name__)

# Dummy credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("Login required to access this page.", "warning")
            return redirect(url_for("feedback_bp.login"))
        return f(*args, **kwargs)
    return decorated_function


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


@feedback_bp.route("/feedback", methods=["GET", "POST"])
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


@feedback_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            flash("Logged in successfully!", "success")
            return redirect(url_for("feedback_bp.view_responses"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")


@feedback_bp.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("feedback_bp.login"))


@feedback_bp.route("/responses")
@login_required
def view_responses():
    cursor, conn = get_db_cursor()
    cursor.execute("SELECT id, selected_class, response, submitted_at FROM form_responses ORDER BY submitted_at DESC")
    rows = cursor.fetchall()

    parsed_rows = []
    for row in rows:
        id, selected_class, response_json, submitted_at = row
        try:
            parsed_response = response_json if isinstance(response_json, dict) else json.loads(response_json)
        except Exception:
            parsed_response = {"error": "Invalid JSON"}

        parsed_rows.append({
            "id": id,
            "selected_class": selected_class,
            "responses": parsed_response,
            "submitted_at": submitted_at
        })

    return render_template("responses.html", responses=parsed_rows)
