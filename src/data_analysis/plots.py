import matplotlib.pyplot as plt
import seaborn as sns

def plot_price_hist(df, city_name, outpath):
    plt.figure(figsize=(8,5))
    sns.histplot(df["price"], kde=True, bins=50)
    plt.title(f"Price Distribution — {city_name}")
    plt.xlabel("Price (€)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def plot_price_by_room_type(df, city_name, outpath):
    if "room_type" not in df.columns:
        return
    
    plt.figure(figsize=(8,5))
    sns.boxplot(x="room_type", y="price", data=df)
    plt.title(f"Price by Room Type — {city_name}")
    plt.xlabel("Room Type")
    plt.ylabel("Price (€)")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()
