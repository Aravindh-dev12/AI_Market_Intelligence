import pandas as pd

def clean_google_play(filepath):
    df = pd.read_csv(filepath)
    df = df.drop_duplicates(subset="App")
    df = df.fillna({"Rating": 0, "Reviews": 0})
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(0)
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce').fillna(0)
    df.to_csv("data/cleaned_data/google_play_clean.csv", index=False)
    return df

def load_d2c_excel(filepath):
    excel_dict = pd.read_excel(filepath, sheet_name=None)
    print("Available sheets in D2C Excel:", list(excel_dict.keys()))
    return excel_dict
