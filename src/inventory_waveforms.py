from pathlib import Path
import re
import pandas as pd

RAW_DIR = Path("data/raw")
OUTPUT_FILE = Path("results/waveform_inventory.csv")

def read_at2_header(path):
    """Extract basic metadata from a PEER AT2 file header."""
    metadata = {
        "File": path.name,
        "Path": str(path),
        "Station": None,
        "Earthquake": None,
        "Component": None,
        "NPTS": None,
        "DT_sec": None,
    }

    try:
        with path.open("r", errors="ignore") as file:
            lines = [file.readline().strip() for _ in range(5)]

        for line in lines[:4]:
            if "Station" in line:
                metadata["Station"] = line
            if "Earthquake" in line:
                metadata["Earthquake"] = line

        # Typical PEER filenames end with a component such as E, N, or V.
        match = re.search(r"-([A-Z0-9]+)\.AT2$", path.name, re.IGNORECASE)
        if match:
            metadata["Component"] = match.group(1).upper()

        for line in lines:
            npts_match = re.search(r"NPTS\s*=\s*(\d+)", line, re.IGNORECASE)
            dt_match = re.search(r"DT\s*=\s*([0-9.]+)", line, re.IGNORECASE)

            if npts_match:
                metadata["NPTS"] = int(npts_match.group(1))
            if dt_match:
                metadata["DT_sec"] = float(dt_match.group(1))

    except OSError as error:
        metadata["Read_Error"] = str(error)

    return metadata

files = list(RAW_DIR.rglob("*.AT2")) + list(RAW_DIR.rglob("*.at2"))
files = sorted(set(files))

print(f"Found {len(files)} AT2 waveform files.")

records = [read_at2_header(path) for path in files]
df = pd.DataFrame(records)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print(f"Inventory saved to: {OUTPUT_FILE}")

if not df.empty:
    print("\nWaveform inventory preview:")
    print(df.head(20).to_string(index=False))
else:
    print("No AT2 files were found under data/raw.")