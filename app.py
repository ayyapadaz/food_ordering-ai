from flask import Flask
from flask import jsonify
from flask import request
from db import init_db, seed_food,add_orders,get_order_db
from db import get_all_foods
from db import get_orders_with_food
from db import get_food_by_id
from db import delete_order
from db import update_order

app=Flask(__name__)


@app.route("/")
def home():
    return "Food ordering API"

@app.route("/menu")
def menu():
    return jsonify(get_all_foods())

@app.route("/orders")
def get_orders():
    return jsonify(get_orders_with_food())

@app.route("/order", methods=["POST"])
def place_order():

    data =request.get_json()

    if "food_id" not in data:
        return jsonify({"error":"food_id is missing"}),400
    
    if "quantity" not in data:
        return jsonify({"error":"quantity is missing"}),400
    
    if data["quantity"] <=0:
        return jsonify({"error":"quantity is invalid"}),400   
    if "user_id" not in data:
        return jsonify({
        "error":"user_id is missing"
    }),400

    print("Received Order:", data)


    order_id=add_orders(data["user_id"], data["food_id"], data["quantity"])
    return jsonify({"message":"order placed successfully", "order_id":order_id})

@app.route("/foods/<int:food_id>")
def get_food(food_id):
    food=get_food_by_id(food_id)
    if food:
        return jsonify(food)
    else:
        return jsonify({"error":"food not found"}),404


@app.route("/orders/<int:order_id>", methods=["DELETE"])
def remove_order(order_id):
    deleted=delete_order(order_id)
    if deleted == 0:
        return jsonify({"error":"order not found"}),404
    else:
        return jsonify({"message":"order deleted successfully"})

@app.route("/orders/<int:order_id>", methods=["PUT"])
def modify_order(order_id):
    data=request.get_json()

    if "quantity" not in data:
        return jsonify({"error":"quantity is missing"}),400
    if data["quantity"] <=0:
        return jsonify({"error":"quantity is invalid"}),400
    
    updated=update_order(order_id, data["quantity"])
    if updated ==0:
        return jsonify({"error":"order not found"}),404
    else:
        return jsonify({"message":"order updated successfully"})

init_db()
seed_food()
if __name__=="__main__":
    app.run(debug=True)