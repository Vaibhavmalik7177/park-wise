import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helper import apology, login_required

from datetime import datetime, timedelta

# Configure application
app = Flask(__name__)


@app.before_request
def auto_uppercase_regno():
    # If a form is submitted containing a vehicle registration field, convert it to UPPERCASE
    if request.method == "POST" and "regno" in request.form:
        request.form = request.form.copy()
        request.form["regno"] = request.form["regno"].strip().upper()


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///parkwise.db")

ira = [1]


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
    """Show portfolio of stocks"""
    ir = session["user_id"]
    if session.get("user_type") == 'vis':

        time_in = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%dT%H:%M")
        return render_template("index_visitor.html", current_time=time_in)
    else:
        return render_template("index_resident.html")


@app.route("/history", methods=["GET"])
@login_required
def history():
    """Show history of parking log for current visitor/resident"""
    # Resident log view
    logs = db.execute("SELECT * FROM visitor_log ORDER BY timein DESC")

    return render_template("history_vis_res.html", logs=logs)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("regno"):
            return apology("must provide Resgistration Number", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM visitor_ids WHERE regno = ? collate nocase", request.form.get("regno")
        )
        if len(rows) != 1 or not check_password_hash(
                rows[0]["hash"], request.form.get("password")):

            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_type"] = 'vis'

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login_visitor.html")


