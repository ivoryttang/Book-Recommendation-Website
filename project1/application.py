import os

from flask import Flask, session, render_template, request, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from book import *
import requests
import json

#Goodreads Key: UXIiLXvWyO2ODR9FaMKXRw

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

db.execute("SELECT username, password FROM user_info").fetchall() # execute this SQL command and return all of the results

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/login.html", methods=['POST','GET'])
def login1():
    return render_template('login.html')

@app.route("/logged_in.html", methods=['POST','GET'])
def logged_in():
    attempted_username = request.form.get('username')
    attempted_password = request.form.get('password')
    if (User.query.filter_by(username = attempted_username, password = attempted_password).first() != None):
        session['user'] = attempted_username
        return render_template("logged_in.html")
    return render_template("login.html")

@app.route("/create_account.html")
def create_account():
    return render_template('create_account.html')

@app.route("/created_account.html", methods=['POST','GET'])
def created_account():
    new_username = request.form.get('username')
    new_password = request.form.get('password')
    new_confirm_password = request.form.get('confirm_password')
    contains_upper = False
    contains_digit = False
    for i in range(0,len(new_password)):
        if new_password[i].isupper():
            contains_upper = True
    for i in range(0,len(new_password)):
            if new_password[i].isdigit():
                contains_digit = True
    if len(new_password) >= 8 and new_password == new_confirm_password and contains_upper and contains_digit:
        new_user = User(username=new_username, password=new_password)
        db.add(new_user)
        db.commit()
        return render_template("login.html")
    else:
        flash('Password did not meet requirements')
    return render_template("create_account.html")

#TODO: If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!
@app.route("/found_book.html", methods=['POST','GET'])
def display_book_info():
    search_string = request.form.get('search_text')
    sql="SELECT * FROM book WHERE isbn LIKE '%{s}%' OR title LIKE '%{s}%' OR author LIKE '%{s}%'".format(s=search_string)
    books = db.execute(sql).fetchall()
    print(sql)
    print(len(books))
    if len(books) != 0:
        return render_template("found_book.html", books=books)
    return render_template("logged_in.html")

@app.route("/book_page.html", methods=['POST','GET'])
def book_page():
    current_id = request.args.get('current_id')
    current_isbn = request.args.get('current_isbn')
    book = db.execute("SELECT * FROM book WHERE id = :s", {"s":current_id}).first()
    print(current_isbn)
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "UXIiLXvWyO2ODR9FaMKXRw", "isbns": "0380803267"})
    res_obj = json.loads(res.text)
    print(res_obj["books"][0]['average_rating'])

    if len(book) != 0:
        return render_template("book_page.html", book=book, goodreads=res_obj["books"][0]['average_rating'])
    return render_template("logged_in.html")

@app.route("/post_review.html", methods=['POST', 'GET'])
def post_review():
    new_review = request.args.get('review')
    new_rating = request.args.get('rating')
    current_id3 = request.args.get('current_id3')
    reviews = db.execute("SELECT * FROM book_review WHERE book_id = :s", {"s":current_id3}).fetchall()
    book = db.execute("SELECT * FROM book WHERE id = :s", {"s":current_id3}).fetchall()
    book_review = Review(review=new_review, rating=new_rating, reviewer=session['user'], book_id=current_id3)
    db.add(book_review)
    db.commit()
    return render_template("post_review.html", book=book, reviews=reviews)