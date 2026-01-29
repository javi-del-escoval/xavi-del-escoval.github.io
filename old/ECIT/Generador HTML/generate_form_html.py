import re

def to_dash_case(name):
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1-\2', name)
    s2 = re.sub('([A-Z]{2,})(?=[A-Z][a-z]+[0-9]*|\\b)', r'\1-', s1)
    s3 = re.sub(r'[\-\.\s]+', '-', s2)
    return s3.lower().strip('-')

files = ['Básicos.txt', 'Avanzados.txt']

def generate_html():
	out = '''<script>
	const detailsElements = document.querySelectorAll('.modulos');
	detailsElements.forEach(details => {
	    details.addEventListener('mouseover', () => {
	        details.setAttribute('open', true);
	    });
	    details.addEventListener('mouseout', () => {
	        details.removeAttribute('open');
	    });
	});
	function onlyOneSubmission(element)
	{
		if(element.form.checkValidity()) {
			setTimeout(() => {
				element.value='Enviando...';
				element.disabled=true;
			} ,0);
		}
		return true;
	}
	function select_module(element)
	{
		var input = element.getElementsByTagName("input")[0];
		if(input) { input.checked = !input.checked; }
		element.parentElement.classList.toggle("selected-module");
		element.parentElement.classList.toggle("unselected-module");
		// floating selected list
		var moduleList = document.getElementsByClassName("list-modulos")[0].getElementsByTagName("li");
		if(moduleList) {
			[...moduleList].forEach(item => { if(input.name == item.id) { item.classList.toggle("hidden"); }});
		}
		// at least one module selected
		var checkboxesList = document.querySelectorAll(".modulo-check");
		var validator = document.getElementById("validator");
		var anyChecked = [...checkboxesList].some(box => box.checked);
		if (anyChecked) {
			validator.value = "ok";
			validator.setCustomValidity('');
		} else {
			validator.value = "";
			validator.setCustomValidity('Selecciona al menos un módulo');
		}
	}
</script>
<form method="post" autocomplete="on">
	<div class="custom-form-modulos">
		<h2>Paso 1: Selecciona los Módulos que Necesitas</h2>
		<h5 style="margin:0;padding:0;"><input type="text" id="validator" tabindex="-1" style="position:absolute;opacity:0;height:0;width:0;" oninvalid="this.setCustomValidity('Selecciona al menos un módulo')" required autocomplete="off" /></h5>
		<div class="separator"></div>'''

	for f in files:
		out += f'''
		<section id="{f[:-4]}">
			<h3>Módulos {f[:-4]}</h3>
			<div class="container-modulos">'''
		with open(f, 'r', encoding='utf-8') as file:
			flag_first = True
			titulo = ''
			n = 0
			for line in file:
				if flag_first:
					flag_first = False
					titulo = line.strip()
					txt_titulo = titulo.replace('H2', 'H<sub>2</sub>')
					out += f'''
				<details class="modulo unselected-module">
					<summary>
						<strong>{txt_titulo}</strong>
					</summary>
					<div>
						<ul>'''
				elif line[0] == '•':
					item = line[:].replace('•', '').strip()
					txt_item = item.replace('H2', 'H<sub>2</sub>')
					out += f'''
							<li>{txt_item}</li>'''
				else:
					out += f'''
						</ul>
						<input type="checkbox" class="modulo-check" style="display:none;" name="modulo-{to_dash_case(titulo)}" value="{titulo}">
						<button type="button" class="button ast-custom-button ast-button" onclick="select_module(this.parentElement)">Seleccionar</button>
					</div>
				</details>'''
					n += 1
					titulo = line.strip()
					txt_titulo = titulo.replace('H2', 'H<sub>2</sub>')
					out += f'''
				<details class="modulo unselected-module">
					<summary>
						<strong>{txt_titulo}</strong>
					</summary>
					<div>
						<ul>'''
			out += f'''
						</ul>
						<input type="checkbox" class="modulo-check" style="display:none;" name="modulo-{to_dash_case(titulo)}" value="{titulo}">
						<button type="button" class="button ast-custom-button ast-button" onclick="select_module(this.parentElement)">Seleccionar</button>
					</div>
				</details>
			</div>
		</section>
		<div class="separator"></div>'''
			n += 1
			if(n%3 == 1):
				index = out.rfind('''
				<details''')
				out = out[:index] + '''
				<details class="empty-module"><summary> </summary></details>''' + out[index:]
	out = out[:-32] + '''
		<div class="separator"></div>
		<section id="otro">
			<h3>Otros Módulos</h3>
			<div class="container-modulos">
				<details class="empty-module"><summary> </summary></details>
 				<details class="modulo unselected-module">
 					<summary>
 						<strong>Módulo Personalizado</strong>
 					</summary>
					<div>
						<textarea name="personalizado-text" placeholder="Describe el módulo personalizado que te interesa cotizar"></textarea>
						<input type="checkbox" class="modulo-check" style="display:none;" name="modulo-personalizado" value="Personalizado">
						<button type="button" class="button ast-custom-button ast-button" onclick="select_module(this.parentElement)">Seleccionar</button>
					</div>
				</details>
			</div>
		</section>
	</div>
	<div class="separator" id="custom-form"></div>
	<div class="custom-form">
		<h2>Paso 2: Rellena el formulario</h2>
		<input type="text" name="name" placeholder="Nombre Completo" autocomplete="name" oninvalid="this.setCustomValidity('Necesitamos saber tu nombre')" oninput="this.setCustomValidity('')" required>
		<input type="email" name="email" placeholder="Email de Contacto" autocomplete="email" oninvalid="this.setCustomValidity('Por favor ingresa tu correo para ponernos en contacto contigo')" oninput="this.setCustomValidity('')" required>
		<input type="text" name="company" placeholder="Institución" autocomplete="organization" oninvalid="this.setCustomValidity('Este campo es requerido')" oninput="this.setCustomValidity('')" required>
		<textarea name="message" placeholder="Hola, me interesa cotizar los módulos seleccionados" oninvalid="this.setCustomValidity('Cuentanos más detalles de lo que necesitas para poder ayudarte mejor')" oninput="this.setCustomValidity('')" required></textarea><br>
		<input type="submit" id="submit-form-modulos" name="submit-form-modulos" onclick="onlyOneSubmission(this)" value="Enviar"/>
	</div>
</form>'''
	return out

with open('form.html', 'w+', encoding='utf-8') as file:
	file.write(generate_html())