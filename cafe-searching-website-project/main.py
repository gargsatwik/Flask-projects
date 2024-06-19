import wtforms
from flask import Flask, redirect, render_template, url_for, request
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_bootstrap import Bootstrap5
import datetime


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret-key-goes-here"
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)
year = datetime.datetime.now().year


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


class NewCafeForm(FlaskForm):
    def __init__(self, cafe=None, *args, **kwargs):
        super(NewCafeForm, self).__init__(*args, **kwargs)
        self.cafe = cafe  # Store the passed Cafe object

        # Set default values and validators based on the cafe object (if provided)
        if cafe:
            self.name.data = cafe.name
            self.location.data = cafe.location
            self.seats.data = cafe.seats
            self.toilets.default = cafe.has_toilet
            self.Wifi.default = cafe.has_wifi
            self.sockets.default = cafe.has_sockets
            self.calls.default = cafe.can_take_calls
            self.price.data = cafe.coffee_price
            self.map_url.data = cafe.map_url
            self.img_url.data = cafe.img_url

    name = wtforms.StringField("Name", default="", validators=[wtforms.validators.DataRequired()])
    location = wtforms.StringField("Location", default="", validators=[wtforms.validators.DataRequired()])
    seats = wtforms.StringField("Number of seats", default="", validators=[wtforms.validators.DataRequired()])
    toilets = wtforms.BooleanField("Has toilets", default=False)
    Wifi = wtforms.BooleanField("Has Wifi", default=False)
    sockets = wtforms.BooleanField("Has Sockets", default=False)
    calls = wtforms.BooleanField("Can answer calls", default=False)
    price = wtforms.IntegerField("Coffee Price", validators=[wtforms.validators.DataRequired()])
    map_url = wtforms.URLField("Map Url", default="", validators=[wtforms.validators.DataRequired()])
    img_url = wtforms.URLField("Image Url", default="", validators=[wtforms.validators.DataRequired()])


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html", all_cafes=Cafe.query.all(), year=year)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = NewCafeForm()
    if request.method == "GET":
        return render_template("add.html", form=form, year=year, edit=False)
    elif request.method == "POST":
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.sockets.data,
            has_toilet=form.toilets.data,
            has_wifi=form.Wifi.data,
            can_take_calls=form.calls.data,
            seats=form.seats.data,
            coffee_price=form.price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))


@app.route('/delete/<to_delete>', methods=['POST'])
def delete(to_delete):
    cafe = Cafe.query.get(to_delete)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for("home"))


@app.route('/edit/<to_edit>', methods=['GET', 'POST'])
def edit(to_edit):
    cafe = Cafe.query.get(to_edit)
    form = NewCafeForm(cafe=cafe)
    if request.method == 'GET':
        return render_template('add.html', year=year, form=form, edit=True)
    elif request.method == 'POST':
        if form.validate_on_submit():
            cafe.name = form.name.data
            cafe.map_url = form.map_url.data
            cafe.img_url = form.img_url.data
            cafe.location = form.location.data
            cafe.has_sockets = form.sockets.data
            cafe.has_toilet = form.toilets.data
            cafe.has_wifi = form.Wifi.data
            cafe.can_take_calls = form.calls.data
            cafe.seats = form.seats.data
            cafe.coffee_price = form.price.data
            db.session.commit()
            return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
