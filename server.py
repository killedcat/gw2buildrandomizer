import asyncio
import os
from pathlib import Path
from typing import Optional, Dict, List
import re
import random
import httpx
import json

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from buildgen import (
    Warrior,
    Guardian,
    Engineer,
    Ranger,
    Thief,
    Elementalist,
    Mesmer,
    Necromancer,
    Revenant,
    generate_build as static_generate_build,
)
from gw2APIdicts import legends_dict

# Hardcoded legend stance icons (skill icon URLs)
LEGEND_NAME_TO_ICON: Dict[str, str] = {
    "Glint": "https://render.guildwars2.com/file/27B5D1D4127A2EE73866E54F5A43E9102618B90B/1058605.png",
    "Shiro": "https://render.guildwars2.com/file/67CDD35F6BC3072E0837715A5E0A90646529BAA2/1030005.png",
    "Jalis": "https://render.guildwars2.com/file/03C66FA8A89697A0C4D309484172080E3A1141EF/961410.png",
    "Mallyx": "https://render.guildwars2.com/file/1A1407F7D34E5ED41B59A25F39EBF728CC926423/961413.png",
    "Scorchrazor": "https://render.guildwars2.com/file/6B3205EF5ED0802DB74BBF7F0CAE04FAA2089B74/1770592.png",
    "Ventari": "https://render.guildwars2.com/file/6CFF31B50AA00CAF3D35A02562964802B55AD292/1024105.png",
    "Alliance": "https://render.guildwars2.com/file/E1910F4C5C74E0B00AB262D2D3DBA3FB51BE90CA/2491626.png",
    "Razah": "https://render.guildwars2.com/file/3FEE4B97282956F1F3654BE36119A0030E08C1D7/3680200.png",
}


app = FastAPI(title="GW2 Random Build Generator", version="0.1.0")

# Allow browser usage during local dev
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


profession_factories = {
    "Warrior": Warrior,
    "Guardian": Guardian,
    "Engineer": Engineer,
    "Ranger": Ranger,
    "Thief": Thief,
    "Elementalist": Elementalist,
    "Mesmer": Mesmer,
    "Necromancer": Necromancer,
    "Revenant": Revenant,
}


# Serve static assets
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")


# Global caches
SKILL_NAME_TO_DETAILS: Dict[str, List[dict]] = {}
SPEC_NAME_TO_DETAILS: Dict[str, List[dict]] = {}
TRAIT_ID_TO_DETAILS: Dict[int, dict] = {}
PVP_AMULET_NAME_TO_DETAILS: Dict[str, dict] = {}
RUNES_RELICS_SIGILS: Dict[str, str] = {}


def _norm(s: str) -> str:
    return re.sub(r"[\"'`""''!?.:,]", "", (s or "").lower()).strip()


