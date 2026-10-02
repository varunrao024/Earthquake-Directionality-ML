from pathlib import Path
import pandas as pd

root = Path("data/raw")

keywords = [
    "EQID", "Earthquake Name", "Magnitude",
    "Station Name", "Station ID", "Latitude", "Longitude",
    "EpiD", "HypD", "Joyner", "Vs30",
    "H1 az", "H2 az", "RotD", "PGA", "PGV",
    "Idirectivity", "Tp", "Ry"
]

for path in root.rglob("*.xlsx"):
    if "Flatfile" not in path.name:
        continue

    print("\n" + "=" * 70)
    print("FILE:", path.name)

    try:
        df = pd.read_excel(path, nrows=0)
        cols = [
            col for col in df.columns
            if any(word.lower() in str(col).lower() for word in keywords)
        ]
        print("\nRelevant columns:")
        for col in cols:
            print("-", col)
    except Exception as e:
        print("Error:", e)
