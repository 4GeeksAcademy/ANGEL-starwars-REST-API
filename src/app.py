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
from models import db, User, Film, People, Planet, Favorites
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

#USER
# return all users from the database
@app.route('/user', methods=['GET'])
def list_all_users():
  try:
    users = User.query.all()
    results = list(map(lambda user: user.serialize(), users))
    response_body = {
      "results": results
    }
    return jsonify(response_body), 200
  except:
    return jsonify({"error": "Error fetching users data"}), 400

# return one user from the database
@app.route('/user/<int:id>', methods=['GET'])
def list_one_user(id):
  try:
    user = User.query.filter(User.id == id).first()
    return jsonify(user.serialize()), 200
  except:
    return jsonify({"error": f"User with id {id} not found"}), 400

# add one user to database
@app.route('/user', methods=['POST'])
def add_user():
  try:
    user_data = request.json
    
    new_user = User(
      username = user_data['username'],
    )
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 200
  except:
    return jsonify({"error": "User cannot be added"}), 400

# update one user from database
@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
  try:
    user_to_update = User.query.get(id)
    if not user_to_update:
      return jsonify({"error": f"User with id {id} not found"}), 404
    
    user_data = request.json
    
    if 'username' in user_data:
      user_to_update.username = user_data['username']
    if 'email' in user_data:
      user_to_update.email = user_data['email']
    if 'password' in user_data:
      user_to_update.password = user_data['password']
    
    db.session.commit()
    return jsonify(user_to_update.serialize()), 200
  except:
    return jsonify({"error": f"User with id {id} cannot be updated"}), 400

# delete one user from database
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
  try:
    user_to_delete = User.query.get(id)
    if not user_to_delete:
      return jsonify({"error": f"User with id {id} not found"}), 404
    
    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({"success": f"User with id {id} deleted"}), 200
  except:
    return jsonify({"error": f"User with id {id} cannot be deleted"}), 400

#FILM
# return all films from the database
@app.route('/film', methods=['GET'])
def list_all_films():
  try:
    films = Film.query.all()
    results = list(map(lambda film: film.serialize(), films))
    response_body = {
      "results": results
    }
    return jsonify(response_body), 200
  except:
    return jsonify({"error": "Error fetching films data"}), 400

# return one film from the database
@app.route('/film/<int:id>', methods=['GET'])
def list_one_film(id):
  try:
    film = Film.query.filter(Film.id == id).first()
    return jsonify(film.serialize())
  except:
    return jsonify({"error": f"Film with id {id} not found"})

# add one film to database
@app.route('/film/', methods=['POST'])
def add_film():
  try:
    film_data = request.json
    
    new_film = Film(
      director = film_data['director'],
      producer = film_data['producer'],
      title = film_data['title']
    )
    
    db.session.add(new_film)
    db.session.commit()
    return jsonify(new_film.serialize()), 200
  except:
    return jsonify({"error": "Film cannot be added"}), 400

# update one film from database
@app.route('/film/<int:id>', methods=['PUT'])
def update_film(id):
  try:
    film_to_update = Film.query.get(id)
    if not film_to_update:
      return jsonify({"error": f"Film with id {id} not found"}), 404
    
    film_data = request.json
    
    if 'director' in film_data:
      film_to_update.director = film_data['director']
    if 'producer' in film_data:
      film_to_update.producer = film_data['producer']
    if 'title' in film_data:
      film_to_update.title = film_data['title']
    
    db.session.commit()
    return jsonify(film_to_update.serialize()), 200
  except:
    return jsonify({"error": f"Film with id {id} cannot be updated"}), 400

# delete one film from database
@app.route('/film/<int:id>', methods=['DELETE'])
def delete_film(id):
  try:
    film_to_delete = Film.query.get(id)
    if not film_to_delete:
      return jsonify({"error": f"Film with id {id} not found"}), 404
    
    db.session.delete(film_to_delete)
    db.session.commit()
    return jsonify({"success": f"Film with id {id} deleted"}), 200
  except:
    return jsonify({"error": f"Film with id {id} cannot be deleted"}), 400

#PEOPLE
# return all characters from the database
@app.route('/people', methods=['GET'])
def list_all_people():
  try:
    people = People.query.all()
    results = list(map(lambda people: people.serialize(), people))
    request_body = {
      "results" : results
    }
    return jsonify(request_body), 200
  except:
    return jsonify({"error": "Error fetching people data"}), 400
  
# return one character from the database
@app.route('/people/<int:id>', methods=['GET'])
def list_one_character(id):
  try:
    character = People.query.filter(People.id == id).first()
    return jsonify(character.serialize()), 200
  except:
    return jsonify({"error": f"Character with id {id} not found"}), 400

