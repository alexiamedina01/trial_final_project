import pandas as pd
import numpy as np

def clean_listings(df):
    """
    Standard cleaning applied to Airbnb listings data.
    Works for Barcelona and Rome datasets.
    """

    # Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Price-related fields (remove currency symbols)
    # Clean price column safely
    if "price" in df.columns:
        df["price"] = (
            df["price"]
            .astype(str)
            .str.replace(r"[^\d\.]", "", regex=True)
            .replace("", "0")     # cadenas vacías → "0"
            .astype(float)
    )

    # remove zero/invalid values (optional)
        df = df[df["price"] > 0]


    # Convert numeric fields
    numeric_fields = [
        "accommodates", "bedrooms", "beds", "bathrooms",
        "minimum_nights", "maximum_nights"
    ]

    for col in numeric_fields:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convert dates
    if "last_review" in df.columns:
        df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce")

    # Drop extreme prices (optional)
    if "price" in df.columns:
        df = df[df["price"] < df["price"].quantile(0.99)]

    # Remove duplicates
    df = df.drop_duplicates()

    return df
