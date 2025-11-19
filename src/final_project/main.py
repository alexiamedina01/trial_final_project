# src/final_project/main.py
import os
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from .city import City

# reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

REPORTS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

def run_simulation(bid_fraction=1.0, steps=180, seed=RANDOM_SEED):
    # reset seeds to ensure reproducible runs independently
    random.seed(seed)
    np.random.seed(seed)

    area_rates = {0: (100, 200), 1: (50, 250), 2: (250, 350), 3: (150, 450)}
    city = City(size=10, area_rates=area_rates, bid_fraction=bid_fraction)
    city.initialize()

    # run steps
    transactions_over_time = []
    for t in range(steps):
        tx = city.iterate()
        transactions_over_time.append(tx)

    return city, transactions_over_time

def compute_wealth(city):
    """
    Wealth per host = host.profits + sum(latest sale price of owned properties)
    Returns DataFrame with columns: host_id, wealth, area, n_assets
    """
    rows = []
    for host in city.hosts:
        assets = list(host.assets)
        latest_prices = []
        for pid in assets:
            place = city.places[pid]
            if place.price:
                latest_step = max(place.price.keys())
                latest_prices.append(place.price[latest_step])
            else:
                latest_prices.append(0.0)
        wealth = host.profits + sum(latest_prices)
        rows.append({
            'host_id': host.host_id,
            'wealth': wealth,
            'area': host.area,
            'n_assets': len(assets)
        })
    df = pd.DataFrame(rows)
    return df

def plot_graph1(df, outpath):
    """
    Vertical bar chart:
     - Each bar = host
     - height = host wealth
     - color = host area (0..3)
     - bars sorted from smallest to largest wealth
    """
    df_sorted = df.sort_values('wealth', ascending=True).reset_index(drop=True)
    colors_map = {0: '#1f77b4', 1: '#ff7f0e', 2: '#2ca02c', 3: '#d62728'}  # clear colors
    bar_colors = [colors_map[a] for a in df_sorted['area']]

    plt.figure(figsize=(12, 6))
    plt.bar(range(len(df_sorted)), df_sorted['wealth'], color=bar_colors)
    plt.xlabel('Hosts (sorted by wealth)')
    plt.ylabel('Wealth (profits + property values)')
    plt.title('Wealth per host (sorted). Color = origin area')
    # legend: show area categories
    from matplotlib.patches import Patch
    legend_handles = [Patch(color=colors_map[i], label=f'Area {i}') for i in range(4)]
    plt.legend(handles=legend_handles, title='Home area', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()

def plot_graph2_assets(df, outpath, top_n=20):
    """
    Additional graph: show concentration of ownership.
    Bar chart of number of assets per host, sorted descending (top_n shown).
    This highlights whether few hosts control most properties.
    """
    df_sorted = df.sort_values('n_assets', ascending=False).reset_index(drop=True)
    df_top = df_sorted.head(top_n)
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(df_top)), df_top['n_assets'])
    plt.xlabel(f'Top {top_n} hosts (by assets)')
    plt.ylabel('Number of assets owned')
    plt.title('Concentration of listings: assets per host (top hosts)')
    plt.xticks(range(len(df_top)), df_top['host_id'], rotation=45)
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()

def main():
    # --- Run original version (v0) ---
    city_v0, tx0 = run_simulation(bid_fraction=1.0, steps=180, seed=RANDOM_SEED)
    df_v0 = compute_wealth(city_v0)

    graph1_path = os.path.join(REPORTS_DIR, 'graph1.png')
    plot_graph1(df_v0, graph1_path)
    print(f"Saved {graph1_path}")

    graph2_v0 = os.path.join(REPORTS_DIR, 'graph2_v0.png')
    plot_graph2_assets(df_v0, graph2_v0, top_n=20)
    print(f"Saved {graph2_v0}")

    # --- Run modified version (v1) with more conservative bidding (50% of profits) ---
    city_v1, tx1 = run_simulation(bid_fraction=0.5, steps=180, seed=RANDOM_SEED)
    df_v1 = compute_wealth(city_v1)

    graph2_v1 = os.path.join(REPORTS_DIR, 'graph2_v1.png')
    plot_graph2_assets(df_v1, graph2_v1, top_n=20)
    print(f"Saved {graph2_v1}")

if __name__ == "__main__":
    main()
