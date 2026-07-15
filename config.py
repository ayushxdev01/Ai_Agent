import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"

MODEL_NAME = "llama-3.3-70b-versatile"

if not API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY not found. Create a .env file (see .env.example) "
        "and set GROQ_API_KEY=your_key_here"
    )