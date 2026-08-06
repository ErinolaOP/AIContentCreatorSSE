from dotenv import load_dotenv
import os

print("Loading .env...")
loaded = load_dotenv()

print("Loaded:", loaded)
print("Current folder:", os.getcwd())
print("Key:", os.getenv("OPENAI_API_KEY"))