import pandas as pd
import joblib


DATA_FILE = "outputs/Member_4_ML_Ready.xlsx"

MODEL_FILE = "outputs/train_eta_model.pkl"


FEATURES = [
    "speed_kmph",
    "current_delay_min",
    "distance_from_origin_km",
    "distance_to_next_km",
    "scheduled_travel_min",
    "dwell_time_min",
    "network_distance_remaining_km",
    "network_scheduled_time_remaining_min",
    "network_delay_min",
    "propagated_delay_min",
    "delay_sections_remaining"
]


# ==================================================
# LOAD MODEL
# ==================================================

print()
print("================================")
print("LOADING ETA MODEL")
print("================================")

model = joblib.load(
    MODEL_FILE
)

print("Model loaded successfully.")


# ==================================================
# LOAD HISTORICAL DATA
# ==================================================

train_12620 = pd.read_excel(
    DATA_FILE,
    sheet_name="Train_12620",
    engine="openpyxl"
)

train_10108 = pd.read_excel(
    DATA_FILE,
    sheet_name="Train_10108",
    engine="openpyxl"
)


# ==================================================
# SELECT ONE HISTORICAL RECORD
# ==================================================

sample = train_12620.iloc[[100]].copy()


# ==================================================
# CREATE INPUT
# ==================================================

X_sample = sample[FEATURES]


# ==================================================
# PREDICT
# ==================================================

prediction = model.predict(
    X_sample
)[0]


# ==================================================
# DISPLAY
# ==================================================

print()
print("================================")
print("ETA PREDICTION DEMO")
print("================================")

print(
    "Train ID:",
    sample.iloc[0].get("train_id")
)

print(
    "Current delay:",
    sample.iloc[0]["current_delay_min"],
    "minutes"
)

print(
    "Distance from origin:",
    sample.iloc[0]["distance_from_origin_km"],
    "km"
)

print(
    "Distance to next station:",
    sample.iloc[0]["distance_to_next_km"],
    "km"
)

print(
    "Remaining network distance:",
    sample.iloc[0]["network_distance_remaining_km"],
    "km"
)

print(
    "Scheduled remaining time:",
    sample.iloc[0][
        "network_scheduled_time_remaining_min"
    ],
    "minutes"
)

print()
print(
    "Predicted target delay:",
    round(prediction, 2),
    "minutes"
)

print(
    "Actual target delay:",
    sample.iloc[0]["target_delay_min"],
    "minutes"
)

print()
print("Prediction completed successfully.")