import pandas as pd

# Input files
file_12620 = "data/Train_ETA_Dataset.tsv"
file_10108 = "data/Train_ETA_Dataset2.tsv"

# Output Excel file
output_file = "data/Train_ETA_Dataset_Master.xlsx"

# Read the two TSV files
train_12620 = pd.read_csv(file_12620, sep="\t")
train_10108 = pd.read_csv(file_10108, sep="\t")

# Create master Excel workbook
with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    # Keep each train's original data separate
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

print("Master dataset created successfully.")
print("File:", output_file)