from flask import Flask
from flask import jsonify
from flask import request
from db import init_db, seed_food,add_orders,get_order_db
from db import get_all_foods


app=Flask(__name__)


@app.route("/")
def home():
    return "Food ordering API"

@app.route("/menu")
def menu():
    return jsonify(get_all_foods())

@app.route("/orders")
def get_orders():
    return jsonify(get_order_db())

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



init_db()
seed_food()
if __name__=="__main__":
    app.run(debug=True)