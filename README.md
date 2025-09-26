##Project Overview

This project implements an AI-powered market intelligence system for mobile apps and D2C campaigns. It ingests data from multiple sources, generates insights using an LLM (OpenAI GPT-4), and produces actionable outputs for decision-making.

##Key Features

Data Pipeline

Cleans and normalizes Google Play Store dataset.

Integrates Apple App Store reviews via RapidAPI.

Handles missing values, duplicates, and inconsistent formats.

LLM Insights

Generates structured insights using GPT-4.

Outputs are stored in insights/insights.json with confidence scores and recommendations.

Reporting

Generates a Markdown report (report.md) summarizing insights.

Phase 5 – D2C Funnel & SEO

Loads a D2C Excel dataset.

Computes funnel metrics (Spend, Revenue, ROAS).

Generates 2–3 AI-powered creative outputs (ad headlines, SEO meta descriptions, PDP text).

Automatically handles missing sheets and columns gracefully.

##Project Structure
AI_Market_Intelligence/
│
├─ main.py                     # Main script to run the project
├─ .env                        # API keys (OpenAI, RapidAPI)
├─ requirements.txt             # Python dependencies
├─ data/                        # Dataset folder
│   ├─ GooglePlayStore.csv
│   └─ Kasparro_Phase5_D2C_Synthetic_Dataset.xlsx
├─ insights/                    # LLM insights JSON output
├─ report.md                    # Generated Markdown report
└─ src/
    ├─ data_pipeline.py         # Cleaning & loading data
    ├─ api_integration.py       # Apple Store API integration
    ├─ llm_insights.py          # GPT-4 insights generation
    ├─ report_generator.py      # Markdown report generator
    └─ d2c_insights.py          # D2C funnel analysis & creative outputs

##Setup Instructions

Clone/download the project folder.

Create a virtual environment:

python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Linux/Mac


##Install dependencies:

pip install -r requirements.txt


Add your API keys to .env:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
RAPIDAPI_KEY=your_rapidapi_key_here


Run the main script:

python main.py


##Outputs:

Cleaned Google Play + Apple data → data/cleaned_data/combined_apps.csv

LLM insights → insights/insights.json

Markdown report → report.md

Phase 5 funnel summary & creative outputs → printed in console

Notes

If D2C Excel sheets don’t match expected names, the first sheet is used as fallback.

Funnel metrics and creative outputs are generated even with minimal data.

Markdown report is fully automated; PDF export is optional.