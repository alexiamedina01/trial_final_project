import os
from pathlib import Path

from .load_data import load_dataset
from .clean_data import clean_listings
from .explore_data import basic_summary
from .plots import plot_price_hist, plot_price_by_room_type

import pandas as pd

REPORTS = Path(__file__).resolve().parents[2] / "reports"
REPORTS.mkdir(exist_ok=True)

def run_city(filename, city_name):
    print(f"\n=== Processing {city_name} ===\n")

    df = load_dataset(filename)
    df = clean_listings(df)

    summary = basic_summary(df)

    # Save summary to CSV
    summary_path = REPORTS / f"{city_name.lower()}_summary.csv"
    pd.DataFrame(summary).to_csv(summary_path)
    print(f"Saved summary → {summary_path}")

    # Plots
    plot_price_hist(df, city_name, REPORTS / f"{city_name.lower()}_hist_price.png")
    plot_price_by_room_type(df, city_name, REPORTS / f"{city_name.lower()}_price_by_room.png")


def main():
    run_city("listings.csv.gz", "Barcelona")
    run_city("rome_listings.csv.gz", "Rome")


if __name__ == "__main__":
    main()
