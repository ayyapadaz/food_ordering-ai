from flask import Blueprint,jsonify, request
from flask_jwt_extended import jwt_required
food_bp = Blueprint("food",__name__)

from services.auth_utils import admin_required

print("FOOD ROUTES LOADED")

from services.food_service import *

@food_bp.route("/foods")
def foods():
    return jsonify(get_all_foods())

@food_bp.route("/foods/<int:food_id>")
def get_food(food_id):
    food=get_food_by_id(food_id)
    if food:
        return jsonify(food)
    else:
        return jsonify({"error":"food not found"}),404

@food_bp.route("/foods", methods=["POST"])
@jwt_required()
def create_food():
    error=admin_required()
    if error:
        return error

    data = request.get_json()

    if "name" not in data:
        return jsonify({"error":"name is missing"}),400

    if "price" not in data:
        return jsonify({"error":"price is missing"}),400

    if "category" not in data:
        return jsonify({"error":"category is missing"}),400

    food_id = add_food(
        data["name"],
        data["price"],
        data["category"]
    )

    return jsonify({
        "message":"food added successfully",
        "food_id":food_id
    })

@food_bp.route("/foods/<string:category>")
def get_foods_by_cat(category):
    foods=get_foods_by_category(category)
    if foods:
        return jsonify(foods)
    else:
        return jsonify({"error":"no food"}),404
    

@food_bp.route("/foods/<int:food_id>", methods=["PUT"])
@jwt_required()
def modify_food(food_id):
    error=admin_required()
    if error:
        return error

    data = request.get_json()

    if "name" not in data:
        return jsonify({"error":"name is missing"}),400

    if "price" not in data:
        return jsonify({"error":"price is missing"}),400

    if "category" not in data:
        return jsonify({"error":"category is missing"}),400

    updated = update_food(
        food_id,
        data["name"],
        data["price"],
        data["category"]
    )

    if updated == 0:
        return jsonify({"error":"food not found"}),404

    return jsonify({
        "message":"food updated successfully"
    })

@food_bp.route("/foods/<int:food_id>", methods=["DELETE"])
@jwt_required()
def remove_food(food_id):
    error=admin_required()
    if error:
        return error

    deleted = delete_food(food_id)

    if deleted == 0:
        return jsonify({"error":"food not found"}),404

    return jsonify({
        "message":"food deleted successfully"
    })
