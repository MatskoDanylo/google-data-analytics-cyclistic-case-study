DAY_ORDER = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]
MONTH_ORDER = list(range(1, 13))

HYPOTHESES = [
    "H1: Casual riders take LONGER rides on average than members (recreation vs commute).",
    "H2: Members ride more during WEEKDAY rush hours; casuals ride more on WEEKENDS.",
    "H3: Casuals show a STRONGER seasonal spike in summer months than members.",
    "H4: Bike type preferences differ between groups (electric vs classic).",
    "H5: Casuals are more likely to take ROUND TRIPS (same start & end station).",
    "H6: Members ride frequency is more CONSISTENT across months; casuals are volatile.",
    "H7: Peak hours differ: members peak at 7-9 AM & 4-6 PM; casuals peak midday.",
]


def print_hypotheses():
    print("\n--- Hypotheses ---")
    for h in HYPOTHESES:
        print(f"  {h}")


def run_analysis(df):
    """Run all analysis computations and return results dict for visualizations."""
    print_hypotheses()

    results = {}

    # 1. Ride duration stats
    print("\n--- 4.1 Ride Duration (minutes) ---")
    duration_stats = df.groupby("member_casual")["ride_length_min"].agg(
        ["mean", "median", "std", "min", "max", "count"]
    )
    print(duration_stats.round(2))
    results["duration_stats"] = duration_stats

    # 2. Rides by day of week
    print("\n--- 4.2 Rides by Day of Week ---")
    rides_by_day = (
        df.groupby(["member_casual", "day_of_week"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=DAY_ORDER)
    )
    print(rides_by_day)

    avg_duration_by_day = (
        df.groupby(["member_casual", "day_of_week"])["ride_length_min"]
        .mean()
        .unstack(fill_value=0)
        .reindex(columns=DAY_ORDER)
    )
    print("\nAverage ride duration by day (minutes):")
    print(avg_duration_by_day.round(2))
    results["rides_by_day"] = rides_by_day
    results["avg_duration_by_day"] = avg_duration_by_day

    # 3. Rides by hour
    print("\n--- 4.3 Rides by Hour of Day ---")
    rides_by_hour = (
        df.groupby(["member_casual", "hour"]).size().unstack(fill_value=0)
    )
    print(rides_by_hour)
    results["rides_by_hour"] = rides_by_hour

    # 4. Monthly ride counts
    print("\n--- 4.4 Monthly Ride Counts ---")
    rides_by_month = (
        df.groupby(["member_casual", "month"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=MONTH_ORDER)
    )
    print(rides_by_month)
    results["rides_by_month"] = rides_by_month

    # 5. Bike type preference
    print("\n--- 4.5 Bike Type Preference ---")
    bike_type = (
        df.groupby(["member_casual", "rideable_type"]).size().unstack(fill_value=0)
    )
    bike_type_pct = bike_type.div(bike_type.sum(axis=1), axis=0) * 100
    print("Counts:")
    print(bike_type)
    print("\nPercentages:")
    print(bike_type_pct.round(2))
    results["bike_type_pct"] = bike_type_pct

    # 6. Round trip rate
    print("\n--- 4.6 Round Trip Rate ---")
    round_trip_rate = df.groupby("member_casual")["is_round_trip"].mean() * 100
    print(round_trip_rate.round(2))
    results["round_trip_rate"] = round_trip_rate

    # 7. Top stations
    print("\n--- 4.7 Top 10 Start Stations ---")
    for rider_type in ["member", "casual"]:
        print(f"\n  Top 10 for {rider_type}s:")
        top = (
            df[df["member_casual"] == rider_type]["start_station_name"]
            .value_counts()
            .head(10)
        )
        for i, (station, count) in enumerate(top.items(), 1):
            print(f"    {i:2d}. {station} -- {count:,} rides")

    # 8. Avg ride duration by hour
    print("\n--- 4.8 Average Ride Duration by Hour ---")
    avg_dur_hour = (
        df.groupby(["member_casual", "hour"])["ride_length_min"]
        .mean()
        .unstack(fill_value=0)
    )
    print(avg_dur_hour.round(2))
    results["avg_dur_hour"] = avg_dur_hour

    return results
