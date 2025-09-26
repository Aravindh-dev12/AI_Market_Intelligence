import json

def generate_markdown_report(insights_path="insights/insights.json"):

    with open(insights_path, "r") as f:
        insights = json.load(f)

    md_content = "# AI Market Intelligence Report\n\n"
    for i, item in enumerate(insights, 1):
        md_content += f"## Insight {i}\n"
        md_content += f"- **Insight:** {item['insight']}\n"
        md_content += f"- **Confidence:** {item['confidence']}\n"
        md_content += f"- **Recommendation:** {item['recommendation']}\n\n"

    with open("report.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    print("✅ Markdown report generated at report.md")
