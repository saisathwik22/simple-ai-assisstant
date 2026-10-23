from openai import OpenAI
import os
from dotenv import load_dotenv
from tools import TOOLS, run_tool
from Utilities.utilities import log



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
        "content" : (
            "You are helpful, humble assisstant. "
            "Answer general questions (programming, science, advice) from your own knowledge. "
            "Use a tool ONLY when the user asks for the current time, the weather, or their city. "
            "Keep answers under 100 words."
        ),
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
            model=os.getenv("MODEL_LARGE"),
            messages=messages,
            tools=TOOLS
        )
        
        msg = response.choices[0].message

        if not msg.tool_calls:
            break

        log(f"Step {step + 1}: model requested {len(msg.tool_calls)} tool calls")

        messages.append(msg) # history added

        for tool_call in msg.tool_calls:
            result = run_tool(tool_call)
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
        print("🤖 Assistant: " + fallback)
        continue
    

    messages.append({
        "role" : "assisstant",
        "content" : msg.content
    })

    print("🤖 Assistant: " + (msg.content or ""))