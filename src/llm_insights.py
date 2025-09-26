import openai
import os
import json
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_insights(df):
    sample_data = df.head(50).to_dict(orient="records")
    prompt = f"""
    Analyze the following app dataset and provide 3 actionable insights with confidence scores (0-1) and recommendations:

    {sample_data}
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    insights_text = response.choices[0].message.content

    insights = [{
        "insight": insights_text,
        "confidence": 0.85,
        "recommendation": "Example recommendation"
    }]

    with open("insights/insights.json", "w") as f:
        json.dump(insights, f, indent=4)

    return insights
