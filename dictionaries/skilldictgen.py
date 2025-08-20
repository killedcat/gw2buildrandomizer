import requests
import json
import time

BASE_URL = "https://api.guildwars2.com/v2"
BATCH_SIZE = 200

def fetch_json(url):
    while True:
        try:
            r = requests.get(url)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f"error fetching {url}: {e}, retrying in 5s...")
            time.sleep(5)

def batch_fetch(ids, endpoint, batch_size=BATCH_SIZE):
    ids = list(dict.fromkeys(map(int, ids)))  # dedupe
    results = {}
    for i in range(0, len(ids), batch_size):
        batch = ids[i:i+batch_size]
        url = f"{BASE_URL}/{endpoint}?ids={','.join(map(str, batch))}&v=latest"
        data = fetch_json(url)
        for entry in data:
            results[entry["id"]] = entry
        print(f"fetched {min(i+batch_size, len(ids))}/{len(ids)} from /v2/{endpoint}")
    return results

def build_profession_palette(prof):
    data = fetch_json(f"{BASE_URL}/professions/{prof}?v=latest")
    pairs = data.get("skills_by_palette", [])
    ids = [p[1] for p in pairs if isinstance(p, list) and len(p) == 2]
    skills = batch_fetch(ids, "skills") if ids else {}

    palette_map = {}
    for palette_id, skill_id in pairs:
        s = skills.get(skill_id)
        if not s:
            continue
        name = s.get("name")
        if name:
            palette_map[name] = palette_id
    return palette_map, {skill_id: palette_id for palette_id, skill_id in pairs}

def patch_revenant(skill_palette, id_to_palette):
    print("\npatching revenant with /v2/legends…")
    legends = fetch_json(f"{BASE_URL}/legends?ids=all&v=latest")

    # fetch all legend skill details
    rev_skill_ids = []
    for lg in legends:
        rev_skill_ids.extend([lg.get("heal"), lg.get("elite")])
        rev_skill_ids.extend(lg.get("utilities", []))
    rev_skill_ids = [sid for sid in rev_skill_ids if isinstance(sid, int)]

    rev_skills = batch_fetch(rev_skill_ids, "skills")

    # slot mapping: group base revenant skills by their slot
    base_skills = batch_fetch(list(id_to_palette.keys()), "skills")
    slot_to_palette = {}
    for sid, palette in id_to_palette.items():
        slot = base_skills[sid].get("slot")
        if slot:
            slot_to_palette[slot] = palette

    added = 0
    for s in rev_skills.values():
        slot = s.get("slot")
        palette = slot_to_palette.get(slot)
        if not palette:
            continue
        name = s.get("name")
        if name and name not in skill_palette:
            skill_palette[name] = palette
            added += 1

    print(f"added {added} revenant legend skills")

def main():
    skill_palette = {}
    professions = fetch_json(f"{BASE_URL}/professions?v=latest")
    print(f"professions: {', '.join(professions)}")

    for prof in professions:
        print(f"\nprocessing {prof}")
        palette_map, id_to_palette = build_profession_palette(prof)
        skill_palette.update(palette_map)
        if prof == "Revenant":
            patch_revenant(skill_palette, id_to_palette)

    # Add missing Alliance stance skills manually (or Alliance stance breaks)
    skill_palette["Selfish Spirit"] = 4572
    skill_palette["Nomad's Advance"] = 4614
    skill_palette["Scavenger Burst"] = 4651
    skill_palette["Reaver's Rage"] = 4564
    skill_palette["Spear of Archemorus"] = 4554

    with open("skill_palette.json", "w", encoding="utf-8") as f:
        json.dump(skill_palette, f, ensure_ascii=False, indent=2)
    print("\ndone. saved to skill_palette.json")

if __name__ == "__main__":
    main()
