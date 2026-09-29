import os
import pandas as pd

from network.graph_builder import (
    load_train_data,
    build_railway_graph
)

from network.network_features import (
    get_route
)

from network.delay_propagation import (
    get_section_delays,
    calculate_propagated_delay
)


DATA_FILE = "data/Train_ETA_Dataset_Master.xlsx"

OUTPUT_FILE = (
    "outputs/Member_4_Delay_Propagation.xlsx"
)


os.makedirs(
    "outputs",
    exist_ok=True
)


def create_delay_propagation_dataset(
    train_data,
    graph,
    destination_station
):

    output_rows = []

    for _, row in train_data.iterrows():

        current_station = row[
            "station_code"
        ]

        current_delay = row[
            "current_delay_min"
        ]

        if pd.isna(current_delay):
            current_delay = 0.0

        route = get_route(
            graph,
            current_station,
            destination_station
        )

        if not route:
            continue

        section_delays = get_section_delays(
            graph,
            route
        )

        propagated_delay = (
            calculate_propagated_delay(
                current_delay,
                section_delays
            )
        )

        delay_sections_remaining = len(
            section_delays
        )

        output_row = row.to_dict()

        output_row[
            "propagated_delay_min"
        ] = round(
            propagated_delay,
            2
        )

        output_row[
            "delay_sections_remaining"
        ] = delay_sections_remaining

        output_row[
            "delay_propagation_route"
        ] = " -> ".join(
            route
        )

        output_rows.append(
            output_row
        )

    return pd.DataFrame(
        output_rows
    )


# ==================================================
# TRAIN 12620
# ==================================================

print()
print("================================")
print("DELAY PROPAGATION - TRAIN 12620")
print("================================")

train_12620 = load_train_data(
    DATA_FILE,
    "Train_12620"
)

graph_12620 = build_railway_graph(
    train_12620
)

delay_features_12620 = (
    create_delay_propagation_dataset(
        train_12620,
        graph_12620,
        "KAWR"
    )
)

print(
    "Original rows:",
    len(train_12620)
)

print(
    "Delay propagation rows:",
    len(delay_features_12620)
)


# ==================================================
# TRAIN 10108
# ==================================================

print()
print("================================")
print("DELAY PROPAGATION - TRAIN 10108")
print("================================")

train_10108 = load_train_data(
    DATA_FILE,
    "Train_10108"
)

graph_10108 = build_railway_graph(
    train_10108
)

delay_features_10108 = (
    create_delay_propagation_dataset(
        train_10108,
        graph_10108,
        "KAWR"
    )
)

print(
    "Original rows:",
    len(train_10108)
)

print(
    "Delay propagation rows:",
    len(delay_features_10108)
)


# ==================================================
# SAVE OUTPUT
# ==================================================

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
) as writer:

    delay_features_12620.to_excel(
        writer,
        sheet_name="Train_12620",
        index=False
    )

    delay_features_10108.to_excel(
        writer,
        sheet_name="Train_10108",
        index=False
    )


print()
print("================================")
print("DELAY PROPAGATION DATASET CREATED")
print("================================")

print(
    "Output file:",
    OUTPUT_FILE
)

print(
    "Train 12620 rows:",
    len(delay_features_12620)
)

print(
    "Train 10108 rows:",
    len(delay_features_10108)
)