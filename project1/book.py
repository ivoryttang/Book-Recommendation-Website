from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
      __tablename__ = "book"
      id = db.Column(db.Integer, primary_key=True)
      isbn = db.Column(db.String, primary_key=False)
      title = db.Column(db.String, nullable=False)
      author = db.Column(db.String, nullable=False)
      year = db.Column(db.Integer, nullable=False)
