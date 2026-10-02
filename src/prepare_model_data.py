import pandas as pd
import numpy as np
from pathlib import Path

INPUT_FILE = "results/filtered_station_pairs.csv"
OUTPUT_FILE = "data/processed/model_dataset.csv"

df = pd.read_csv(INPUT_FILE)

# Keep rows with valid positive PGA values
df = df[
    df["PGA_1_g"].notna()
    & df["PGA_2_g"].notna()
    & (df["PGA_1_g"] > 0)
    & (df["PGA_2_g"] > 0)
].copy()

# Calculate the target: absolute log10 PGA difference
df["PGA_Log_Difference"] = (
    np.log10(df["PGA_1_g"]) - np.log10(df["PGA_2_g"])
).abs()

# Calculate the smallest circular difference between source-to-site azimuths
df["Azimuth_Difference_deg"] = (
    (df["Azimuth_1_deg"] - df["Azimuth_2_deg"] + 180) % 360
) - 180
df["Azimuth_Difference_deg"] = df["Azimuth_Difference_deg"].abs()

# Use only predictors that do not directly contain the target PGA/PGV values
features = [
    "Magnitude",
    "Distance_km",
    "Azimuth_Difference_deg",
]
target = "PGA_Log_Difference"

dataset = df[["EQID"] + features + [target]].dropna().copy()

Path("data/processed").mkdir(parents=True, exist_ok=True)
dataset.to_csv(OUTPUT_FILE, index=False)

print("Model dataset created.")
print("Rows:", len(dataset))
print("Unique earthquakes:", dataset["EQID"].nunique())
print("Features:", features)
print("Target:", target)
print("Saved to:", OUTPUT_FILE)
print("\nTarget statistics:")
print(dataset[target].describe())
print("\nPreview:")
print(dataset.head(10).to_string(index=False))