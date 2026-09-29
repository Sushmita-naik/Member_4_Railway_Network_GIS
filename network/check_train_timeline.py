import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILE = BASE_DIR / "data" / "Train_ETA_Dataset_Master.xlsx"

df = pd.read_excel(
    FILE,
    sheet_name="Train_12620"
)

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

df = df.sort_values("timestamp").reset_index(drop=True)

# Show records around the time we are investigating
target_time = pd.Timestamp("2025-01-08 13:49:00")

nearby = df[
    (df["timestamp"] >= target_time - pd.Timedelta(minutes=30))
    &
    (df["timestamp"] <= target_time + pd.Timedelta(minutes=60))
]

columns = [
    "timestamp",
    "station_code",
    "Station_full_name",
    "speed_kmph",
    "Arrival_time",
    "Dep. Time",
    "distance_from_origin_km",
    "distance_to_next_km",
    "current_delay_min"
]

print()
print("=" * 100)
print("TRAIN 12620 TIMELINE")
print("=" * 100)

print(
    nearby[columns].to_string(index=False)
)

print("=" * 100)