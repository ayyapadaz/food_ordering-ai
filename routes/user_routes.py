from flask import Blueprint,jsonify, request
from flask_jwt_extended import create_access_token
user_bp = Blueprint("users",__name__)

print("USER ROUTES LOADED")

from services.user_service import *

@user_bp.route("/users", methods=["POST"])
def create_user():

    data = request.get_json()

    if "name" not in data:
        return jsonify({"error":"name is missing"}),400

    if "email" not in data:
        return jsonify({"error":"email is missing"}),400

    if "password" not in data:
        return jsonify({"error":"password is missing"}),400

    user_id = add_user(
        data["name"],
        data["email"],
        data["password"]
    )

    return jsonify({
        "message":"user created successfully",
        "user_id":user_id
    }),201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if "email" not in data:
        return jsonify({"error":"email is missing"}),400
    if "password" not in data:
        return jsonify({"error":"password is missing"}),400
    user = verify_user(
        data["email"],
        data["password"])
    if not user:
        return jsonify({
            "error":"invalid email or password"
        }),401
    token = create_access_token(
        identity=str(user["id"]),
        additional_claims={"role": user["role"]})
    return jsonify({
    "message": "login successful",
    "access_token": token,
    "user": {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"]
    }
})



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
