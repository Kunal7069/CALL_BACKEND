import os

from openai import OpenAI

# Load credentials from environment variables
SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY")
SAMBANOVA_ENDPOINT = os.getenv("SAMBANOVA_ENDPOINT")

# Instantiate the SambaNova OpenAI client
client = OpenAI(api_key=SAMBANOVA_API_KEY, base_url=SAMBANOVA_ENDPOINT)
