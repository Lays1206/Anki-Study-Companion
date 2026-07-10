import pandas as pd


def load_terms(filepath):
    df = pd.read_csv(filepath, names=["terms", "readings", "definitions"])

    for i, row in df.iterrows():
        if pd.isna(row["terms"]):
            reading = row["readings"]
            df.at[i, "terms"] = reading
        
    return df["terms"].tolist()