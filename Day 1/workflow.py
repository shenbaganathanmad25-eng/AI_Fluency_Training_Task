"""System 2: a rule-based workflow. Fixed if/else rules, no LLM at all."""
import re
from config import MEDICINES
 
def workflow(question):
    codes = re.findall(r"[A-Z]{4}\d{2}", question.upper())
    known = [c for c in codes if c in MEDICINES]
    if not known:
        return "Sorry, I can only answer questions about known medicine codes."
 
    text = question.lower()
 
    # Rule 1: single price lookup
    if "price" in text and len(known) == 1:
        code = known[0]
        return f"Price of {MEDICINES[code]['name']}: Rs. {MEDICINES[code]['price']}"
 
    # Rule 2: total cost for stated quantities ("N units of CODE")
    if "total cost" in text:
        pairs = re.findall(r"(\d+)\s*units?\s*of\s*[A-Za-z ]*?\(?([A-Z]{4}\d{2})\)?", question.upper())
        if pairs:
            total = sum(int(qty) * MEDICINES[c]["price"] for qty, c in pairs if c in MEDICINES)
            return f"Total cost: Rs. {total:,.0f}"
 
    return "Sorry, I do not have a rule for this type of question."
 
if __name__ == "__main__":
    from config import QUESTIONS
    print("\n=== SYSTEM 2: RULE-BASED WORKFLOW (no LLM) ===\n")
    for question in QUESTIONS:
        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)
