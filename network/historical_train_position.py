import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "Train_ETA_Dataset_Master.xlsx"


# ============================================================
# TRAIN CONFIGURATION
# ============================================================

TRAIN_ID = 12620

# Select the historical record number that you want to examine.
# 0 = first record
# 100 = 101st record
# Change this number later.
RECORD_INDEX = 100


# ============================================================
# LOAD TRAIN DATA
# ============================================================

def load_train_data(train_id):

    excel = pd.ExcelFile(DATA_FILE)

    selected_sheet = None

    for sheet in excel.sheet_names:

        df = pd.read_excel(
            DATA_FILE,
            sheet_name=sheet
        )

        if "train_id" not in df.columns:
            continue

        train_ids = pd.to_numeric(
            df["train_id"],
            errors="coerce"
        )

        if train_id in train_ids.dropna().astype(int).unique():

            selected_sheet = sheet
            break

    if selected_sheet is None:

        raise ValueError(
            f"Train {train_id} was not found."
        )

    df = pd.read_excel(
        DATA_FILE,
        sheet_name=selected_sheet
    )

    df["train_id"] = pd.to_numeric(
        df["train_id"],
        errors="coerce"
    )

    df = df[df["train_id"] == train_id].copy()

    print(f"Train ID       : {train_id}")
    print(f"Sheet           : {selected_sheet}")
    print(f"Total records   : {len(df)}")

    return df


# ============================================================
# CLEAN TIME
# ============================================================

def convert_to_datetime(df):

    # --------------------------------------------------------
    # 12620 has timestamp
    # --------------------------------------------------------

    if "timestamp" in df.columns:

        df["datetime"] = pd.to_datetime(
            df["timestamp"],
            errors="coerce"
        )

    # --------------------------------------------------------
    # 10108 may have journey_date + time
    # --------------------------------------------------------

    elif (
        "journey_date" in df.columns
        and "Actual_Arrival_time" in df.columns
    ):

        df["datetime"] = pd.to_datetime(
            df["journey_date"].astype(str)
            + " "
            + df["Actual_Arrival_time"].astype(str),
            errors="coerce"
        )

    else:

        raise ValueError(
            "Could not find a usable date/time column."
        )

    return df


# ============================================================
# FIND HISTORICAL POSITION
# ============================================================

def get_historical_position(df, record_index):

    # Remove rows where time is unavailable

    df = df.dropna(
        subset=["datetime"]
    ).copy()

    if df.empty:

        raise ValueError(
            "No valid timestamp records found."
        )

    # Sort chronologically

    df = df.sort_values(
        "datetime"
    ).reset_index(drop=True)

    # Check requested index

    if record_index >= len(df):

        raise IndexError(
            f"Record {record_index} does not exist. "
            f"Available records: 0 to {len(df)-1}"
        )

    row = df.iloc[record_index]

    return row


# ============================================================
# CALCULATE EXPECTED SECTION POSITION
# ============================================================

def calculate_position(row):

    station = row.get(
        "station_code",
        "UNKNOWN"
    )

    distance_from_origin = pd.to_numeric(
        row.get("distance_from_origin_km"),
        errors="coerce"
    )

    distance_to_next = pd.to_numeric(
        row.get("distance_to_next_km"),
        errors="coerce"
    )

    speed = pd.to_numeric(
        row.get("speed_kmph"),
        errors="coerce"
    )

    current_delay = pd.to_numeric(
        row.get("current_delay_min"),
        errors="coerce"
    )

    scheduled_travel = pd.to_numeric(
        row.get("scheduled_travel_min"),
        errors="coerce"
    )

    print()
    print("=" * 60)
    print("HISTORICAL TRAIN POSITION")
    print("=" * 60)

    print(f"Train ID                 : {row['train_id']}")
    print(f"Recorded time            : {row['datetime']}")
    print(f"Recorded station         : {station}")

    print(
        f"Distance from origin    : "
        f"{distance_from_origin} km"
    )

    print(
        f"Distance to next station: "
        f"{distance_to_next} km"
    )

    print(
        f"Speed                   : "
        f"{speed} km/h"
    )

    print(
        f"Current delay           : "
        f"{current_delay} min"
    )

    print(
        f"Scheduled travel        : "
        f"{scheduled_travel} min"
    )

    # --------------------------------------------------------
    # Determine whether train is moving
    # --------------------------------------------------------

    if pd.notna(speed) and speed > 0:

        status = "Train is moving"

    else:

        status = "Train is stopped / station record"

    print(f"Status                  : {status}")

    # --------------------------------------------------------
    # Estimate travel time to next station
    # --------------------------------------------------------

    if (
        pd.notna(distance_to_next)
        and pd.notna(speed)
        and speed > 0
    ):

        estimated_minutes = (
            distance_to_next / speed
        ) * 60

        print(
            f"Estimated time to next "
            f"station                 : "
            f"{estimated_minutes:.2f} min"
        )

    else:

        estimated_minutes = None

        print(
            "Estimated time to next "
            "station                 : Not available"
        )

    return {
        "train_id": row["train_id"],
        "datetime": row["datetime"],
        "station_code": station,
        "distance_from_origin_km": distance_from_origin,
        "distance_to_next_km": distance_to_next,
        "speed_kmph": speed,
        "current_delay_min": current_delay,
        "estimated_minutes_to_next": estimated_minutes,
    }


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print("Loading historical train data...")

    train_df = load_train_data(
        TRAIN_ID
    )

    train_df = convert_to_datetime(
        train_df
    )

    position = get_historical_position(
        train_df,
        RECORD_INDEX
    )

    result = calculate_position(
        position
    )

    print()
    print("=" * 60)
    print("POSITION RESULT")
    print("=" * 60)

    print(result)

    print()
    print("Historical position calculation completed.")