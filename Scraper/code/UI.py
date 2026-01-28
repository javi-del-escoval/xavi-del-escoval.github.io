from tkinter_unblur import Tk
from tkinter import font as tkFont
from tkinter import ttk, END, Toplevel, StringVar, Frame, Spinbox, Text, VERTICAL, RIGHT, Y
from tkinter.messagebox import showinfo, showerror
from pandas import DataFrame, read_excel
import sys
from os import path, environ, startfile
from json import load, dump
from time import perf_counter
from reset_config import reset_config
import scraper

if getattr(sys, "frozen", False):
	base_path = sys._MEIPASS if hasattr(sys, "_MEIPASS") else path.dirname(sys.executable)
	environ["PLAYWRIGHT_BROWSERS_PATH"] = path.join(base_path, "ms-playwright")
else:
	environ["PLAYWRIGHT_BROWSERS_PATH"] = ""

# cargar configuración
_CONFIG = {}
try:
	with open('config.json', 'r', encoding='utf-8') as file:
		_CONFIG = load(file)
except FileNotFoundError:
	reset_config()
	try:
		with open('config.json', 'r', encoding='utf-8') as file:
			_CONFIG = load(file)
	except Exception as e:
		showerror('Web Scraper - ECIT', f'[Load Config] Error: {e}')
except Exception as e:
	showerror('Web Scraper - ECIT', f'[Load Config] Error: {e}')

'''
┃				UTILS				┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'''
def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS  # PyInstaller temp folder
	except Exception:
		base_path = path.abspath(".")
	return path.join(base_path, relative_path)

def load_keywords():
	keywords = ''
	for k in _CONFIG['keywords']:
		keywords += k +'\n'
	text_keywords.delete('1.0', END)
	text_keywords.insert('1.0', keywords[:-1])

	exclusions = ''
	for e in _CONFIG['exclusions']:
		exclusions += e + '\n'
	text_exclusions.delete('1.0', END)
	text_exclusions.insert('1.0', exclusions[:-1])

	entry_ticket.delete(0,END)
	entry_ticket.insert(0, _CONFIG['ticket'])

def open_save_file():
	try:
		startfile(path.abspath(_CONFIG['save_path']))
	except FileNotFoundError:
		showerror('Web Scraper - ECIT', f'[Open Save File] Error:\nEl archivo{_CONFIG['save_path']} no esxiste!\nIntenta iniciar un scrap para generar el archivo')
	except Exception as e:
		showerror('Web Scraper - ECIT', f'[Open Save File] Error:\n{type(e)}\n\n{e}')

def on_tab_changed(event):
	tab_id = event.widget.select()
	tab_text = event.widget.tab(tab_id, 'text')
	if tab_text == 'Keywords':
		load_keywords()
	elif tab_text == 'Data':
		entry_save_file.delete(0, END)
		entry_save_file.insert(0, _CONFIG['save_path'])
		# try:
		# 	df = read_excel(_CONFIG['save_path'])
		# 	results = df.to_dict(orient='records')
		# 	for entry in results:
		# 		tree_resultados.insert('', END, values=list(entry.values()))
		# except Exception as e:
		# 	showerror('Web Scraper - ECIT', f'[Load Data] Error: {type(e)}\n{e}')

def save_config(keywords, exclusions, ticket):
	global _CONFIG
	_CONFIG['keywords'] = keywords.get('1.0', END + '-1c').split('\n')
	_CONFIG['exclusions'] = exclusions.get('1.0', END + '-1c').split('\n')
	_CONFIG['ticket'] = ticket.get()
	try:
		with open('config.json', 'w') as file:
			dump(_CONFIG, file, indent=4)
	except Exception as e:
		showerror('Web Scraper - ECIT', f'[Save Config] Error: {e}')
	showinfo('Web Scraper - ECIT', 'Configuración guardada!')

def modify_save_location(entry):
	file_path = entry.get()
	_CONFIG['save_path'] = file_path
	scraper._SAVE_FILE = file_path
	try:
		with open('config.json', 'w') as file:
			dump(_CONFIG, file, indent=4)
		showinfo('Web Scraper - ECIT', 'Archivo de destino modificado exitosamente!')
	except Exception as e:
		showerror('Web Scraper - ECIT', f'[Save Config] Error: {e}')

def on_spinbox_change():
	global _CONFIG
	_CONFIG['days_mp'] = spinbox_mercado_publico.get()
	try:
		with open('config.json', 'w') as file:
			dump(_CONFIG, file, indent=4)
	except Exception as e:
		showerror('Web Scraper - ECIT', f'[Mercado Publico] Error: {e}')

