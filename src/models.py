from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250))
    email = db.Column(db.String(250), unique=True)
    subscription_date = db.Column(db.Date, nullable=False)

    # login = db.relationship("Login", back_populates="user")
    favorite_planets = db.relationship("FavoritePlanet", back_populates="user")
    favorite_characters = db.relationship("FavoriteCharacter", back_populates="user")
    favorite_vehicles = db.relationship("FavoriteVehicle", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.first_name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "subscription_date": self.subscription_date
        }
    
    def serialize_favorites(self):
        result = {}
        result['favorites'] = {}
        result["user"] = self.serialize()
        if len(self.favorite_characters) > 0:
            result["favorites"]["characters"] = [character.character.serialize() for character in self.favorite_characters] 
        if len(self.favorite_vehicles) > 0:
            result["favorites"]["vehicles"] = [vehicle.vehicle.serialize() for vehicle in self.favorite_vehicles] 
        if len(self.favorite_planets) > 0:
            result["favorites"]["planets"] = [planet.planet.serialize() for planet in self.favorite_planets] 
        return result

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    population = db.Column(db.BigInteger, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.Float, nullable=False)
    terrain = db.Column(db.String(250))
    surface_water = db.Column(db.Float, nullable=False)
    climate = db.Column(db.String(250))
    favorite_planets = db.relationship("FavoritePlanet", back_populates="planet")


    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "climate": self.climate
        }
class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    species = db.Column(db.String(250))
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    favorite_characters = db.relationship("FavoriteCharacter", back_populates="character")

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species":self.species,
            "height":self.height,
            "mass":self.mass,
            "gender":self.gender,
            "hair_color":self.hair_color,
            "skin_color":self.skin_color
        }
    
class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    model = db.Column(db.String(250))
    manufacturer = db.Column(db.String(250))
    class_vehicle = db.Column(db.String(250))
    cost = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Float, nullable=False)
    cargo_capacity = db.Column(db.Integer, nullable=False)
    minimum_crew = db.Column(db.Integer, nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    favorite_vehicles = db.relationship("FavoriteVehicle", back_populates="vehicle")

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model":self.model,
            "manufacturer":self.manufacturer,
            "class_vehicle":self.class_vehicle,
            "cost":self.cost,
            "speed":self.speed,
            "length":self.length,
            "cargo_capacity":self.cargo_capacity,
            "minimum_crew":self.minimum_crew,
            "passengers":self.passengers
        }
class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)

    user = db.relationship("User", back_populates="favorite_planets")
    planet = db.relationship("Planet")

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.id

class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_character'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)

    user = db.relationship("User", back_populates="favorite_characters")
    character = db.relationship("Character")

    def __repr__(self):
        return '<FavoriteCharacter %r>' % self.id

class FavoriteVehicle(db.Model):
    __tablename__ = 'favorite_vehicle'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)

    user = db.relationship("User", back_populates="favorite_vehicles")
    vehicle = db.relationship("Vehicle")

    def __repr__(self):
        return '<FavoriteVehicle %r>' % self.id
