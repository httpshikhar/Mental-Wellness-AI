from flask import Flask, request, jsonify
from flask_cors import CORS
from response import *

app = Flask(__name__)
CORS(app)

# Health check route
@app.route("/", methods=["GET"])
def home():
    return "🧠 AI Mental Health Assistant Backend is running!"

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        message = data.get("message")

        if not user_id or not message:
            return jsonify({"error": "Missing user_id or message"}), 400

        reply = get_ai_reply(message)
        return jsonify({"response": reply})

    except Exception as e:
        print(">>> Chat Error:", e)
        return jsonify({"error": "Chat failed", "details": str(e)}), 500

# Speech-to-Text endpoint
@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        file = request.files['file']
        transcript = transcribe_audio(file)
        return jsonify({"text": transcript})

    except Exception as e:
        print(">>> Whisper Transcription Error:", e)
        return jsonify({"error": "Transcription failed", "details": str(e)}), 500

# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
