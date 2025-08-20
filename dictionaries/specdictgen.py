import requests
import math
import json

BASE_URL = "https://api.guildwars2.com/v2/specializations"
BATCH_SIZE = 200
OUTPUT_FILE = "specializations.json"

def fetch_specializations():
    print("Fetching all specialization IDs...")
    resp = requests.get(BASE_URL)
    resp.raise_for_status()
    all_ids = resp.json()
    total = len(all_ids)
    print(f"Found {total} specializations.")

    spec_dict = {}
    total_batches = math.ceil(total / BATCH_SIZE)

    for batch_idx in range(total_batches):
        start = batch_idx * BATCH_SIZE
        end = start + BATCH_SIZE
        batch = all_ids[start:end]
        ids_param = ",".join(map(str, batch))
        url = f"{BASE_URL}?ids={ids_param}"
        resp = requests.get(url)
        resp.raise_for_status()
        specs = resp.json()

        for spec in specs:
            name = spec.get("name")
            sid = spec.get("id")
            if name is not None and sid is not None:
                spec_dict[name] = sid

        print(f"[{batch_idx + 1}/{total_batches}] Processed {len(batch)} IDs.")

    return spec_dict

if __name__ == "__main__":
    spec_dict = fetch_specializations()

    print(f"Writing {len(spec_dict)} entries to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(spec_dict, f, ensure_ascii=False, indent=2)

    print("Done.")
