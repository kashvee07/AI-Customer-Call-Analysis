from pipeline import analyze_customer_call
from utils.report import generate_report

result = analyze_customer_call("uploads/customer_call.wav")

if result["success"]:
    print(generate_report(result))
else:
    print("Error:", result["error"])