from flask import Blueprint,jsonify, request
restaurant_bp = Blueprint("restaurant",__name__)

print("RESTAURANT ROUTES LOADED")

from services.restaurant_service import *
from services.food_service import *
from flask_jwt_extended import jwt_required
from services.auth_utils import admin_required


@restaurant_bp.route("/restaurants", methods=["POST"])
@jwt_required()
def create_restaurant():
    error=admin_required()
    if error:
        return error
    data = request.get_json()

    if "name" not in data:
        return jsonify({"error":"name is missing"}),400

    if "cuisine" not in data:
        return jsonify({"error":"cuisine is missing"}),400

    if "rating" not in data:
        return jsonify({"error":"rating is missing"}),400

    restaurant_id = add_restaurants(
        data["name"],
        data["cuisine"],
        data["rating"]
    )

    return jsonify({
        "message":"restaurant added successfully",
        "restaurant_id":restaurant_id
    })

@restaurant_bp.route("/restaurants", methods=["GET"])
def list_restaurants():
    restaurants = get_restaurants()
    return jsonify(restaurants)

@restaurant_bp.route("/restaurants/<int:restaurant_id>", methods=["GET"])
def get_restaurant(restaurant_id):
    restaurant = get_restaurants_by_id(restaurant_id)
    if restaurant:
        return jsonify(restaurant)
    else:
        return jsonify({"error":"restaurant not found"}),404

@restaurant_bp.route("/restaurants/<int:restaurant_id>", methods=["PUT"])
@jwt_required()
def modify_restaurant(restaurant_id):
    error=admin_required()
    if error:
        return error

    data = request.get_json()

    if "name" not in data:
        return jsonify({"error":"name is missing"}),400

    if "cuisine" not in data:
        return jsonify({"error":"cuisine is missing"}),400

    if "rating" not in data:
        return jsonify({"error":"rating is missing"}),400

    updated = update_restaurant(
        restaurant_id,
        data["name"],
        data["cuisine"],
        data["rating"]
    )

    if updated == 0:
        return jsonify({"error":"restaurant not found"}),404

    return jsonify({
        "message":"restaurant updated successfully"
    })

@restaurant_bp.route("/restaurants/<int:restaurant_id>", methods=["DELETE"])
@jwt_required()
def remove_restaurant(restaurant_id):
    error=admin_required()
    if error:
        return error

    deleted = delete_restaurant(restaurant_id)

    if deleted == 0:
        return jsonify({"error":"restaurant not found"}),404

    return jsonify({
        "message":"restaurant deleted successfully"
    })

@restaurant_bp.route("/restaurants/menu", methods=["POST"])
def add_menu_item_route():
    data = request.get_json()
    if "restaurant_id" not in data:
            return jsonify({"error":"restaurant_id is missing"}),400
    
    restaurant = get_restaurants_by_id(data["restaurant_id"])
    if not restaurant:
            return jsonify({"error":"restaurant not found"}),404

    if "food_id" not in data:
        return jsonify({"error":"food_id is missing"}),400
    food = get_food_by_id(data["food_id"])
    if not food:
        return jsonify({"error":"food not found"}),404

    if "price" not in data:
        return jsonify({"error":"price is missing"}),400

    menu_id = add_menu_item(
        data["restaurant_id"],
        data["food_id"],
        data["price"]
    )

    return jsonify({
        "message":"menu item added successfully",
        "menu_id": menu_id
    })

@restaurant_bp.route("/restaurants/menu", methods=["GET"])
def list_menu_items():
    menu = get_restaurant_menu()
    return jsonify(menu)

@restaurant_bp.route("/restaurants/<int:restaurant_id>/menu", methods=["GET"])
def list_menu_items_by_restaurant(restaurant_id):
    restaurant = get_restaurants_by_id(restaurant_id)
    if not restaurant:
        return jsonify({"error":"restaurant not found"}),404
    
    menu = get_menu_by_restaurant(restaurant_id)
    if menu:
        return jsonify(menu)
    else:
        return jsonify({"error":"no menu items found for this restaurant"}),404
