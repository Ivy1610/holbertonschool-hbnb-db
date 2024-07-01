from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User

protected_bp = Blueprint('proteced', __name__)

@protected_bp.route('/profile', metods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify(user.to.dict()), 200

@protected_bp.route('admin', methods=['GET'])
@jwt_required()
def admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return jsonify({"msg": "Admin access required"}), 403
    
    return jsonify({"msg": "Welcome, admin!"}), 200