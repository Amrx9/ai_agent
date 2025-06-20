import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

try:
    user_prompt = sys.argv[1]
except IndexError:
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

usage_metadata = response.usage_metadata

if "--verbose" in sys.argv:
    print(f"""User prompt: {user_prompt}
    Prompt tokens: {usage_metadata.prompt_token_count}
    Response tokens: {usage_metadata.candidates_token_count}\n""")

print(response.text)
