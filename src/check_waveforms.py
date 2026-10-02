from pathlib import Path

root = Path("data/raw")
extensions = {".AT2", ".V2", ".asc", ".txt", ".csv", ".dat"}

matches = [
    p for p in root.rglob("*")
    if p.is_file() and p.suffix.upper() in extensions
]

print(f"Potential waveform/data files found: {len(matches)}")
for p in matches[:50]:
    print(p)

if len(matches) > 50:
    print(f"... and {len(matches) - 50} more")
