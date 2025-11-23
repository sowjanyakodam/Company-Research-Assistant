import os
from dotenv import load_dotenv, find_dotenv
from groq import Groq

# Force load .env
env_path = find_dotenv()
load_dotenv(env_path)

print("Loaded .env from:", env_path)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

models = client.models.list()

print("\nAVAILABLE MODELS:")
for m in models.data:
    print("-", m.id)
