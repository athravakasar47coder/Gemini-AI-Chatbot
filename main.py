import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.8-flash"

history = []

print("===== GEMINI AI CHATBOT =====")
print("Type 'exit' to stop.")
print("Type 'new' for a new conversation.\n")


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    if user_input.lower() == "new":
        history = []
        print("Chatbot: New conversation started.\n")
        continue

    # Save user message
    history.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })

    # Check if real-time information is needed
    keywords = [
        "current",
        "latest",
        "today",
        "now",
        "weather",
        "price",
        "news",
        "bitcoin",
        "stock"
    ]

    realtime = any(word in user_input.lower() for word in keywords)

    try:

        if realtime:
            response = client.models.generate_content(
                model=MODEL,
                contents=history,
                config={
                    "tools": [{"google_search": {}}]
                }
            )

        else:
            response = client.models.generate_content(
                model=MODEL,
                contents=history
            )

        print("\nGemini:", response.text)

        # Save Gemini response
        history.append({
            "role": "model",
            "parts": [{"text": response.text}]
        })

        print()

    except Exception as e:
        print("\nError:", e)