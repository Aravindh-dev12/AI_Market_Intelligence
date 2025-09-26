import os
import json
import openai
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_insights(df):
    sample_data = df.head(50).to_dict(orient="records")
    prompt = f"""
    Analyze the dataset below. Return EXACT valid JSON with this schema:
    [
      {{"insight": "...", "confidence": 0.0-1.0, "recommendation": "..."}},
      ...
    ]

    Dataset sample: {sample_data}
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    raw_text = response.choices[0].message.content.strip()

    try:
        insights = json.loads(raw_text)
    except json.JSONDecodeError:
        insights = [{"insight": raw_text, "confidence": 0.5, "recommendation": "Parse fallback"}]

    os.makedirs("insights", exist_ok=True)
    with open("insights/insights.json", "w") as f:
        json.dump(insights, f, indent=4)

    return insights
