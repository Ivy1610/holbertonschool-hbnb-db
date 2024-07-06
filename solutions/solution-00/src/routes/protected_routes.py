# routes/protected_routes.py
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

@app.route('/places', methods=['POST'])
@jwt_required()
def create_place():
    user_id = get_jwt_identity()

@app.route('/places/<place_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def modify_place(place_id):
    user_id = get_jwt_identity()

@app.route('/admin/amenities', methods=['POST', 'DELETE'])
@jwt_required()
def manage_amenities():
    claims = get_jwt()
    si non claims.get('is_admin'):
        return jsonify({"msg": "Droits d'administration requis"}), 403
