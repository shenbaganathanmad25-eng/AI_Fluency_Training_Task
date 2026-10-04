"""Day 5, Part D: compare two models on the same prompts."""
import time
import requests
BASE = "http://localhost:11434"
MODELS = ["qwen2.5:1.5b"]   # put YOUR two models here
PROMPTS = [
    "Reply with exactly: OK",
    "In two sentences, what is an AI agent?",
    "Paracetamol costs Rs. 2 and Cough Syrup Rs. 85 per unit. What is the total "
    "for 10 Paracetamol and 5 Cough Syrup? Show the steps.",
    "Amoxicillin stock is 200 units and Cough Syrup stock is 100 units. "
    "Which is more, and by how much?",
]
def run(model, prompt):
    start = time.time()
    data = requests.post(f"{BASE}/api/generate",
                         json={"model": model, "prompt": prompt, "stream": False},
                         timeout=600).json()
    elapsed = time.time() - start
    tokens = data.get("eval_count", 0)
    load_ms = data.get("load_duration", 0) / 1e6
    rate = tokens / elapsed if elapsed else 0
    return elapsed, tokens, rate, load_ms, data.get("response", "").strip()
if __name__ == "__main__":
    for model in MODELS:
        print("=" * 72)
        print("MODEL:", model)
        for prompt in PROMPTS:
            elapsed, tokens, rate, load_ms, text = run(model, prompt)
            print(f"\n  prompt: {prompt[:50]}")
            print(f"  {elapsed:5.1f} s | {tokens:4d} tokens | {rate:5.1f} tok/s | load {load_ms:7.1f} ms")
            print(f"  answer: {text[:160]}")
        print()