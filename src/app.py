"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Vehicle, FavoritePlanet, FavoriteCharacter, FavoriteVehicle
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_all_characters():
    all_characters = Character.query.all()
    if not all_characters:
        return jsonify({"error": "Characters not found"}), 404
    all_characters_serialize = []
    for character in all_characters:
        all_characters_serialize.append(character.serialize())
    return jsonify(all_characters_serialize), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Character not found"}), 404
    single_person_serialize = person.serialize()
    return jsonify(single_person_serialize), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = Planet.query.all()
    if not all_planets:
        return jsonify({"error": "Planets not found"}), 404
    all_planets_serialize = []
    for planet in all_planets:
        all_planets_serialize.append(planet.serialize())
    return jsonify(all_planets_serialize), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    single_planet = Planet.query.get(planet_id)
    if not single_planet:
        return jsonify({"error": "Planet not found"}), 404
    single_planet_serialize = single_planet.serialize()
    return jsonify(single_planet_serialize), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    if not all_users:
        return jsonify({"error": "Users not found"}), 404
    all_users_serialize = []
    for user in all_users:
        all_users_serialize.append(user.serialize())
    return jsonify(all_users_serialize), 200

@app.route('/users/<int:user_id>/favorites', methods=["GET"])
def get_user_favorites(user_id):
    user_by_id = User.query.get(user_id)
    if not user_by_id:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user_by_id.serialize_favorites()), 200

@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_new_favorite_planet(user_id, planet_id):
    single_user = User.query.get(user_id)
    if not single_user:
        return jsonify({"error": "User not found"}), 404
    single_planet = Planet.query.get(planet_id)
    if not single_planet:
        return jsonify({"error": "Planet not found"}), 404
    already_favorite = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if already_favorite:
        return jsonify({"error": "Planet is already a favorite"}), 409
    new_favorite_planet = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite_planet)
    db.session.commit()
    return jsonify({"message": "Favorite planet added successfully"}), 201

@app.route('/users/<int:user_id>/favorite/people/<int:character_id>', methods=['POST'])
def add_new_favorite_character(user_id, character_id):
    single_user = User.query.get(user_id)
    if not single_user:
        return jsonify({"error": "User not found"}), 404
    single_character = Character.query.get(character_id)
    if not single_character:
        return jsonify({"error": "Character not found"}), 404
    already_favorite = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=character_id).first()
    if already_favorite:
        return jsonify({"error": "Character is already a favorite"}), 409
    new_favorite_character = FavoriteCharacter(user_id=user_id, character_id=character_id)
    db.session.add(new_favorite_character)
    db.session.commit()
    return jsonify({"message": "Favorite character added successfully"}), 201

@app.route('/users/<int:user_id>/planet/<int:planet_id>/favorite', methods=['DELETE'])
def delete_favorte_planet(user_id, planet_id):
    single_user = User.query.get(user_id)
    if not single_user:
        return jsonify({"error": "User not found"}), 400
    single_planet = Planet.query.get(planet_id)
    if not single_planet:
        return jsonify({"error": "Planet not found"}), 400
    selected_favorite = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.delete(selected_favorite)
    db.session.commit()
    return jsonify({"message": "Favorite planet deleted successfully"}), 204

@app.route('/users/<int:user_id>/poeple/<int:character_id>/favorite', methods=['DELETE'])
def delete_favortie_character(user_id, character_id):
    single_user = User.query.get(user_id)
    if not single_user:
        return jsonify({"error": "User not found"}), 400
    single_character = Character.query.get(character_id)
    if not single_character:
        return jsonify({"error": "Character not found"}), 400
    selected_favorite_character = FavoriteCharacter(user_id=user_id, character_id=character_id)
    db.session.delete(selected_favorite_character)
    db.session.commit()
    return jsonify({"message": "Favorite character deleted successfully"}), 204

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