# add one character to database
@app.route('/people', methods=['POST'])
def add_people():
  try:
    character_data = request.json
    new_character = People(
      name = character_data['name'],
      eye_color = character_data['eye_color'],
      gender = character_data['gender'],
    )
    
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 200
  except: 
    return jsonify({"eroror": "Film cannot be added"}), 400
  
# update one character from database
@app.route('/people/<int:id>', methods=['PUT'])
def update_people(id):
  try:
    character_to_update = People.query.get(id)
    if not character_to_update:
      return jsonify({"error": f"Character with id {id} not found"}), 404
    
    character_data = request.json
    
    if 'name' in  character_data:
      character_to_update.name = character_data['name']
    if 'eye_color' in character_data:
      character_to_update.eye_color = character_data['eye_color']
    if 'gender' in character_data:
      character_to_update.gender = character_data['gender']
    
    db.session.commit()
    return jsonify(character_to_update.serialize()), 200
  except:
    return jsonify({"error": f"Character with id {id} cannot be updated"}), 400

# delete one character from database
@app.route('/people/<int:id>', methods=['DELETE'])
def delete_people(id):
  try:
    character_to_delete = People.query.get(id)
    if not character_to_delete:
      return jsonify({"error": f"Character with id {id} not found"}), 404
    
    db.session.delete(character_to_delete)
    db.session.commit()
    return jsonify({"success": f"Character with id {id} deleted"}), 200
  except:
    return jsonify({"error": f"Character with id {id} cannot be deleted"}), 400

#PLANET
# return all planets from database
@app.route('/planet', methods=['GET'])
def list_all_planets():
  try:
    planets = Planet.query.all()
    results = list(map(lambda planet: planet.serialize(), planets))
    resquest_body = {
      "results": results
    }
    return jsonify(resquest_body), 200
  except:
    return jsonify({"error": "Error fetching planets data"}), 400
  
#return one planet from database
@app.route('/planet/<int:id>', methods=['GET'])
def list_one_planet(id):
  try:
    planet = Planet.query.filter(Planet.id == id).first()
    return jsonify(planet.serialize()), 200
  except:
    return({"error": f"Planet with id {id} not found"}), 400

# add one planet to database
@app.route('/planet', methods=['POST'])
def add_planet():
  try:
    planet_data = request.json
    
    new_planet = Planet(
      name = planet_data['name'],
      climate = planet_data['climate'],
      diameter = planet_data['diameter'],
    )
    
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 200
  except:
    return jsonify({"error": "Planet cannot be dded"}), 400

# update one planet from database
@app.route('/planet/<int:id>', methods=['PUT'])
def update_planet(id):
  try:
    planet_to_update = Planet.query.get(id)
    if not planet_to_update:
      return jsonify({"error": f"Planet with id {id} not found"}), 404
    
    planet_data = request.json
    
    if 'name' in planet_data:
      planet_to_update.name = planet_data['name']
    if 'climate' in planet_data:
      planet_to_update.climate = planet_data['climate']
    if 'diameter' in planet_data:
      planet_to_update.diameter = planet_data['diameter']
    
    db.session.commit()
    return jsonify(planet_to_update.serialize()), 200
  except:
    return jsonify({"error": f"Planet with id {id} cannot be updated"}), 400

# delete one planet from database
@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
  try:
    planet_to_delete = Planet.query.get(id)
    if not planet_to_delete:
      return jsonify({"error": f"Planet with id {id} not found"}), 404
    
    db.session.delete(planet_to_delete)
    db.session.commit()
    return jsonify({"success": f"Planet with id {id} deleted"}), 200
  except:
    return jsonify({"error": f"Planet with id {id} cannot be deleted"}), 400
  
#FAVORITES
# return all the favorites from one user
@app.route('/favorites/<int:id>', methods=['GET'])
def list_all_favorites(id):
  try:
    favorites = Favorites.query.filter(Favorites.user_id == id).all()
    results = list(map(lambda favorite: favorite.serialize(), favorites))
    response_body = {
      "results": results
    }
    return jsonify(response_body), 200
  except:
    return jsonify({"error": "Error fetching favorites data"}), 400

# add one favorite from one user to database
@app.route('/favorites/<int:id>', methods=['POST'])
def add_favorite(id):
  try:
    favorite_data = request.json
    
    if not favorite_data.get('people_id') and not favorite_data.get('planet_id') and not favorite_data.get('film_id'):
            return jsonify({"error": "At least one of 'people_id', 'planet_id', or 'film_id' must be provided"}), 400
    
    new_favorite = Favorites(
      user_id = id,
      people_id = favorite_data.get('people_id'),
      planet_id = favorite_data.get('planet_id'),
      film_id = favorite_data.get('film_id')
    )
    
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201
  except:
    return jsonify({"error": "Favorite cannot be added"}), 400





  
      
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
