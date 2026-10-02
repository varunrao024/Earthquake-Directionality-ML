
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree


def haversine_km(lat1, lon1, lat2, lon2):
    """Calculate distance between two geographic coordinates."""
    earth_radius_km = 6371.0

    coordinates = np.radians(
        np.column_stack([lat1, lon1])
    )
    other_coordinates = np.radians(
        np.column_stack([lat2, lon2])
    )

    tree = BallTree(coordinates, metric="haversine")
    distances, indices = tree.query(
        other_coordinates, k=1
    )

    return distances[:, 0] * earth_radius_km


def main():
    project_dir = Path(__file__).resolve().parent.parent
    data_dir = project_dir / "data" / "raw"
    results_dir = project_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    flatfile = (
        data_dir
        / "Updated_NGA_West2_flatfiles_part1"
        / "Updated_NGA_West2_Flatfile_RotD50_d005_public_version.xlsx"
    )

    print("Loading NGA-West2 flatfile...")
    df = pd.read_excel(flatfile)

    # Normalize column names to avoid whitespace issues.
    df.columns = df.columns.astype(str).str.strip()

    required = [
        "Record Sequence Number",
        "EQID",
        "Earthquake Magnitude",
        "Station ID  No.",
        "Station Name",
        "Station Latitude",
        "Station Longitude",
        "PGA (g)",
        "PGV (cm/sec)",
        "Source to Site Azimuth (deg)",
    ]

    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Convert relevant fields to numeric values.
    numeric_cols = [
        "EQID",
        "Earthquake Magnitude",
        "Station ID  No.",
        "Station Latitude",
        "Station Longitude",
        "PGA (g)",
        "PGV (cm/sec)",
        "Source to Site Azimuth (deg)",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove invalid and placeholder values.
    df = df.replace([-999, -999.0], np.nan)
    df = df.dropna(
        subset=[
            "EQID",
            "Earthquake Magnitude",
            "Station ID  No.",
            "Station Latitude",
            "Station Longitude",
        ]
    )

    # Apply the research filters.
    df = df[df["Earthquake Magnitude"] > 5].copy()
    df = df[
        df["Station Latitude"].between(-90, 90)
        & df["Station Longitude"].between(-180, 180)
    ]

    print(f"Records after basic filtering: {len(df):,}")

    # Keep one record per earthquake and station.
    # If multiple records exist, retain the first for this initial
    # candidate-pair analysis.
    df = df.sort_values("Record Sequence Number")
    df = df.drop_duplicates(
        subset=["EQID", "Station ID  No."],
        keep="first"
    )

    pairs = []
    radius_radians = 5.0 / 6371.0

    # Compare stations only within the same earthquake.
    for eqid, group in df.groupby("EQID"):
        if len(group) < 2:
            continue

        group = group.reset_index(drop=True)

        coordinates = np.radians(
            group[
                ["Station Latitude", "Station Longitude"]
            ].to_numpy()
        )

        tree = BallTree(coordinates, metric="haversine")
        neighborhoods = tree.query_radius(
            coordinates, r=radius_radians
        )

        for i, neighbors in enumerate(neighborhoods):
            for j in neighbors:
                if j <= i:
                    continue

                first = group.iloc[i]
                second = group.iloc[j]

                # Exclude duplicate station IDs.
                if first["Station ID  No."] == second["Station ID  No."]:
                    continue

                distance = haversine_km(
                    np.array([first["Station Latitude"]]),
                    np.array([first["Station Longitude"]]),
                    np.array([second["Station Latitude"]]),
                    np.array([second["Station Longitude"]]),
                )[0]

                pairs.append({
                    "EQID": int(eqid),
                    "RSN_1": first["Record Sequence Number"],
                    "RSN_2": second["Record Sequence Number"],
                    "Station_1": first["Station Name"],
                    "Station_2": second["Station Name"],
                    "Station_ID_1": int(first["Station ID  No."]),
                    "Station_ID_2": int(second["Station ID  No."]),
                    "Magnitude": first["Earthquake Magnitude"],
                    "Distance_km": round(float(distance), 4),
                    "PGA_1_g": first["PGA (g)"],
                    "PGA_2_g": second["PGA (g)"],
                    "PGV_1_cm_s": first["PGV (cm/sec)"],
                    "PGV_2_cm_s": second["PGV (cm/sec)"],
                    "Azimuth_1_deg": first["Source to Site Azimuth (deg)"],
                    "Azimuth_2_deg": second["Source to Site Azimuth (deg)"],
                })

    output_file = results_dir / "candidate_station_pairs.csv"

    if pairs:
        result = pd.DataFrame(pairs)
        result = result.sort_values(
            ["EQID", "Distance_km"]
        )
        result.to_csv(output_file, index=False)

        print(f"\nCandidate station pairs: {len(result):,}")
        print(f"Unique earthquakes: {result['EQID'].nunique():,}")
        print(f"Saved to: {output_file}")
        print("\nPreview:")
        print(result.head(10).to_string(index=False))
    else:
        print(
            "\nNo qualifying station pairs found. "
            "Check the filters and flatfile contents."
        )


if __name__ == "__main__":
    main()
