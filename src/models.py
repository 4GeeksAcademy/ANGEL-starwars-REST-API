from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

        
class Film(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  director = db.Column(db.String(255), nullable = False)
  producer = db.Column(db.String(255), nullable = False)
  title = db.Column(db.String(255), nullable = False)
  
  
  def __repr__(self):
    return '<Film %r>' % self.id, self.director, self.producer, self.title
  
  def serialize(self):
    return {
      "id": self.id,
      "director": self.director,
      "producer": self.producer,
      "title": self.title
    }

class People(db.Model):
  id = db.Column(db.Integer, primary_key = True) 
  name = db.Column(db.String(255), nullable = False)
  eye_color = db.Column(db.String(255), nullable = False)
  gender = db.Column(db.String(255), nullable = False)
  
  def __repr__(self):
    return '<People %r>' % self.id, self.name, self.eye_color, self.gender
  
  def serialize(self):
    return {
      "id" : self.id,
      "name" : self.name,
      "eye_color" : self.eye_color,
      "gender" : self.gender,
    }
    
class Planet(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(255), nullable = False)
  climate = db.Column(db.String(255), nullable = False)
  diameter = db.Column(db.String(255), nullable = False)
  

  
  def __repr__(self):
    return '<Planet %r>' % self.id, self.name, self.climate, self.diameter
  
  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "climate": self.climate,
      "diameter": self.diameter
    }

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(255), nullable = False)

  
  def __repr__(self):
    return '<User %r>' % self.id
  
  def serialize(self):
    return {
      "id": self.id,
      "username": self.username
    }
    
class Favorites(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
  people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable = True)
  planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable = True)
  film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable = True)

  def __repr__(self):
    return '<Favorites %r>' % self.id, self.user_id, self.people_id, self.planet_id, self.film_id

  def serialize(self):
    return {
      "id": self.id,
      "user_id": self.user_id,
      "film_id": self.film_id,
      "people_id": self.people_id,
      "planet_id": self.planet_id
    }
  