@app.on_event("startup")
async def on_startup() -> None:
    # Hydrate all caches for robust icon lookups
    try:
        # Load runes, relics, and sigils dictionary
        print("Loading runes, relics, and sigils dictionary...")
        try:
            with open("runes_relics_sigils.json", "r", encoding="utf-8") as f:
                global RUNES_RELICS_SIGILS
                RUNES_RELICS_SIGILS = json.load(f)
            print(f"Loaded {len(RUNES_RELICS_SIGILS)} runes, relics, and sigils")
        except Exception as e:
            print(f"Error loading runes_relics_sigils.json: {e}")
            RUNES_RELICS_SIGILS = {}
        
        async with httpx.AsyncClient(base_url="https://api.guildwars2.com", timeout=60.0) as client:
            print("Loading GW2 API caches...")
            
            # 1. Skills cache
            print("Loading skills...")
            ids = (await client.get("/v2/skills")).json()
            if isinstance(ids, list) and ids:
                # chunk fetch details
                details: List[dict] = []
                for i in range(0, len(ids), 200):
                    chunk = ids[i : i + 200]
                    det = (await client.get("/v2/skills", params={"ids": ",".join(str(x) for x in chunk), "lang": "en"})).json()
                    if isinstance(det, list):
                        details.extend(det)
                # build normalized map
                cache: Dict[str, List[dict]] = {}
                for d in details:
                    name = d.get("name")
                    if not name:
                        continue
                    key = _norm(name)
                    cache.setdefault(key, []).append(d)
                global SKILL_NAME_TO_DETAILS
                SKILL_NAME_TO_DETAILS = cache
                print(f"Loaded {len(details)} skills")
            
            # 2. Specializations cache
            print("Loading specializations...")
            spec_ids = (await client.get("/v2/specializations")).json()
            if isinstance(spec_ids, list) and spec_ids:
                spec_details: List[dict] = []
                for i in range(0, len(spec_ids), 200):
                    chunk = spec_ids[i : i + 200]
                    det = (await client.get("/v2/specializations", params={"ids": ",".join(str(x) for x in chunk), "lang": "en"})).json()
                    if isinstance(det, list):
                        spec_details.extend(det)
                spec_cache: Dict[str, List[dict]] = {}
                for d in spec_details:
                    name = d.get("name")
                    if not name:
                        continue
                    key = _norm(name)
                    spec_cache.setdefault(key, []).append(d)
                global SPEC_NAME_TO_DETAILS
                SPEC_NAME_TO_DETAILS = spec_cache
                print(f"Loaded {len(spec_details)} specializations")
            
            # 3. Traits cache (for trait icons)
            print("Loading traits...")
            trait_ids = (await client.get("/v2/traits")).json()
            if isinstance(trait_ids, list) and trait_ids:
                trait_details: List[dict] = []
                for i in range(0, len(trait_ids), 200):
                    chunk = trait_ids[i : i + 200]
                    det = (await client.get("/v2/traits", params={"ids": ",".join(str(x) for x in chunk), "lang": "en"})).json()
                    if isinstance(det, list):
                        trait_details.extend(det)
                
                # Build ID-based map for traits
                trait_cache: Dict[int, dict] = {}
                for trait in trait_details:
                    trait_id = trait.get("id")
                    if trait_id is not None:
                        trait_cache[trait_id] = trait
                global TRAIT_ID_TO_DETAILS
                TRAIT_ID_TO_DETAILS = trait_cache
                print(f"Loaded {len(trait_details)} traits")
            
            # 4. PvP Amulets cache
            print("Loading PvP amulets...")
            pvp_amulets = (await client.get("/v2/pvp/amulets", params={"ids": "all", "lang": "en"})).json()
            if isinstance(pvp_amulets, list):
                amulet_cache: Dict[str, dict] = {}
                for amulet in pvp_amulets:
                    name = amulet.get("name")
                    if name:
                        amulet_cache[name] = amulet
                global PVP_AMULET_NAME_TO_DETAILS
                PVP_AMULET_NAME_TO_DETAILS = amulet_cache
                print(f"Loaded {len(pvp_amulets)} PvP amulets")
            
            print("All caches loaded successfully!")
            
    except Exception as e:
        print(f"Error loading caches: {e}")
        # Leave cache empty on failure; UI will still work
        pass


@app.get("/api/health")
async def health() -> dict:
	return {"status": "ok"}


@app.get("/api/professions")
async def list_professions() -> dict:
    return {"professions": sorted(list(profession_factories.keys()))}


