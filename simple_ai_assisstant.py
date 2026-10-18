from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"), # ollama serve
    api_key=os.getenv("API_KEY")
)

while True:

    user_input = input("\nSathwik: ")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        break

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": "Hello LLM!"
            }
        ]
    )

    print("LLM: " + response.choices[0].message.content)
    print(response.choices[0].message.role)