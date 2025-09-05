import os
import glob
import pandas as pd
import numpy as np

TEMPS_FOLDER = "Assignment 2/temperatures"
OUT_AVG = "Assignment 2/average_temp.txt"
OUT_RANGE = "Assignment 2/largest_temp_range_station.txt"
OUT_STABILITY = "Assignment 2/temperature_stability_stations.txt"

# ---------- Helpers ----------
def month_to_season(month):
    # Australian meteorological seasons
    # Summer (Dec-Feb), Autumn (Mar-May), Winter (Jun-Aug), Spring (Sep-Nov)
    if month in (12, 1, 2):
        return "Summer"
    if month in (3, 4, 5):
        return "Autumn"
    if month in (6, 7, 8):
        return "Winter"
    return "Spring"

def write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line.rstrip() + "\n")

def read_all_temperature_data(folder):
    files = sorted(glob.glob(os.path.join(folder, "*.csv")))
    if not files:
        raise FileNotFoundError(f"No CSV files found in '{folder}'")

    frames = []
    for fp in files:
        df = pd.read_csv(fp)
        # Keep station name & monthly columns
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        df = df[["STATION_NAME"] + months]
        # Melt to long format: Station, Month, Temperature
        df_long = df.melt(id_vars="STATION_NAME", value_vars=months,
                          var_name="Month", value_name="Temperature")
        # Map month names to numbers
        month_map = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }
        df_long["Month_Num"] = df_long["Month"].map(month_map)
        df_long["Temperature"] = pd.to_numeric(df_long["Temperature"], errors="coerce")
        frames.append(df_long)
    
    all_data = pd.concat(frames, ignore_index=True)
    # Drop NaNs
    all_data = all_data.dropna(subset=["Temperature"])
    return all_data

# ---------- Calculations ----------
def compute_seasonal_averages(df):
    df["Season"] = df["Month_Num"].apply(month_to_season)
    season_means = df.groupby("Season")["Temperature"].mean()
    order = ["Summer", "Autumn", "Winter", "Spring"]
    lines = []
    for s in order:
        if s in season_means.index:
            lines.append(f"{s}: {season_means.loc[s]:.1f}°C")
        else:
            lines.append(f"{s}: N/A")
    return lines

def compute_largest_temperature_range(df):
    g = df.groupby("STATION_NAME")["Temperature"]
    stats = g.agg(temp_min="min", temp_max="max")
    stats["Range"] = stats["temp_max"] - stats["temp_min"]
    max_range = stats["Range"].max()
    winners = stats[np.isclose(stats["Range"], max_range)]
    lines = [
        f"{station}: Range {row['Range']:.1f}°C (Max: {row['temp_max']:.1f}°C, Min: {row['temp_min']:.1f}°C)"
        for station, row in winners.iterrows()
    ]
    return lines

def compute_temperature_stability(df):
    g = df.groupby("STATION_NAME")["Temperature"]
    stds = g.std(ddof=1).dropna()
    min_std = stds.min()
    max_std = stds.max()
    most_stable = stds[np.isclose(stds, min_std)]
    most_variable = stds[np.isclose(stds, max_std)]
    lines = [f"Most Stable: {st}: StdDev {most_stable.loc[st]:.1f}°C" for st in most_stable.index]
    lines += [f"Most Variable: {st}: StdDev {most_variable.loc[st]:.1f}°C" for st in most_variable.index]
    return lines

# ---------- Main ----------
def main():
    df = read_all_temperature_data(TEMPS_FOLDER)

    # 1) Seasonal averages
    avg_lines = compute_seasonal_averages(df)
    write_lines(OUT_AVG, avg_lines)

    # 2) Largest temperature range
    range_lines = compute_largest_temperature_range(df)
    write_lines(OUT_RANGE, range_lines)

    # 3) Temperature stability
    stability_lines = compute_temperature_stability(df)
    write_lines(OUT_STABILITY, stability_lines)

    # Console summary
    print(f"Wrote {OUT_AVG}")
    print(f"Wrote {OUT_RANGE}")
    print(f"Wrote {OUT_STABILITY}")

if __name__ == "__main__":
    main()
