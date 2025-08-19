from typing import List, Tuple

from gw2APIdicts import specializations_dict, profession_ids, pets_dict, legends_dict, skills_dict


def _int_hex_byte(value: int) -> str:
	return f"{value:02X}"


def _int_hex_double(value: int) -> str:
	return f"{int(value):04X}"


def _little_endify(hex_string: str) -> str:
	ba = bytearray.fromhex(hex_string)
	ba.reverse()
	return ''.join(f"{x:02x}" for x in ba)


def _trait_bits(traits: List[int]) -> str:
	bits = '00'
	for t in traits:
		if t == 1:
			bits += '01'
		elif t == 2:
			bits += '10'
		elif t == 3:
			bits += '11'
		else:
			bits += '01'
	return _int_hex_byte(int(bits, 2))


def _palette_id(skill_name: str) -> int:
	val = skills_dict.get(skill_name)
	if val is None:
		return 0
	# Per wiki palette table, values may be like '408;4857' → use only the first value
	val_str = str(val).strip()
	primary = val_str.split(';', 1)[0]
	primary = primary.split(',', 1)[0]
	# Strip non-digits defensively
	primary_digits = ''.join(ch for ch in primary if ch.isdigit())
	try:
		return int(primary_digits) if primary_digits else 0
	except Exception:
		return 0


def _encode_hex(payload: dict) -> str:
	profession = payload.get('profession')
	specs = payload.get('specializations') or []
	sk = payload.get('skills') or {}

	if not profession or len(specs) != 3:
		return "0D"

	code = '0D'
	code += profession_ids[profession]

	# specs and traits
	for spec in specs:
		name = spec['name']
		traits = spec['traits']
		code += _int_hex_byte(specializations_dict[name])
		code += _trait_bits(traits)

	# skills
	if profession != 'Revenant':
		heal = sk.get('heal')
		utils = sk.get('utilities') or []
		elite = sk.get('elite')
		# ensure three utilities
		if len(utils) < 3:
			utils = utils + [u for u in utils[:1]] * (3 - len(utils))
		utils = utils[:3]

		if heal:
			code += _little_endify(_int_hex_double(_palette_id(heal)))
			code += '0000'
		for u in utils:
			code += _little_endify(_int_hex_double(_palette_id(u)))
			code += '0000'
		if elite:
			code += _little_endify(_int_hex_double(_palette_id(elite)))
			code += '0000'

		# profession-specific 16 bytes
		if profession == 'Ranger':
			# pick two arbitrary pets if not provided in payload
			pet_ids = list(pets_dict.values())
			if pet_ids:
				code += _int_hex_byte(pet_ids[0])
				code += _int_hex_byte(pet_ids[1 if len(pet_ids) > 1 else 0])
			code += '00' * 14
		else:
			code += '00' * 16
	else:
		# Revenant path uses legend-specific skill palette
		# emulate buildgen.py: choose two legends, allowing elite legend by elite spec
		elite_spec_name = specs[2]['name']
		elite_legend = {
			'Herald': 'Glint',
			'Renegade': 'Scorchrazor',
			'Vindicator': 'Alliance',
		}.get(elite_spec_name)
		legends = ['Mallyx', 'Ventari', 'Shiro', 'Jalis']
		if elite_legend:
			legends.append(elite_legend)
		# deterministic pick for stability
		leg1 = legends[0]
		leg2 = legends[1]

		def add_skill(name: str) -> None:
			nonlocal code
			code += _little_endify(_int_hex_double(_palette_id(name)))
			code += '0000'

		# legend 1 full kit (heal, 3 utils, elite)
		if leg1 == 'Shiro':
			for sn in ["Enchanted Daggers", "Phase Traversal", "Riposting Shadows", "Impossible Odds", "Jade Winds"]:
				add_skill(sn)
		elif leg1 == 'Ventari':
			for sn in ["Project Tranquility", "Natural Harmony", "Protective Solace", "Purifying Essence", "Energy Expulsion"]:
				add_skill(sn)
		elif leg1 == 'Mallyx':
			for sn in ["Empowering Misery", "Banish Enchantment", "Pain Absorption", "Call to Anguish", "Embrace the Darkness"]:
				add_skill(sn)
		elif leg1 == 'Jalis':
			for sn in ["Soothing Stone", "Inspiring Reinforcement", "Forced Engagement", "Vengeful Hammers", "Rite of the Great Dwarf"]:
				add_skill(sn)
		elif leg1 == 'Glint':
			for sn in ["Facet of Light", "Facet of Darkness", "Facet of Elements", "Facet of Strength", "Facet of Chaos"]:
				add_skill(sn)
		elif leg1 == 'Scorchrazor':
			for sn in ["Breakrazor's Bastion", "Razorclaw's Rage", "Darkrazor's Daring", "Icerazor's Ire", "Soulcleave's Summit"]:
				add_skill(sn)
		elif leg1 == 'Alliance':
			for sn in ["Selfish Spirit", "Nomad's Advance", "Scavenger Burst", "Reaver's Rage", "Spear of Archemorus"]:
				add_skill(sn)

		# legends bytes
		code += _int_hex_byte(legends_dict[leg1])
		code += _int_hex_byte(legends_dict[leg2])
		code += '0000'

		# legend 2 subset
		if leg2 == 'Shiro':
			for sn in ["Phase Traversal", "Riposting Shadows", "Impossible Odds"]:
				code += _little_endify(_int_hex_double(_palette_id(sn)))
			code += '000000000000'
		elif leg2 == 'Ventari':
			for sn in ["Natural Harmony", "Protective Solace", "Purifying Essence"]:
				code += _little_endify(_int_hex_double(_palette_id(sn)))
			code += '000000000000'
		elif leg2 == 'Mallyx':
			for sn in ["Banish Enchantment", "Pain Absorption", "Call to Anguish"]:
				code += _little_endify(_int_hex_double(_palette_id(sn)))
			code += '000000000000'
		elif leg2 == 'Jalis':
			for sn in ["Inspiring Reinforcement", "Forced Engagement", "Vengeful Hammers"]:
				code += _little_endify(_int_hex_double(_palette_id(sn)))
			code += '000000000000'
		elif leg2 == 'Glint':
			for sn in ["Facet of Darkness", "Facet of Elements", "Facet of Strength"]:
				code += _little_endify(_int_hex_double(_palette_id(sn)))
			code += '000000000000'
		elif leg2 == 'Scorchrazor':
			for sn in ["Razorclaw's Rage", "Darkrazor's Daring", "Icerazor's Ire"]:
				code += _little_endify(_int_hex_double(_palette_id(sn)))
			code += '000000000000'
		elif leg2 == 'Alliance':
			for sn in ["Nomad's Advance", "Scavenger Burst", "Reaver's Rage"]:
				code += _little_endify(_int_hex_double(_palette_id(sn)))
			code += '000000000000'

 	return code.upper()


def encode_build(payload: dict) -> str:
	# Build hex and then base64-wrap
	code = _encode_hex(payload)
	import codecs as _codecs
	try:
		code_b64 = _codecs.encode(_codecs.decode(code, 'hex'), 'base64').decode().strip()
	except Exception:
		return "[&BQQAAAA=]"
	return f"[&{code_b64}]"


def encode_build_with_hex(payload: dict) -> Tuple[str, str]:
	code = _encode_hex(payload)
	import codecs as _codecs
	try:
		code_b64 = _codecs.encode(_codecs.decode(code, 'hex'), 'base64').decode().strip()
		return f"[&{code_b64}]", code.upper()
	except Exception:
		return "[&BQQAAAA=]", code.upper()


