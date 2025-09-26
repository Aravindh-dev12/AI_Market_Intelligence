import pandas as pd

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

    if not seo_sheet:
        print("⚠️ 'SEO Metrics' sheet not found, skipping SEO analysis")
        seo_sheet = None

    funnel_df = excel_dict[funnel_sheet]

    funnel_summary = pd.DataFrame({
        "Campaign": funnel_df.get("Campaign", funnel_df.columns[0:1][0]),
        "Spend": funnel_df.get("Spend", [0]*len(funnel_df)),
        "Revenue": funnel_df.get("Revenue", [0]*len(funnel_df)),
        "ROAS": [r/s if s else 0 for r, s in zip(funnel_df.get("Revenue", [0]*len(funnel_df)),
                                                 funnel_df.get("Spend", [1]*len(funnel_df)))]
    })

    creative_outputs = []
    for i, row in funnel_df.head(3).iterrows():
        campaign_name = row.get("Campaign", f"Campaign {i+1}")
        creative_outputs.append({
            "headline": f"Boost your {campaign_name} now!",
            "seo_meta": f"{campaign_name} with high conversion rate",
            "pdp_text": f"Maximize ROI for {campaign_name} campaign."
        })

    return funnel_summary, creative_outputs
