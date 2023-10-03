from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///starwars.db'
db = SQLAlchemy()
#api = Api(app)

# Define database models
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    gender = db.Column(String(250), nullable=False)
    birth = db.Column(String(250), nullable=False)
    height = db.Column(Integer)
    skin_color = db.Column(String(250), nullable=False)
    mass = db.Column(Integer)
    hair_color = db.Column(String(250), nullable=False)
    eye_color = db.Column(String(250), nullable=False)

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    population = db.Column(Integer)
    terrain = db.Column(String(250), nullable=False)
    climate = db.Column(String(250), nullable=False)
    diameter = db.Column(Integer)
    gravity = db.Column(String(250), nullable=False)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    model = db.Column(String(250), nullable=False)
    cost = db.Column(Integer)
    speed = db.Column(Integer)
    passengers = db.Column(Integer)
    vehicle_class = db.Column(String(250), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    firstname = db.Column(String(250), nullable=False)
    lastname = db.Column(String(250), nullable=False)
    email = db.Column(String(250), nullable=False)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))


