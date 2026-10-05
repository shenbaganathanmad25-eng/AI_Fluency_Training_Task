"""Day 6: prove the guards work, without needing the model to misbehave."""
import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "Day 1"))
import config
from robust_agent import handle_tool_call
class FakeFunction:
    def __init__(self, name, arguments):
        self.name, self.arguments = name, arguments
class FakeCall:
    """Looks exactly like one entry of message.tool_calls."""
    def __init__(self, name, arguments, call_id="call_test"):
        self.id, self.type = call_id, "function"
        self.function = FakeFunction(name, arguments)
FAULTS = [
    ("a good call",            FakeCall("get_medicine_price", '{"code": "AMOX02"}')),
    ("invalid JSON",           FakeCall("get_medicine_price", '{"code": "AMOX02"')),
    ("unknown tool",           FakeCall("order_medicine", '{"code": "PARA01", "quantity": 10}')),
    ("missing required",       FakeCall("get_medicine_price", '{}')),
    ("wrong type",             FakeCall("get_medicine_price", '{"code": 101}')),
    ("value outside the enum", FakeCall("get_medicine_price",
                                        '{"code": "PARA01", "price_type": "discount"}')),
    ("invented extra argument", FakeCall("get_medicine_price",
                                        '{"code": "PARA01", "batch": "B12"}')),
    ("unknown medicine code",  FakeCall("get_medicine_price", '{"code": "IBUP04"}')),
    ("unsafe expression",      FakeCall("calculator", json.dumps(
                                        {"expression": "__import__('os').system('ls')"}))),
    ("empty arguments string", FakeCall("calculator", '')),
    # your own faults
    ("tool name capitalised",  FakeCall("Get_Medicine_Price", '{"code": "AMOX02"}')),
    ("arguments are an array", FakeCall("get_medicine_stock", '["AMOX02"]')),
]
if __name__ == "__main__":
    print("=" * 78)
    for label, call in FAULTS:
        result = handle_tool_call(call, log=False)
        print(f"{label:<24} -> {result[:72]}")
    print("=" * 78)
    print("Every line above is a STRING. Nothing raised, nothing crashed:")
    print("each message goes back to the model, which can try again.")
