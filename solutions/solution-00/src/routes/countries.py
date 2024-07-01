"""
This module contains the routes for the countries endpoint
"""

from flask import Blueprint
from src.controllers.countries import (
    get_countries,
    get_country_by_code,
    get_country_cities,
)

countries_bp = Blueprint("countries", __name__, url_prefix="/countries")

@countries_bp.route("/", methods=["GET"])
def get_all_countries():
    return get_countries()

@countries_bp.route("/<code>", methods=["GET"])
def get_country(code):
    return get_country_by_code(code)

@countries_bp.route("/<code>/cities", methods=["GET"])
def get_country_cities_by_code(code):
    return get_country_cities(code)