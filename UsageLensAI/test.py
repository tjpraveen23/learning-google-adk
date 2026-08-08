import os
from dotenv import load_dotenv

load_dotenv()

print("Groq key:", os.getenv("GROQ_API_KEY"))