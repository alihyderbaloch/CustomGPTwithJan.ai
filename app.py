from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__, static_folder=".")

# Replace this with your actual Jan.ai API key
API_KEY = "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"

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("message", "")

    try:
        # Use the live API endpoint instead of localhost
        response = requests.post(
            "https://api.jan.ai/v1/chat/completions",  # Correct live URL
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "Phi-3_5-mini-instruct_IQ4_XS",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30  # optional, to avoid hanging requests
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
