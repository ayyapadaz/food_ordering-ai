from flask import Blueprint,jsonify, request
food_bp = Blueprint("food",__name__)

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
def create_food():

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
def modify_food(food_id):

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
def remove_food(food_id):

    deleted = delete_food(food_id)

    if deleted == 0:
        return jsonify({"error":"food not found"}),404

    return jsonify({
        "message":"food deleted successfully"
    })
