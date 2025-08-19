import random
import codecs
import os
from wonderwords import RandomWord
from gw2APIdicts import *

amulets = ["Assassin", "Avatar", "Berserker", "Carrion", "Demolisher", "Destroyer", "Grieving", "Marauder", "Paladin", "Rabid", "Rampager", "Sage", "Sinister", "Swashbuckler", "Valkyrie", "Wizard"]
runes = ["Adventure", "Air", "Altruism", "Balthazar", "Divinity", "Dwayna", "Earth", "Evasion", "Exuberance", "Fire", "Grenth", "Hoelbrak", "Ice", "Infiltration", "Leadership", "Lyssa", "Melandru", "Orr", "Radiance", "Rage", "Rata Sum", "Resistance", "Sanctuary", "Scavenging", "Speed", "Strength", "Afflicted", "Aristocracy", "Baelfire", "Berserker", "Centaur", "Chronomancer", "Citadel", "Daredevil", "Deadeye", "Dolyak", "Dragonhunter", "Druid", "Eagle", "Elementalist", "Engineer", "Fighter", "Firebrand", "Flame Legion", "Flock", "Forge", "Grove", "Guardian", "Herald", "Holosmith", "Krait", "Lynx", "Mad King", "Mesmer", "Mirage", "Monk", "Necromancer", "Nightmare", "Ranger", "Reaper", "Renegade", "Revenant", "Scholar", "Scrapper", "Soldier", "Soulbeast", "Spellbreaker", "Sunless", "Svanir", "Tempest", "Thief", "Trapper", "Traveler", "Undead", "Warrior", "Water", "Weaver", "Wurm", "Thorns", "Vampirism"]
relics = [
    # Core relics (40 at launch + 12 from Core Set 2)
    "Agony", "Akeem", "Altruism", "Antitoxin", "Atrocity", "Bava Nisos", "Bloodstone",  "Living City", "Mistburn",  "Phenom",
    "Dagda", "Febe",  "Midnight King",  "Demon Queen", "Nourys", "Nayos", "Karakosa",  "Twin Generals",  "Founding", "Mosyn",
     "Sorcerer",  "Wayfinder", "Zakiros",  "Blightbringer", "Rivers",  "Stormsinger",  "Claw", "Sorrow", "Geysers",  "Steamshrieker",
    "Mount Balrior",  "Mists Tide",  "Beehive", "Reunification",  "Eagle", "Thorns", "Fire", "Abaddon", "Balthazar", "Dwayna",
    "Lyssa", "Melandru", "Grenth",  "Flock", "Isgarren",  "Monk", "Ice", "Surging", "Cerus",  "Dragonhunter",
    "Mabon",  "Warrior", "Speed",  "Fractal",  "Mirage",  "Necromancer", "Peitha",  "Weaver",  "Herald",  "Krait",
     "Lich",  "Citadel", "Fireworks",  "Ogre",  "Daredevil",  "Scourge",  "Centaur",  "Astral Ward",  "Sunless",
     "Trooper", "Mercy", "Earth",  "Chronomancer",  "Firebrand", "Durability", "Lyhr",  "Privateer",  "Brawler", "Water",
     "Cavalier",  "Wizard's Tower",  "Adventurer",  "Nightmare", "Evasion", "Leadership", "Vampirism",  "Afflicted",  "Unseen Invasion",  "Reaper",
     "Pack", "Vass", "Resistance",  "Aristocracy",  "Zephyrite",  "Holosmith",  "Thief",  "Deadeye",  "Defender"
]
sigils = ["Absorption", "Agony", "Battle", "Cleansing", "Compounding", "Confusion", "Courage", "Doom", "Energy", "Enhancement", "Escape", "Exploitation", "Exposure", "Intelligence", "Misery", "Opportunity", "Peril", "Purging", "Revocation", "Ruthlessness", "Savagery", "Separation", "Smoldering", "Stagnation", "Transference", "Venom"]

def intHexByteStr(integerVariable):
    return "%0.2X" % integerVariable

def intHexDoubleStr(integerVariable):
    return "%0.4X" % int(integerVariable)

