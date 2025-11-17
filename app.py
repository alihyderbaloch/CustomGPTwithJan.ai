from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__, static_folder=".")

API_KEY = "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"

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("message", "")

    try:
        response = requests.post(
            "http://localhost:1337/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "Phi-3_5-mini-instruct_IQ4_XS",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
