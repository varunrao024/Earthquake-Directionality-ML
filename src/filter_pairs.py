import pandas as pd

input_file = "results/candidate_station_pairs.csv"
output_file = "results/filtered_station_pairs.csv"

df = pd.read_csv(input_file)

before = len(df)
df = df[df["Distance_km"] >= 0.01].copy()
after = len(df)

df.to_csv(output_file, index=False)

print(f"Original pairs: {before}")
print(f"Removed near-zero-distance pairs: {before - after}")
print(f"Remaining pairs: {after}")
print(f"Saved to: {output_file}")