class Warrior:
    def __init__(self):
        self.professionname = "Warrior"
        self.core_specs = ["Strength", "Arms", "Defense", "Tactics", "Discipline"]
        self.elite_specs = ["Berserker", "Spellbreaker", "Bladesworn"]
        # Note: two-handed weapons must be in both the mainhand list and the offhand list (because i'm too lazy to figure out a more elegant way to do this)
        self.mainhands = ["Axe", "mace", "sword", "Greatsword", "Hammer", "Longbow", "Rifle", "Dagger", "Staff", "Spear"]
        self.offhands = ["Shield", "Warhorn", "Axe", "Mace", "Sword", "Pistol", "Dagger"]
        self.twohands = ["Greatsword", "Hammer", "Longbow", "Rifle", "Staff", "Spear"]
        self.healing_skill_list = ["Mending", '"To the Limit!"', "Healing Signet", "Defiant Stance"]
        self.utility_skill_list = ["Banner of Defense", "Banner of Discipline", "Banner of Strength",
                                    "Banner of Tactics", "Bull's Charge", "Kick", "Stomp", "Throw Bolas",
                                    '"Fear Me!"', '"For Great Justice!"', '"On My Mark!"', '"Shake It Off!"',
                                    "Dolyak Signet", "Signet of Fury", "Signet of Might", "Signet of Stamina",
                                    "Balanced Stance", "Berserker Stance", "Endure Pain", "Frenzy"]
        self.elite_skill_list = ["Battle Standard", "Rampage", "Signet of Rage"]
        # Format: {ELITE_SPEC: [spec heal, [spec utilities], spec elite]}
        self.elite_spec_skills = {
            "Bladesworn": ["Combat Stimulant", ["Flow Stabilizer", "Overcharged Cartridges", "Electric Fence", "Dragonspike Mine"], "Tactical Reload"], 
            "Berserker": ["Blood Reckoning", ["Outrage", "Shattering Blow", "Sundering Leap", "Wild Blow"], "Head Butt"], 
            "Spellbreaker": ["Natural Healing", ["Sight beyond Sight", "Featherfoot Grace", "Imminent Threat", "Break Enchantments"], "Winds of Disenchantment"] 
            }
        pass

class Mesmer:
    def __init__(self):
        self.professionname = "Mesmer"
        self.core_specs = ["Domination", "Dueling", "Chaos", "Inspiration", "Illusions"]
        self.elite_specs = ["Mirage", "Chronomancer", "Virtuoso"]
        # Note: two-handed weapons must be in both the mainhand list and the offhand list (because i'm too lazy to figure out a more elegant way to do this)
        self.mainhands = ["Axe", "Sword", "Scepter", "Greatsword", "Staff", "Dagger", "Rifle", "Spear"]
        self.offhands = ["Sword", "Pistol", "Focus", "Shield", "Torch"]
        self.twohands = ["Greatsword", "Staff", "Rifle", "Spear"]
        self.healing_skill_list = ["Ether Feast", "Mirror", "Mantra of Recovery", "Signet of the Ether"]
        self.utility_skill_list = ["Decoy", "Mirror Images", "Feedback",
                                    "Null Field", "Portal Entre", "Veil", "Arcane Thievery", "Blink",
                                    "Illusion of Life", "Mimic", "Mantra of Concentration", "Mantra of Distraction",
                                    "Mantra of Pain", "Mantra of Resolve", "Phantasmal Defender", "Phantasmal Disenchanter",
                                    "Signet of Domination", "Signet of Illusions", "Signet of Inspiration", "Signet of Midnight"]
        self.elite_skill_list = ["Time Warp", "Mass Invisibility", "Signet of Humility"]
        # Format: {ELITE_SPEC: [spec heal, [spec utilities], spec elite]}
        self.elite_spec_skills = {
            "Chronomancer": ["Well of Eternity", ["Well of Action", "Well of Calamity", "Well of Precognition", "Well of Senility"], "Gravity Well"], 
            "Mirage": ["False Oasis", ["Crystal Sands", "Illusionary Ambush", "Mirage Advance", "Sand through Glass"], "Jaunt"], 
            "Virtuoso": ["Twin Blade Restoration", ["Blade Renewal", "Rain of Swords", "Psychic Force", "Sword of Decimation"], "Thousand Cuts"] 
            }
        pass

