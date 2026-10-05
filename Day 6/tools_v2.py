"""Day 6: the Greenleaf Pharmacy tools, with stricter JSON Schemas."""
import ast
import operator
from config import MEDICINES
VALID_CODES = ", ".join(MEDICINES)          # PARA01, AMOX02, COUG03
def get_medicine_price(code: str, price_type: str = "retail") -> str:
    """Return the price per unit for one medicine code."""
    item = MEDICINES.get(code.strip().upper())
    if item is None:
        return f"Unknown medicine code: {code}. Valid codes: {VALID_CODES}"
    return str(item["price"])
def get_medicine_stock(code: str) -> str:
    """Return the stock quantity for one medicine code."""
    item = MEDICINES.get(code.strip().upper())
    if item is None:
        return f"Unknown medicine code: {code}. Valid codes: {VALID_CODES}"
    return str(item["stock"])
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
    """Evaluate a basic arithmetic expression."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}. Use only numbers and + - * / ( )."
TOOL_FUNCTIONS = {
    "get_medicine_price": get_medicine_price,
    "get_medicine_stock": get_medicine_stock,
    "calculator": calculator,
}
TOOLS = [
    {"type": "function", "function": {
        "name": "get_medicine_price",
        "description": ("Get the price in rupees per unit for ONE medicine code, "
                        "for example AMOX02. Returns the number only. "
                        "Valid codes: PARA01, AMOX02, COUG03."),
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string",
                         "description": "Medicine code such as AMOX02"},
                "price_type": {"type": "string", "enum": ["retail", "wholesale"],
                               "description": "Price list; defaults to retail"},
            },
            "required": ["code"],
            "additionalProperties": False,
        }}},
    {"type": "function", "function": {
        "name": "get_medicine_stock",
        "description": ("Get the stock quantity in units for ONE medicine code, "
                        "for example AMOX02. Returns the number only. "
                        "Valid codes: PARA01, AMOX02, COUG03."),
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string",
                         "description": "Medicine code such as AMOX02"},
            },
            "required": ["code"],
            "additionalProperties": False,
        }}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": ("Evaluate one arithmetic expression using + - * / and "
                        "brackets, for example (10 * 2 + 5 * 85) * 0.9. "
                        "Returns the number only."),
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string",
                               "description": "Arithmetic expression, digits "
                                              "and operators only"},
            },
            "required": ["expression"],
            "additionalProperties": False,
        }}},
]
# name -> the "parameters" block above, used by validate.py
SCHEMAS = {t["function"]["name"]: t["function"]["parameters"] for t in TOOLS}