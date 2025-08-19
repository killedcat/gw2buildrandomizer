'''
Alrighty! it's byte lookup time n stuff.

here's how build chat links work:

a link is formed with [&bytes-in-hex]

1 byte for link type (this byte in this instance will always be 00001101, or 0D in hex)
1 byte for profession id's

for any given class, this'll be in self.professionname. we can just make a dictionary to look it up to do this string.

then 3 pairs of bytes; these are specialization id (a full byte, from the API) and each trait (one unused bit, then 3 bits based on position).

the trait bit is 01, 10, or 11 -- this corresponds fine to our way of doing things, and won't require any lookup from the api - we can just take the
int and convert it as is to hex.

for example:

guardian zeal 2-3-1 would be converted to

42, 0 2 3 1

converting to binary that's

101010, 00101101

and to hex that's

2A2D.

so this build template would start like [&0D012A2D...]

We will need a dictionary of specializations to their corresponding hex, and then convert the trait choices to hex as well.

After these comes the most annoying part for us, which is the skill palette. 
Each skill is two bytes and consists of terrestial heal, then aquatic heal, terrestial util 1, aquatic util 1, etc.
Since we only care about terrestial palette, we will alternate empty doubles.

After the skill palette, there's 16 empty bytes that are only utilized by ranger (for pets) and revenant (for legends).
    
'''

# let's go ahead and make a dictionary with each specialization and its name

'''
import requests
import json

specializations_dict = {}
response = requests.get('https://api.guildwars2.com/v2/pets')
specializations_list = json.loads(response.text)

for specialization in specializations_list:
    print(f"Fetching {specialization}...")
    spec_response = requests.get(f'https://api.guildwars2.com/v2/pets/{specialization}')
    print("Success!")
    spec_data = json.loads(spec_response.text)
    specializations_dict[spec_data['name']] = spec_data['id']

print(specializations_dict)
'''


# For speed and memory reasons I'm hardcoding this dictionary but if the API breaks for some reason use the code commented out above to fix it.
specializations_dict = {'Dueling': 1, 'Death Magic': 2, 'Invocation': 3, 'Strength': 4, 'Druid': 5, 'Explosives': 6, 'Daredevil': 7, 'Marksmanship': 8, 'Retribution': 9, 'Domination': 10, 'Tactics': 11, 'Salvation': 12, 'Valor': 13, 'Corruption': 14, 'Devastation': 15, 'Radiance': 16, 'Water': 17, 'Berserker': 18, 'Blood Magic': 19, 'Shadow Arts': 20, 'Tools': 21, 'Defense': 22, 'Inspiration': 23, 'Illusions': 24, 'Nature Magic': 25, 'Earth': 26, 'Dragonhunter': 27, 'Deadly Arts': 28, 'Alchemy': 29, 'Skirmishing': 30, 'Fire': 31, 'Beastmastery': 32, 'Wilderness Survival': 33, 'Reaper': 34, 'Critical Strikes': 35, 'Arms': 36, 'Arcane': 37, 'Firearms': 38, 'Curses': 39, 'Chronomancer': 40, 'Air': 41, 'Zeal': 42, 'Scrapper': 43, 'Trickery': 44, 'Chaos': 45, 'Virtues': 46, 'Inventions': 47, 'Tempest': 48, 'Honor': 49, 'Soul Reaping': 50, 'Discipline': 51, 'Herald': 52, 'Spite': 53, 'Acrobatics': 54, 'Soulbeast': 55, 'Weaver': 56, 'Holosmith': 57, 'Deadeye': 58, 'Mirage': 59, 'Scourge': 60, 'Spellbreaker': 61, 'Firebrand': 62, 'Renegade': 63, 'Harbinger': 64, 'Willbender': 65, 'Virtuoso': 66, 'Catalyst': 67, 'Bladesworn': 68, 'Vindicator': 69, 'Mechanist': 70, 'Specter': 71, 'Untamed': 72}
profession_ids = {
    'Guardian': '01',
    'Warrior': '02',
    'Engineer': '03',
    'Ranger': '04',
    'Thief': '05',
    'Elementalist': '06',
    'Mesmer': '07',
    'Necromancer': '08',
    'Revenant': '09'
}

