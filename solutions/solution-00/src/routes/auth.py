from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from src.models.user import User
from src.persistence.sqlalchemy_repository import SQLAlchemyRepository

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"mgs": "Missing email or password"}), 400
    
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        access_token = create_access_token(identify=user.id)
        return jsonify(access_token=access_token), 200
    
    return jsonify({"mgs": "Invalide credentials"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')

    if not email or not first_name or not last_name or not password:
        return jsonify({"msg": "Missing data"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 400
    
    user_data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'password': password
    }

    try:
        user = User.create(user_data)
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    
    access_token =create_access_token(identify=user.id)
    return jsonify(access_token=access_token), 201