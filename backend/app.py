from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import os

# --- Paths ---
ROOT = Path(__file__).resolve().parent.parent  # project root (../)
ANGULAR_DIST = ROOT / "frontend" / "dist" / "ai-schedule-organizer-angular" / "browser"

# Safety check: helpful in dev if you forgot to build Angular
if not ANGULAR_DIST.exists():
    raise RuntimeError(
        f"Angular build not found at {ANGULAR_DIST}. "
        f"Run 'cd frontend && npm ci && npm run build' first."
    )

# --- Flask app configured to serve Angular build ---
app = Flask(
    __name__,
    static_folder=str(ANGULAR_DIST),  # serve Angular's built assets
    static_url_path="/"               # mount at root
)

# --------------------- API ROUTES ---------------------
# Your original endpoint moved under /api so Angular can own "/"
@app.route('/api/hello')
def hello_world():
    return 'Hello World!'

# Example JSON API (you can delete if not needed)
@app.post('/api/echo')
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"you_sent": data}), 201

# ------------------- SPA FALLBACK ---------------------
# Serve Angular files for all non-/api routes.
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def spa(path):
    # Keep API namespace reserved
    if path.startswith("api/"):
        return jsonify({"error": "Not found"}), 404

    # If the requested file exists (e.g., main.js, styles.css), serve it
    file_path = ANGULAR_DIST / path
    if file_path.is_file():
        return send_from_directory(app.static_folder, path)

    # Otherwise, serve index.html so Angular Router can handle the route
    return send_from_directory(app.static_folder, "index.html")

# --------------------- DEV RUNNER ---------------------
if __name__ == '__main__':
    port = int(os.getenv("PORT", "7680"))
    app.run(host="0.0.0.0", port=port, debug=True)
