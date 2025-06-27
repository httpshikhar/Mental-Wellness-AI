from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load environment variables
AZURE_GPT_KEY = os.getenv("AZURE_GPT_KEY")
AZURE_GPT_ENDPOINT = os.getenv("AZURE_GPT_ENDPOINT")
AZURE_GPT_DEPLOYMENT = os.getenv("AZURE_GPT_DEPLOYMENT")
AZURE_GPT_VERSION = os.getenv("AZURE_GPT_VERSION", "2024-02-15-preview")

AZURE_WHISPER_KEY = os.getenv("AZURE_WHISPER_KEY")
AZURE_WHISPER_ENDPOINT = os.getenv("AZURE_WHISPER_ENDPOINT")
AZURE_WHISPER_DEPLOYMENT = os.getenv("AZURE_WHISPER_DEPLOYMENT")
AZURE_WHISPER_VERSION = os.getenv("AZURE_WHISPER_VERSION", "2023-09-01-preview")

# Dictionary to store chat history per user
chat_history = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_id = data.get("user_id")
    user_message = data.get("message")

    if user_id not in chat_history:
        chat_history[user_id] = [
            {
                "role": "system",
                "content": (
                    "You are a chill, supportive AI friend who helps people deal with anxiety, overthinking, or tough feelings. "
                    "Keep replies short (2–4 sentences), warm, and casual. Think like a Gen Z friend: kind, validating, maybe a light emoji. "
                    "Don’t give medical advice. Just offer emotional support, breathing tips, grounding thoughts, or affirmations. "
                    "You're someone people can trust and open up to."
                )
            }
        ]

    chat_history[user_id].append({"role": "user", "content": user_message})

    # Set up Azure GPT
    openai.api_type = "azure"
    openai.api_base = AZURE_GPT_ENDPOINT
    openai.api_version = AZURE_GPT_VERSION
    openai.api_key = AZURE_GPT_KEY

    response = openai.ChatCompletion.create(
        model=AZURE_GPT_DEPLOYMENT,
        messages=chat_history[user_id],
        temperature=0.9,
        max_tokens=200,
    )

    assistant_reply = response.choices[0].message["content"]
    chat_history[user_id].append({"role": "assistant", "content": assistant_reply})

    return jsonify({"response": assistant_reply})


@app.route("/transcribe", methods=["POST"])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    audio_file = request.files['file']

    try:
        # Azure Whisper setup
        openai.api_type = "azure"
        openai.api_base = AZURE_WHISPER_ENDPOINT
        openai.api_version = AZURE_WHISPER_VERSION
        openai.api_key = AZURE_WHISPER_KEY

        transcript = openai.Audio.transcribe(
            model=AZURE_WHISPER_DEPLOYMENT,
            file=audio_file
        )
        return jsonify({"text": transcript["text"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
