<script>
	fetch('https://api.github.com/repos/javi-del-escoval/javi-del-escoval.github.io/contents/Scraper/Installers')
	.then(res => res.json())
	.then(files => {
		const container = document.getElementById('scraper-installers');
		files.forEach(file => {
			if (file.type === 'file') {
				const a = document.createElement('a');
				a.href = file.download_url;
				a.download = file.name;
				a.textContent = file.name;
				container.appendChild(a);
				container.appendChild(document.createElement('br'));
			}
		});
	});
</script>
# Proyectos ECIT
## Web Scraper
### Descarga e instalación
Selecciona la ultima version disponible, ejecuta y sigue las instrucciones del instalador\
(Por defecto el programa se instala en Documentos)\
[¿Que cambio en la ultima version?]("/Scraper/Changelog.md")\
### Uso</h3>
#### Inicio</h4>
Aquí se da la instrucción al programa de realizar scraping, todo proceso de scraping genera un archivo Excel con los resultados (ver Data).\
Cada vez que se realiza un scraping ya sea general o individual los resultados sobrescriben el archivo Excel.\
![Tab de Inicio]("Scraper/readme/inicio.png")\
Con La configuración por defecto un scraping general toma aproximadamente 12 minutos\
Desglose por plataforma:\
- Mercado Publico: 13 segundos
- BID: 9 segundos
- ANID: 3 segundos
- SERCOTEC: 9 minutos 8 segundos
- CORFO: 48 segundos
- CODESSER: 50 segundos
#### Data<
En Data puedes editar el nombre del archivo en donde se guardarán los resultados, este archivo se escribe de manera relativa a donde está el instalado el programa, si el archivo no existe se creará. Si desea que sus archivos se guarden en una carpeta por separado la carpeta debe existir antes de iniciar un proceso de scraping.\
E.g.1:\
![Tab de Data]("Scraper/readme/data.png")/
Web Scraper 0.1.5/\
├─ _internal/\
├─ config.json\
├─ 
$\color{blue}{\text{Scraping.xlsx*}}$\
├─ unins000.dat\
├─ unins000.exe\
└─ Web Scraper.exe\
E.g.2:\
![Tab de Data Ruta Invalida]("Scraper/readme/data1.png")\
Web Scraper 0.1.5/\
└─ 
$\color{red}{\text{data/ <-- No existe}}$\
&emsp;└─ 
$color{red}{\text{Scraping.xlsx*}}$\
├─ _internal/\
├─ config.json\
├─ unins000.dat\
├─ unins000.exe\
└─ Web Scraper.exe
#### Keywords
![Tab de Keywords]("Scraper/readme/keywords.png")\
Aquí se añade la información para filtrar los resultados, tanto las keywords como las palabras de exclusión deben estar separadas, dejando una por línea. Tambien el ticket de Mercado Publico para acceso a su [API]("https://api.mercadopublico.cl/modules/api.aspx")\\
### Generadores de HTML
generador de html/\
├─ <a href="/custom-form" download="Generador HTML/Básicos.txt">Básicos.txt</a>\
├─ <a href="/custom-form" download="Generador HTML/Avanzados.txt">Avanzados.txt</a>\
├─ <a href="/custom-form" download="Generador HTML/form.html">Form.html</a>\
├─ <a href="/custom-form" download="Generador HTML/generate-form-html.py">generate_form_html.py</a>\
├─ <a href="/custom-form" download="Generador HTML/generate-list-html.py">generate_list_html.py</a>\
├─ <a href="/custom-form" download="Generador HTML/list.html">List.html</a>\
└─ <a href="/custom-form" download="Generador HTML/modulos.txt">Módulos</a>\
Cada Archivo txt crea una sección de módulos, si se quiere agregar o quitar un txt se debe modificar esta línea de generate_form_html.py\
<img src="Generador HTML/archivos.png">\
El programa lee cada línea de cada txt y busca la siguiente estructura:\
![File Internal Structure]("Generador HTML/file_structure.png")\
Ósea toda línea que empiece por alguna letra genera un módulo y toma esa línea como título y toda línea que empiece por “•” genera un ítem en la lista del desglose.\\
Módulos.txt incluye los títulos de los módulos, uno por línea.\
Es importante para la funcionalidad que el título de form.html y list.html de cada uno debe ser exactamente igual para que la funcionalidad de la lista funcione correctamente.\
![Nombre de los Módulos Iguales]("Generador%20HTML/module_name.png")\
Finalmente se debe copiar el contenido de cada archivo .html en la sección correspondiente de la página en WordPress.\
![Donde Pegar Cada HTML]("Generador%20HTML/place.png")\
