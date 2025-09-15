from flask import jsonify

class BadRequest(Exception):
    def __init__(self, message="Bad Request"):
        self.message = message

class NotFound(Exception):
    def __init__(self, message="Not Found"):
        self.message = message

def register_error_handlers(app):
    @app.errorhandler(BadRequest)
    def _bad_request(e):
        return jsonify({"error": e.message}), 400

    @app.errorhandler(NotFound)
    def _not_found(e):
        return jsonify({"error": e.message}), 404

    @app.errorhandler(422)
    def _unprocessable(_):
        return jsonify({"error": "Unprocessable entity"}), 422

    @app.errorhandler(500)
    def _server(_):
        return jsonify({"error": "Internal server error"}), 500
