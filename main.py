import os
from src.load import load_and_merge
from src.clean import inspect, clean
from src.analyze import run_analysis
from src.visualize import generate_charts

ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, "datasets")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")


def main():
    # 1. Load & merge
    df = load_and_merge(DATA_DIR)

    # 2. Inspect & clean
    inspect(df)
    df = clean(df)

    # 3. Analyze
    results = run_analysis(df)

    # 4. Visualize
    generate_charts(df, results, OUTPUT_DIR)

    # 5. Export cleaned data into single CSV
    final_dataset_path = os.path.join(OUTPUT_DIR, "cyclistic_cleaned.csv")
    df.to_csv(final_dataset_path, index=False)
    print(f"\nExported {len(df):,} rows to: {final_dataset_path}")
    print(f"File size: {os.path.getsize(final_dataset_path) / (1024**2):.1f} MB")


if __name__ == "__main__":
    main()
