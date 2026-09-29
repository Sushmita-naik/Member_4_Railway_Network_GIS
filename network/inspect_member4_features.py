import pandas as pd


FILE = "outputs/Member_4_Final_Features.xlsx"


print()
print("================================")
print("MEMBER 4 FEATURE INSPECTION")
print("================================")


# ==========================================
# TRAIN 12620
# ==========================================

train_12620 = pd.read_excel(
    FILE,
    sheet_name="Train_12620",
    engine="openpyxl"
)

print()
print("TRAIN 12620")
print("Rows:", len(train_12620))
print("Columns:", len(train_12620.columns))

print()
print("Column names:")

for number, column in enumerate(
    train_12620.columns,
    start=1
):
    print(
        number,
        "->",
        column
    )


# ==========================================
# TRAIN 10108
# ==========================================

train_10108 = pd.read_excel(
    FILE,
    sheet_name="Train_10108",
    engine="openpyxl"
)

print()
print("TRAIN 10108")
print("Rows:", len(train_10108))
print("Columns:", len(train_10108.columns))

print()
print("Column names:")

for number, column in enumerate(
    train_10108.columns,
    start=1
):
    print(
        number,
        "->",
        column
    )


# ==========================================
# TARGET CHECK
# ==========================================

print()
print("================================")
print("TARGET CHECK")
print("================================")

for column in train_12620.columns:

    if "target" in column.lower():

        print(
            "12620 target column:",
            column
        )


for column in train_10108.columns:

    if "target" in column.lower():

        print(
            "10108 target column:",
            column
        )


print()
print("Inspection completed.")