class Thief:
    def __init__(self):
        self.professionname = "Thief"
        self.core_specs = ["Deadly Arts","Critical Strikes","Shadow Arts","Acrobatics","Trickery"]
        self.elite_specs = ["Daredevil","Deadeye","Specter"]
        # Note: two-handed weapons must be in both the mainhand list and the offhand list (because i'm too lazy to figure out a more elegant way to do this)
        self.mainhands = ["Rifle", "Shortbow","Staff","Dagger","Pistol","Sword","Scepter", "Axe", "Spear"]
        self.offhands = ["Dagger","Pistol"]
        self.twohands = ["Rifle", "Shortbow","Staff", "Spear"]
        self.healing_skill_list = ["Hide in Shadows","Signet of Malice","Withdraw","Skelk Venom"]
        self.utility_skill_list = ["Blinding Powder","Shadow Refuge","Shadowstep","Smoke Screen","Prepare Pitfall","Prepare Thousand Needles","Prepare Shadow Portal","Prepare Seal Area","Assassin's Signet","Infiltrator's Signet","Signet of Agility","Signet of Shadows","Caltrops","Haste","Roll for Initiative","Scorpion Wire","Devourer Venom","Ice Drake Venom","Skale Venom","Spider Venom"]
        self.elite_skill_list = ["Thieves Guild","Basilisk Venom","Dagger Storm"]
        # Format: {ELITE_SPEC: [spec heal, [spec utilities], spec elite]}
        self.elite_spec_skills = {
            "Daredevil": ["Channeled Vigor", ["Bandit's Defense","Distracting Daggers","Fist Flurry","Impairing Daggers"], "Impact Strike"], 
            "Deadeye": ["Malicious Restoration", ["Binding Shadow","Mercy","Shadow Flare","Shadow Gust"], "Shadow Meld"], 
            "Specter": ["Well of Gloom", ["Well of Bounty","Well of Silence","Well of Sorrow","Well of Tears"], "Shadowfall"] 
            }
        pass


class Guardian:
    def __init__(self):
        self.professionname = "Guardian"
        self.core_specs = ["Zeal", "Radiance", "Valor", "Honor", "Virtues"]
        self.elite_specs = ["Dragonhunter", "Firebrand", "Willbender"]
        # Note: two-handed weapons must be in both the mainhand list and the offhand list (because i'm too lazy to figure out a more elegant way to do this)
        self.mainhands = ["Axe", "Sword", "Scepter", "Greatsword", "Staff", "Longbow", "Mace", "Pistol", "Spear"]
        self.offhands = ["Sword", "Focus", "Shield", "Torch", "Pistol"]
        self.twohands = ["Greatsword", "Staff", "Longbow", "Hammer", "Spear"]
        self.healing_skill_list = ['"Receive the Light!"', "Litany of Wrath", "Shelter", "Signet of Resolve"]
        self.utility_skill_list = ["Hallowed Ground", "Purging Flames", "Sanctuary", "Wall of Reflection", "Contemplation of Purity", "Judge's Intervention", "Merciful Intervention", "Smite Condition", '"Hold the Line!"', '"Advance!"', '"Save Yourselves!"', '"Stand Your Ground!"', "Bane Signet", "Signet of Judgment", "Signet of Mercy", "Signet of Wrath", "Bow of Truth", "Hammer of Wisdom", "Shield of the Avenger", "Sword of Justice"]
        self.elite_skill_list = ['"Feel My Wrath!"', "Renewed Focus", "Signet of Courage"]
        # Format: {ELITE_SPEC: [spec heal, [spec utilities], spec elite]}
        self.elite_spec_skills = {
            "Dragonhunter": ["Purification", ["Fragments of Faith", "Light's Judgment", "Test of Faith", "Procession of Blades"], "Dragon's Maw"], 
            "Firebrand": ["Mantra of Solace", ["Mantra of Flame", "Mantra of Lore","Mantra of Truth","Mantra of Potence"], "Mantra of Liberation"], 
            "Willbender": ["Reversal of Fortune", ["Flash Combo", "Whirling Light", "Heel Crack","Roiling Light"], "Heaven's Palm"] 
            }
        pass

