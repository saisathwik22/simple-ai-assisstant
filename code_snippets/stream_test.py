import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url = os.getenv("BASE_URL"),
    api_key = os.getenv("API_KEY")
)

stream = client.chat.completions.create(
    model = os.getenv("MODEL_SMALL"),
    messages = [{ "role": "user", "content": "Explain what an API is in 100 words." }],
    tools = os.getenv("TOOLS"),
    stream=True,
)

full_response = ""

for chunk in stream:
    if not chunk.choices:
        continue
    
    piece = chunk.choices[0].delta.content
    if piece:
        print(piece, end="", flush=True)
        full_response += piece


print("\nFull response:")
print(full_response)