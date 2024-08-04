#!/usr/bin/python3
"""views to handle API action of Stae class
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states/<state_id>",
                 methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
@app_views.route("/states", methods=["GET", "POST"],
                 strict_slashes=False)
def get_state(state_id=None):
    """Retrieved all state in database
    """
    # Get the key/value pair of state object in db
    states = storage.all(State)

    # GET REQUESTS #
    if request.method == "GET":

        # Return all state if no state_id is pass arg
        if not state_id:
            return jsonify([state.to_dict() for state in states.values()])

        # If state_id is pass as arg
        key = "State." + state_id
        if not states.get(key):
            abort(404)
        return jsonify(states.get(key).to_dict())

    # DELETE REQUESTS #
    if request.method == "DELETE":
        state = states.get("State." + state_id)

        if not state:
            abort(404)
        storage.delete(state)
        storage.save()
        storage.close()
        return jsonify({}), 200

    #  POST REQUESTS #
    if request.method == "POST":
        data = request.get_json()

        # Check if request_body is valid json
        if not data:
            abort(400, "Not a JSON")

        # Try to retrieved name field
        if not data.get("name"):
            abort(400, "Missing name")

        state = State(name=data.get("name"))
        storage.new(state)
        storage.save()
        storage.close()
        return jsonify(state.to_dict()), 201

    # PUT REQUESTS #
    if request.method == "PUT":
        data = request.get_json()
        key = "State." + state_id
        state = states.get(key)

        if not data:
            abort(400, "Not a JSON")
        elif not state:
            abort(404)
        elif not data.get("name"):
            abort(400, "Missing name")

        state.name = data.get("name")
        storage.new(state)
        storage.save()
        storage.close()
        return jsonify(state.to_dict())
