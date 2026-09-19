from flask import Flask, request
import json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# PostgreSQL database connection
import os
from dotenv import load_dotenv

load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route("/api/places")
def get_places():
    result = db.session.execute(db.text("SELECT * FROM place_reviews"))
    places = [dict(row._mapping) for row in result]

    return places

@app.route("/api/places/<int:place_id>")
def get_place(place_id):
    result = db.session.execute(
        db.text("SELECT * FROM place_reviews WHERE place_id = :place_id"),
        {"place_id": place_id}
    )

    place = result.fetchone()

    if place is None:
        return {"error": "Place not found"}, 404

    return dict(place._mapping)

    return places

@app.route("/api/places/<int:place_id>/reviews")
def get_place_reviews(place_id):
    result = db.session.execute(
        db.text("""
            SELECT
                r.id,
                u.name AS user_name,
                r.rating,
                r.comment
            FROM review r
            JOIN "user" u ON r.user_id = u.id
            WHERE r.place_id = :place_id
            ORDER BY r.id
        """),
        {"place_id": place_id}
    )

    reviews = [dict(row._mapping) for row in result]

    return reviews

@app.route("/api/sites", methods=["POST"])
def create_site():
    data = request.get_json()

    site_name = data.get("name")
    geojson = data.get("geometry")

    if not site_name or not geojson:
        return {
            "error": "Site name and boundary are required"
        }, 400

    result = db.session.execute(
        db.text("""
            INSERT INTO site (
                project_id,
                name,
                area_hectares,
                boundary
            )
            VALUES (
                1,
                :name,
                ST_Area(
                    ST_GeomFromGeoJSON(:geojson)::geography
                ) / 10000,
                ST_SetSRID(
                    ST_GeomFromGeoJSON(:geojson),
                    4326
                )
            )
            RETURNING
                id,
                name,
                area_hectares
        """),
        {
            "name": site_name,
            "geojson": json.dumps(geojson)
        }
    )

    db.session.commit()

    site = result.fetchone()

    return {
        "message": "Site saved successfully",
        "site": dict(site._mapping)
    }, 201

@app.route("/api/sites", methods=["GET"])
def get_sites():

    result = db.session.execute(
        db.text("""
            SELECT
                id,
                project_id,
                name,
                area_hectares,
                carbon_stored,
                biodiversity_score,
                ST_AsGeoJSON(boundary) AS geometry
            FROM site
            ORDER BY id
        """)
    )

    sites = [dict(row._mapping) for row in result]

    return sites

@app.route("/api/reviews")
def get_reviews():
    result = db.session.execute(
        db.text("""
            SELECT
                r.id,
                u.name AS user_name,
                p.name AS place_name,
                r.rating,
                r.comment
            FROM review r
            JOIN "user" u ON r.user_id = u.id
            JOIN place p ON r.place_id = p.id
            ORDER BY r.id
        """)
    )

    reviews = [dict(row._mapping) for row in result]

    return reviews

@app.route("/")
def home():
    return "Darukaa.Earth Backend is Running!"

with app.app_context():
    db.engine.connect()
    print("PostgreSQL connected successfully!")

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
    
if __name__ == "__main__":
    app.run(debug=True)