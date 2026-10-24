import pandas as pd
import json

DATA_PATH = "../data/cleaned_lending_club.csv"

# Grab one real row from the dataset (excluding the target) as a realistic test case
df = pd.read_csv(DATA_PATH, nrows=1000)  # just need a few rows, not the whole file
row = df.drop(columns=["default"]).iloc[0]

# Convert to plain Python types (JSON can't serialize numpy types directly)
payload = {}
for key, value in row.items():
    if pd.isna(value):
        payload[key] = None
    elif isinstance(value, (int, float)):
        payload[key] = float(value)
    else:
        payload[key] = str(value)

with open("test_payload.json", "w") as f:
    json.dump(payload, f, indent=2)

print("✅ Saved test_payload.json")
print(json.dumps(payload, indent=2))
