from flask import Blueprint,jsonify, request
analytics_bp = Blueprint("analytics",__name__)

print("analytics ROUTES LOADED")

from services.analytics_service import *

@analytics_bp.route("/orders/total")
def get_total_orders_count():
      total = get_total_orders()
      return jsonify({"total_orders": total})

@analytics_bp.route("/orders/revenue")
def get_revenue():
      revenue = get_total_revenue()
      if revenue is None:
          revenue = 0
      return jsonify({"total_revenue": revenue})

@analytics_bp.route("/orders/top_food")
def get_topfood():
      top_food = get_top_food()
      if top_food:
          return jsonify(top_food)
      else:
          return jsonify({"error":"no food found"}),404
      

@analytics_bp.route("/orders/top_customer")
def get_topcustomer():
      top_customer = get_top_customer()
      if top_customer:
          return jsonify(top_customer)
      else:
          return jsonify({"error":"no customer found"}),404
