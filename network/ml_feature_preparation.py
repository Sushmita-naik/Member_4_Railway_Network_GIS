import os
import pandas as pd


INPUT_FILE = "outputs/Member_4_Final_Features.xlsx"

OUTPUT_FILE = "outputs/Member_4_ML_Ready.xlsx"


os.makedirs(
    "outputs",
    exist_ok=True
)


# ==================================================
# FEATURES
# ==================================================

FEATURE_COLUMNS = [
    "speed_kmph",
    "current_delay_min",
    "distance_from_origin_km",
    "distance_to_next_km",
    "scheduled_travel_min",
    "dwell_time_min",
    "preceding_train_delay_min",
    "network_distance_remaining_km",
    "network_scheduled_time_remaining_min",
    "network_delay_min",
    "propagated_delay_min",
    "delay_sections_remaining"
]


TARGET_COLUMN = "target_delay_min"


# ==================================================
# FUNCTION
# ==================================================

def prepare_train_data(
    input_file,
    sheet_name
):

    data = pd.read_excel(
        input_file,
        sheet_name=sheet_name,
        engine="openpyxl"
    )

    print()
    print("Original rows:", len(data))

    # ----------------------------------------------
    # Keep only required columns
    # ----------------------------------------------

    selected_columns = (
        FEATURE_COLUMNS
        + [TARGET_COLUMN]
    )

    data = data[selected_columns].copy()

    # ----------------------------------------------
    # Convert feature columns to numeric
    # ----------------------------------------------

    for column in FEATURE_COLUMNS:

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    # ----------------------------------------------
    # Convert target to numeric
    # ----------------------------------------------

    data[TARGET_COLUMN] = pd.to_numeric(
        data[TARGET_COLUMN],
        errors="coerce"
    )

    # ----------------------------------------------
    # Missing values before cleaning
    # ----------------------------------------------

    print()
    print("Missing values before cleaning:")

    print(
        data.isnull().sum()
    )

    # ----------------------------------------------
    # Fill missing FEATURE values
    # ----------------------------------------------

    for column in FEATURE_COLUMNS:

        median_value = data[column].median()

        data[column] = data[column].fillna(
            median_value
        )

    # ----------------------------------------------
    # Remove rows with missing TARGET
    # ----------------------------------------------

    before_target_removal = len(data)

    data = data.dropna(
        subset=[TARGET_COLUMN]
    )

    removed_rows = (
        before_target_removal
        - len(data)
    )

    print()
    print(
        "Rows removed because target was missing:",
        removed_rows
    )

    # ----------------------------------------------
    # Final missing-value check
    # ----------------------------------------------

    print()
    print("Missing values after cleaning:")

    print(
        data.isnull().sum()
    )

    return data


# ==================================================
# TRAIN 12620
# ==================================================

print()
print("================================")
print("PREPARING TRAIN 12620")
print("================================")

train_12620 = prepare_train_data(
    INPUT_FILE,
    "Train_12620"
)

print()
print(
    "Final Train 12620 rows:",
    len(train_12620)
)

print(
    "Final Train 12620 columns:",
    len(train_12620.columns)
)


# ==================================================
# TRAIN 10108
# ==================================================

print()
print("================================")
print("PREPARING TRAIN 10108")
print("================================")

train_10108 = prepare_train_data(
    INPUT_FILE,
    "Train_10108"
)

print()
print(
    "Final Train 10108 rows:",
    len(train_10108)
)

print(
    "Final Train 10108 columns:",
    len(train_10108.columns)
)


# ==================================================
# SAVE
# ==================================================

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
) as writer:

    train_12620.to_excel(
        writer,
        sheet_name="Train_12620",
        index=False
    )

    train_10108.to_excel(
        writer,
        sheet_name="Train_10108",
        index=False
    )


# ==================================================
# FINAL MESSAGE
# ==================================================

print()
print("================================")
print("ML-READY DATASET CREATED")
print("================================")

print(
    "Output file:",
    OUTPUT_FILE
)

print()
print(
    "Train 12620 rows:",
    len(train_12620)
)

print(
    "Train 10108 rows:",
    len(train_10108)
)

print()
print(
    "Number of input features:",
    len(FEATURE_COLUMNS)
)

print(
    "Target:",
    TARGET_COLUMN
)

print()
print("Dataset preparation completed successfully.")