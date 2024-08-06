#!/usr/bin/python3
"""Handle view for cities related object."""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import abort, request, jsonify


@app_views.route("/states/<state_id>/cities",
                 methods=["GET", "POST"], strict_slashes=False)
def cities(state_id):
    """Handle request for cities views."""
    states = storage.all(State)

    # GET REQUEST #
    if request.method == "GET":
        key = "State." + state_id
        state = states.get(key)
        print(state)
        if not state:
            abort(404)

        # Return the list of cities in the specified state
        return jsonify([city.to_dict() for city in state.cities])

    # POST REQUEST #
    if request.method == "POST":
        data = request.get_json()
        state = "State." + state_id
        if not data:
            abort(404, "Not a JSON")
        elif not data.get("name"):
            abort(400, "Missing name")
        elif not state:
            abort(404)

        city = City(state_id=state_id, name=data.get("name"))
        return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>",
                 methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def city(city_id):
    """Handle request for city views."""
    cities = storage.all(City)

    # GET REQUEST #
    if request.method == "GET":
        city = cities.get("City." + city_id)
        if not city:
            abort(404)
        return jsonify(city.to_dict())

    # PUT REQUEST #
    if request.method == "PUT":
        data = request.get_json()
        city = cities.get("City." + city_id)
        if not data:
            abort(404, "Not a JSON")
        elif not data.get("name"):
            abort(400, "Missing name")
        elif not city:
            abort(404)
        city.name = data.get("name")
        storage.new(city)
        storage.save()
        storage.close()
        return jsonify(city.to_dict())

    # DELETE REQUEST #
    if request.method == "DELETE":
        city = cities.get("City." + city_id)
        if not city:
            abort(404)
        storage.delete(city)
        storage.save()
        storage.close()
        return jsonify({}), 200
