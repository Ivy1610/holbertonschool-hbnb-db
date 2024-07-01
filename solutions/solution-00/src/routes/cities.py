"""
This module contains the routes for the cities blueprint
"""

from flask import Blueprint
from src.controllers.cities import (
    create_city,
    delete_city,
    get_city_by_id,
    get_cities,
    update_city,
)

cities_bp = Blueprint("cities", __name__, url_prefix="/cities")

@cities_bp.route("/", methods=["GET"])
def retrieve_cities():
    return get_cities()

@cities_bp.route("/", methods=["POST"])
def add_city(city_id):
    return create_city()

@cities_bp.route("/<city_id>", methods=["GET"])
def retrieve_city(city_id):
    return get_city_by_id(city_id)

@cities_bp.route("/<city_id>", methods=["PUT"])
def modify_city(city_id):
    return update_city(city_id)

@cities_bp.route("/<city_id>", methods=["DELETE"])
def remove_city(city_id):
    return delete_city(city_id)