class Engineer:
    def __init__(self):
        self.professionname = "Engineer"
        self.core_specs = ["Explosives","Firearms","Inventions","Alchemy","Tools"]
        self.elite_specs = ["Scrapper","Holosmith","Mechanist"]
        # Note: two-handed weapons must be in both the mainhand list and the offhand list (because i'm too lazy to figure out a more elegant way to do this)
        self.mainhands = ["Hammer","Rifle","Sword","Mace", "Shortbow", "Spear"]
        self.offhands = ["Pistol","Shield"]
        self.twohands = ["Hammer","Rifle", "Shortbow", "Spear"]
        self.healing_skill_list = ["A.E.D.","Elixir H","Healing Turret","Med Kit"]
        self.utility_skill_list = ["Bomb Kit","Grenade Kit","Elixir Gun","Flamethrower","Tool Kit","Elixir B","Elixir C","Elixir R","Elixir S","Elixir U","Personal Battering Ram","Rocket Boots","Slick Shoes","Throw Mine","Utility Goggles","Flame Turret","Net Turret","Rifle Turret","Rocket Turret","Thumper Turret"]
        self.elite_skill_list = ["Elite Mortar Kit","Elixir X","Supply Crate"]
        # Format: {ELITE_SPEC: [spec heal, [spec utilities], spec elite]}
        self.elite_spec_skills = {
            "Scrapper": ["Medic Gyro", ["Blast Gyro","Bulwark Gyro","Purge Gyro","Shredder Gyro"], "Sneak Gyro"], 
            "Holosmith": ["Coolant Blast", ["Spectrum Shield","Hard Light Arena","Laser Disk","Photon Wall"], "Prime Light Beam"], 
            "Mechanist": ["Rectifier Signet", ["Barrier Signet","Force Signet","Shift Signet","Superconducting Signet"], "Overclock Signet"] 
            }
        pass

class Elementalist:
    def __init__(self):
        self.professionname = "Elementalist"
        self.core_specs = ["Fire","Air","Water","Earth","Arcane"]
        self.elite_specs = ["Tempest","Weaver","Catalyst"]
        # Note: two-handed weapons must be in both the mainhand list and the offhand list (because i'm too lazy to figure out a more elegant way to do this)
        self.mainhands = ["Hammer","Staff","Dagger","Scepter","Sword", "Pistol", "Spear"]
        self.offhands = ["Dagger","Focus","Warhorn"]
        self.twohands = ["Hammer","Staff", "Spear"]
        self.healing_skill_list = ["Arcane Brilliance","Ether Renewal","Glyph of Elemental Harmony","Signet of Restoration"]
        self.utility_skill_list = ["Arcane Blast","Arcane Power","Arcane Shield","Arcane Wave","Armor of Earth","Cleansing Fire","Lightning Flash","Mist Form","Conjure Earth Shield","Conjure Flame Axe","Conjure Frost Bow","Conjure Lightning Hammer","Glyph of Elemental Power","Glyph of Lesser Elementals","Glyph of Renewal","Glyph of Storms","Signet of Air","Signet of Earth","Signet of Water","Signet of Fire"]
        self.elite_skill_list = ["Conjure Fiery Greatsword","Glyph of Elementals","Tornado"]
        # Format: {ELITE_SPEC: [spec heal, [spec utilities], spec elite]}
        self.elite_spec_skills = {
            "Tempest": ['"Wash the Pain Away!"', ['"Feel the Burn!"','"Eye of the Storm!"','"Aftershock!"','"Flash-Freeze!"'], '"Rebound!"'], 
            "Weaver": ["Aquatic Stance", ["Primordial Stance","Stone Resonance","Unravel","Twist of Fate"], "Weave Self"], 
            "Catalyst": ["Soothing Water", ["Relentless Fire","Shattering Ice","Invigorating Air","Fortified Earth"], "Elemental Celerity"] 
            }
        pass

class Necromancer:
    def __init__(self):
        self.professionname = "Necromancer"
        self.core_specs = ["Spite","Curses","Death Magic","Blood Magic","Soul Reaping"]
        self.elite_specs = ["Reaper","Scourge","Harbinger"]
        # Note: two-handed weapons must be in both the mainhand list and the offhand list (because i'm too lazy to figure out a more elegant way to do this)
        self.mainhands = ["Greatsword","Staff","Axe","Dagger","Scepter","Pistol", "Sword", "Spear"]
        self.offhands = ["Dagger","Focus","Warhorn","Torch", "Sword"]
        self.twohands = ["Greatsword","Staff", "Spear"]
        self.healing_skill_list = ["Consume Conditions","Summon Blood Fiend","Signet of Vampirism","Well of Blood"]
        self.utility_skill_list = ["Blood Is Power","Corrosive Poison Cloud","Corrupt Boon","Epidemic","Summon Bone Fiend","Summon Bone Minions","Summon Flesh Wurm","Summon Shadow Fiend", "Plague Signet","Signet of Spite","Signet of the Locust","Signet of Undeath","Spectral Armor","Spectral Grasp","Spectral Walk","Spectral Ring","Well of Corruption","Well of Darkness","Well of Power","Well of Suffering"]
        self.elite_skill_list = ["Plaguelands","Summon Flesh Golem","Lich Form"]
        # Format: {ELITE_SPEC: [spec heal, [spec utilities], spec elite]}
        self.elite_spec_skills = {
            "Reaper": ['"Your Soul Is Mine!"', ['"Nothing Can Save You!"','"Rise!"','"Suffer!"','"You Are All Weaklings!"'], '"Chilled to the Bone!"'], 
            "Scourge": ["Sand Flare", ["Trail of Anguish","Desiccate","Sand Swell","Serpent Siphon"], "Ghastly Breach"], 
            "Harbinger": ["Elixir of Promise", ["Elixir of Risk","Elixir of Anguish","Elixir of Bliss","Elixir of Ignorance"], "Elixir of Ambition"] 
            }
        pass    

