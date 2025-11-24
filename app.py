from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder=".")

# Read API key from environment
API_KEY = os.environ.get("JANAI_API_KEY")

# Debug: check if API key is being read
if not API_KEY:
    print("ERROR: JANAI_API_KEY environment variable is NOT set!")
else:
    print(f"API_KEY detected: {len(API_KEY)} characters")  # prints length only for safety

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("message", "")

    if not API_KEY:
        return jsonify({"error": "API key not set on server!"}), 500

    if not prompt:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = requests.post(
            "https://api.jan.ai/v1/chat/completions",  # live Jan.ai endpoint
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

        # Debug: log status and content length
        print(f"Jan.ai status: {response.status_code}, response length: {len(response.text)}")

        # Return JSON from Jan.ai directly
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        print("RequestException:", e)
        return jsonify({"error": str(e)}), 500

# Test endpoint to verify env variable without sending a prompt
@app.route("/test-key")
def test_key():
    if API_KEY:
        return jsonify({"status": "API key detected", "length": len(API_KEY)})
    else:
        return jsonify({"status": "API key NOT detected"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
