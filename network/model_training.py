import os
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import joblib


INPUT_FILE = "outputs/Member_4_ML_Ready.xlsx"

MODEL_FILE = "outputs/train_eta_model.pkl"


os.makedirs(
    "outputs",
    exist_ok=True
)


# ==================================================
# FEATURES
# ==================================================

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

TARGET = "target_delay_min"


# ==================================================
# LOAD DATA
# ==================================================

print()
print("================================")
print("LOADING ML DATASET")
print("================================")

train_12620 = pd.read_excel(
    INPUT_FILE,
    sheet_name="Train_12620",
    engine="openpyxl"
)

train_10108 = pd.read_excel(
    INPUT_FILE,
    sheet_name="Train_10108",
    engine="openpyxl"
)


# ==================================================
# COMBINE TRAINS
# ==================================================

data = pd.concat(
    [
        train_12620,
        train_10108
    ],
    ignore_index=True
)

print(
    "Total rows:",
    len(data)
)


# ==================================================
# CHECK FEATURES
# ==================================================

print()
print("Features used:")

for feature in FEATURES:
    print(
        "-",
        feature
    )


# ==================================================
# CREATE X AND Y
# ==================================================

X = data[FEATURES]

y = data[TARGET]


print()
print(
    "Input feature rows:",
    X.shape
)

print(
    "Target rows:",
    y.shape
)


# ==================================================
# TRAIN TEST SPLIT
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


print()
print("================================")
print("TRAIN TEST SPLIT")
print("================================")

print(
    "Training rows:",
    len(X_train)
)

print(
    "Testing rows:",
    len(X_test)
)


# ==================================================
# RANDOM FOREST MODEL
# ==================================================

print()
print("================================")
print("TRAINING RANDOM FOREST")
print("================================")

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


model.fit(
    X_train,
    y_train
)


print(
    "Model training completed."
)


# ==================================================
# PREDICTION
# ==================================================

y_pred = model.predict(
    X_test
)


# ==================================================
# EVALUATION
# ==================================================

mae = mean_absolute_error(
    y_test,
    y_pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred
    )
)

r2 = r2_score(
    y_test,
    y_pred
)


print()
print("================================")
print("MODEL EVALUATION")
print("================================")

print(
    "MAE:",
    round(mae, 3),
    "minutes"
)

print(
    "RMSE:",
    round(rmse, 3),
    "minutes"
)

print(
    "R2 Score:",
    round(r2, 3)
)


# ==================================================
# FEATURE IMPORTANCE
# ==================================================

print()
print("================================")
print("FEATURE IMPORTANCE")
print("================================")

importance = pd.DataFrame(
    {
        "feature": FEATURES,
        "importance": model.feature_importances_
    }
)

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print(
    importance.to_string(
        index=False
    )
)


# ==================================================
# SAVE MODEL
# ==================================================

joblib.dump(
    model,
    MODEL_FILE
)


print()
print("================================")
print("MODEL SAVED")
print("================================")

print(
    "Model file:",
    MODEL_FILE
)

print()
print("Training completed successfully.")