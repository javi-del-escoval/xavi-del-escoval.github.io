import re

def to_dash_case(name):
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1-\2', name)
    s2 = re.sub('([A-Z]{2,})(?=[A-Z][a-z]+[0-9]*|\\b)', r'\1-', s1)
    s3 = re.sub(r'[\-\.\s]+', '-', s2)
    return s3.lower().strip('-')

def generate_html():
	out = '<div class="list-modulos">\n	<ul>\n	<strong>Modulos Seleccionados:</strong>\n'

	with open('modulos.txt', 'r', encoding='utf-8') as file:
		for line in file:
			out += f'		<li class="hidden" id="modulo-{to_dash_case(line.strip())}">{line.strip().replace('H2', 'H<sub>2</sub>')}</li>\n'
	out += f'	</ul>\n	<a href="#custom-form" class="button" style="float:right">Paso 2</a>\n</div>' #<img draggable="false" role="img" class="emoji" alt="✔️" src="https://s.w.org/images/core/emoji/17.0.2/svg/2714.svg">
	return out

with open('list.html', 'w+', encoding='utf-8') as file:
	file.write(generate_html())