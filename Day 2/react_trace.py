"""Day 2, Part B: print the agent's real ReAct trace to compare with the paper trace."""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]/"Day 1"))

from agent import agent
 
QUESTION = ("Which is cheaper: 40 units of Paracetamol (PARA01) and 10 units of Amoxicillin (AMOX02) "
            "with a 10% bulk discount, or the same order plus 4 units of Cough Syrup (COUG03) with a "
            "25% bulk discount? By how much?")
 
print("QUESTION:", QUESTION, "\n")
print("--- the agent's actions and observations ---")
answer = agent(QUESTION, max_steps=8)
print("\nFINAL ANSWER:", answer)