class Revenant:
    # ...because it's weird
    def __init__(self):
        self.professionname = "Revenant"
        self.core_specs = ["Corruption", "Retribution", "Salvation", "Invocation", "Devastation"]
        self.elite_specs = ["Herald", "Renegade", "Vindicator"]
        self.mainhands = ["Mace", "Sword", "Greatsword", "Hammer", "Shortbow", "Staff", "Scepter", "Spear"]
        self.offhands = ["Axe", "Shield", "Sword"]
        self.twohands = ["Greatsword", "Hammer", "Shortbow", "Staff", "Spear"]
        self.legends = ["Mallyx", "Ventari", "Shiro", "Jalis"]
        self.elitelegends = {"Herald": "Glint", "Renegade": "Scorchrazor", "Vindicator": "Alliance"}
        pass

class Ranger:
    def __init__(self):
        self.professionname = "Ranger"
        self.core_specs = ["Marksmanship", "Skirmishing", "Wilderness Survival", "Nature Magic", "Beastmastery"]
        self.elite_specs = ["Druid", "Soulbeast", "Untamed"]
        self.mainhands = ["Axe", "Staff", "Sword", "Dagger", "Greatsword", "Hammer", "Longbow", "Shortbow", "Mace", "Spear"]
        self.offhands = ["Axe", "Warhorn", "Dagger", "Torch", "Mace"]
        self.twohands = ["Greatsword", "Hammer", "Longbow", "Shortbow", "Staff", "Spear"]
        self.healing_skill_list = ['"We Heal As One!"', "Water Spirit", "Troll Unguent", "Healing Spring"]
        self.utility_skill_list = ['"Guard!"', '"Protect Me!"', '"Search and Rescue!"',
                                    '"Sic \'Em!"', "Signet of Renewal", "Signet of Stone", "Signet of the Hunt", "Signet of the Wild",
                                    "Frost Spirit", "Stone Spirit", "Storm Spirit", "Sun Spirit",
                                    "Lightning Reflexes", "Muddy Terrain", "Quickening Zephyr", "Sharpening Stone",
                                    "Flame Trap", "Frost Trap", "Spike Trap", "Viper's Nest"]
        self.elite_skill_list = ['"Strength of the Pack!"', "Spirit of Nature", "Entangle"]
        # Format: {ELITE_SPEC: [spec heal, [spec utilities], spec elite]}
        self.pets = ["Aether Hunter", "Arctodus", "Black Bear", "Brown Bear", "Murellow", "Polar Bear", "Eagle", "Hawk", "Owl", "Raven", "White Raven", "Bristleback", "Alpine Wolf", "Fern Hound", "Krytan Drakehound", "Wolf", "Hyena", "Carrion Devourer", "Lashtail Devourer", "Whiptail Devourer", "Ice Drake", "Marsh Drake", "Reef Drake", "River Drake", "Salamander Drake", "Jaguar", "Jungle Stalker", "Snow Leopard", "Tiger", "White Tiger", "Cheetah", "Lynx", "Sand Lion", "Fanged Iboga", "Jacaranda", "Black Moa", "Blue Moa", "Pink Moa", "Red Moa", "White Moa", "Phoenix", "Boar", "Pig", "Siamoth", "Warthog", "Rock Gazelle", "Siege Turtle", "Smokescale", "Black Widow Spider", "Cave Spider", "Forest Spider", "Jungle Spider", "Wallow", "Electric Wyvern", "Fire Wyvern"]
        self.elite_spec_skills = {
            "Druid": ["Glyph of Rejuvenation", ["Glyph of Alignment", "Glyph of Equality", "Glyph of Unity", "Glyph of the Tides"], "Glyph of the Stars"], 
            "Soulbeast": ["Bear Stance", ["Dolyak Stance", "Griffon Stance", "Moa Stance", "Vulture Stance"], "One Wolf Pack"], 
            "Untamed": ["Perilous Gift", ["Exploding Spores", "Mutate Conditions", "Unnatural Traversal", "Nature's Binding"], "Forest's Fortification"] 
            }
        pass

