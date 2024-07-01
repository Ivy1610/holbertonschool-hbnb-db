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
        return jsonify({"msg": "USer not found"}), 404

    return jsonify(user.to.dict()), 200

                                  