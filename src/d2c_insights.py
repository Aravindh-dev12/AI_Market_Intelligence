from src.data_pipeline import clean_google_play, load_d2c_excel
from src.api_integration import merge_google_apple
from src.llm_insights import generate_insights
from src.report_generator import generate_markdown_report
from src.streamlit_app import analyze_d2c_funnel

def main():
    print("Cleaning Google Play data...")
    google_df = clean_google_play("data/GooglePlayStore.csv")

    print("Merging with Apple App Store data...")
    combined_df = merge_google_apple(google_df)

    print("Generating LLM insights...")
    insights = generate_insights(combined_df)

    print("Generating report...")
    generate_markdown_report()

    print("Loading D2C dataset for Phase 5...")
    d2c_data = load_d2c_excel("data/Kasparro_Phase5_D2C_Synthetic_Dataset.xlsx")

    print("Analyzing D2C funnel and generating creative outputs...")
    funnel, creative_outputs = analyze_d2c_funnel(d2c_data)

    print("✅ Process complete!")
    print("Funnel Insights:\n", funnel.head())
    print("Creative Outputs:\n", creative_outputs)

if __name__ == "__main__":
    main()
