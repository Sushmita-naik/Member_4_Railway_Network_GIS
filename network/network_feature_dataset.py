import os
import pandas as pd

from network.graph_builder import (
    load_train_data,
    build_railway_graph
)

from network.network_features import (
    create_network_feature_dataset
)


DATA_FILE = "data/Train_ETA_Dataset_Master.xlsx"

OUTPUT_FILE = "outputs/Member_4_Network_Features.xlsx"


os.makedirs(
    "outputs",
    exist_ok=True
)


# ==================================================
# TRAIN 12620
# ==================================================

print()
print("================================")
print("PROCESSING TRAIN 12620")
print("================================")

train_12620 = load_train_data(
    DATA_FILE,
    "Train_12620"
)

graph_12620 = build_railway_graph(
    train_12620
)

features_12620 = create_network_feature_dataset(
    train_12620,
    graph_12620,
    "KAWR"
)

print(
    "Original rows:",
    len(train_12620)
)

print(
    "Network feature rows:",
    len(features_12620)
)


# ==================================================
# TRAIN 10108
# ==================================================

print()
print("================================")
print("PROCESSING TRAIN 10108")
print("================================")

train_10108 = load_train_data(
    DATA_FILE,
    "Train_10108"
)

graph_10108 = build_railway_graph(
    train_10108
)

features_10108 = create_network_feature_dataset(
    train_10108,
    graph_10108,
    "KAWR"
)

print(
    "Original rows:",
    len(train_10108)
)

print(
    "Network feature rows:",
    len(features_10108)
)


# ==================================================
# SAVE OUTPUT
# ==================================================

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
) as writer:

    features_12620.to_excel(
        writer,
        sheet_name="Train_12620",
        index=False
    )

    features_10108.to_excel(
        writer,
        sheet_name="Train_10108",
        index=False
    )


print()
print("================================")
print("NETWORK FEATURE DATASET CREATED")
print("================================")

print(
    "Output file:",
    OUTPUT_FILE
)

print(
    "Train 12620 rows:",
    len(features_12620)
)

print(
    "Train 10108 rows:",
    len(features_10108)
)