@app.route("/loginr", methods=["GET", "POST"])
def loginr():
    """log resident in"""
    # Forget any user_id
 # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide Username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM resident WHERE username = ? collate nocase", request.form.get("username")
        )
        if len(rows) != 1 or not check_password_hash(
                rows[0]["hash"], request.form.get("password")):

            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)

    else:
        return render_template("login_resident.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("name"):
            return apology("must provide name", 400)

        # Ensure password was submitted
        elif not request.form.get("username"):
            return apology("must provide registration no", 400)

        # Ensure registration no was submitted
        elif not request.form.get("password"):

            return apology("must provide password", 400)
        # Ensure that phoneno was submitted
        elif not request.form.get("phno"):

            return apology("must provide Phone No", 400)

        rows = db.execute(
            "SELECT * FROM visitor_ids WHERE regno = ? collate nocase", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) == 1:
            return apology("You already have a account", 400)
        elif len(rows) == 0:
            username = request.form.get("name")
            password = request.form.get("password")
            passworda = request.form.get("cp")
            regno = request.form.get("username")
            phn = request.form.get("phno")
            if password == passworda:
                try:

                    db.execute("insert into visitor_ids (username , hash ,regno,phone) values(?,?,?,?)",
                               username, generate_password_hash(password, method='scrypt', salt_length=16), regno, phn)
                except ValueError:
                    return apology("Registration Failed (Try Again)")
            elif password != passworda:
                return apology("Password didnot match(password should be same in both column)", 400)
        rows = db.execute(
            "SELECT * FROM visitor_ids WHERE regno = ?", regno
        )
        session["user_id"] = rows[0]["id"]
        session["user_type"] = "vis"

        return redirect("/")
    return render_template("register.html")


@app.route("/setting", methods=["GET", "POST"])
@login_required
def setting():
    """Change password"""
    ir = session["user_id"]
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("Password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("cp"):
            return apology("must provide password(confirmation)", 400)

        password = request.form.get("Password")
        passworda = request.form.get("cp")
        if password == passworda:
            db.execute("update visitor_ids  set hash = ? where id =?", generate_password_hash(
                password, method='scrypt', salt_length=16), ir)
            return redirect("/")
        elif password != passworda:
            return apology("Password didnot match(password should be same in both column)", 400)

    return render_template("setting_visitor.html")


@app.route("/settingr", methods=["GET", "POST"])
@login_required
def settingr():
    """Change password"""
    ir = session["user_id"]
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("Password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("cp"):
            return apology("must provide password(confirmation)", 400)

        password = request.form.get("Password")
        passworda = request.form.get("cp")
        if password == passworda:
            db.execute("update resident  set hash = ? where id =?", generate_password_hash(
                password, method='scrypt', salt_length=16), ir)
            return redirect("/a")
        elif password != passworda:
            return apology("Password didnot match(password should be same in both column)", 400)

    return render_template("setting.html")


@app.route("/fcono", methods=["GET", "POST"])
@login_required
def fno():
    """Search for contact number linked to vehicle registration"""
    if request.method == "POST":
        regno = request.form.get("regno")
        if not regno:
            return apology("Must provide registration number", 400)

        # Query database for matching record
        rows = db.execute(
            "SELECT username, phone FROM visitor_ids WHERE regno = ? collate nocase", regno)

        if len(rows) != 1:
            return apology("No record found for this vehicle number", 404)

        # Pass specific name and phone variables to find_number_represent.html
        return render_template("find_number_represent.html", name=rows[0]["username"], phno=rows[0]["phone"])

    return render_template("find_number.html")


@app.route("/cyv", methods=["GET"])
@login_required
def myvehicle():
    """Display registered vehicle and recent parking logs for the logged-in visitor"""
    ir = session["user_id"]

    # 1. Fetch visitor registration details
    user = db.execute(
        "SELECT username, regno, phone FROM visitor_ids WHERE id = ?", ir)
    if not user:
        return apology("Visitor account not found", 404)

    visitor_info = user[0]

    # 2. Fetch parking logs matching this visitor's ID
    logs = db.execute(
        "SELECT * FROM visitor_log WHERE visitor_id = ? ORDER BY timein DESC", ir
    )

    return render_template("checkmyvehicle.html", info=visitor_info, logs=logs)


@app.route("/fpr")
def fpr():
    return apology("Contact HOA For Password Retrival")


@app.route("/fpv", methods=["POST", "GET"])
def fpv():

    return render_template("forgotpass_visitor.html")


@app.route("/prv", methods=["POST", "GET"])
def prv():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("regno"):
            return apology("must provide Resgistration Number", 403)
        row = db.execute("SELECT * FROM visitor_ids WHERE regno = ? collate nocase",
                         request.form.get("regno"))
        if len(row) != 1:
            return apology("Wrong Registration Number/ You does not have register yet")
        ir = row[0]["id"]
        session["ira"] = ir
        return render_template("fprv.html")
    return render_template("/prv")


@app.route("/fprv", methods=["POST", "GET"])
def fprv():
    if request.method == "POST":
        ir = session["ira"]
        username = request.form.get("name")
        phone = request.form.get("phno")

        row = db.execute("SELECT * FROM visitor_ids WHERE id = ?", ir)
        if len(row) != 0:
            print('false')
        if username != row[0]["username"] or phone != str(row[0]["phone"]):
            return apology("Can't reset password (Wrong Info)")
        return render_template("updatepaasv.html")
    return render_template("/fprv")


@app.route("/upf", methods=["POST", "GET"])
def upf():
    ir = session["ira"]

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("Password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("cp"):
            return apology("must provide password(confirmation)", 400)

        password = request.form.get("Password")
        passworda = request.form.get("cp")
        if password == passworda:
            db.execute("update visitor_ids  set hash = ? where id =?", generate_password_hash(
                password, method='scrypt', salt_length=16), ir)
            return redirect("/")
        elif password != passworda:
            return apology("Password didnot match(password should be same in both column)", 400)

    return redirect("/login")


@app.route("/iyv", methods=["POST"])
@login_required
def iyv():
    """Handle visitor entry / exit logging"""
    exit_time = request.form.get("exit")
    ir = session["user_id"]

    if not exit_time:
        return apology("Must provide exit time", 400)

    user = db.execute("SELECT regno FROM visitor_ids WHERE id = ?", ir)
    if not user:
        return apology("User not found", 400)

    regno = user[0]["regno"]

    time_in = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")

    if exit_time < time_in:
        return apology("Exit time cannot be in past")

    db.execute("INSERT INTO visitor_log (regisitration_no, etime, visitor_id, timein) VALUES (?, ?, ?, ?)",
               regno, exit_time, ir, time_in)

    flash("Parking exit time logged successfully!")
    return redirect("/")
