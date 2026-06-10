from flask import Flask
from flask import jsonify
from flask import request
from db import  init_db, seed_food
from db import get_all_foods
from db import get_orders_with_food
from db import get_food_by_id
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
from db import get_total_orders
from db import get_total_revenue
from db import get_top_food
from db import get_top_customer,add_restaurants,get_restaurants,get_restaurants_by_id
from db import update_restaurant,delete_restaurant
from db import add_menu_item,get_restaurant_menu,get_menu_by_restaurant
from db import get_cart_by_user
from db import create_cart
from db import get_menu_item_by_id
from db import add_cart_item,get_cart_details,delete_cart_items,update_cart_item
from db import checkout_cart,get_cart_items,clear_cart
from db import update_order_status

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

@app.route("/foods/<int:food_id>")
def get_food(food_id):
    food=get_food_by_id(food_id)
    if food:
        return jsonify(food)
    else:
        return jsonify({"error":"food not found"}),404



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

@app.route("/orders/total")
def get_total_orders_count():
      total = get_total_orders()
      return jsonify({"total_orders": total})

@app.route("/orders/revenue")
def get_revenue():
      revenue = get_total_revenue()
      if revenue is None:
          revenue = 0
      return jsonify({"total_revenue": revenue})

@app.route("/orders/top_food")
def get_topfood():
      top_food = get_top_food()
      if top_food:
          return jsonify(top_food)
      else:
          return jsonify({"error":"no food found"}),404
      

@app.route("/orders/top_customer")
def get_topcustomer():
      top_customer = get_top_customer()
      if top_customer:
          return jsonify(top_customer)
      else:
          return jsonify({"error":"no customer found"}),404

@app.route("/restaurants", methods=["POST"])
def create_restaurant():
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

@app.route("/restaurants", methods=["GET"])
def list_restaurants():
    restaurants = get_restaurants()
    return jsonify(restaurants)

@app.route("/restaurants/<int:restaurant_id>", methods=["GET"])
def get_restaurant(restaurant_id):
    restaurant = get_restaurants_by_id(restaurant_id)
    if restaurant:
        return jsonify(restaurant)
    else:
        return jsonify({"error":"restaurant not found"}),404

@app.route("/restaurants/<int:restaurant_id>", methods=["PUT"])
def modify_restaurant(restaurant_id):

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

@app.route("/restaurants/<int:restaurant_id>", methods=["DELETE"])
def remove_restaurant(restaurant_id):

    deleted = delete_restaurant(restaurant_id)

    if deleted == 0:
        return jsonify({"error":"restaurant not found"}),404

    return jsonify({
        "message":"restaurant deleted successfully"
    })

@app.route("/restaurants/menu", methods=["POST"])
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

@app.route("/restaurants/menu", methods=["GET"])
def list_menu_items():
    menu = get_restaurant_menu()
    return jsonify(menu)

@app.route("/restaurants/<int:restaurant_id>/menu", methods=["GET"])
def list_menu_items_by_restaurant(restaurant_id):
    restaurant = get_restaurants_by_id(restaurant_id)
    if not restaurant:
        return jsonify({"error":"restaurant not found"}),404
    
    menu = get_menu_by_restaurant(restaurant_id)
    if menu:
        return jsonify(menu)
    else:
        return jsonify({"error":"no menu items found for this restaurant"}),404

@app.route("/cart/add", methods=["POST"])
def add_to_cart():

    data = request.get_json()

    if "user_id" not in data:
        return jsonify({"error":"user_id is missing"}),400

    if "menu_id" not in data:
        return jsonify({"error":"menu_id is missing"}),400

    if "quantity" not in data:
        return jsonify({"error":"quantity is missing"}),400

    if data["quantity"] <= 0:
        return jsonify({"error":"quantity is invalid"}),400

    user = get_user_by_id(data["user_id"])

    if not user:
        return jsonify({"error":"user not found"}),404

    menu_item = get_menu_item_by_id(data["menu_id"])

    if not menu_item:
        return jsonify({"error":"menu item not found"}),404

    cart = get_cart_by_user(data["user_id"])
    if cart:
        items = get_cart_items(cart["id"])
        if len(items) == 0:
            clear_cart(cart["id"])   
            cart = None

    restaurant_id = menu_item["restaurant_id"]

    if not cart:

        cart_id = create_cart(
            data["user_id"],
            restaurant_id
        )

    else:

        if cart["restaurant_id"] != restaurant_id:
            return jsonify({
                "error":"cart contains items from another restaurant"
            }),400

        cart_id = cart["id"]

    item_id = add_cart_item(
        cart_id,
        data["menu_id"],
        data["quantity"]
    )

    return jsonify({
        "message":"item added to cart",
        "cart_item_id": item_id
    })

@app.route("/cart/<int:user_id>")
def view_cart(user_id):
    user=get_user_by_id(user_id)
    if not user:
        return jsonify({"error":"user not found"}),404
    rows=get_cart_details(user_id)
    if not rows:
        return jsonify({"error":"cart is empty"}),404
    restaurant_name=rows[0][0]
    items=[]
    cart_total=0
    for row in rows:
        item_total=row[3]*row[4]
        cart_total += item_total

        items.append({"cart_item_id": row[1],
            "food_name": row[2],
            "price": row[3],
            "quantity": row[4],
            "total": item_total})
        
    return jsonify({
        "restaurant": restaurant_name,
        "items": items,
        "cart_total": cart_total})

@app.route("/cart/item/<int:cart_item_id>", methods=["DELETE"])
def remove_cart_item(cart_item_id):
    deleted=delete_cart_items(cart_item_id)
    if deleted ==0:
        return jsonify({"error":"cart item not found"}),404
    return jsonify({"message":"cart item deleted successfully"})

@app.route("/cart/item/<int:cart_item_id>",methods=["PUT"])
def modify_cart_item(cart_item_id):
    data=request.get_json()
    if "quantity" not in data:
        return jsonify({"error":"quantity is missing"}),400
    if data["quantity"]<=0:
        return jsonify({"error":"quantity is invalid"}),400
    
    updated=update_cart_item(cart_item_id,data["quantity"])
    if updated == 0:
        return jsonify({
            "error":"cart item not found"
        }),404

    return jsonify({
        "message":"cart item updated successfully"
    })

@app.route("/cart/checkout/<int:user_id>",methods=["POST"])
def checkout(user_id):
    result=checkout_cart(user_id)
    if not result:
        return jsonify({"error":"cart is empty"}),404
    return jsonify({
        "message": "checkout successful",
        "order_id": result["order_id"],
        "total_amount": result["total_amount"]
    })

@app.route("/orders/<int:order_id>/status", methods=["PUT"])
def change_order_status(order_id):

    data = request.get_json()
    allowed_statuses = [
        "Placed",
        "Confirmed",
        "Preparing",
        "Out for Delivery",
        "Delivered",
        "Cancelled"
    ]
    if data["status"] not in allowed_statuses:
        return jsonify({"error": "invalid status"}), 400

    updated = update_order_status(
        order_id,
        data["status"]
    )
    if updated == 0:
        return jsonify({"error": "order not found"}), 404
    return jsonify({"message": "status updated"})

init_db()
seed_food()
if __name__=="__main__":
    print(app.url_map)
    app.run(debug=True)