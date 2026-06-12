from flask import Blueprint,jsonify, request
cart_bp = Blueprint("cart",__name__)

print("CART ROUTES LOADED")

from services.cart_service import *
from services.user_service import *
from services.restaurant_service import *

@cart_bp.route("/cart/add", methods=["POST"])
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

@cart_bp.route("/cart/<int:user_id>")
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

        items.cart_bpend({"cart_item_id": row[1],
            "food_name": row[2],
            "price": row[3],
            "quantity": row[4],
            "total": item_total})
        
    return jsonify({
        "restaurant": restaurant_name,
        "items": items,
        "cart_total": cart_total})

@cart_bp.route("/cart/item/<int:cart_item_id>", methods=["DELETE"])
def remove_cart_item(cart_item_id):
    deleted=delete_cart_items(cart_item_id)
    if deleted ==0:
        return jsonify({"error":"cart item not found"}),404
    return jsonify({"message":"cart item deleted successfully"})

@cart_bp.route("/cart/item/<int:cart_item_id>",methods=["PUT"])
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

@cart_bp.route("/cart/checkout/<int:user_id>",methods=["POST"])
def checkout(user_id):
    result=checkout_cart(user_id)
    if not result:
        return jsonify({"error":"cart is empty"}),404
    return jsonify({
        "message": "checkout successful",
        "order_id": result["order_id"],
        "total_amount": result["total_amount"]
    })
