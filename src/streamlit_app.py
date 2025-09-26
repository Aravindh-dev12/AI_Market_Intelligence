import pandas as pd
import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_creatives_with_llm(campaign_rows):
    prompt = f"""
    You are a copywriter. For each campaign below, generate:
    - headline
    - seo_meta
    - pdp_text

    Return JSON list in this format:
    [{{"campaign": "...", "headline": "...", "seo_meta": "...", "pdp_text": "..."}}]

    Campaigns: {campaign_rows}
    """
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    try:
        return json.loads(response.choices[0].message.content)
    except:
        return []

def analyze_d2c_funnel(excel_dict):
    funnel_sheet = None
    seo_sheet = None

    for sheet in excel_dict:
        if "ad" in sheet.lower() or "campaign" in sheet.lower():
            funnel_sheet = sheet
        if "seo" in sheet.lower():
            seo_sheet = sheet

    if not funnel_sheet:
        print("⚠️ 'Ad Campaign Metrics' sheet not found, using first sheet as funnel data")
        funnel_sheet = list(excel_dict.keys())[0]

    funnel_df = excel_dict[funnel_sheet]

    funnel_summary = pd.DataFrame({
        "Campaign": funnel_df.get("Campaign", funnel_df.columns[0:1][0]),
        "Spend": funnel_df.get("Spend", [0]*len(funnel_df)),
        "Revenue": funnel_df.get("Revenue", [0]*len(funnel_df)),
        "ROAS": [r/s if s else 0 for r, s in zip(funnel_df.get("Revenue", [0]*len(funnel_df)),
                                                 funnel_df.get("Spend", [1]*len(funnel_df)))]
    })

    creative_outputs = generate_creatives_with_llm(funnel_df.head(3).to_dict(orient="records"))

    return funnel_summary, creative_outputs
