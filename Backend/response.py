# To run this code you need to install the following dependencies:
# pip install google-genai

# import base64
# import os
# from google import genai
# from google.genai import types

# def generate():
#     client = genai.Client(
#         api_key=api,
#     )

#     model = "gemini-2.5-pro"
#     contents = [
#         types.Content(
#             role="user",
#             parts=[
#                 types.Part.from_text(text="""Hey there!"""),
#             ],
#         ),
#     ]
#     generate_content_config = types.GenerateContentConfig(
#         thinking_config = types.ThinkingConfig(
#             thinking_budget=-1,
#         ),
#         response_mime_type="text/plain",
#     )

#     for chunk in client.models.generate_content_stream(
#         model=model,
#         contents=contents,
#         config=generate_content_config,
#     ):
#         print(chunk.text, end="")

# if __name__ == "__main__":
#     generate()


# import os
# from mistralai import Mistral
# from dotenv import load_dotenv

# load_dotenv()
# api = os.getenv("MISTRAL_API_KEY")

# api_key = api
# model = "mistral-medium-latest"

# client = Mistral(api_key=api_key)

# chat_response = client.chat.complete(
#     model=model,
#     messages=[
#         {
#             "role": "system",
#             "content": (
#                 "You are a chill, supportive AI friend for people feeling anxious, low, or overwhelmed. "
#                 "You respond like a Gen Z friend would: kind, casual, relatable. "
#                 "Keep your replies short (2–4 sentences), friendly, emotionally validating, and sometimes use light emojis. "
#                 "No medical advice, no judging — just empathy, grounding tips, and good vibes."
#             ),
#         },
#         # Example 1
#         {
#             "role": "user",
#             "content": "I feel like everything is falling apart. I don’t even know what to do anymore.",
#         },
#         {
#             "role": "assistant",
#             "content": "Oof, I hear you. That sounds really heavy. Just remember — you don’t have to fix everything right now. One deep breath at a time. You got this 🤍",
#         },
#         # Example 2
#         {
#             "role": "user",
#             "content": "I’m so tired of pretending like I’m fine.",
#         },
#         {
#             "role": "assistant",
#             "content": "You don’t have to fake it here. It’s okay to not be okay — seriously. Your feelings are valid, and you’re not alone in this.",
#         },
#         # Example 3
#         {
#             "role": "user",
#             "content": "My thoughts just won’t stop at night. I can’t sleep.",
#         },
#         {
#             "role": "assistant",
#             "content": "That’s rough — overthinking at night hits hard. Try a lil’ deep breathing or writing your thoughts down. Sometimes a brain dump helps clear the noise 💤",
#         },
#         # Actual User Message
#         {
#             "role": "user",
#             "content": "I’ve been feeling really anxious lately, and I don’t know why.",
#         },
#     ]
# )


# print(chat_response.choices[0].message.content)


import os
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
if __name__ == "__main__":
    print("Welcome to the AI Support Chat 💬 (type 'exit' to quit)\n")

    while True:
        user_msg = input("You: ")
        if user_msg.lower() in ["exit", "quit"]:
            break

        ai_response = get_ai_reply(user_msg)
        print("AI:", ai_response)
