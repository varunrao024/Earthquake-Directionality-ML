import pandas as pd

pairs = pd.read_csv("results/filtered_station_pairs.csv")

rsn = 1616

matches = pairs[
    (pairs["RSN_1"] == rsn) |
    (pairs["RSN_2"] == rsn)
]

print(f"Candidate pairs containing RSN {rsn}: {len(matches)}")

if not matches.empty:
    print(matches.to_string(index=False))
else:
    print("This waveform record is not present in the filtered candidate-pair dataset.")