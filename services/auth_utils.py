from flask_jwt_extended import get_jwt
from flask import jsonify

def admin_required():
    claims=get_jwt()
    if claims["role"]!="admin":
        return jsonify({"error":"admin access equired"}),403
    return None