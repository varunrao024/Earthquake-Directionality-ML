import pandas as pd

df = pd.read_csv("results/candidate_station_pairs.csv")

# Check pairs with zero or near-zero separation
zero = df[df["Distance_km"] < 0.01]

print("Pairs with distance below 0.01 km:", len(zero))
if not zero.empty:
    print(zero[
        ["EQID", "RSN_1", "RSN_2", "Station_1", "Station_2",
         "Station_ID_1", "Station_ID_2", "Distance_km"]
    ].to_string(index=False))

# Check whether any station is paired with itself
same_station = df[df["Station_ID_1"] == df["Station_ID_2"]]
print("\nPairs with identical station IDs:", len(same_station))

# Check missing values
print("\nMissing values by column:")
print(df.isnull().sum().to_string())

# Check duplicate event/station combinations
pair_key = ["EQID", "Station_ID_1", "Station_ID_2"]
duplicates = df[df.duplicated(pair_key, keep=False)]
print("\nDuplicate event/station pairs:", len(duplicates))

# Save the zero-distance rows for review
zero.to_csv("results/zero_distance_pairs.csv", index=False)
print("\nSaved zero-distance rows to results/zero_distance_pairs.csv")