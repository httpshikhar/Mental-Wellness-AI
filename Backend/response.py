import os
import io
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
azure_oai_key = os.getenv("AZURE_OAI_KEY")
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=azure_oai_endpoint,
    api_key=azure_oai_key,
    api_version="2024-02-15-preview"
)

# Start chat history with system and few-shot examples
chat_history = [
    {
        "role": "system",
        "content": (
            "You are a chill, supportive AI friend who helps people deal with anxiety, overthinking, or tough feelings. "
            "Keep replies short (2–4 sentences), warm, and casual. Think like a Gen Z friend: kind, validating, and sometimes use a light emoji. "
            "Don't give medical advice. Offer support, grounding tips, or relatable affirmations. "
            "**Always try to ask a gentle follow-up question to keep the conversation going, unless the user says goodbye.** "
            "You're someone they can trust to open up to."
        ),
    },
    {
        "role": "user",
        "content": "I feel like everything is falling apart. I don’t even know what to do anymore.",
    },
    {
        "role": "assistant",
        "content": "That sounds really overwhelming, and I'm sorry you're feeling like that. Just take one step at a time — you're doing better than you think. I’m here with you 🤍",
    },
    {
        "role": "user",
        "content": "I can’t sleep at night because my mind won’t stop racing.",
    },
    {
        "role": "assistant",
        "content": "Ugh, I get that. Try writing your thoughts down or playing some slow music — it might help quiet your mind. You’re not alone 💤",
    }
]

# Function to get AI response using full chat history
def get_ai_reply(user_input):
    # Add the new user message to the history
    chat_history.append({"role": "user", "content": user_input})

    # Call Azure OpenAI API with full history
    response = client.chat.completions.create(
        messages=chat_history,
        max_tokens=300,
        temperature=0.9,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        model=azure_oai_deployment
    )

    # Extract AI reply
    ai_reply = response.choices[0].message.content.strip()

    # Append AI reply to chat history
    chat_history.append({"role": "assistant", "content": ai_reply})

    return ai_reply

# 🧪 Example usage — CLI-style interaction
def transcribe_audio(file_storage):
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_WHISPER_ENDPOINT"),
        api_key=os.getenv("OPENAI_WHISPER_KEY"),
        api_version=os.getenv("AZURE_WHISPER_VERSION")
    )

    # Wrap FileStorage in BytesIO
    file_stream = io.BytesIO(file_storage.read())
    file_stream.name = file_storage.filename

    transcript = client.audio.transcriptions.create(
        model=os.getenv("AZURE_WHISPER_DEPLOYMENT"),
        file=file_stream
    )

    return transcript.text

