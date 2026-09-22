"""Tools the agent is allowed to use, plus their JSON Schema descriptions."""
import ast
import operator
from config import MEDICINES
 
def get_medicine_price(code: str) -> str:
    """Look up the price for one medicine code."""
    item = MEDICINES.get(code.strip().upper())
    return str(item["price"]) if item else f"Unknown medicine code: {code}"
 
def get_medicine_stock(code: str) -> str:
    """Look up the stock quantity for one medicine code."""
    item = MEDICINES.get(code.strip().upper())
    return str(item["stock"]) if item else f"Unknown medicine code: {code}"
 
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.USub: operator.neg}
 
def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Unsupported expression")
 
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression such as (10*2 + 5*85)."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}"
 
TOOL_FUNCTIONS = {
    "get_medicine_price": get_medicine_price,
    "get_medicine_stock": get_medicine_stock,
    "calculator": calculator,
}
 
TOOLS = [
    {"type": "function", "function": {
        "name": "get_medicine_price",
        "description": "Get the price in rupees per unit for a medicine code, e.g. AMOX02.",
        "parameters": {"type": "object",
            "properties": {"code": {"type": "string"}},
            "required": ["code"]}}},
    {"type": "function", "function": {
        "name": "get_medicine_stock",
        "description": "Get the stock quantity in units for a medicine code, e.g. AMOX02.",
        "parameters": {"type": "object",
            "properties": {"code": {"type": "string"}},
            "required": ["code"]}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression using + - * / and brackets.",
        "parameters": {"type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"]}}},
]
