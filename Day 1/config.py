"""Shared configuration: chooses the LLM provider and holds the pharmacy data."""
import os
from dotenv import load_dotenv
from openai import OpenAI
 
load_dotenv()
 
PROVIDER = os.getenv("PROVIDER", "ollama").strip().lower()
 
if PROVIDER == "ollama":
    BASE_URL = "http://localhost:11434/v1"
    API_KEY = "ollama"
    MODEL = os.getenv("MODEL", "qwen2.5:1.5b")
elif PROVIDER == "groq":
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
elif PROVIDER == "huggingface":
    BASE_URL = "https://router.huggingface.co/v1"
    API_KEY = os.getenv("HF_TOKEN")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
else:
    raise SystemExit(f"Unknown PROVIDER '{PROVIDER}'. Use ollama, groq or huggingface.")
 
if not API_KEY:
    raise SystemExit(f"No API key found for PROVIDER={PROVIDER}. Check your .env file.")
 
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
 
# Private pharmacy data that no public LLM has ever seen
MEDICINES = {
    "PARA01": {"name": "Paracetamol 500mg", "price": 2,  "stock": 500},
    "AMOX02": {"name": "Amoxicillin 250mg", "price": 15, "stock": 200},
    "COUG03": {"name": "Cough Syrup 100ml", "price": 85, "stock": 100},
}
 
QUESTIONS = [
    "What is the price of Amoxicillin (AMOX02)?",
    "What is the total cost of 10 units of Paracetamol (PARA01) and 5 units of Cough Syrup (COUG03)?",
    "Is the stock of Amoxicillin (AMOX02) more than Cough Syrup (COUG03), and by how much?",
    "Write a two-line message advertising a free health checkup camp at the pharmacy.",
]
 
def banner(system_name):
    print(f"\n=== {system_name} | provider: {PROVIDER} | model: {MODEL} ===\n")
