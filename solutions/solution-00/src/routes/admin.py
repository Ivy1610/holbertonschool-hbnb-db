# routes/admin.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin/data', methods=['POST', 'DELETE'])
@jwt_required()
def admin_data():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Droits d'administration requis"}), 403
    # Procéder avec la fonctionnalité réservée aux administrateurs
    return jsonify({"msg": "Point de terminaison des données admin accédé"}), 200

