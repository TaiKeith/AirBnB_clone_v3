#!/usr/bin/python3
"""Handle views for User related object.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from models import storage


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/users/<user_id>",
                 methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def users(user_id=None):
    """Handle user object request.
    """
    users = storage.all(User)

    # GET REQUEST #
    if request.method == "GET":
        if not user_id:
            return jsonify([user.to_dict() for user in users.values()])
        user = users.get("User." + user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict())

    # POST REQUEST #
    if request.method == "POST":
        # Check for valid json
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")

        # Check for require filed
        require_field = ["email", "password"]
        for field in require_field:
            if not data.get(field):
                abort(400, f"Missing {field}")
        user = User(**data)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201

    # DELETE REQUEST #
    if request.method == "DELETE":
        user = users.get("User." + user_id)
        if not user:
            abort(404)
        storage.delete(user)
        storage.save()
        storage.close()
        return jsonify({}), 200

    # PUT REQUEST #
    if request.method == "PUT":
        body = request.get_json()
        user = users.get("User." + user_id)
        if not body:
            abort(400, "Not a JSON")
        elif not user:
            abort(404)

        ignore_list = ["id", "email", "create_at", "updated_at"]
        for key, value in body.items():
            if key not in ignore_list:
                setattr(user, key, value)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201
