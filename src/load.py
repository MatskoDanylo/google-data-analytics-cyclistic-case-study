import os
import glob
import pandas as pd


def load_and_merge(data_path):
    """Load all CSV files from data_path and merge into a single DataFrame."""
    csv_files = sorted(glob.glob(os.path.join(data_path, "*.csv")))

    print(f"Found {len(csv_files)} CSV files:")
    for f in csv_files:
        print(f"  - {os.path.basename(f)}")

    df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
    print(f"\nTotal rows after merge: {len(df):,}")
    print(f"Columns: {list(df.columns)}")
    return df
