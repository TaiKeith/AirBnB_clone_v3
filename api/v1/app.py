#!/usr/bin/python3
"""Creates a Flask application"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS


# Create a Flask application instance
app = Flask(__name__)

# Register the blueprint app_views
app.register_blueprint(app_views)

# Initialize CORS with the app instance
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """Handles teardown of the app context"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors and return JSON reponse"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)
