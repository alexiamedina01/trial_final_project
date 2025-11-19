def basic_summary(df):
    summary = {
        "num_rows": len(df),
        "num_cols": len(df.columns),
        "missing_values_percent": df.isnull().mean().sort_values(ascending=False).head(10),
        "avg_price": df["price"].mean() if "price" in df.columns else None,
        "median_price": df["price"].median() if "price" in df.columns else None,
        "room_types": df["room_type"].value_counts() if "room_type" in df.columns else None,
    }
    return summary
