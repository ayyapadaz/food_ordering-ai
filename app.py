from flask import Flask
from flask import jsonify
from flask import request
from db import init_db, seed_food,add_orders,get_order_db
from db import get_all_foods
from db import get_orders_with_food
from db import get_food_by_id
from db import delete_order
from db import update_order
from db import add_user
from db import get_user
from db import get_user_by_id
from db import update_user
from db import delete_user
from db import get_order_by_id
from db import add_food
from db import get_foods_by_category
from db import update_food
from db import delete_food  
from db import get_orders_by_user

app=Flask(__name__)


@app.route("/")
def home():
    return "Food ordering API"

@app.route("/foods")
def foods():
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

    food = get_food_by_id(data["food_id"])
    if not food:
        return jsonify({
        "error":"food not found"}),404
    
    user = get_user_by_id(data["user_id"])
    
    if not user:
        return jsonify({
        "error":"user not found"
    }),404
    
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

@app.route("/users",methods=["POST"])
def create_user():
    data=request.get_json()
    if "name" not in data:
        return jsonify({"error":"name is missing"}),400
    if "email" not in data:
        return jsonify({"error":"email is missing"}),400
    user_id=add_user(data["name"],data["email"])
    return jsonify({"message":"user created successfully","user_id":user_id})

@app.route("/users",methods=["GET"])
def list_users():
    users=get_user()
    return jsonify(users)

@app.route("/users/<int:user_id>")
def get_user_detail(user_id):
    user=get_user_by_id(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error":"user not found"}),404

@app.route("/users/<int:user_id>",methods=["PUT"])
def modify_user(user_id):
    data=request.get_json()
    if "name" not in data:
        return jsonify({"error":"name is missing"}),400

    if "email" not in data:
        return jsonify({"error":"email is missing"}),400

    updated=update_user(user_id, data["name"], data["email"])
    if updated ==0:
        return jsonify({"error":"user not found"}),404
    else:
        return jsonify({"message":"user updated successfully"})

@app.route("/users/<int:user_id>",methods=["DELETE"])
def remove_user(user_id):
    deleted=delete_user(user_id)
    if deleted ==0:
        return jsonify({"error":"user not found"}),404
    else:
        return jsonify({"message":"user deleted successfully"})

@app.route("/orders/<int:order_id>")
def get_order(order_id):

    order = get_order_by_id(order_id)

    if order:
        return jsonify(order)

    return jsonify({
        "error":"order not found"
    }),404

@app.route("/foods", methods=["POST"])
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

@app.route("/foods/<string:category>")
def get_foods_by_cat(category):
    foods=get_foods_by_category(category)
    if foods:
        return jsonify(foods)
    else:
        return jsonify({"error":"no food"}),404
    

@app.route("/foods/<int:food_id>", methods=["PUT"])
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

@app.route("/foods/<int:food_id>", methods=["DELETE"])
def remove_food(food_id):

    deleted = delete_food(food_id)

    if deleted == 0:
        return jsonify({"error":"food not found"}),404

    return jsonify({
        "message":"food deleted successfully"
    })

@app.route("/users/<int:user_id>/orders")
def get_user_orders(user_id):
      orders = get_orders_by_user(user_id)
      if orders:
            return jsonify(orders)
      else:
            return jsonify({"error":"no orders found for this user"}),404


init_db()
seed_food()
if __name__=="__main__":
    app.run(debug=True)