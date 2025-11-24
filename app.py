from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder=".")

# Get API key from Render environment variables
API_KEY = os.environ.get("JANAI_API_KEY")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("message", "")

    try:
        response = requests.post(
            "https://api.jan.ai/v1/chat/completions",  # Live API URL
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "Phi-3_5-mini-instruct_IQ4_XS",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