pets_dict = {'Jungle Stalker': 1, 'Boar': 2, 'Lynx': 3, 'Krytan Drakehound': 4, 'Brown Bear': 5, 'Carrion Devourer': 6, 'Salamander Drake': 7, 'Alpine Wolf': 8, 'Snow Leopard': 9, 'Raven': 10, 'Jaguar': 11, 'Marsh Drake': 12, 'Blue Moa': 13, 'White Moa': 14, 'Pink Moa': 15, 'Black Moa': 16, 'Red Moa': 17, 'Ice Drake': 18, 'River Drake': 19, 'Murellow': 20, 'Shark': 21, 'Fern Hound': 22, 'Black Bear': 23, 'Polar Bear': 24, 'Arctodus': 25, 'Whiptail Devourer': 26, 'Lashtail Devourer': 27, 'Hyena': 28, 'Wolf': 29, 'Owl': 30, 'Eagle': 31, 'White Raven': 32, 'Forest Spider': 33, 'Jungle Spider': 34, 'Cave Spider': 35, 'Black Widow Spider': 36, 'Warthog': 37, 'Siamoth': 38, 'Pig': 39, 'Armor Fish': 40, 'Blue Jellyfish': 41, 'Red Jellyfish': 42, 'Rainbow Jellyfish': 43, 'Hawk': 44, 'Reef Drake': 45, 'Smokescale': 46, 'Tiger': 47, 'Electric Wyvern': 48, 'Fire Wyvern': 51, 'Bristleback': 52, 'Cheetah': 54, 'Sand Lion': 55, 'Jacaranda': 57, 'Rock Gazelle': 59, 'Fanged Iboga': 61, 'White Tiger': 63, 'Wallow': 64, 'Phoenix': 65, 'Siege Turtle': 66, 'Aether Hunter': 67}
legends_dict = { 
    "Glint": 1,
    "Shiro": 2,
    "Jalis": 3,
    "Mallyx": 4,
    "Scorchrazor": 5,
    "Ventari": 6,
    "Alliance": 7 
}

'''
import requests
import json

skills_dict = {}
response = requests.get('https://api.guildwars2.com/v2/skills')
skills_list = json.loads(response.text)

for skill in skills_list:
    print(f"Fetching {skill}...")
    skill_response = requests.get(f'https://api.guildwars2.com/v2/skills/{skill}')
    print("Success!")
    skill_data = json.loads(skill_response.text)
    try:
        if skill_data['slot'] in ["Utility", "Heal", "Elite"]:
            skills_dict[skill_data['name']] = skill_data['id']
    except KeyError:
        print(f"No slot found for {skill_data['name']}!")

print(skills_dict)
'''


'''
from bs4 import BeautifulSoup
import requests

url = "https://wiki.guildwars2.com/wiki/Chat_link_format/skill_palette_table"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table')
rows = table.find_all('tr')

palette_dict = {}
for row in rows[1:]:
    cols = row.find_all('td')
    palette_id = cols[0].text.strip()
    name = cols[1].text.strip()
    palette_dict[name] = palette_id

print(palette_dict)
'''


