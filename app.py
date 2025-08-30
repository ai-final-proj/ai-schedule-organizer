from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import os

# --- Paths ---
ROOT = Path(__file__).resolve().parent  # root = AiScheduleOrganizer/
ANGULAR_DIST = ROOT / "frontend" / "dist" / "ai-schedule-organizer-angular" / "browser"

# Safety check
if not ANGULAR_DIST.exists():
    raise RuntimeError(
        f"Angular build not found at {ANGULAR_DIST}. "
        f"Run 'cd frontend && npm ci && npm run build' first."
    )

# --- Flask app ---
app = Flask(
    __name__,
    static_folder=str(ANGULAR_DIST),
    static_url_path="/"
)

# ---------------- API ROUTES ----------------
@app.route('/api/hello')
def hello_world():
    return 'Hello World!'

@app.post('/api/echo')
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"you_sent": data}), 201

# ---------------- SPA Fallback ----------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def spa(path):
    if path.startswith("api/"):
        return jsonify({"error": "Not found"}), 404

    file_path = ANGULAR_DIST / path
    if file_path.is_file():
        return send_from_directory(app.static_folder, path)

    return send_from_directory(app.static_folder, "index.html")

# ---------------- Local Dev ----------------
if __name__ == '__main__':
    port = int(os.getenv("PORT", "7860"))
    app.run(host="0.0.0.0", port=port, debug=True)