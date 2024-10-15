from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random
'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
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


with app.app_context():
    db.create_all()

def cafe_to_dict(cafe):
    """Convert a Cafe object to a dictionary format."""
    return {
        "id": cafe.id,
        "name": cafe.name,
        "map_url": cafe.map_url,
        "img_url": cafe.img_url,
        "location": cafe.location,
        "seats": cafe.seats,
        "has_toilet": cafe.has_toilet,
        "has_wifi": cafe.has_wifi,
        "has_sockets": cafe.has_sockets,
        "can_take_calls": cafe.can_take_calls,
        "coffee_price": cafe.coffee_price,
    }

def get_cafes(action, location=None):
    if action == "random":
        cafes = Cafe.query.all()
        if not cafes:
            return {"error": "No cafes found."}, 404
        random_cafe = random.choice(cafes)
        return {"cafe": [cafe_to_dict(random_cafe)]}  # Wrap in "cafes" key
    elif action == "all":
        cafes = Cafe.query.all()
        return {"cafes": [cafe_to_dict(cafe) for cafe in cafes]}  # Wrap all cafes in "cafes" key
    elif action == "search" and location:
        cafes = Cafe.query.filter(Cafe.location.ilike(f"%{location}%")).all()
        if not cafes:
            return {"error": f"No cafes found in {location}."}, 404
        return {"cafes": [cafe_to_dict(cafe) for cafe in cafes]}
    else:
        return {"error": "Invalid action."}, 400
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random")
def random_cafe():
    result = get_cafes(action="random")
    return jsonify(result)

@app.route("/all")
def all_cafes():
    result = get_cafes(action="all")
    return jsonify(result)

@app.route("/search/<location>")
def search_cafes(location):
    result = get_cafes(action="search", location=location)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
