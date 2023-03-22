import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from functions import login_required

# Global variables
study_types = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
prices = {"Level 1": 50.00, "Level 2": 75.00, "Level 3": 100.00, "Level 4": 150.00, "Level 5": 200.00}
specialties = ["Urologist", "Radiologist", "Dermatologist", "Oncologist Surgeon", "Oncologist", "Radio-Oncologist", "Gastroenterologist", "Cardiologist",
               "Neurologist", "Gynaecologist", "Pediatrician", "Ophthalmologist", "Internist", "Nephrologist", "Surgeon", "Mastologist", "Hematologist", "Pathologist"]

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_NAME"] = "session"
Session(app)

# Load database
db = SQL("sqlite:///pathology.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    logs = db.execute("SELECT d.name AS doctorsName , p.name, p.email , p.type, p.price, strftime('%Y',p.date) AS year, strftime('%m',p.date) AS month,strftime('%d',p.date) AS day FROM doctors d, pathology p WHERE p.doctor_id = d.id ORDER BY date DESC;")
    return render_template("index.html", logs=logs)


@app.route("/login", methods=["GET", "POST"])
def login():

    # clear session
    session.clear()

    if request.method == "POST":
        # get variables from form
        username = request.form.get("username")
        password = request.form.get("password")

        # check for input errors
        if not username or not password:
            flash("You must insert password AND username")
            return (redirect("/login"))
        # Query database
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        # check if username and password exist
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password")
            return (redirect("/login"))
        # Remember logged in user
        session["user_id"] = rows[0]["id"]

        # redirect
        return redirect("/")
    # Get method
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Clear session
    session.clear()

    # redirect
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    # render template
    if request.method == "GET":
        return render_template("register.html")
    else:
        # get variables from form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # check for input errors
        if not username or not password or not confirmation:
            flash("Unable to register due to incorrect input")
            return redirect("/register")
        if password != confirmation:
            flash("The password needs to match the confirmation")
            return redirect("/register")
        hash = generate_password_hash(password)
        # add to data base
        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (? , ?)", username, hash)
        except:
            flash("Username already in existence")
            return redirect("/register")

        session["user_id"] = new_user
        return redirect("/")


@app.route("/doctors", methods=["GET", "POST"])
@login_required
def doctors():
    if request.method == "POST":
        # get variables from form
        name = request.form.get("doctorsname")
        specialty = request.form.get("specialty")
        # check for input errors
        if not name or specialty not in specialties:
            flash("Incorrect Input!")
            return redirect("/doctors")
            # return flash error("Incorrect Input")
        if name.isdigit():
            flash("Input must be a string!")
            return redirect("/doctors")
            # return flash error("Input must be a string")
        try:
            db.execute("INSERT INTO doctors(name, especialty) VALUES (? , ?)", name, specialty)
        except:
            flash("Doctor already registered")
            return redirect("/doctors")
        # if insert successful, return a message and redirect
        redirect("/")
        flash("Doctor added successfully!")
        return (redirect("/"))
    else:
        # GET method
        return render_template("doctors.html", specialties=specialties)


@app.route("/patients", methods=["GET", "POST"])
@login_required
def patients():
    if request.method == "POST":
        # get data from FORM
        doctor = request.form.get("doctor_name")
        patient = request.form.get("patient_name")
        study_type = request.form.get("study_type")
        email = request.form.get("email")

        # date variable
        date = datetime.datetime.now()

        # check for input errors
        if not doctor or not patient or not study_type or not email:
            flash("Incorrect input, fill every form")
            return redirect("/patients")
        if patient.isdigit():
            flash("Numbers are not allowed!")
            return redirect("/patients")
        if study_type not in study_types or doctor == "Choose doctor":
            flash("Incorrect input, fill every form")
            return redirect("/patients")
        # if there are no errors declare price variable
        price = prices[str(study_type)]

        # insert into database
        doctor_id = db.execute("SELECT id FROM doctors WHERE name = ?", doctor)
        doctor_id2 = doctor_id[0]['id']
        db.execute("INSERT INTO pathology(doctor_id, name, type, price, date, email) VALUES (? , ? , ? , ? , ?, ?)",
                   doctor_id2, patient, study_type, float(price), date, email)

        # redirect to index
        redirect("/")
        flash("Study successfully recorded")
        return redirect("/")
    else:
        # GET method
        doctors_names = db.execute("SELECT name FROM doctors;")
        return render_template("patients.html", doctors_names=doctors_names, study_types=study_types)


@app.route("/search_doctor")
@login_required
# only render template
def search_doctor():
    return render_template("search_doctor.html")


@app.route("/search_doctor/search")
def search_doctor2():
    # When input, return query as json so ir can be displayed dinamically
    q = request.args.get("q")
    if q:
        results = db.execute("SELECT d.name AS doctorsName , p.name, p.email, p.type, p.price, strftime('%Y',p.date) AS year, strftime('%m',p.date) AS month,strftime('%d',p.date) AS day FROM doctors d, pathology p WHERE p.doctor_id = d.id AND d.name LIKE ? ORDER BY date DESC;", "%" + q + "%")
    else:
        results = []
    return jsonify(results)


@app.route("/search_name")
# only render template
@login_required
def search_name():
    return render_template("search_name.html")


@app.route("/search_name/search")
def search_name2():
    # When input, return query as json so ir can be displayed dinamically
    q = request.args.get("q")
    if q:
        results = db.execute("SELECT d.name AS doctorsName , p.name, p.email, p.type, p.price, strftime('%Y',p.date) AS year, strftime('%m',p.date) AS month,strftime('%d',p.date) AS day FROM doctors d, pathology p WHERE p.doctor_id = d.id AND p.name LIKE ? ORDER BY date DESC;", "%" + q + "%")
    else:
        results = []
    return jsonify(results)


@app.route("/search_date")
@login_required
# only render template
def search_date():
    today = datetime.datetime.now()
    return render_template("search_date.html", today=today)


@app.route("/search_date/search")
def search_date2():
    # When input, return query as json so ir can be displayed dinamically
    q = request.args.get("q")
    if q:
       # separate string in year, month and day for query
        year = q[0:4]
        month = q[5:7]
        day = q[8:10]

        results = db.execute("SELECT d.name AS doctorsName , p.name, p.email, p.type, p.price, strftime('%Y',p.date) AS year, strftime('%m',p.date) AS month,strftime('%d',p.date) AS day FROM doctors d, pathology p WHERE p.doctor_id = d.id AND strftime('%Y',p.date) = ? AND strftime('%m',p.date) = ? AND strftime('%d',p.date) = ? ORDER BY date DESC;", year, month, day)
    else:
        results = []
    return jsonify(results)

