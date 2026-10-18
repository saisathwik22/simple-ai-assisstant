from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"), # ollama serve
    api_key=os.getenv("API_KEY")
)

messages = []

messages.append(
    {
        "role" : "system",
        "content" : "Act like a very rude agent and always respond under 20 words."
    }
)

while True:

    user_input = input("\nSathwik: ")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        break

    messages.append(
        {
            "role" : "user",
            "content" : user_input
        }
    )

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )

    messages.append(
        {
            "role" : "assisstant",
            "content" : response.choices[0].message.content
        }
    )

    print("LLM: " + response.choices[0].message.content)
    print(response.choices[0].message.role)