import requests
import time
import json

BASE_URL = "https://api.guildwars2.com/v2/items"
OUTPUT_FILE = "runes_relics_sigils.json"
BATCH_SIZE = 200

PREFIXES = ("Rune of", "Relic of", "Sigil of")

def fetch_all_ids():
    print("fetching all item ids...")
    return requests.get(BASE_URL).json()

def fetch_items(batch):
    ids_str = ",".join(str(i) for i in batch)
    url = f"{BASE_URL}?ids={ids_str}"
    return requests.get(url).json()

def main():
    ids = fetch_all_ids()
    total = len(ids)
    print(f"total ids: {total}")

    data = {}
    for i in range(0, total, BATCH_SIZE):
        batch = ids[i:i+BATCH_SIZE]
        items = fetch_items(batch)

        for item in items:
            name = item.get("name", "")
            icon = item.get("icon", "")
            if not (name and icon and name.startswith(PREFIXES)):
                continue

            # For relics, ensure rarity is Exotic
            if name.startswith("Relic of"):
                if item.get("rarity") != "Exotic":
                    continue

            data[name] = icon
            print(f"✔ added: {name}")

        processed = min(i + BATCH_SIZE, total)
        print(f"[{processed}/{total}] processed batch {i//BATCH_SIZE + 1}")
        time.sleep(0.2)  # don’t hammer api too hard

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"done. saved {len(data)} runes/relics/sigils to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