'''
┃			  SCRAPING				┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'''
def scrape():
	try:
		start_time = perf_counter()

		top_level = Toplevel(root)
		top_level.title("[Log] Scraping...")
		top_level.geometry("350x550+25+100")
		log_var = StringVar()
		log_var.set('Iniciando scraping...')
		ttk.Label(top_level, textvariable=log_var).pack()
		root.update()

		output, results = scraper.main(root=root, log_var=log_var)

		end_time = perf_counter()
		elapsed_time = end_time - start_time
		log_var.set(output+f'\n\nTiempo total: {elapsed_time:.2f} segundos')
		print(f'Tiempo total: {elapsed_time:.2f} segundos')
		root.update()

		# for entry in results:
		# 	tree_resultados.insert('', END, values=list(entry.values()))

		hrs = int(elapsed_time//3600)
		minutes = int((elapsed_time-hrs*3600)//60)
		seconds = elapsed_time-(hrs*3600)-(minutes*60)
		formated_time = f'{f'{hrs} horas, ' if hrs>0 else ''}{f'{minutes} minutos, ' if minutes>0 else ''}{f'{seconds:.2f} segundos' if seconds>0 else ''}'
		showinfo('Web Scraper - ECIT', f'Scraping finalizado\n\nTiempo total: {formated_time}')
		top_level.destroy()
	except Exception as e:
		showerror('Web Scraper - ECIT', f'[Scraper] Error: {e}')

def mercado_publico():
	try:
		start_time = perf_counter()
		results, included, excluded = scraper.mercado_publico(dias=int(_CONFIG['days_mp']))
		end_time = perf_counter()
		elapsed_time = end_time - start_time

		df = DataFrame(results)
		df['se toma'] = False
		df = df.drop_duplicates()
		df.to_excel(_CONFIG['save_path'])

		# for entry in results:
		# 	tree_resultados.insert('', END, values=list(entry.values()))

		hrs = int(elapsed_time//3600)
		minutes = int((elapsed_time-hrs*3600)//60)
		seconds = elapsed_time-(hrs*3600)-(minutes*60)
		formated_time = f'{f'{hrs} horas, ' if hrs>0 else ''}{f'{minutes} minutos, ' if minutes>0 else ''}{f'{seconds:.2f} segundos' if seconds>0 else ''}'
		print(f'Tiempo total: {formated_time}')
		showinfo('Web Scraper - ECIT', f'Scraping finalizado exitosamente!\n{_CONFIG['days_mp']+1} dias consultados.\n{included} resultados incluidos\n{excluded} resultados excluidos.\n\nTiempo total: {formated_time}')
	except Exception as e:
		showerror('Web Scraper - ECIT', f'[Save] Error: {e}')

def independent_scraping(platform):
	try:
		start_time = perf_counter()
		results, included, excluded = platform()
		end_time = perf_counter()
		elapsed_time = end_time - start_time
		df = DataFrame(results)
		df['se toma'] = False
		df = df.drop_duplicates()
		df.to_excel(_CONFIG['save_path'])

		# for entry in results:
		# 	tree_resultados.insert('', END, values=list(entry.values()))

		hrs = int(elapsed_time//3600)
		minutes = int((elapsed_time-hrs*3600)//60)
		seconds = elapsed_time-(hrs*3600)-(minutes*60)
		formated_time = f'{f'{hrs} horas, ' if hrs>0 else ''}{f'{minutes} minutos, ' if minutes>0 else ''}{f'{seconds:.2f} segundos' if seconds>0 else ''}'
		print(f'Tiempo total: {formated_time} segundos')
		showinfo('Web Scraper - ECIT', f'Scraping finalizado exitosamente!\n{included} resultados incluidos\n{excluded} resultados excluidos.\n\nTiempo total: {formated_time}')
	except Exception as e:
		showerror('Web Scraper - ECIT', f'[Save] Error: {e}')

def keyword_independent_scraping(platform):
	success = True
	results = []
	excluded = 0
	included = 0
	start_time = perf_counter()
	for keyword in _CONFIG['keywords']:
		try:
			tmp, x, n = platform(keyword)
			results += tmp
			included += x
			excluded += n
			df = DataFrame(results)
			df['se toma'] = False
			df = df.drop_duplicates()
			df.to_excel(_CONFIG['save_path'])
		except Exception as e:
			success = False
			showerror('Web Scraper - ECIT', f'[Save] Error: {e}')
	if success:
		end_time = perf_counter()
		elapsed_time = end_time - start_time
		df['se toma'] = False
		df = df.drop_duplicates()
		df.to_excel(_CONFIG['save_path'])

		# for entry in results:
		# 	tree_resultados.insert('', tk.END, values=entry)

		hrs = int(elapsed_time//3600)
		minutes = int((elapsed_time-hrs*3600)//60)
		seconds = elapsed_time-(hrs*3600)-(minutes*60)
		formated_time = f'{f'{hrs} horas, ' if hrs>0 else ''}{f'{minutes} minutos, ' if minutes>0 else ''}{f'{seconds:.2f} segundos' if seconds>0 else ''}'
		print(f'Tiempo total: {formated_time} segundos')
		showinfo('Web Scraper - ECIT', f'Scraping finalizado exitosamente!\n{included} resultados incluidos\n{excluded} resultados excluidos.\n\nTiempo total: {formated_time}')

'''
┃				MAIN UI				┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'''
root = Tk()
root.title('Web Scraper - ECIT')
root.geometry('600x400+400+100')
root.iconbitmap(resource_path("icon.ico"))
default_font = tkFont.nametofont('TkDefaultFont')
default_font.config(size=12)

tab_control = ttk.Notebook(root)

'''
┃				STYLES				┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'''
ttk.Style().configure('R.Warning.TLabel', foreground='red')

'''
┃				TABS				┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'''
tab_home = ttk.Frame(tab_control)
tab_control.add(tab_home, text='Inicio')

tab_data = ttk.Frame(tab_control)
tab_control.add(tab_data, text='Data')

tab_keywords = ttk.Frame(tab_control)
tab_control.add(tab_keywords, text='Keywords')

tab_control.pack(expand=1, fill='both')

'''
┃				HOME				┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'''

tab_home.grid_rowconfigure([0,3,4], weight=1, uniform='home_tab')
tab_home.grid_columnconfigure(list(range(3)), weight=1, uniform='home_tab')

btn_run = ttk.Button(tab_home, text='Iniciar Scraping', command=scrape)
btn_run.grid(row=0, column=1, sticky='nsew', padx=20, pady=20)

label_platforms = ttk.Label(tab_home, text='Scraping individual:')
label_platforms.grid(row=1, column=0, padx=20, pady=5)

label_warning = ttk.Label(tab_home, text='Advertencia: Estas acciones borran información prexistente,\nasegurate de revisar el archivo de destino en \'Data\'', style='R.Warning.TLabel')
label_warning.grid(row=2, column=0, columnspan=3, padx=20, pady=5)

frame_individual_scraping = Frame(tab_home, borderwidth=1, relief="sunken")#, background='gray'
frame_individual_scraping.grid_rowconfigure(list(range(3)), weight=1, uniform='buttons')
frame_individual_scraping.grid_columnconfigure(list(range(3)), weight=1, uniform='buttons')

frame_mercado_publico = Frame(frame_individual_scraping)
frame_mercado_publico.grid_rowconfigure(0, weight=1)
frame_mercado_publico.grid_columnconfigure(list(range(4)), weight=1, uniform='mp')

btn_mercado_publico = ttk.Button(frame_mercado_publico, text='Mercado Publico', command=mercado_publico)
btn_mercado_publico.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=3, pady=5)
spinbox_mercado_publico = Spinbox(frame_mercado_publico, from_=0, to=31, font=('Arial', 12), justify='center', command=on_spinbox_change)
spinbox_mercado_publico.delete(0, END)
spinbox_mercado_publico.insert(0, _CONFIG['days_mp'])
spinbox_mercado_publico.grid(row=0, column=3, sticky='ns', padx=3, pady=10)

frame_mercado_publico.grid(row=0, column=0, sticky='nsew', padx=5)

btn_corfo = ttk.Button(frame_individual_scraping, text='CORFO', command=lambda p=scraper.corfo: keyword_independent_scraping(p))
btn_corfo.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

btn_sercotec = ttk.Button(frame_individual_scraping, text='SERCOTEC', command=lambda p=scraper.sercotec: independent_scraping(p))
btn_sercotec.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)

btn_anid = ttk.Button(frame_individual_scraping, text='ANID', command=lambda p=scraper.anid: independent_scraping(p))
btn_anid.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

btn_bid = ttk.Button(frame_individual_scraping, text='BID', command=lambda p=scraper.bid: independent_scraping(p))
btn_bid.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)

btn_codesser = ttk.Button(frame_individual_scraping, text='CODESSER', command=lambda p=scraper.codesser: keyword_independent_scraping(p))
btn_codesser.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)

frame_individual_scraping.grid(row=3, column=0, rowspan=5, columnspan=3, sticky='nsew', padx=0, pady=0)

'''
┃				DATA				┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'''

tab_data.grid_rowconfigure(list(range(4)), weight=1, uniform='data')
tab_data.grid_columnconfigure(list(range(4)), weight=1)

label_save_file = ttk.Label(tab_data, text='Archivo de destino:')
label_save_file.grid(row=1, column=0, rowspan=1, sticky='nsew', padx=5, pady=20)

entry_save_file = ttk.Entry(tab_data, font='Arial 12')
entry_save_file.grid(row=1, column=1, rowspan=1, columnspan=3, sticky='nsew', padx=5, pady=20)

btn_modify = ttk.Button(tab_data, text='Cambiar', command=lambda x=entry_save_file: modify_save_location(x))
btn_modify.grid(row=2, column=2, sticky='nse', padx=5, pady=20)

btn_abrir = ttk.Button(tab_data, text='Abrir', command=open_save_file)
btn_abrir.grid(row=2, column=3, sticky='nsw', padx=5, pady=20)

# columns = ('titulo', 'fecha-inicio', 'fecha-fin', 'descripcion', 'plataforma', 'anunciante', 'take')
# tree_resultados = ttk.Treeview(tab_data, columns=columns, show='headings')
# # definir titulos de columna
# tree_resultados.heading('titulo', text='Titulo')
# tree_resultados.heading('fecha-inicio', text='Fecha de Apertura')
# tree_resultados.heading('fecha-fin', text='Fecha de Cierre')
# tree_resultados.heading('descripcion', text='Link')
# tree_resultados.heading('plataforma', text='Plataforma')
# tree_resultados.heading('anunciante', text='Anunciante')
# tree_resultados.heading('take', text='Se Toma')

# tree_resultados.column('titulo', width=500)
# tree_resultados.column('fecha-inicio', width=50)
# tree_resultados.column('fecha-fin', width=50)
# tree_resultados.column('descripcion', width=500)
# tree_resultados.column('plataforma', width=40)
# tree_resultados.column('anunciante', width=150)
# tree_resultados.column('take', width=10)

# tree_resultados.grid(row=2, column=0, rowspan=3, columnspan=7, sticky='nsew', padx=5, pady=20)

'''
┃			  KEYWORDS				┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'''

tab_keywords.grid_rowconfigure(list(range(1,5)), weight=1, uniform='keywords_tab')
tab_keywords.grid_columnconfigure(list(range(4)), weight=1, uniform='keywords_tab')

'''━━━━━━━━━━ Keywords ━━━━━━━━━━'''

label_keywords = ttk.Label(tab_keywords, text='Keywords:')
label_keywords.grid(row=0, column=0, sticky='sew', padx=20, pady=5)

text_keywords = Text(tab_keywords, height=50, width=100, font='Arial 12')
text_keywords.grid(row=1, column=0, rowspan=2, columnspan=2, sticky='nsew', padx=20, pady=5)

scrollbar_keywords = ttk.Scrollbar(text_keywords, command=text_keywords.yview, orient=VERTICAL)
scrollbar_keywords.pack(side=RIGHT, fill=Y)

text_keywords.config(yscrollcommand=scrollbar_keywords.set)

'''━━━━━━━━━━ Exclusiones ━━━━━━━━━━'''

label_exclusions = ttk.Label(tab_keywords, text='Exclusiones:')
label_exclusions.grid(row=0, column=2, sticky='sew', padx=20, pady=5)

text_exclusions = Text(tab_keywords, height=50, width=100, font='Arial 12')
text_exclusions.grid(row=1, column=2, rowspan=2, columnspan=2, sticky='nsew', padx=20, pady=5)

# Add a ttk Scrollbar
scrollbar_exclusions = ttk.Scrollbar(text_exclusions, command=text_exclusions.yview, orient=VERTICAL)
scrollbar_exclusions.pack(side=RIGHT, fill=Y)

text_exclusions.config(yscrollcommand=scrollbar_exclusions.set)

'''━━━━━━━━━━ Ticket ━━━━━━━━━━'''

frame_ticket = Frame(tab_keywords)#, background='red'
frame_ticket.grid(row=3, column=0, columnspan=4, sticky='nsew', padx=20, pady=0)
frame_ticket.grid_columnconfigure(0, weight=1)
frame_ticket.grid_columnconfigure([1,2,3], weight=2, uniform='ticket')
frame_ticket.grid_rowconfigure(list(range(5)), weight=1)

label_ticket = ttk.Label(frame_ticket, text='Ticket API Mercado Publico:')
label_ticket.grid(row=2, column=0, sticky='nsw', padx=5, pady=5)

entry_ticket = ttk.Entry(frame_ticket, font='Arial 11')
entry_ticket.grid(row=2, column=1, columnspan=3, sticky='nsew', padx=5, pady=5)

### --- Save --- ###

btn_save = ttk.Button(tab_keywords, text='Guardar', command=lambda k = text_keywords, e = text_exclusions, t = entry_ticket: save_config(k, e, t))
btn_save.grid(row=4, column=3, sticky='new', padx=20, pady=5)


'''
┃				END					┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'''

root.bind('<<NotebookTabChanged>>', on_tab_changed)

root.mainloop()