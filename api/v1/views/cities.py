#!/usr/bin/python3
"""Handle view for cities related object."""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import abort, request, jsonify


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
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
