"""Day 2, Part C: the same questions asked WITHOUT and WITH Chain-of-Thought."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]/"Day 1"))

from config import client, MODEL, banner
 
QUESTIONS = [
    # 1. Multi-step arithmetic with a discount and instalments
    "Greenleaf Pharmacy orders 40 units of Paracetamol, 10 units of Amoxicillin and 4 units of Cough "
    "Syrup for a hospital client. With a 20% bulk discount on the total, paid in 3 equal instalments, "
    "how much is each instalment?",
    # 2. Counting in two parts
    "The pharmacy has 3 dispensing counters. Each counter serves 25 patients in the morning and 40 in "
    "the afternoon. How many patient services happen in one day, across all counters?",
    # 3. Ordering / logic
    "Amoxicillin has more stock than Cough Syrup. Cough Syrup has more stock than a new item, Vitamin C "
    "tablets. Paracetamol has less stock than Vitamin C tablets. Which item has the most stock, and "
    "which has the least?",
]
 
DIRECT_PROMPT = "You are a helpful assistant. Give only the final answer. Do not explain."
 
COT_PROMPT = ("You are a helpful assistant. Solve the problem step by step. "
              "Number each step and show the calculation in that step. "
              "After the steps, write the last line exactly as: Final Answer: <answer>")
 
def ask(system_prompt, question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": question}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()
 
if __name__ == "__main__":
    banner("CHAIN-OF-THOUGHT COMPARISON")
    for number, question in enumerate(QUESTIONS, start=1):
        print("=" * 72)
        print(f"QUESTION {number}: {question}\n")
        print("--- WITHOUT CoT ---")
        print(ask(DIRECT_PROMPT, question), "\n")
        print("--- WITH CoT ---")
        print(ask(COT_PROMPT, question), "\n")
