import os
from dotenv import load_dotenv
from google import genai
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

try:
    arg = sys.argv[1:]
except IndexError:
    sys.exit(1)

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents = arg
)

usage_metadata = response.usage_metadata

print(response.text)
print(f"Prompt tokens: {usage_metadata.prompt_token_count}\nResponse tokens: {usage_metadata.candidates_token_count}")
