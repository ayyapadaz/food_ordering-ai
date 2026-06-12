from flask import Blueprint,jsonify, request
order_bp = Blueprint("order",__name__)

print("order ROUTES LOADED")

from services.order_service import *

@order_bp.route("/orders")
def get_orders():
    return jsonify(get_orders_with_food())

@order_bp.route("/orders/<int:order_id>")
def get_order(order_id):

    order = get_order_by_id(order_id)

    if order:
        return jsonify(order)

    return jsonify({
        "error":"order not found"
    }),404

@order_bp.route("/orders/<int:order_id>/status", methods=["PUT"])
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

@order_bp.route("/users/<int:user_id>/orders")
def get_user_orders(user_id):
      orders = get_orders_by_user(user_id)
      if orders:
            return jsonify(orders)
      else:
            return jsonify({"error":"no orders found for this user"}),404


