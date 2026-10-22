from openai import OpenAI
import os
from dotenv import load_dotenv
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP
import json


load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"), # ollama serve
    api_key=os.getenv("API_KEY")
)

messages = []

MAX_STEPS = 5

messages.append(
    {
        "role" : "system",
        "content" : "Act like a very humble agent and always respond under 20 words."
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

    
    # Chained Tool Calling
    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=TOOLS
        )
        
        msg = response.choices[0].message

        if not msg.tool_calls:
            break

        messages.append(msg) # history added

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = {}

            try:
                func_args = json.loads(tool_call.function.arguments or "{}")
                fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
                result = fn(**func_args)
            except Exception as e:
                result = f"Error while running {func_name} : {e}"

            messages.append({
                "role" : "tool",
                "tool_call_id" : tool_call.id,
                "content" : str(result)
            })

    else:
        # Ran out of steps: the model never gave final answer
        fallback = "Sorry, I could not finish this within the step limit."
        messages.append({
            "role": "assisstant",
            "content": fallback
        })
        print("Assisstant: " + fallback)
        continue
    

    messages.append({
        "role" : "assisstant",
        "content" : msg.content
    })

    print("Assisstant: " + msg.content)