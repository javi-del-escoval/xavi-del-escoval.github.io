# Herramienta de Web Scraping - ECIT
## Descarga e Instalación
En este mismo repositorio ir a la carpeta [Installers](https://github.com/javi-del-escoval/web-scraper-ecit/tree/main/Installers "Installers") y descargar la ultima versión disponible.\
Por defecto la carpeta de instalación es Documentos.
## Uso
### 1.- Inicio
Aquí se da la instrucción al programa de realizar scraping, todo proceso de scraping genera un archivo Excel con los resultados (ver Data).\
Cada vez que se realiza un scraping ya sea general o individual los resultados sobrescriben el archivo Excel.\
![Pantalla "Inicio" con indicaciones de que hace cada botón](/readme/inicio.png "Tab de Inicio")\
Con La configuración por defecto un scraping general toma aproximadamente 12 minutos\
Desglose por plataforma:
-	Mercado Publico: 13 segundos
-	BID: 9 segundos
-	ANID: 3 segundos
-	SERCOTEC: 9 minutos 8 segundos
-	CORFO: 48 segundos
-	CODESSER: 50 segundos

---
### 2.- Data
En Data puedes editar el nombre del archivo en donde se guardarán los resultados, este archivo se escribe de manera relativa a donde está el instalado el programa, si el archivo no existe se creará.
Si desea que sus archivos se guarden en una carpeta por separado la carpeta debe existir antes de iniciar un proceso de scraping.\
E.g.1:\
![Pantalla "Data" con indicaciones de que hace cada botón](/readme/data.png "Tab de Data")\
Web Scraper 0.1.5/\
├─ _internal/\
├─ config.json\
├─ 
$\color{blue}{\text{Scraping.xlsx*}}$\
├─ unins000.dat\
├─ unins000.exe\
└─ Web Scraper.exe\
E.g.2:
![Pantalla "Data" destacando la ruta de archivo invalida](/readme/data1.png "Ruta invalida")\
Web Scraper 0.1.5/\
└─ 
$\color{red}{\text{data/	<-- No existe}}$\
&emsp;└─ 
$\color{red}{\text{Scraping.xlsx*}}$\
├─ _internal/\
├─ config.json\
├─ unins000.dat\
├─ unins000.exe\
└─ Web Scraper.exe\

---
### 3.- Keywords
![Pantalla "Keywords" con indicaciones de que hace cada sección](/readme/keywords.png "Tabs de Keywords")\
Aquí se añade la información para filtrar los resultados, tanto las keywords como las palabras de exclusión deben estar separadas, dejando una por línea.
Tambien el ticket de Mercado Publico para acceso a su [API](https://api.mercadopublico.cl/modules/api.aspx "API Mercado Publico")
