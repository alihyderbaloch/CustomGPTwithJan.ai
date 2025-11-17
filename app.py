from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Put your Jan.ai API key here (never in frontend)
API_KEY = "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"

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("message", "")

    if not prompt:
        return jsonify({"error": "No message received"}), 400

    try:
        response = requests.post(
            "http://localhost:1337/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "Phi-3_5-mini-instruct_IQ4_XS",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=10
        )
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
