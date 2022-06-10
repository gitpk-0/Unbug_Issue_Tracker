from crypt import methods
import os
import psycopg2

from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# uri = os.getenv("DATABASE_URL")
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://")
# db = SQL(uri)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='unbug_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


conn = get_db_connection()
db = conn.cursor()  # Database connection


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
# @login_required
def index():
    """ Landing page """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index.html', users=users)


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in """

    # Forget previous user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":
        username = request.form.get("username")
        pw = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("no username entered", 403)

        # Ensure password was submitted
        elif not pw:
            return apology("no password entered", 403)

        # Query database for username
        db.execute('SELECT * from users WHERE username = %s;', (username,))
        rows = db.fetchall()
        print(rows)

        pw_hash = rows[0][2]

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(pw_hash, pw):
            return apology("invalid username or password", 403)

        # Remember which user has logged in
        user_id = rows[0][0]
        session["user_id"] = user_id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """  Register user  """

    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST
    if request.method == "POST":
        username = request.form.get("username")
        pw = request.form.get("password")
        pw_confirm = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username")

        elif not pw:
            return apology("must provide password")

        elif not pw == pw_confirm:
            return apology("passwords do not match")

        # Generate a hash of the password
        pw_hash = generate_password_hash(pw)

        db.execute(
            'SELECT username FROM users WHERE username = %s', (username,))
        in_use = db.fetchall()
        print(in_use)
        print(in_use == [])

        if in_use == []:
            db.execute(
                'INSERT INTO users(username, hash) VALUES (%s, %s)', (username, pw_hash))
            conn.commit()  # commit changes to database
        else:
            return apology("username already taken")

        # Remember which user has logged in
        db.execute('SELECT * FROM users WHERE username = %s', (username,))
        rows = db.fetchall()
        user_id = rows[0][0]
        session["user_id"] = user_id

        # Redirect new user to index page
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/new_issue", methods=["GET", "POST"])
def new_issue():
    """ Report a new issue """

    # Display form to report a new issue
    if request.method == "GET":
        return render_template("new_issue.html")

    # Display summary of submission
    if request.method == "POST":

        # Form info
        subject = request.form.get("subject")
        summary = request.form.get("summary")

        return render_template("submission.html", subject=subject, summary=summary)
