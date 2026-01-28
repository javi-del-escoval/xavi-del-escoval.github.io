from json import dump

def reset_config():
	data = {
		"save_path"	:	"Scraping.xlsx",
		"days_mp"	:	7,
		"keywords"	:
		[
			"Hidrógeno",
			"Energía renovable",
			"Innovación",
			"Cambio climático",
			"Transición energética",
			"Sostenibilidad",
			"Sostenible",
			"Ciencia"
		],
		"exclusions":
		[
			"Peróxido",
			"Salud",
			"Esteriliza",
			"Médicos",
			"Dental",
			"Medicamento"
		],
		"ticket"	:	"139EBBDA-64D8-411C-9DF0-83E4D8D62701"
	}

	with open('config.json', 'w+', encoding='utf-8') as file:
		dump(data, file, indent=4)

if __name__ == '__main__':
	reset_config()