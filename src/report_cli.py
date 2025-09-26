import json

def run_cli():
    with open("insights/insights.json") as f:
        insights = json.load(f)

    print("AI Market Intelligence CLI\n")
    for i, item in enumerate(insights, 1):
        print(f"{i}. {item['insight']} (Confidence: {item['confidence']})")

    choice = int(input("Enter insight number for details: "))
    selected = insights[choice-1]
    print(f"Recommendation: {selected['recommendation']}")
