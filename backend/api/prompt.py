from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
import requests
from uuid import uuid4
from ..config import Config

blp = Blueprint("prompt", __name__, description="Forward prompts to n8n")


@blp.route("/prompt")
class PromptAPI(MethodView):
    def post(self):
        """
        Forward user prompts to the n8n webhook for AI processing.
        
        Expected JSON body:
            - prompt (required): The user's message/question
            - sessionId (optional): Persistent session identifier. If not provided, 
              a new UUID will be generated. The frontend should persist this in 
              localStorage to maintain conversation context across page reloads.
            - action (optional): Action type, defaults to "sendMessage"
        
        Returns:
            JSON response from n8n webhook
        """
        data = request.get_json(silent=True) or {}
        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"error": "missing prompt"}), 400

        # Use provided sessionId for conversation continuity, or generate new one
        session_id = data.get("sessionId") or str(uuid4())
        action = data.get("action", "sendMessage")

        # Build payload to send to n8n. Match the webhook contract.
        payload = [
            {
                "sessionId": session_id,
                "action": action,
                "chatInput": prompt,
            }
        ]

        n8n_url = Config.N8N_WEBHOOK_URL

        try:
            # forward the prompt to n8n webhook and wait for JSON response
            # Use a 5 minute timeout (300 seconds) to accommodate longer n8n flows
            resp = requests.post(n8n_url, json=payload, timeout=300)
        except requests.RequestException as exc:
            return jsonify({"error": "failed to contact n8n", "details": str(exc)}), 502

        # Try to parse JSON from n8n; return raw text if parse fails
        try:
            resp_json = resp.json()
        except ValueError:
            resp_json = {"text": resp.text}

        return jsonify({"n8n_response": resp_json}), resp.status_code
