import pandas as pd
import numpy as np
from pathlib import Path

INPUT_FILE = "results/filtered_station_pairs.csv"
OUTPUT_FILE = "data/processed/pga_difference_dataset.csv"

# Load candidate station pairs
df = pd.read_csv(INPUT_FILE)
print("Original candidate pairs:", len(df))

# Keep pairs with valid, positive PGA values
df = df[
    df["PGA_1_g"].notna()
    & df["PGA_2_g"].notna()
    & (df["PGA_1_g"] > 0)
    & (df["PGA_2_g"] > 0)
].copy()

# Define the prediction target:
# Absolute difference between the log10 PGA values
df["LogPGA_1"] = np.log10(df["PGA_1_g"])
df["LogPGA_2"] = np.log10(df["PGA_2_g"])
df["PGA_Log_Difference"] = (
    df["LogPGA_1"] - df["LogPGA_2"]
).abs()

# Select input features and target
features = [
    "Magnitude",
    "Distance_km",
    "PGA_1_g",
    "PGA_2_g",
    "PGV_1_cm_s",
    "PGV_2_cm_s",
    "Azimuth_1_deg",
    "Azimuth_2_deg",
]

target = "PGA_Log_Difference"

# Retain rows with all selected feature values available
dataset = df[["EQID"] + features + [target]].dropna().copy()

# Save processed dataset
Path("data/processed").mkdir(parents=True, exist_ok=True)
dataset.to_csv(OUTPUT_FILE, index=False)

print("\nRows with valid positive PGA:", len(df))
print("Rows in final dataset:", len(dataset))
print("Unique earthquakes:", dataset["EQID"].nunique())
print("Features:", features)
print("Target:", target)
print(f"\nSaved dataset to: {OUTPUT_FILE}")

print("\nTarget summary:")
print(dataset[target].describe())

print("\nPreview:")
print(dataset.head(10).to_string(index=False))