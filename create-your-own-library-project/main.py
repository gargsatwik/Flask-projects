from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DB_URI', "sqlite:///project.db")


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    rating: Mapped[float] = mapped_column(String(250), unique=True, nullable=False)


db.init_app(app)


@app.route('/')
def home():
    all_books = User.query.all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    elif request.method == "POST":
        book_name = request.form['book_name']
        book_author = request.form['book_author']
        book_rating = request.form['book_rating']
        with app.app_context():
            db.create_all()
            new_book = User(title=book_name, author=book_author, rating=book_rating)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('home'))


@app.route("/edit-rating/<num>", methods=["GET", "POST"])
def edit_rating(num):
    all_books = User.query.all()
    if request.method == "GET":
        return render_template("edit.html", books=all_books, num=float(num))
    elif request.method == "POST":
        new_rating = request.form['new_rating']
        for book in all_books:
            if book.id == float(num):
                book_ = User.query.get(num)
                book_.rating = new_rating
                db.session.commit()
        return redirect(url_for("home"))


@app.route("/delete/<num>", methods=["GET"])
def delete(num):
    all_books = User.query.all()
    for book in all_books:
        if book.id == int(num):
            db.session.delete(book)
            db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
