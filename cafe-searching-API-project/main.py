from flask import Flask, jsonify, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, func
import wtforms
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
import datetime


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


# with app.app_context():
#     db.create_all()

def cafe_data_converter(data):
    cafe_list = []
    for cafe in data:
        cafe_data = {
            "id": cafe.id,
            "name": cafe.name,
            "map_url": cafe.map_url,
            "image_url": cafe.img_url,
            "location": cafe.location,
            "has_sockets": cafe.has_sockets,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "can_make_calls": cafe.can_take_calls,
            "seats": cafe.seats,
            "coffee_price": cafe.coffee_price,
        }
        cafe_list.append(cafe_data)
    return jsonify(cafe_list)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=["GET"])
def random():
    data = [Cafe.query.order_by(func.random()).first()]
    return cafe_data_converter(data)


@app.route("/all", methods=["GET"])
def all_cafes():
    data = Cafe.query.all()
    return cafe_data_converter(data)


@app.route("/search/<loc>", methods=["GET"])
def find_cafes(loc):
    data = Cafe.query.all()
    cafe_list = []
    for cafe in data:
        if str(cafe.location) == str(loc):
            cafe_list.append(cafe)
    if len(cafe_list) == 0:
        return {
            "error": {
                "Not Found": "Sorry, we don't have a cafe at that location."
            }
        }
    else:
        return cafe_data_converter(cafe_list)


@app.route("/add", methods=["GET", "POST"])
def post_new_cafe():
    if request.method == "GET":
        return render_template("add-cafe.html")
    elif request.method == "POST":
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    cafe = Cafe.query.get_or_404(id=cafe_id)
    if cafe:
        cafe.id = request.form.get("coffee_price")
        db.session.commit()
        return jsonify({"success": "Successfully updated the price"})
    else:
        return jsonify({"error": {"Not found": "Sorry a cafe with that id was not found in the database."}})


@app.route("/cafe-closed/<cafe_id>", methods=["POST"])
def delete_record(cafe_id):
    cafe = Cafe.query.get_or_404(id=cafe_id)
    if cafe:
        db.session.remove(cafe)
        db.session.commit()
        return jsonify({"success": "Successfully removed the cafe"})
    else:
        return jsonify({"error": {"Not found": "Sorry a cafe with that id was not found in the database."}})


if __name__ == '__main__':
    app.run(debug=True)
