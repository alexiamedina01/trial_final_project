import pandas as pd
from pathlib import Path

def load_dataset(filename):
    """
    Loads a compressed CSV (.csv.gz) file safely with pandas.
    """
    path = Path(__file__).resolve().parents[2] / "data" / filename
    
    df = pd.read_csv(path, compression="gzip", low_memory=False)
    print(f"Loaded {filename} → {df.shape[0]:,} rows, {df.shape[1]} columns")
    return df
