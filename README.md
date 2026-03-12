# Cyclistic Bike-Share Analysis

A data analysis project exploring how **annual members** and **casual riders** use Cyclistic bikes differently. Built as part of the Google Data Analytics Professional Certificate case study.

## Business Question

> How do annual members and casual riders use Cyclistic bikes differently?

## Dataset

- **Source:** Divvy trip data (January–December 2025)
- **Size:** ~5.5 million rides across 12 monthly CSV files
- **Key fields:** `ride_id`, `rideable_type`, `started_at`, `ended_at`, `start_station_name`, `end_station_name`, `start_lat/lng`, `end_lat/lng`, `member_casual`

> CSV files are not included in this repository due to size constraints. Download them from [Divvy trip data](https://divvy-tripdata.s3.amazonaws.com/index.html) and place them in the `datasets/` folder.

## Key Findings

| Metric | Members | Casuals |
|---|---|---|
| Avg ride duration | 12.2 min | 19.9 min |
| Share of total rides | 64.5% | 35.5% |
| Busiest days | Weekdays (Tue–Thu) | Weekends (Sat–Sun) |
| Peak hours | 7–9 AM & 4–6 PM | 12–5 PM |
| Round trip rate | 1.5% | 5.6% |
| Top stations | Near offices & transit | Near parks & tourist spots |
| Seasonality | Stable year-round | Sharp summer spike |

**Conclusion:** Members use bikes primarily for **daily commuting** (short, consistent, weekday rush-hour rides). Casuals use bikes for **recreation and tourism** (longer rides, weekends, afternoons, lakefront areas, more round trips).

## Project Structure

```
├── main.py                 # Entry point — runs the full pipeline
├── src/
│   ├── __init__.py
│   ├── load.py             # Load & merge 12 monthly CSV files
│   ├── clean.py            # Data cleaning & feature engineering
│   ├── analyze.py          # Statistical analysis & summary
│   └── visualize.py        # Matplotlib chart generation
├── datasets/               # Raw CSV files (git-ignored)
│   └── .gitkeep
├── output/                 # Generated charts & cleaned CSV (git-ignored)
│   └── .gitkeep
├── requirements.txt
└── .gitignore
```

## Setup & Usage

```bash
# Clone the repository
git clone https://github.com/<your-username>/cyclistic-bike-share-analysis.git
cd cyclistic-bike-share-analysis

# Install dependencies
pip install -r requirements.txt

# Place the 12 CSV files in the datasets/ folder, then run:
python main.py
```

## Output

The script generates:

- **6 charts** in `output/` — day of week, hour of day, seasonality, bike type, duration distribution, round trip rate
- **`cyclistic_cleaned.csv`** in `output/` — the merged and cleaned dataset ready for Tableau or further analysis

## Tools Used

- **Python** — pandas, numpy, matplotlib