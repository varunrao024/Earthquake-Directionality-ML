
from pathlib import Path
import csv
import numpy as np


def read_at2(filepath):
    """Read acceleration data and time step from a PEER AT2 file."""
    with open(filepath, "r") as file:
        lines = file.readlines()

    dt = float(
        lines[3].split("DT=")[1].split()[0].replace(",", "")
    )

    values = []
    for line in lines[4:]:
        values.extend(float(value) for value in line.split())

    acceleration = np.array(values, dtype=float)

    if acceleration.size == 0:
        raise ValueError(f"No acceleration data found in {filepath}")

    return acceleration, dt


def calculate_max_direction(north, east):
    """Calculate the PGA-based maximum-motion direction."""
    angles = np.arange(0, 180, 0.5)
    peak_accelerations = []

    for angle in angles:
        radians = np.radians(angle)
        rotated = (
            north * np.cos(radians)
            + east * np.sin(radians)
        )
        peak_accelerations.append(np.max(np.abs(rotated)))

    best_index = int(np.argmax(peak_accelerations))

    return angles[best_index], peak_accelerations[best_index]


def process_pair(north_file, east_file):
    """Process one matching North/East record pair."""
    north, dt_n = read_at2(north_file)
    east, dt_e = read_at2(east_file)

    if not np.isclose(dt_n, dt_e):
        raise ValueError("North and East time steps do not match")

    if len(north) != len(east):
        raise ValueError("North and East sample counts do not match")

    direction, peak_acceleration = calculate_max_direction(
        north, east
    )

    return {
        "record_pair": north_file.stem.replace("-N", ""),
        "north_samples": len(north),
        "east_samples": len(east),
        "dt_seconds": dt_n,
        "duration_seconds": len(north) * dt_n,
        "max_direction_deg": direction,
        "peak_acceleration_g": peak_acceleration,
    }


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parent.parent
    data_dir = project_dir / "data" / "raw"
    results_dir = project_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    output_file = results_dir / "directionality_results.csv"

    north_files = sorted(data_dir.glob("*-N.AT2"))
    results = []

    if not north_files:
        raise FileNotFoundError(
            f"No North component files found in {data_dir}"
        )

    for north_file in north_files:
        east_file = north_file.with_name(
            north_file.name.replace("-N.AT2", "-E.AT2")
        )

        if not east_file.exists():
            print(f"Skipping unmatched pair: {north_file.name}")
            continue

        try:
            result = process_pair(north_file, east_file)
            results.append(result)
            print(
                f"Processed {result['record_pair']}: "
                f"{result['max_direction_deg']:.1f} degrees"
            )
        except (ValueError, IndexError) as error:
            print(f"Could not process {north_file.name}: {error}")

    if results:
        with open(output_file, "w", newline="") as file:
            writer = csv.DictWriter(
                file, fieldnames=results[0].keys()
            )
            writer.writeheader()
            writer.writerows(results)

        print(f"\nProcessed {len(results)} record pairs.")
        print(f"Results saved to: {output_file}")
    else:
        print("No complete record pairs could be processed.")
