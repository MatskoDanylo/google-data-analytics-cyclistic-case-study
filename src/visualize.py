import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from .analyze import DAY_ORDER

COLORS = {"member": "#4C72B0", "casual": "#DD8452"}
MONTH_LABELS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


def generate_charts(df, results, output_dir):
    """Generate and save all analysis charts to output_dir."""
    os.makedirs(output_dir, exist_ok=True)

    _fig_day_of_week(results, output_dir)
    _fig_hour_of_day(results, output_dir)
    _fig_monthly(results, output_dir)
    _fig_bike_type(results, output_dir)
    _fig_duration_dist(df, output_dir)
    _fig_round_trip(results, output_dir)

    print(f"\nAll charts saved to: {output_dir}/")


# -- individual chart functions ------------------------------------------

def _fig_day_of_week(results, output_dir):
    rides_by_day = results["rides_by_day"]
    avg_duration_by_day = results["avg_duration_by_day"]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    for rider_type in ["member", "casual"]:
        vals = rides_by_day.loc[rider_type]
        axes[0].bar(
            [d[:3] for d in DAY_ORDER], vals,
            label=rider_type.capitalize(), color=COLORS[rider_type],
            alpha=0.8, width=0.35,
            align="edge" if rider_type == "member" else "center",
        )
    axes[0].set_title("Number of Rides by Day of Week", fontsize=13, fontweight="bold")
    axes[0].set_ylabel("Ride Count")
    axes[0].yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}K")
    )
    axes[0].legend()

    for rider_type in ["member", "casual"]:
        vals = avg_duration_by_day.loc[rider_type]
        axes[1].plot(
            [d[:3] for d in DAY_ORDER], vals,
            marker="o", label=rider_type.capitalize(),
            color=COLORS[rider_type], linewidth=2,
        )
    axes[1].set_title(
        "Avg Ride Duration by Day of Week", fontsize=13, fontweight="bold"
    )
    axes[1].set_ylabel("Minutes")
    axes[1].legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "01_day_of_week.png"), dpi=150)
    plt.close()


def _fig_hour_of_day(results, output_dir):
    rides_by_hour = results["rides_by_hour"]
    avg_dur_hour = results["avg_dur_hour"]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    for rider_type in ["member", "casual"]:
        axes[0].plot(
            rides_by_hour.columns, rides_by_hour.loc[rider_type],
            marker="o", label=rider_type.capitalize(),
            color=COLORS[rider_type], linewidth=2,
        )
    axes[0].set_title("Rides by Hour of Day", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Hour")
    axes[0].set_ylabel("Ride Count")
    axes[0].yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}K")
    )
    axes[0].legend()

    for rider_type in ["member", "casual"]:
        axes[1].plot(
            avg_dur_hour.columns, avg_dur_hour.loc[rider_type],
            marker="o", label=rider_type.capitalize(),
            color=COLORS[rider_type], linewidth=2,
        )
    axes[1].set_title("Avg Ride Duration by Hour", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Hour")
    axes[1].set_ylabel("Minutes")
    axes[1].legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "02_hour_of_day.png"), dpi=150)
    plt.close()


def _fig_monthly(results, output_dir):
    rides_by_month = results["rides_by_month"]

    fig, ax = plt.subplots(figsize=(12, 6))
    for rider_type in ["member", "casual"]:
        ax.plot(
            MONTH_LABELS, rides_by_month.loc[rider_type],
            marker="o", label=rider_type.capitalize(),
            color=COLORS[rider_type], linewidth=2.5,
        )
    ax.set_title("Monthly Ride Counts - Seasonality", fontsize=13, fontweight="bold")
    ax.set_ylabel("Ride Count")
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}K")
    )
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "03_monthly_seasonality.png"), dpi=150)
    plt.close()


def _fig_bike_type(results, output_dir):
    bike_type_pct = results["bike_type_pct"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for i, rider_type in enumerate(["member", "casual"]):
        row = bike_type_pct.loc[rider_type]
        axes[i].pie(
            row, labels=row.index, autopct="%1.1f%%",
            startangle=90,
            colors=["#4C72B0", "#DD8452", "#55A868"][: len(row)],
        )
        axes[i].set_title(
            f"{rider_type.capitalize()} - Bike Type",
            fontsize=13, fontweight="bold",
        )
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "04_bike_type.png"), dpi=150)
    plt.close()


def _fig_duration_dist(df, output_dir):
    fig, ax = plt.subplots(figsize=(12, 6))
    for rider_type in ["member", "casual"]:
        subset = df[df["member_casual"] == rider_type]["ride_length_min"]
        ax.hist(
            subset, bins=60, range=(0, 60), alpha=0.6,
            label=rider_type.capitalize(), color=COLORS[rider_type],
        )
    ax.set_title(
        "Ride Duration Distribution (0-60 min)", fontsize=13, fontweight="bold"
    )
    ax.set_xlabel("Ride Duration (minutes)")
    ax.set_ylabel("Number of Rides")
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}K")
    )
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "05_duration_distribution.png"), dpi=150)
    plt.close()


def _fig_round_trip(results, output_dir):
    round_trip_rate = results["round_trip_rate"]

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(
        round_trip_rate.index.str.capitalize(),
        round_trip_rate.values,
        color=[COLORS["member"], COLORS["casual"]],
    )
    ax.set_title("Round Trip Rate (%)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Percentage (%)")
    for i, v in enumerate(round_trip_rate.values):
        ax.text(i, v + 0.3, f"{v:.1f}%", ha="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "06_round_trip_rate.png"), dpi=150)
    plt.close()
