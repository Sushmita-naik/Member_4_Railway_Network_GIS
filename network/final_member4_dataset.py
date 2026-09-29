import os
import pandas as pd


ORIGINAL_FILE = "data/Train_ETA_Dataset_Master.xlsx"

NETWORK_FILE = "outputs/Member_4_Network_Features.xlsx"

DELAY_FILE = "outputs/Member_4_Delay_Propagation.xlsx"

OUTPUT_FILE = "outputs/Member_4_Final_Features.xlsx"


os.makedirs(
    "outputs",
    exist_ok=True
)


def combine_features(
    original_data,
    network_data,
    delay_data
):
    if len(original_data) != len(network_data):
        raise ValueError(
            "Original and network datasets have different row counts."
        )

    if len(original_data) != len(delay_data):
        raise ValueError(
            "Original and delay datasets have different row counts."
        )

    result = original_data.copy()

    network_columns = [
        "network_distance_remaining_km",
        "network_scheduled_time_remaining_min",
        "network_delay_min",
        "network_route"
    ]

    delay_columns = [
        "propagated_delay_min",
        "delay_sections_remaining",
        "delay_propagation_route"
    ]

    for column in network_columns:
        if column not in network_data.columns:
            raise ValueError(
                f"Missing network column: {column}"
            )

        result[column] = network_data[column].values

    for column in delay_columns:
        if column not in delay_data.columns:
            raise ValueError(
                f"Missing delay column: {column}"
            )

        result[column] = delay_data[column].values

    return result


# ==================================================
# TRAIN 12620
# ==================================================

print()
print("================================")
print("COMBINING TRAIN 12620")
print("================================")

original_12620 = pd.read_excel(
    ORIGINAL_FILE,
    sheet_name="Train_12620",
    engine="openpyxl"
)

network_12620 = pd.read_excel(
    NETWORK_FILE,
    sheet_name="Train_12620",
    engine="openpyxl"
)

delay_12620 = pd.read_excel(
    DELAY_FILE,
    sheet_name="Train_12620",
    engine="openpyxl"
)

final_12620 = combine_features(
    original_12620,
    network_12620,
    delay_12620
)

print(
    "Original rows:",
    len(original_12620)
)

print(
    "Final rows:",
    len(final_12620)
)


# ==================================================
# TRAIN 10108
# ==================================================

print()
print("================================")
print("COMBINING TRAIN 10108")
print("================================")

original_10108 = pd.read_excel(
    ORIGINAL_FILE,
    sheet_name="Train_10108",
    engine="openpyxl"
)

network_10108 = pd.read_excel(
    NETWORK_FILE,
    sheet_name="Train_10108",
    engine="openpyxl"
)

delay_10108 = pd.read_excel(
    DELAY_FILE,
    sheet_name="Train_10108",
    engine="openpyxl"
)

final_10108 = combine_features(
    original_10108,
    network_10108,
    delay_10108
)

print(
    "Original rows:",
    len(original_10108)
)

print(
    "Final rows:",
    len(final_10108)
)


# ==================================================
# SAVE FINAL DATASET
# ==================================================

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
) as writer:

    final_12620.to_excel(
        writer,
        sheet_name="Train_12620",
        index=False
    )

    final_10108.to_excel(
        writer,
        sheet_name="Train_10108",
        index=False
    )


print()
print("================================")
print("FINAL MEMBER 4 DATASET CREATED")
print("================================")

print(
    "Output file:",
    OUTPUT_FILE
)

print(
    "Train 12620 rows:",
    len(final_12620)
)

print(
    "Train 10108 rows:",
    len(final_10108)
)

print(
    "Train 12620 columns:",
    len(final_12620.columns)
)

print(
    "Train 10108 columns:",
    len(final_10108.columns)
)