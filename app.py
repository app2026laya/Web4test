from flask import Flask, render_template, request, redirect, url_for, g
from datetime import datetime
import sqlite3

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# ────────────────────────────────────────
#  Helpers
# ────────────────────────────────────────

def get_db():
    """Get per-request database connection"""
    if 'db' not in g:
        g.db = sqlite3.connect('main_db.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    if one:
        rv = cur.fetchone()
        return dict(rv) if rv else None
    return [dict(row) for row in cur.fetchall()]

def get_activities(limit=6):
    if limit:
        return query_db(
            "SELECT * FROM activities ORDER BY id DESC LIMIT ?",
            (limit,)
        )
    return query_db("SELECT * FROM activities ORDER BY id DESC")

def get_services():
    return query_db("SELECT * FROM services")

def get_officers():
    return query_db("SELECT * FROM officers")

def get_residents_gender_counts():
    return query_db("""
        SELECT gender, COUNT(*) as count
        FROM aplaya_res
        GROUP BY gender
    """)

# Optional: context processor to inject common variables
@app.context_processor
def inject_common_data():
    return dict(
        current_time = datetime.now().strftime("%A, %B %d, %Y, %I:%M:%S %p")
    )

# ────────────────────────────────────────
#  Routes
# ────────────────────────────────────────

@app.route("/")
def home():
    return render_template(
        "index.html",
        activities    = get_activities(limit=10),
        officers      = get_officers(),
        services      = get_services(),
        residents     = get_residents_gender_counts(),
        # news        = get_news()   # ← will define this function later
    )

@app.route("/residents")
def residents():
    return render_template("residents.html", residents=get_residents_gender_counts())

@app.route("/officers")
def officers():
    return render_template("officers.html", officers=get_officers())

@app.route("/activities")
def activities():
    return render_template("activities.html", activities=get_activities())

@app.route("/cert_services")
def fillupform():
    return render_template("fillupform.html")

@app.route("/Print-cert", methods=["GET", "POST"])
def printcertificate():
    valid_types = {
        "clearance": "certifications/clearance.html",
        "indigency":          "certifications/indigency.html",
        "residency":          "certifications/residency.html"
    }

    if request.form.get("cert_type") not in valid_types:
        return "Invalid certificate type", 400

    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        address  = request.form.get("address",  "").strip()
        purpose  = request.form.get("purpose",  "").strip()

        if not fullname or not address:
            return "Missing required fields", 400

        return render_template(valid_types[request.form.get("cert_type")],
            fullname = fullname,
            address  = address,
            purpose  = purpose,
            today    = datetime.now().strftime("%B %d, %Y")
            )

# ────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)