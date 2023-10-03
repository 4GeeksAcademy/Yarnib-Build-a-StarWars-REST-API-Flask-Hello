"""characters
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, People, Planet, Vehicle, User, Favorite

api = Blueprint('api', __name__)

# Define your new routes and endpoints here

@api.route('/characters', methods=['GET'])
def get_characters():
    people = People.query.all()
    return jsonify([person.name for person in people])

@api.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.name for planet in planets])

@api.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.name for vehicle in vehicles])

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.username for user in users])

@api.route('/favorites/<string:category>/<int:item_id>', methods=['GET', 'POST', 'DELETE'])
@jwt_required()  # Requires authentication (JWT)
def manage_favorites(category, item_id):
    # Get the current user's identity from the JWT token
    current_user = get_jwt_identity()

    # Check if the provided category is valid (e.g., 'planets', 'characters', 'vehicles')
    valid_categories = ['planets', 'characters', 'vehicles']
    if category not in valid_categories:
        return jsonify({"error": "Invalid category"}), 400

    if request.method == 'GET':
        # Implement logic to retrieve favorites for the current user
        user_favorites = Favorite.query.filter_by(user_id=current_user['id'], category=category).all()
        
        # Create a list of favorite items (e.g., planet names, character names)
        favorites = []
        for favorite in user_favorites:
            item = None
            if category == 'planets':
                item = Planet.query.get(favorite.item_id)
            elif category == 'characters':
                item = People.query.get(favorite.item_id)
            elif category == 'vehicles':
                item = Vehicle.query.get(favorite.item_id)
            
            if item:
                favorites.append({"category": category, "name": item.name})
        
        return jsonify(favorites)

    elif request.method == 'POST':
        # Check if the item with the given ID exists in the specified category
        item = None
        if category == 'planets':
            item = Planet.query.get(item_id)
        elif category == 'characters':
            item = People.query.get(item_id)
        elif category == 'vehicles':
            item = Vehicle.query.get(item_id)
        
        if not item:
            return jsonify({"error": "Item not found"}), 404
        
        # Add the item as a favorite for the current user
        favorite = Favorite(user_id=current_user['id'], category=category, item_id=item_id)
        db.session.add(favorite)
        db.session.commit()
        
        return jsonify({"message": "Favorite added"})

    elif request.method == 'DELETE':
        # Check if the item with the given ID exists in the specified category
        item = None
        if category == 'planets':
            item = Planet.query.get(item_id)
        elif category == 'characters':
            item = People.query.get(item_id)
        elif category == 'vehicles':
            item = Vehicle.query.get(item_id)
        
        if not item:
            return jsonify({"error": "Item not found"}), 404
        
        # Check if the item is in the user's favorites
        favorite = Favorite.query.filter_by(user_id=current_user['id'], category=category, item_id=item_id).first()
        if not favorite:
            return jsonify({"error": "Favorite not found"}), 404
        
        # Delete the favorite item for the current user
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({"message": "Favorite deleted"})

# Add more routes and endpoints as needed

