# backend/__init__.py
from pathlib import Path
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_smorest import Api

from .config import Config
from .db import db, init_alembic
from .errors import register_error_handlers
from .api import register_blueprints

def create_app() -> Flask:
    ROOT = Path(__file__).resolve().parent.parent
    ANGULAR_DIST = ROOT / "frontend" / "dist" / "ai-schedule-organizer-angular" / "browser"

    app = Flask(
        __name__,
        static_folder=str(ANGULAR_DIST),
        static_url_path="/",
    )
    app.config.from_object(Config)

    app.config.update(
        API_TITLE="AI Schedule Organizer API",
        API_VERSION="1.0.0",
        OPENAPI_VERSION="3.0.3",
        OPENAPI_URL_PREFIX="/api",
        OPENAPI_SWAGGER_UI_PATH="/docs",
        OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
    )
    api = Api(app)

    db.init_app(app)
    init_alembic(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})


    register_blueprints(app, api)
    register_error_handlers(app)

    @app.get("/api/hello")
    def hello():
        return "Hello World!"

    @app.post("/api/echo")
    def echo():
        from flask import request
        data = request.get_json(silent=True) or {}
        return jsonify({"you_sent": data}), 201

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def spa(path: str):
        if path.startswith("api/"):
            return jsonify({"error": "Not found"}), 404
        try:
            file_path = ANGULAR_DIST / path
            if file_path.is_file():
                return send_from_directory(app.static_folder, path)
            index = ANGULAR_DIST / "index.html"
            if index.is_file():
                return send_from_directory(app.static_folder, "index.html")
        except Exception:
            pass
        return jsonify({"error": "Front-end build not found"}), 404

    return app
