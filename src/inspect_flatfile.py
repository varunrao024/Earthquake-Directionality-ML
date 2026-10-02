
from pathlib import Path
import pandas as pd

# Locate the project and flatfile
project_dir = Path(__file__).resolve().parent.parent
data_dir = project_dir / "data" / "raw"

flatfile = (
    data_dir
    / "Updated_NGA_West2_flatfiles_part1"
    / "Updated_NGA_West2_Flatfile_RotD50_d005_public_version.xlsx"
)

# Load the first sheet
print("Loading NGA-West2 flatfile...")
df = pd.read_excel(flatfile)

print("\nDataset shape:")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]:,}")

print("\nColumn names:")
for col in df.columns:
    print(col)

# Show key columns if available
keywords = [
    "RSN", "EQID", "Earthquake", "Magnitude",
    "Station", "Latitude", "Longitude",
    "Azimuth", "PGA", "PGV"
]

selected = [
    col for col in df.columns
    if any(word.lower() in str(col).lower() for word in keywords)
]

print("\nPreview of relevant columns:")
print(df[selected].head(10).to_string(index=False))

# Save a compact summary
summary_path = project_dir / "results" / "flatfile_summary.txt"
summary_path.parent.mkdir(parents=True, exist_ok=True)

with open(summary_path, "w", encoding="utf-8") as f:
    f.write(f"Rows: {df.shape[0]}\n")
    f.write(f"Columns: {df.shape[1]}\n\n")
    f.write("\n".join(str(col) for col in df.columns))

print(f"\nColumn summary saved to: {summary_path}")
