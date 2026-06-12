from flask import Blueprint,jsonify, request
user_bp = Blueprint("users",__name__)

print("USER ROUTES LOADED")

from services.user_service import (
    add_user,
    get_user,
    get_user_by_id,
    update_user,
    delete_user
)

@user_bp.route("/users",methods=["POST"])
def create_user():
    data=request.get_json()
    if "name" not in data:
        return jsonify({"error":"name is missing"}),400
    if "email" not in data:
        return jsonify({"error":"email is missing"}),400
    user_id=add_user(data["name"],data["email"])
    return jsonify({"message":"user created successfully","user_id":user_id})

@user_bp.route("/users",methods=["GET"])
def list_users():
    users=get_user()
    return jsonify(users)

@user_bp.route("/users/<int:user_id>")
def get_user_detail(user_id):
    user=get_user_by_id(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error":"user not found"}),404

@user_bp.route("/users/<int:user_id>",methods=["PUT"])
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

@user_bp.route("/users/<int:user_id>",methods=["DELETE"])
def remove_user(user_id):
    deleted=delete_user(user_id)
    if deleted ==0:
        return jsonify({"error":"user not found"}),404
    else:
        return jsonify({"message":"user deleted successfully"})