@app.get("/api/build")
async def api_build(
    profession: Optional[str] = Query(default=None, description="Profession name, e.g., Guardian"),
    spec: Optional[str] = Query(default=None, description="Elite spec name or 'core'"),
) -> dict:
    if not profession:
        profession = random.choice(list(profession_factories.keys()))
    prof_name = profession.capitalize()
    if prof_name not in profession_factories:
        return {"error": "Unknown profession"}
    instance = profession_factories[prof_name]()
    text = static_generate_build(instance, spec)
    m = re.search(r"\[&[^\]]+\]", text)
    chat_link = m.group(0) if m else ""
    # Parse details for UI
    skills_match = re.search(r"Skills:\s*([^\n]+)", text)
    skills = []
    if skills_match:
        parts = [s.strip() for s in skills_match.group(1).split(',') if s.strip()]
        if len(parts) >= 5:
            skills = [parts[0], parts[1], parts[2], parts[3], parts[-1]]
    # Parse specializations: lines like "Zeal: 2-3-1"
    specs = []
    for line in text.splitlines():
        line = line.strip()
        m2 = re.match(r"^([A-Za-z'! ]+):\s*(\d-\d-\d)$", line)
        if m2:
            name = m2.group(1).strip()
            triad = m2.group(2).split('-')
            # Reverse order to match in-game visual order (Adept-Master-GM → GM-Master-Adept correction)
            traits = list(reversed(triad))
            specs.append({"name": name, "traits": traits})
    # Parse weapons (first line with sigils)
    weapons = []
    wline_match = re.search(r"^(.*?\(Sigil of .*?\))(?:\s*\+\s*(.*?\(Sigil of .*?\)))?", text, re.M)
    if wline_match:
        line1 = wline_match.group(1) or ""
        line2 = wline_match.group(2) or ""
        sets = [seg for seg in [line1, line2] if seg]
        for seg in sets:
            name_only = seg.split("(Sigil of ", 1)[0].strip()
            if name_only:
                weapons.append(name_only)

    # Parse sigils per weapon set
    def extract_sigils(segment: str) -> list[str]:
        return re.findall(r"Sigil of\s*([^,\)]+)", segment)

    weapon_sigil_names: list[list[str]] = []
    if wline_match:
        segs = [wline_match.group(1) or "", wline_match.group(2) or ""]
        for seg in segs:
            if not seg:
                continue
            names = extract_sigils(seg)
            weapon_sigil_names.append(names[:2])

    def norm(s: str) -> str:
        return _norm(s)

    # Skill icons strictly from preloaded cache (no search), using IDs we already have in details
    skill_icons = []
    for idx, sk in enumerate(skills):
        target = norm(sk)
        expected_slot = "Heal" if idx == 0 else ("Elite" if idx == 4 else "Utility")
        candidates = SKILL_NAME_TO_DETAILS.get(target, [])
        match = next((d for d in candidates if d.get("slot") == expected_slot and prof_name in (d.get("professions") or [])), None)
        if not match:
            match = next((d for d in candidates if d.get("slot") == expected_slot), None)
        if not match and candidates:
            match = candidates[0]
        skill_icons.append((match or {}).get("icon", ""))

    # Sigil icons (using dictionary)
    def fetch_sigil_icon(name: str) -> str:
        candidates = [
            f"Superior Sigil of {name}",
            f"Major Sigil of {name}",
            f"Minor Sigil of {name}",
            f"Sigil of {name}",
        ]
        try:
            for query in candidates:
                if query in RUNES_RELICS_SIGILS:
                    return RUNES_RELICS_SIGILS[query]
            return ""
        except Exception:
            return ""

    weapon_sigils: list[list[dict]] = []
    for names in weapon_sigil_names:
        set_icons: list[dict] = []
        for n in names:
            icon = fetch_sigil_icon(n.strip())
            set_icons.append({"name": f"Sigil of {n.strip()}", "icon": icon})
        weapon_sigils.append(set_icons)

    # Revenant legend icons (hardcoded map; more reliable than API lookups)
    legend_icons: list[str] = []
    if prof_name == "Revenant":
        # find legends line like "Shiro / Ventari"
        mleg = re.search(r"^\s*([A-Za-z' ]+)\s*/\s*([A-Za-z' ]+)\s*$", text, re.M)
        if mleg:
            names = [mleg.group(1).strip(), mleg.group(2).strip()]
            for nm in names:
                icon = LEGEND_NAME_TO_ICON.get(nm, "")
                legend_icons.append(icon)

    # Spec icons and trait icons (use specialization cache per API:2/specializations)
    enriched_specs = []
    for s in specs:
        icon = ""
        matrix_icons: list[list[str]] = [ ["", "", ""], ["", "", ""], ["", "", ""] ]
        try:
            cand = SPEC_NAME_TO_DETAILS.get(norm(s["name"])) or []
            if cand:
                det = next((d for d in cand if d.get("profession") == prof_name), cand[0])
                icon = det.get("icon", "") or ""
                majors = det.get("major_traits") or []
                if len(majors) == 9:
                    triad = [int(x) for x in s.get("traits", []) if x]
                    if len(triad) == 3:
                        # Use cached trait icons for the 3x3 matrix
                        for r in range(3):
                            for c in range(3):
                                trait_id = majors[r*3 + c]
                                trait_data = TRAIT_ID_TO_DETAILS.get(trait_id, {})
                                matrix_icons[r][c] = trait_data.get("icon", "") or ""
        except Exception:
            pass
        enriched_specs.append({"name": s["name"], "traits": s["traits"], "icon": icon, "trait_matrix": matrix_icons})

        # PvP amulet, rune, and relic parsing
        amulet_icon = ""
        amulet_name = ""
        rune_name = ""
        relic_name = ""
        rune_icon = ""
        relic_icon = ""
        try:
            am_match = re.search(r"^(.+?) Amulet, Rune of (.+?), Relic of (.+?)$", text, re.M)
            if am_match:
                amulet_name = am_match.group(1).strip()
                rune_name = am_match.group(2).strip()
                relic_name = am_match.group(3).strip()
                
                # Get amulet icon from cache
                target = f"{amulet_name} Amulet"
                hit = PVP_AMULET_NAME_TO_DETAILS.get(target, {})
                amulet_icon = hit.get("icon", "") or ""
                
                # Get rune icon from dictionary
                try:
                    rune_candidates = [
                        f"Superior Rune of {rune_name}",
                        f"Major Rune of {rune_name}",
                        f"Minor Rune of {rune_name}",
                        f"Rune of {rune_name}",
                    ]
                    for query in rune_candidates:
                        if query in RUNES_RELICS_SIGILS:
                            rune_icon = RUNES_RELICS_SIGILS[query]
                            break
                except Exception:
                    pass
                
                # Get relic icon from dictionary
                try:
                    relic_candidates = [
                        f"Relic of {relic_name}",
                    ]
                    for query in relic_candidates:
                        if query in RUNES_RELICS_SIGILS:
                            relic_icon = RUNES_RELICS_SIGILS[query]
                            break
                except Exception:
                    pass
        except Exception:
            pass

    return {
        "profession": prof_name,
        "text": text,
        "chat_link": chat_link,
        "skills": skills,
        "skills_icons": skill_icons,
        "specializations": enriched_specs,
        "weapons": weapons,
        "weapon_sigils": weapon_sigils,
        "legend_icons": legend_icons,
        "amulet_icon": amulet_icon,
        "amulet_name": amulet_name,
        "rune_name": rune_name,
        "relic_name": relic_name,
        "rune_icon": rune_icon,
        "relic_icon": relic_icon,
    }


@app.get("/api/specs")
async def api_specs(profession: str) -> dict:
    prof_name = profession.capitalize()
    if prof_name not in profession_factories:
        return {"specs": []}
    inst = profession_factories[prof_name]()
    # core marker plus elite specs
    return {"specs": ["core"] + list(inst.elite_specs)}


@app.get("/")
async def index() -> FileResponse:
	index_path = Path(__file__).parent / "static" / "index.html"
	return FileResponse(index_path)


# SPA fallback so any unknown path serves the UI
@app.get("/{full_path:path}")
async def spa_fallback(full_path: str) -> FileResponse:
	index_path = Path(__file__).parent / "static" / "index.html"
	return FileResponse(index_path)


