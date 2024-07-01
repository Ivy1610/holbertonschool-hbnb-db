"""
This module contains the routes for the places blueprint
"""

from flask import Blueprint
from src.controllers.places import (
    create_place,
    delete_place,
    get_place_by_id,
    get_places,
    update_place,
)

places_bp = Blueprint("places", __name__, url_prefix="/places")

@places_bp.route("/", methods=["GET"])
def list_places():
    return get_places()

@places_bp.route("/", methods=["POST"])
def add_place():
    return create_place()

@places_bp.route("/<place_id>", methods=["GET"])
def retrieve_place(place_id):
    return get_place_by_id(place_id)

@places_bp.route("/<place_id>", methods=["PUT"])
def modify_place(place_id):
    return update_place(place_id)

@places_bp.route("/<place_id>", methods=["DELETE"])
def remove_place(place_id):
    return delete_place(place_id)
