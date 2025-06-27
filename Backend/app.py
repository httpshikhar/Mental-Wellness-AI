from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import AzureOpenAI
import os
import uuid

# Load env vars
load_dotenv()
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
azure_oai_key = os.getenv("AZURE_OAI_KEY")
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")

# Init Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=azure_oai_endpoint,
    api_key=azure_oai_key,
    api_version="2024-02-15-preview"
)

# Init Flask app
app = Flask(__name__)

# Store chat history per user in memory (you can later use DB or files)
user_sessions = {}

# Initial system message to guide chatbot behavior
system_prompt = {
    "role": "system",
    "content": (
        "You are a chill, supportive AI friend who helps people deal with anxiety, overthinking, or tough feelings. "
        "Keep replies short (2–4 sentences), warm, and casual. Think like a Gen Z friend: kind, validating, and sometimes use a light emoji. "
        "Don't give medical advice. Offer support, grounding tips, or relatable affirmations. "
        "Always try to ask a gentle follow-up question to keep the conversation going, unless the user says goodbye. "
        "You're someone they can trust to open up to."
    )
}

# Route to handle messages
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id")
    user_input = data.get("message")

    if not user_id or not user_input:
        return jsonify({"error": "Missing user_id or message"}), 400

    # Create new session if not exists
    if user_id not in user_sessions:
        user_sessions[user_id] = [system_prompt]

    # Append user message to history
    user_sessions[user_id].append({"role": "user", "content": user_input})

    # Get assistant response
    try:
        response = client.chat.completions.create(
            model=azure_oai_deployment,
            messages=user_sessions[user_id],
            max_tokens=300,
            temperature=0.9,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.6
        )

        ai_reply = response.choices[0].message.content.strip()

        # Append AI reply to history
        user_sessions[user_id].append({"role": "assistant", "content": ai_reply})

        return jsonify({"response": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Test route
@app.route("/", methods=["GET"])
def home():
    return "Mental Health Chatbot API is running"

# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
