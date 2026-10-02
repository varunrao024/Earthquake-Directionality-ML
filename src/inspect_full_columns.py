from pathlib import Path
import pandas as pd

path = next(
    Path("data/raw").rglob(
        "Updated_NGA_West2_Flatfile_RotD50_d005_public_version.xlsx"
    ),
    None
)

if path is None:
    print("Flatfile not found.")
else:
    print("File:", path)
    xls = pd.ExcelFile(path)
    print("Sheets:", xls.sheet_names)

    df = pd.read_excel(path, sheet_name=0, nrows=0)
    print("\nAll columns:")
    for col in df.columns:
        print(col)
