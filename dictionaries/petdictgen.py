import requests
import math
import json

BASE_URL = "https://api.guildwars2.com/v2/pets"
BATCH_SIZE = 200
OUTPUT_FILE = "pets.json"

def fetch_pets():
    print("fetching all pet ids...")
    resp = requests.get(BASE_URL)
    resp.raise_for_status()
    all_ids = resp.json()
    total = len(all_ids)
    print(f"found {total} pets.")

    pet_dict = {}
    total_batches = math.ceil(total / BATCH_SIZE)

    for batch_idx in range(total_batches):
        start = batch_idx * BATCH_SIZE
        end = start + BATCH_SIZE
        batch = all_ids[start:end]
        ids_param = ",".join(map(str, batch))
        url = f"{BASE_URL}?ids={ids_param}"
        resp = requests.get(url)
        resp.raise_for_status()
        pets = resp.json()

        for pet in pets:
            name = pet.get("name")
            pid = pet.get("id")
            if name is not None and pid is not None:
                pet_dict[name] = pid

        print(f"[{batch_idx + 1}/{total_batches}] processed {len(batch)} ids.")

    return pet_dict

if __name__ == "__main__":
    pet_dict = fetch_pets()

    print(f"writing {len(pet_dict)} entries to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(pet_dict, f, ensure_ascii=False, indent=2)

    print("done.")
