import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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

    # Get the id of the user currently logged in
    user_id = int(session["user_id"])

    # Extract relevant values from db
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = float(cash[0]["cash"])
    try:
        SQL_extracted = db.execute("SELECT symbol, stock, SUM(shares) AS shares, price,\
        ROUND(price*sum(shares), 2) AS total FROM buy WHERE user_id = ? GROUP BY stock", user_id)

        # Need to get the total value of stocks bought
        total = 0
        for a in SQL_extracted:
            total += a["total"]

        # add cash to the value of stocks to get the total value of all
        total = cash + total

        # Turn cash and total to usd
        cash = usd(cash)
        total = usd(total)

        # Turn values inside the extracted dictionary from database into usd
        for d in SQL_extracted:
            d["price"] = usd(d["price"])
            d["total"] = usd(d["total"])

        return render_template("index.html", SQL_extracted=SQL_extracted, cash=cash, total=total)
    except:
        return render_template("index.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")

        # If user doesnt type any stock symbol
        if not symbol:
            return apology("Please type the stock symbol.", 400)

        # Check if this is a valid symbol that exists in the API call
        stock = lookup(symbol)
        if stock == None:
            return apology("Invalid stock symbol.", 400)

        # Get the share number and check its validity
        try:
            shares = float(request.form.get("shares"))
        except:
            return apology("Must enter numeric character", 400)
        if shares < 1 or shares % 1 != 0:
            return apology("Number of shares must be more than 0", 400)
        # As the validity is checked cast it to int to display properly later
        shares = int(shares)

        # Requirements met, so the data flow can continue
        name, price, symbol = stock["name"], float(stock["price"]), stock["symbol"]

        # Extract the currently logged in user's id from the session
        user_id = int(session["user_id"])

        # Use this id to extract the cash that the user currently has
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = float(cash[0]["cash"])
        if cash - shares*price >= 0:
            db.execute("UPDATE users SET cash = cash - ? * ? WHERE id = ?", shares, price, user_id)
            db.execute("INSERT INTO buy (user_id, symbol, price, shares, stock, date) VALUES (?, ?, ?, ?, ?, ?)",
                       user_id, symbol, price, shares, name, datetime.now())
        else:
            return apology("Don't have enough money", 400)
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get the id of the user currently logged in
    user_id = int(session["user_id"])

    # Extract what is need to display appropriate table
    db_extracted = db.execute("SELECT symbol, shares, price, date FROM buy WHERE user_id = ?", user_id)

    return render_template("history.html", db_extracted=db_extracted)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")

        # Check for invalid symbol
        if lookup(symbol) == None or symbol == "":
            return apology("Invalid symbol.")

        # return appropriate values to HTML
        stock = lookup(symbol)
        name, price, symbol = stock["name"], usd(stock["price"]), stock["symbol"]
        return render_template("quoted.html", name=name, price=price, symbol=symbol)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # username
        username = request.form.get("username")
        existing_usernames = db.execute("SELECT username FROM users")
        if username == "":
            return apology("type the username please.")
        for existing_username in existing_usernames:
            if existing_username["username"] == username:
                return apology("This username already exists.")

        # password
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return apology("Passwords do not match!")
        if password == "":
            return apology("Type the password please.")

        # hash the password to store it securily
        password = generate_password_hash(password)

        # insert the login credentials to the database
        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, password)
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Get the id of the user currently logged in
    user_id = int(session["user_id"])
    if request.method == "GET":

        # Extract the symbols of bought stocks to list them in the HTML
        symbol = db.execute("SELECT DISTINCT symbol FROM buy")
        return render_template("sell.html", symbol=symbol)

    # For the POST method
    else:
        symbol = request.form.get("symbol")
        print(f"the symbol {symbol} {type(symbol)}")

        # Check if the symbol for sure had been bought by the client
        symbol_check = db.execute("SELECT DISTINCT symbol FROM buy")
        flag = True
        for a in symbol_check:
            if symbol == a["symbol"]:
                flag = False
                break
        if flag:
            return apology("Choose a valid stock symbol")

        # Check if the user input valid shares number
        shares = request.form.get("shares")
        if shares == "" or float(shares) % 1 != 0.0:
            return apology("Type a valid number of shares. Positive integer.")
        shares = int(shares)

        # Check if user owns that many shares of the selected stock
        db_extracted = db.execute(
            "SELECT symbol, sum(shares) AS shares, price, stock FROM buy WHERE symbol = ? GROUP BY symbol", symbol)
        shares_owned = db_extracted[0]["shares"]
        if shares_owned - shares < 0:
            return apology("You don't have enough shares. Choose smaller amount")

        # Update the SQL table
        price = db_extracted[0]["price"]
        name = db_extracted[0]["stock"]
        order = shares*price
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", order, user_id)
        db.execute("INSERT INTO buy (user_id, symbol, price, shares, stock, date) VALUES (?, ?, ?, ?, ?, ?)",
                   user_id, symbol, price, -shares, name, datetime.now())

        return redirect("/")