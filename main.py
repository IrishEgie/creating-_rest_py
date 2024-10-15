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

@app.route("/search")
def search_cafes():
    location = request.args.get("loc")
    result = get_cafes(action="search", location=location)
    return jsonify(result)

@app.route("/add", methods=["POST"])
def add_cafe():
    # Get data from the request body
    new_cafe_data = request.json

    # Create a new Cafe object
    new_cafe = Cafe(
        name=new_cafe_data["name"],
        map_url=new_cafe_data["map_url"],
        img_url=new_cafe_data["img_url"],
        location=new_cafe_data["location"],
        seats=new_cafe_data["seats"],
        has_toilet=new_cafe_data["has_toilet"],
        has_wifi=new_cafe_data["has_wifi"],
        has_sockets=new_cafe_data["has_sockets"],
        can_take_calls=new_cafe_data["can_take_calls"],
        coffee_price=new_cafe_data["coffee_price"],
    )

    # Add the new café to the database
    db.session.add(new_cafe)
    db.session.commit()

    return jsonify({"message": "Cafe added successfully!", "cafe": cafe_to_dict(new_cafe)}), 201


@app.route("/update-price", methods=["PATCH"])
def patch_cafe():
    # Get the café ID from the query parameters
    cafe_id = request.args.get("id")

    # Validate input
    if not cafe_id:
        return jsonify({"error": "Missing café ID."}), 400

    # Find the café by ID
    cafe = Cafe.query.get(cafe_id)
    if not cafe:
        return jsonify({"error": "Cafe not found."}), 404

    # Get all optional parameters from the query parameters
    new_data = {
        "name": request.args.get("name"),
        "map_url": request.args.get("map_url"),
        "img_url": request.args.get("img_url"),
        "location": request.args.get("location"),
        "seats": request.args.get("seats"),
        "has_toilet": request.args.get("has_toilet") == 'true',
        "has_wifi": request.args.get("has_wifi") == 'true',
        "has_sockets": request.args.get("has_sockets") == 'true',
        "can_take_calls": request.args.get("can_take_calls") == 'true',
        "coffee_price": request.args.get("coffee_price"),
    }

    # Update only the fields that are provided
    for key, value in new_data.items():
        if value is not None:
            setattr(cafe, key, value)

    db.session.commit()

    return jsonify({"message": "Cafe updated successfully!", "cafe": cafe_to_dict(cafe)}), 200


# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
