from pathlib import Path
import pandas as pd

root = Path("data/raw")
extensions = {".csv", ".txt", ".xlsx", ".xls"}

for path in root.rglob("*"):
    if path.is_file() and path.suffix.lower() in extensions:
        print("\n" + "=" * 80)
        print(f"FILE: {path}")
        try:
            if path.suffix.lower() == ".csv":
                df = pd.read_csv(path, nrows=5)
            elif path.suffix.lower() == ".txt":
                df = pd.read_csv(path, sep=None, engine="python", nrows=5)
            else:
                df = pd.read_excel(path, nrows=5)

            print("COLUMNS:")
            print(list(df.columns))
            print("\nSAMPLE:")
            print(df.head(3).to_string(index=False))
        except Exception as e:
            print(f"Could not preview: {e}")
