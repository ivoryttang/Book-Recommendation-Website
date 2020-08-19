from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
      __tablename__ = "user_info"
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String, nullable=False)
      password = db.Column(db.String, nullable=False)

class Book(db.Model):
      __tablename__ = "book"
      id = db.Column(db.Integer, primary_key=True)
      isbn = db.Column(db.String, primary_key=False)
      title = db.Column(db.String, nullable=False)
      author = db.Column(db.String, nullable=False)
      year = db.Column(db.Integer, nullable=False)

class Review(db.Model):
      __tablename__ = "book_review"
      id = db.Column(db.Integer, primary_key=True)
      review = db.Column(db.String, primary_key=False)
      rating = db.Column(db.Integer, nullable=False)
      reviewer = db.Column(db.String, nullable=False)
      book_id = db.Column(db.Integer, nullable=True)

