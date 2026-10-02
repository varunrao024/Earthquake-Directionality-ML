import pandas as pd

file_path = "results/candidate_station_pairs.csv"
df = pd.read_csv(file_path)

print("Dataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nUnique earthquakes:", df["EQID"].nunique())
print("Unique station pairs:", df[["EQID", "Station_ID_1", "Station_ID_2"]].drop_duplicates().shape[0])

print("\nDistance statistics (km):")
print(df["Distance_km"].describe())

print("\nPairs per earthquake:")
print(df.groupby("EQID").size().describe())

print("\nFirst 15 rows:")
print(df.head(15).to_string(index=False))