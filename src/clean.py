import numpy as np
import pandas as pd


def inspect(df):
    """Print initial data quality info."""
    print("\n--- Data types (before cleaning) ---")
    print(df.dtypes)
    print(f"\n--- Shape: {df.shape} ---")
    print(f"\n--- Null counts ---")
    print(df.isnull().sum())
    print(f"\n--- Duplicated ride_id count: {df['ride_id'].duplicated().sum()} ---")


def clean(df):
    """Clean the merged DataFrame and derive new columns.

    Steps:
      1. Remove duplicate ride IDs
      2. Parse datetime columns
      3. Derive: ride_length_min, day_of_week, month, month_name,
                 hour, is_round_trip, weekday_weekend
      4. Drop invalid rides (< 1 min, > 24 h, null timestamps)
    """
    # Duplicates
    before = len(df)
    df = df.drop_duplicates(subset="ride_id")
    print(f"Dropped {before - len(df):,} duplicate ride_id rows")

    # Datetime parsing
    df["started_at"] = pd.to_datetime(df["started_at"], errors="coerce")
    df["ended_at"] = pd.to_datetime(df["ended_at"], errors="coerce")

    # Derived columns
    df["ride_length_min"] = (
        (df["ended_at"] - df["started_at"]).dt.total_seconds() / 60
    )
    df["day_of_week"] = df["started_at"].dt.day_name()
    df["month"] = df["started_at"].dt.month
    df["month_name"] = df["started_at"].dt.month_name()
    df["hour"] = df["started_at"].dt.hour
    df["is_round_trip"] = (
        (df["start_station_id"] == df["end_station_id"])
        & df["start_station_id"].notna()
        & df["end_station_id"].notna()
    ).astype(int)
    df["weekday_weekend"] = np.where(
        df["started_at"].dt.dayofweek < 5, "Weekday", "Weekend"
    )

    # Remove invalid rides
    before = len(df)
    df = df[
        (df["ride_length_min"] >= 1)
        & (df["ride_length_min"] <= 1440)
        & df["started_at"].notna()
        & df["ended_at"].notna()
    ]
    print(
        f"Dropped {before - len(df):,} invalid rides "
        "(< 1 min, > 24 h, or null timestamps)"
    )
    print(f"Clean dataset size: {len(df):,} rows")

    # Verify target column
    print(f"\nmember_casual values: {df['member_casual'].unique()}")
    print(df["member_casual"].value_counts())

    return df
