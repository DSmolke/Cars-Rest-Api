from decimal import Decimal

from flask import Blueprint, Response, jsonify, request
from app.service.configuration import cars_service_instance
from app.service.common_objects import SortOrder

from app.security.configuration import token_required

cars_blueprint = Blueprint('cars', __name__, url_prefix='/cars')

"""
ALL FUNCTIONALITIES ARE DOCUMENTED AT app/service/cars/service
"""
@cars_blueprint.route('/all', methods=['GET'])
@token_required(['USER', 'ADMIN'])
def get_all_cars() -> Response:
    return jsonify(cars_service_instance.all_cars())

@cars_blueprint.route('/all/<string:attr_name>/<string:order>', methods=['GET'])
@token_required(['USER', 'ADMIN'])
def get_all_cars_sorted_by(attr_name: str, order: str) -> Response:
    return jsonify(cars_service_instance.all_sorted_by(attr_name, SortOrder[order.upper()]))

@cars_blueprint.route('/mileage_gt/<int:mileage>', methods=['GET'])
@token_required(['USER', 'ADMIN'])
def get_all_cars_mileage_gt(mileage: int) -> Response:
    return jsonify(cars_service_instance.with_mileage_gt(mileage))

@cars_blueprint.route('/colors_map', methods=['GET'])
@token_required(['USER', 'ADMIN'])
def get_colors_map():
    return jsonify(cars_service_instance.cars_colors_map())

@cars_blueprint.route('/models_most_expensive_car_map', methods=['GET'])
@token_required(['USER', 'ADMIN'])
def get_models_most_expensive_car_map() -> Response:
    return jsonify(cars_service_instance.models_with_most_expensive_cars())

@cars_blueprint.route('/numeric_field_statistics/<string:field_names>', methods=['GET'])
@token_required(['USER', 'ADMIN'])
def get_numeric_fields_statistics(field_names: str) -> Response:
    field_names = field_names.split("&")
    return jsonify(cars_service_instance.get_statistics_for_numeric_fields(field_names))

@cars_blueprint.route('/most_expensive', methods=['GET'])
@token_required(['USER', 'ADMIN'])
def get_most_expensive_cars() -> Response:
    return jsonify(cars_service_instance.most_expensive_cars())

@cars_blueprint.route('/with_sorted_components', methods=['GET'])
@token_required(['USER', 'ADMIN'])
def get_cars_with_sorted_components() -> Response:
    return jsonify(cars_service_instance.cars_with_sorted_components())

@cars_blueprint.route('/with_price_between/<string:price_min>/<string:price_max>/<string:order>', methods=['GET'])
@token_required(['USER', 'ADMIN'])
def get_cars_in_price_range(price_min: str, price_max: str, order: str) -> Response:
    return jsonify(cars_service_instance.cars_with_price_in_range_sorted_by((Decimal(price_min), Decimal(price_max)),
                                                                            SortOrder[order.upper()]))