def little_endify(hexstring):
    ba = bytearray.fromhex(hexstring)
    ba.reverse()
    s = ''.join(format(x, '02x') for x in ba)
    return s

def generate_build(profession, specchoice = None):
    # Profession specs and elite specs
    templatecode = '0D'
    templatecode += profession_ids[profession.professionname]
    core_specs = profession.core_specs
    elite_specs = profession.elite_specs
    isElite = False
    if specchoice:
        # Preserve 'core' exactly; otherwise normalize capitalization for elite names
        if specchoice.lower() != "core":
            specchoice = specchoice.capitalize()


    # Randomly choose core specs
    core_spec1 = random.choice(core_specs)
    core_spec2 = random.choice([spec for spec in core_specs if spec != core_spec1])
    if specchoice in elite_specs:
        elite_spec = specchoice
        isElite = True
    elif isinstance(specchoice, str) and specchoice.lower() == "core":
        elite_spec = random.choice([spec for spec in core_specs if spec not in [core_spec1, core_spec2]])
    else: 
        if random.randint(1,4) == 1:
            elite_spec = random.choice([spec for spec in core_specs if spec not in [core_spec1, core_spec2]])
        else:
            elite_spec = random.choice(elite_specs)
            isElite = True

    # Randomly assign integers to core specs and elite spec
    core_spec1_key = [random.randint(1, 3) for _ in range(3)]
    core_spec1_values = '-'.join(str(_) for _ in core_spec1_key)
    core_spec2_key = [random.randint(1, 3) for _ in range(3)]
    core_spec2_values = '-'.join(str(_) for _ in core_spec2_key)
    elite_spec_key = [random.randint(1, 3) for _ in range(3)]
    elite_spec_values = '-'.join(str(_) for _ in elite_spec_key)

    # template code adds specs and trait choices
    templatecode += intHexByteStr(specializations_dict[core_spec1])
    traitsspec1 = '00'
    for _ in core_spec1_key:
        if _ == 1:
            traitsspec1 += '01'
        if _ == 2:
            traitsspec1 += '10'
        if _ == 3:
            traitsspec1 += '11'
    traitsspec1 = int(traitsspec1, 2)
    traitsspec1 = intHexByteStr(traitsspec1)
    templatecode += traitsspec1

    templatecode += intHexByteStr(specializations_dict[core_spec2])
    traitsspec2 = '00'
    for _ in core_spec2_key:
        if _ == 1:
            traitsspec2 += '01'
        if _ == 2:
            traitsspec2 += '10'
        if _ == 3:
            traitsspec2 += '11'
    traitsspec2 = int(traitsspec2, 2)
    traitsspec2 = intHexByteStr(traitsspec2)
    templatecode += traitsspec2

    templatecode += intHexByteStr(specializations_dict[elite_spec])
    traitsspec3 = '00'
    for _ in elite_spec_key:
        if _ == 1:
            traitsspec3 += '01'
        if _ == 2:
            traitsspec3 += '10'
        if _ == 3:
            traitsspec3 += '11'
    traitsspec3 = int(traitsspec3, 2)
    traitsspec3 = intHexByteStr(traitsspec3)
    templatecode += traitsspec3

    # Randomly choose sigils for weapons
    sigil1 = random.choice(sigils)
    sigil2 = random.choice([sigil for sigil in sigils if sigil != sigil1])
    sigil3 = random.choice(sigils)
    sigil4 = random.choice([sigil for sigil in sigils if sigil != sigil3])

    # Randomly choose amulet, rune, and relic
    amulet = random.choice(amulets)
    rune = random.choice(runes)
    relic = random.choice(relics)

    # Randomly choose weapon sets
    mainhands = profession.mainhands
    offhands = profession.offhands
    twohands = profession.twohands

    weapon_set1 = random.choice(mainhands)
    initmainhand = weapon_set1
    initoffhand = None
    if weapon_set1 not in twohands:
        initoffhand = random.choice(offhands)
        weapon_set1 = weapon_set1 + "/" + initoffhand
    weapon_set2 = random.choice([mainhand for mainhand in mainhands if mainhand != initmainhand])
    if weapon_set2 not in twohands:
        weapon_set2 = weapon_set2 + "/" + random.choice([offhand for offhand in offhands if offhand != initoffhand])

    if profession.professionname != "Revenant":
        # Randomly choose healing and utility skills
        healing_skill_list = profession.healing_skill_list
        utility_skill_list = profession.utility_skill_list
        elite_skill_list = profession.elite_skill_list
        if isElite == True:
            healing_skill_list.append(profession.elite_spec_skills[elite_spec][0])
            utility_skill_list.extend(profession.elite_spec_skills[elite_spec][1])
            elite_skill_list.append(profession.elite_spec_skills[elite_spec][2])

        healing_skill = random.choice(healing_skill_list)
        templatecode += little_endify(intHexDoubleStr(skills_dict[healing_skill]))
        templatecode += '0000'
        utility_skills = random.sample(utility_skill_list, 3)
        for _ in utility_skills:
            templatecode += little_endify(intHexDoubleStr(skills_dict[_]))
            templatecode += '0000'
        elite_skill = random.choice(elite_skill_list)
        templatecode += little_endify(intHexDoubleStr(skills_dict[elite_skill]))
        templatecode += '0000'

       
        # Construct the final build string
        r = RandomWord()
        build_string = f"The {r.word(include_parts_of_speech=['adjectives']).capitalize()} {r.word(include_parts_of_speech=['nouns']).capitalize()}\n\n"
        if elite_spec == "Bladesworn" or profession.professionname in ["Elementalist", "Engineer"]:
            build_string += f"{weapon_set1} (Sigil of {sigil1}, Sigil of {sigil2})\n\n"
        else:
            build_string += f"{weapon_set1} (Sigil of {sigil1}, Sigil of {sigil2}) + {weapon_set2} (Sigil of {sigil3}, Sigil of {sigil4})\n\n"

        build_string += f"{amulet} Amulet, Rune of {rune}, Relic of {relic}\n\n"
        build_string += f"{profession.professionname}\n\n{core_spec1}: {core_spec1_values}\n{core_spec2}: {core_spec2_values}\n"
        build_string += f"{elite_spec}: {elite_spec_values}\n\n"
        build_string += f"Skills: {healing_skill}, {', '.join(utility_skills)}, {elite_skill}\n"
        if profession.professionname == "Ranger":
            petschoice = random.sample(profession.pets, 2)
            build_string += f"{petschoice[0]} / {petschoice[1]}\n\n"
            for _ in petschoice:
                templatecode += intHexByteStr(pets_dict[_])
            templatecode += "0000000000000000000000000000"
        else: 
            templatecode += '00000000000000000000000000000000'
        print(templatecode)
        templatecode = codecs.encode(codecs.decode(templatecode, 'hex'), 'base64').decode().strip()
        templatecode = '[&' + templatecode + ']'
        build_string += f"\nBuild template code: \n`{templatecode}`"

    else:
        # Choose two legends
        if isElite:
            legends = profession.legends
            legends.append(profession.elitelegends[elite_spec])
            legends = random.sample(legends, 2)
        else:
            legends = random.sample(profession.legends, 2)

        # The next 150 lines are brought to you by Satan. ty rev

        if legends[0] == "Shiro":
            templatecode += little_endify(intHexDoubleStr(skills_dict["Enchanted Daggers"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Phase Traversal"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Riposting Shadows"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Impossible Odds"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Jade Winds"]))
            templatecode += '0000'

        if legends[0] == "Ventari":
            templatecode += little_endify(intHexDoubleStr(skills_dict["Project Tranquility"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Natural Harmony"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Protective Solace"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Purifying Essence"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Energy Expulsion"]))
            templatecode += '0000'
        
        if legends[0] == "Mallyx":
            templatecode += little_endify(intHexDoubleStr(skills_dict["Empowering Misery"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Banish Enchantment"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Pain Absorption"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Call to Anguish"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Embrace the Darkness"]))
            templatecode += '0000'

        if legends[0] == "Jalis":
            templatecode += little_endify(intHexDoubleStr(skills_dict["Soothing Stone"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Inspiring Reinforcement"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Forced Engagement"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Vengeful Hammers"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Rite of the Great Dwarf"]))
            templatecode += '0000'

        if legends[0] == "Glint":
            templatecode += little_endify(intHexDoubleStr(skills_dict["Facet of Light"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Facet of Darkness"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Facet of Elements"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Facet of Strength"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Facet of Chaos"]))
            templatecode += '0000'

        if legends[0] == "Scorchrazor":
            templatecode += little_endify(intHexDoubleStr(skills_dict["Breakrazor's Bastion"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Razorclaw's Rage"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Darkrazor's Daring"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Icerazor's Ire"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Soulcleave's Summit"]))
            templatecode += '0000'

        if legends[0] == "Alliance":
            templatecode += little_endify(intHexDoubleStr(skills_dict["Selfish Spirit"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Nomad's Advance"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Scavenger Burst"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Reaver's Rage"]))
            templatecode += '0000'
            templatecode += little_endify(intHexDoubleStr(skills_dict["Spear of Archemorus"]))
            templatecode += '0000'
        
        templatecode += intHexByteStr(legends_dict[legends[0]])
        templatecode += intHexByteStr(legends_dict[legends[1]])
        templatecode += '0000'

        if legends[1] == "Shiro":
            templatecode += little_endify(intHexDoubleStr(skills_dict["Phase Traversal"]))
            templatecode += little_endify(intHexDoubleStr(skills_dict["Riposting Shadows"]))
            templatecode += little_endify(intHexDoubleStr(skills_dict["Impossible Odds"]))
            templatecode += '000000000000'

        if legends[1] == "Ventari":
            templatecode += little_endify(intHexDoubleStr(skills_dict["Natural Harmony"]))
            templatecode += little_endify(intHexDoubleStr(skills_dict["Protective Solace"]))
            templatecode += little_endify(intHexDoubleStr(skills_dict["Purifying Essence"]))
            templatecode += '000000000000'

        
        if legends[1] == "Mallyx":
            templatecode += little_endify(intHexDoubleStr(skills_dict["Banish Enchantment"]))
            templatecode += little_endify(intHexDoubleStr(skills_dict["Pain Absorption"]))
            templatecode += little_endify(intHexDoubleStr(skills_dict["Call to Anguish"]))
            templatecode += '000000000000'



        if legends[1] == "Jalis":
            templatecode += little_endify(intHexDoubleStr(skills_dict["Inspiring Reinforcement"]))
            templatecode += little_endify(intHexDoubleStr(skills_dict["Forced Engagement"]))
            templatecode += little_endify(intHexDoubleStr(skills_dict["Vengeful Hammers"]))
            templatecode += '000000000000'



        if legends[1] == "Glint":
            templatecode += little_endify(intHexDoubleStr(skills_dict["Facet of Darkness"]))
            templatecode += little_endify(intHexDoubleStr(skills_dict["Facet of Elements"]))
            templatecode += little_endify(intHexDoubleStr(skills_dict["Facet of Strength"]))
            templatecode += '000000000000'

        if legends[1] == "Scorchrazor":
            templatecode += little_endify(intHexDoubleStr(skills_dict["Razorclaw's Rage"]))
            templatecode += little_endify(intHexDoubleStr(skills_dict["Darkrazor's Daring"]))
            templatecode += little_endify(intHexDoubleStr(skills_dict["Icerazor's Ire"]))
            templatecode += '000000000000'

        if legends[1] == "Alliance":
            templatecode += little_endify(intHexDoubleStr(skills_dict["Nomad's Advance"]))
            templatecode += little_endify(intHexDoubleStr(skills_dict["Scavenger Burst"]))
            templatecode += little_endify(intHexDoubleStr(skills_dict["Reaver's Rage"]))
            templatecode += '000000000000'
            




        # Construct the final build string
        r = RandomWord()
        build_string = f"The {r.word(include_parts_of_speech=['adjectives']).capitalize()} {r.word(include_parts_of_speech=['nouns']).capitalize()}\n\n"
        build_string += f"{weapon_set1} (Sigil of {sigil1}, Sigil of {sigil2}) + {weapon_set2} (Sigil of {sigil3}, Sigil of {sigil4})\n\n"
        build_string += f"{amulet} Amulet, Rune of {rune}, Relic of {relic}\n\n"
        build_string += f"{profession.professionname}\n\n{core_spec1}: {core_spec1_values}\n{core_spec2}: {core_spec2_values}\n"
        build_string += f"{elite_spec}: {elite_spec_values}\n\n"
        build_string += f"{legends[0]} / {legends[1]}\n\n"
        print(templatecode)
        templatecode = codecs.encode(codecs.decode(templatecode, 'hex'), 'base64').decode().strip()
        templatecode = '[&' + templatecode + ']'
        build_string += f"\nBuild template code: \n`{templatecode}`"

    

    return build_string