skills_dict = {'Artillery Barrage': '1', 'Call Wurm': '2', 'Shrapnel Mine': '4', 'Avatar of Melandru': '7', 'Battle Roar': '8', 'Technobabble': '9', 'Throw Bolas': '10', 'Radiation Field': '11', 'Pain Inverter': '12', 'Call Owl': '13', 'Summon 7-Series Golem': '14', 'Summon Power Suit': '17', 'Well of Blood': '18', 'Become the Wolf': '20', 'Healing Seed': '21', 'Summon Druid Spirit': '23', 'Summon Sylvan Hound': '25', 'Spike Trap': '27', 'Grasping Vines': '28', 'Become the Snow Leopard': '29', 'Seed Turret': '30', 'Become the Raven': '31', 'Hidden Pistol': '33', 'Warband Support': '34', 'Take Root': '37', 'Glyph of Elementals': '38', 
'Thieves Guild': '40', 'Shadowstep': '88', 'Frenzy': '105', '"Shake It Off!"': '106', 'Stomp': '110', 'Healing Signet': '112', 'Endure Pain': '113', 'Glyph of Lesser Elementals': '114', 'Glyph of Elemental Power': '115', 'Signet of Restoration': '116', 'Ether Renewal': '117', 'Summon Bone Fiend': '118', 'Troll Unguent': '120', '"We Heal As One!"': '121', '"Receive the Light!"': '127', 'Blood Is Power': '128', 'Well of Suffering': '129', 'Med Kit': '132', 'Signet of Malice': '133', 'Grenade Kit': '134', 'Personal Battering Ram': '136', 'Scorpion Wire': '137', '"Save Yourselves!"': '138', 'Corrosive Poison Cloud': '139', 'Cleansing Fire': '142', 'Signet of Water': '143', 'Lightning Flash': '144', 'Signet of Earth': '145', 'Plaguelands': '146', 'Summon Flesh Golem': '149', 'Tornado': '150', 'Whirlpool': '150', 'Conjure Fiery Greatsword': '151', 'Become the Bear': '152', 'Signet of the Hunt': '154', 'Summon Blood Fiend': '155', 'Signet of Rage': '156', 'Healing Spring': '161', 'Consume Conditions': '162', 'Rifle Turret': '163', 'Harpoon Turret': '163', '"To the Limit!"': '166', 'Mending': '167', '"For Great Justice!"': '168', 'Signet of Might': '169', 'Banner of Strength': '170', 'Berserker Stance': '171', 'Banner of Discipline': '172', "Bull's Charge": '173', '"Fear Me!"': '174', 'Signet of Fury': '175', 'Banner of Tactics': '176', 'Balanced Stance': '178', 'Dolyak Signet': '179', '"Search and Rescue!"': '180', 'Frost Trap': '181', 'Storm Spirit': '182', '"Guard!"': '183', 'Lightning Reflexes': '184', 'Stone Spirit': '185', "Viper's Nest": '186', 
'"Protect Me!"': '187', 'Frost Spirit': '188', 'Sun Spirit': '189', 'Flame Trap': '190', 'Sharpening Stone': '191', 'Entangle': '192', 'Muddy Terrain': '193', 'Signet of Renewal': '194', 'Conjure Flame Axe': '202', 'Signet of Fire': '203', 'Prayer to Dwayna': '210', 'Summon Bone Minions': '228', 'Conjure Earth Shield': '230', 'Mist Form': '235', '"Strength of the Pack!"': '237', 'Battle Standard': '238', 'Plague Signet': '245', 'Arcane Shield': '246', 'Spectral Armor': '250', 'Bane Signet': '254', 'Wall of Reflection': '255', 'Hammer of Wisdom': '256', 'Elixir B': '257', 'Shelter': '259', 'Contemplation of Purity': '260', 'Conjure Frost Bow': '261', 'Bomb Kit': '263', 'Withdraw': '266', 'Prepare Thousand Needles': '267', 'Hide in Shadows': '268', 'Caltrops': '269', 'Basilisk Venom': '270', 'Mirror': '271', 'Elixir X': '274', 'Slick Shoes': '275', 'Elixir H': '276', 'Sanctuary': '278', 'Glyph of Elemental Harmony': '279', 'Arcane Thievery': '280', 'Roll for Initiative': '281', 'Veil': '282', 'Prepare Shadow Portal': '283', 'Signet of Air': '284', 'Glyph of Renewal': '285', 'Flame Turret': '290', 'Net Turret': '291', 'Thumper Turret': '292', 'Throw Mine': '294', 'Deploy Mine': '294', 'Healing Turret': '296', '"Advance!"': '301', 'Summon Flesh Wurm': '302', 'Spider Venom': '303', 'Corrupt Boon': '304', 'Signet of Wrath': '305', 'Signet of Mercy': '306', "Assassin's Signet": '307', 'Blinding Powder': '308', '"Hold the Line!"': '309', '"Stand Your Ground!"': '310', 'Renewed Focus': '311', 'Signet of Resolve': '312', 'Signet of Stamina': '317', 'Skale Venom': '318', 'Well of Darkness': '320', 'Conjure Lightning Hammer': '322', 'Prayer to Kormir': '324', 'Signet of Judgment': '326', "Judge's Intervention": '327', 'Sword of Justice': '328', 'Bow of Truth': '329', 'Shield of the Avenger': '330', 'Hallowed Ground': '331', 'Purging Flames': '332', 'Arcane Power': '333', 'Arcane Wave': '334', 'Armor of Earth': '335', 'Arcane Blast': '336', 'Prayer to Lyssa': '337', 'Hounds of Balthazar': '338', 'Prepare Seal Area': '339', 'Prepare Pitfall': '340', 'Devourer Venom': '341', 'Signet of Shadows': '342', 'Signet of Agility': '343', "Infiltrator's Signet": '344', 'Smoke Screen': '345', 'Ice Drake Venom': '346', 'Haste': '347', 'Reaper of Grenth': '349', 'Elixir S': '350', 'Elixir U': '351', 'Utility Goggles': '352', 'Elixir R': '353', 'Portal Entre': '356', 'Blink': '357', 'Decoy': '358', 'Mantra of Distraction': '359', 'Mantra of Resolve': '360', 'Mantra of Pain': '361', 'Null Field': '362', 'Mirror Images': '363', 'Spectral Ring': '364', 'Mantra of Recovery': '365', 'Ether Feast': '366', 'Signet of Undeath': '367', 'Summon Shadow Fiend': '368', 'Summon D-Series Golem': '369', 'Well of Corruption': '371', 'Well of Power': '372', 'Signet of Spite': '373', 'Signet of the Locust': '374', 'Spectral Grasp': '375', 'Smite Condition': '376', 'Lich Form': '378', 'Rampage': '380', 'Feedback': '383', 'Signet of Inspiration': '384', 'Signet of Domination': 
'385', 'Signet of Illusions': '386', 'Signet of Midnight': '387', 'Illusion of Life': '388', 'Mantra of Concentration': '389', 'Phantasmal Defender': '390', 
'Supply Crate': '393', 'Tool Kit': '394', 'Elixir C': '396', 'Rocket Boots': '397', 'Rocket Turret': '398', 'Phantasmal Disenchanter': '399', 'Flamethrower': '403', 'Elixir Gun': '405', 'Quickening Zephyr': '406', 'Spirit of Nature': '407', 'Elite Mortar Kit': '408', 'Epidemic': '409', 'Mass Invisibility': '410', 'Dagger Storm': '415', 'Kick': '418', '"Sic \'Em!"': '421', 'Signet of Stone': '427', 'Signet of the Wild': '428', 'Banner of Defense': '429', 'Mimic': '438', 'Merciful Intervention': '441', 'Shadow Refuge': '443', 'Time Warp': '444', 'Spectral Walk': '445', 'Glyph of Storms': '446', 'Charrzooka': '456', 'Mistfire Wolf': '458', '"On My Mark!"': '482', 'Signet of the Ether': '3875', 'Skelk Venom': '3876', 'Water Spirit': '3877', 'Litany of Wrath': '3878', 'Arcane Brilliance': '3879', 'Signet of Vampirism': '3880', 'Defiant Stance': '3881', 'A.E.D.': '3882', 'Spear of Archemorus': '4554', 'Jade Winds': '4554', 'Energy Expulsion': '4554', 'Embrace the Darkness': '4554', 'Facet of Chaos': '4554', 'Rite of the Great Dwarf': '4554', "Soulcleave's Summit": '4554', "Reaver's Rage": '4564', 'Impossible Odds': '4564', 'Purifying Essence': '4564', 'Call to Anguish': '4564', 'Facet of Strength': '4564', 'Vengeful Hammers': '4564', "Darkrazor's Daring": '4564', 'Selfish Spirit': '4572', 'Enchanted Daggers': '4572', 'Project Tranquility': '4572', 'Empowering Misery': '4572', 'Facet of Light': '4572', 'Soothing Stone': '4572', "Breakrazor's Bastion": '4572', "Nomad's Advance": '4614', 'Riposting Shadows': '4614', 'Protective Solace': '4614', 'Pain Absorption': '4614', 'Facet of Darkness': '4614', 'Inspiring Reinforcement': '4614', "Razorclaw's Rage": '4614', 'Scavenger Burst': '4651', 'Phase Traversal': '4651', 'Natural Harmony': '4651', 'Banish Enchantment': '4651', 'Facet of Elements': '4651', 'Forced Engagement': '4651', "Icerazor's Ire": '4651', 'Signet of Courage': '4721', '"Aftershock!"': '4724', '"Eye of the Storm!"': '4726', 'Distracting Daggers': '4727', 'Sneak Gyro': '4739', 'Fragments of Faith': 
'4740', 'Well of Senility': '4743', '"Feel My Wrath!"': '4745', 'Procession of Blades': '4746', 'Well of Precognition': '4755', 'Channeled Vigor': '4756', '"Rebound!"': '4761', 'Sundering Leap': '4769', '"Flash-Freeze!"': '4773', '"Suffer!"': '4774', 'Glyph of the Tides': '4776', 'Shredder Gyro': '4782', 'Fist Flurry': '4784', 'Gravity Well': '4787', 'Glyph of the Stars': '4788', "Dragon's Maw": '4789', "Bandit's Defense": '4790', 'Glyph of Unity': '4792', 'Purification': '4796', '"Your Soul Is Mine!"': '4801', 'Head Butt': '4802', '"Feel the Burn!"': '4803', 'Wild Blow': '4804', '"Wash the Pain Away!"': '4807', 'Purge Gyro': '4812', 'Well of Action': '4815', 'Glyph of Alignment': '4821', 'Outrage': '4823', 'Medic Gyro': '4825', 'Shattering Blow': '4828', 'Glyph of Equality': '4838', '"Nothing Can Save You!"': '4843', 'Signet of Humility': '4845', 'Impact Strike': '4846', 'Well of Eternity': '4848', '"You Are All Weaklings!"': '4849', 'Blood Reckoning': '4850', "Light's Judgment": '4858', 'Test of Faith': '4862', '"Chilled to the Bone!"': '4867', 'Well of Calamity': '4868', 'Glyph of Rejuvenation': '4873', 'Bulwark Gyro': '4878', '"Rise!"': '4879', 'Blast Gyro': '4903', 'Impairing Daggers': '4905', 'Crystal Sands': '5600', 'False Oasis': '5614', 'Prime Light Beam': '5616', 'Malicious Restoration': '5617', 'Twist of Fate': '5621', 'Aquatic Stance': '5632', 'Sand through Glass': '5639', 'Mantra of Liberation': '5656', 'Shadow Gust': '5663', 'Break Enchantments': '5671', 'One Wolf Pack': '5678', 'Spectrum Shield': '5679', 'Moa Stance': '5684', 'Hard Light Arena': '5685', 'Shadow Meld': '5693', 'Coolant Blast': '5717', 'Laser Disk': '5719', 'Imminent Threat': '5738', 'Trail of Anguish': '5746', 'Sight beyond Sight': '5750', 'Sand Swell': '5752', 'Mantra of Potence': '5754', 'Unravel': '5755', 'Sand Flare': '5758', 'Illusionary Ambush': '5770', 'Winds of Disenchantment': '5789', 'Shadow Flare': '5804', 'Mirage Advance': '5810', 'Mantra of Truth': '5827', 'Stone Resonance': '5851', 'Binding Shadow': '5860', 'Photon Wall': '5861', 'Vulture Stance': '5865', 'Dolyak Stance': '5882', 'Griffon Stance': '5889', 'Featherfoot Grace': '5904', 'Weave Self': '5906', 'Mantra of Flame': '5909', 'Mercy': '5920', 'Serpent Siphon': '5921', 'Desiccate': '5924', 'Bear Stance': '5934', 'Primordial Stance': '5941', 'Jaunt': '5958', 'Natural Healing': '5959', 'Mantra of Solace': '5963', 'Mantra of Lore': '5971', 'Ghastly Breach': '5984', 'Elixir of Risk': '6868', 'Elixir of Ignorance': '6871', 
'Whirling Light': '6872', 'Twin Blade Restoration': '6875', 'Blade Renewal': '6876', 'Rain of Swords': '6877', 'Flash Combo': '6878', 'Psychic Force': '6879', 'Heel Crack': '6880', 'Roiling Light': '6881', 'Reversal of Fortune': '6883', 'Thousand Cuts': '6885', 'Elixir of Promise': '6887', 'Elixir of Ambition': '6888', "Heaven's Palm": '6889', 'Sword of Decimation': '6890', 'Elixir of Bliss': '6891', 'Elixir of Anguish': '6892', 'Electric Fence': '6893', 'Shattering Ice': '6894', 'Fortified Earth': '6895', 'Dragonspike Mine': '6896', 'Invigorating Air': '6897', 'Flow Stabilizer': '6898', 'Elemental Celerity': '6903', 'Relentless Fire': '6904', 'Tactical Reload': '6908', 'Overcharged Cartridges': '6909', 'Soothing Water': '6910', 'Combat Stimulant': '6911', 'Exploding Spores': '6913', "Nature's Binding": '6916', 'Well of Tears': '6917', 'Well of Sorrow': '6918', 'Well of Silence': '6919', 'Well of Bounty': '6920', 'Overclock Signet': '6921', 'Barrier Signet': '6923', 'Rectifier Signet': '6925', 'Superconducting Signet': '6926', "Forest's Fortification": '6927', 'Shift Signet': '6928', 'Shadowfall': '6929', 'Unnatural Traversal': '6931', 'Perilous Gift': '6932', 'Well of Gloom': '6933', 'Mutate Conditions': '6937', 'Force Signet': '6938'}