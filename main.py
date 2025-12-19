import tkinter, yt_dlp, ctypes, sys, tools, winsound, data, threading, tkinter.font
from types import SimpleNamespace

ui = SimpleNamespace()

ui.second_pass = False

class StdoutHook:
    def __init__(self, original_stdout):
        self.original_stdout = original_stdout

    def write(self, text):
        # Luego mandar el texto original a la consola
        self.original_stdout.write(text)
        self.original_stdout.flush()

        # Ejecutar código cada vez que se imprime algo
        if text.strip() and "Deleting original file" in text.strip():  # para evitar ejecutar con saltos de línea vacíos
            if ui.download_option_var.get() == "Video":
                if ui.second_pass == True:
                    ui.second_pass = not ui.second_pass
                    ui.texto_estado.set("Descarga finalizada")
                    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
                else: ui.second_pass = True
            else:
                ui.texto_estado.set("Descarga finalizada")
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
            #self.original_stdout.write(f"[HOOK] Capturado: {text.strip()}\n")

    def flush(self):
        self.original_stdout.flush()

sys.stdout = StdoutHook(sys.stdout)

##***************# # # # # # # # # # #*******************##
##               #    Main WINDOW    #                   ##
## # # # # # # # # # # # # # # # # # # # # # # # # # # # ##
def main_window():

    if not data.is_compiled(): # Pide permisos de administrador en caso de que este ejecutandose como script .py
        if not admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
    
    # Rutas de los iconos de la app
    ui.icons = {
        "main_ico" : data.script_directory + "\\tools\\icon.ico",
        "empty_ico" : data.script_directory + "\\tools\\empty.ico"
    }

    ui.ventana = tkinter.Tk() # Crea la ventana
    ui.ventana.title("Youtube Downloader") # Titulo de la ventana
    ui.ventana.resizable(False, False) # Deshabilita el redimensionamiento de la ventana

    ui.main_width, ui.main_height = 400, 260 # Dimensiones de la ventana
    width_screen, height_screen = ui.ventana.winfo_screenwidth(), ui.ventana.winfo_screenheight() # Obtener dimensiones de la pantalla
    
    # Calcular posición centrada de la ventana
    main_x = (width_screen - ui.main_width) // 2
    main_y = (height_screen - ui.main_height - 200) // 2

    ui.ventana.geometry(f"{ui.main_width}x{ui.main_height}+{main_x}+{main_y}") # Aplicar geometry centrado

    # Colores de la app
    ui.colors = {
        "MAIN_BG" : "#1e1e1e",
    }

    ui.ventana.configure(bg=ui.colors["MAIN_BG"]) # Configura el color del fondo de la ventana
    
    ui.ventana.iconbitmap(ui.icons["main_ico"]) # Establece el ícono de la ventana

    ui.main_font = tkinter.font.Font(family="Segoe UI", size=12) # Variable con la fuente por defecto de la app
    
    # Establece el tamaño de las columnas de la red de la ventana
    columns = 6
    for i in range(columns):
        ui.ventana.grid_columnconfigure(i, weight=1)
    
    # Establece el tamaño de las filas de la red de la ventana
    rows = 6
    for i in range(rows):
        ui.ventana.grid_rowconfigure(i, weight=1)

    label = tkinter.Label(ui.ventana, text="Introduzca la URL de Youtube", font=ui.main_font, bg=ui.colors["MAIN_BG"], fg="white", width=30, justify="left")
    label.grid(row=1, column=2, sticky="swe", pady=1, padx=1)
    
    ui.url = tkinter.Entry(ui.ventana)
    ui.url.grid(row=2, column=2, sticky="we", pady=10, padx=5)

    clear_button = tkinter.Button(text="Limpiar", font=ui.main_font, command= clear_url, width=6, height=1)
    clear_button.grid(row=2, column=3, sticky="", pady=1, padx=1)

    ui.download_option_var = tkinter.StringVar()
    ui.download_option_var.set("Audio")

    download_audio = tkinter.Radiobutton(ui.ventana, text="Audio", variable=ui.download_option_var, value="Audio", bg=ui.colors["MAIN_BG"], fg="white", selectcolor=ui.colors["MAIN_BG"])
    download_audio.grid(row=3, column=2, sticky="nw", pady=1, padx=40)

    download_video = tkinter.Radiobutton(ui.ventana, text="Video", variable=ui.download_option_var, value="Video", bg=ui.colors["MAIN_BG"], fg="white", selectcolor=ui.colors["MAIN_BG"])
    download_video.grid(row=3, column=2, sticky="ne", pady=1, padx=40)


    ui.download_button = tkinter.Button(text="Descargar", font=ui.main_font, command=download_window)
    ui.download_button.grid(row=4, column=2, sticky="nwe", pady=1, padx=1)

    dev_label = tkinter.Label(ui.ventana, text=f"Dev: bhmint", font=ui.main_font, bg=ui.colors["MAIN_BG"], fg="white", width=17)
    dev_label.grid(row=5, column=1, sticky="w", pady=1, padx=1)

    version = tools.version

    version_label = tkinter.Label(ui.ventana, text=f"Version: {version}", font=ui.main_font, bg=ui.colors["MAIN_BG"], fg="white", width=17)
    version_label.grid(row=5, column=3, sticky="e", pady=1, padx=1)

    ui.ventana.mainloop()


##***************# # # # # # # # # # #*******************##
##               #  Download WINDOW  #                   ##
## # # # # # # # # # # # # # # # # # # # # # # # # # # # ##

def download_window(): # this use threading
    if ui.url.get() == "":
        return error_message("URL Inválida")
    
    ui.downloading = tkinter.Toplevel()
    ui.downloading.title("Descargando...")
        
    width, height = 250, 100 # Tamaño de la ventana
        
    # Obtener posición y tamaño de la ventana principal
    ui.ventana.update_idletasks()
        
    x_main = ui.ventana.winfo_x()
    y_main = ui.ventana.winfo_y()
    ancho_main = ui.ventana.winfo_width()
    alto_main = ui.ventana.winfo_height()
        
    # Calcular posición centrada
    x = x_main + (ancho_main - width) // 2
    y = y_main + (alto_main - height) // 2
        
    ui.downloading.geometry(f"{width}x{height}+{x}+{y}")

    ui.downloading.configure(bg=ui.colors["MAIN_BG"])
        
    ui.downloading.iconbitmap(ui.icons["empty_ico"])

    ui.downloading.resizable(False, False)

    for i in range(3):
        ui.downloading.grid_columnconfigure(i, weight=1)

    for i in range(3):
        ui.downloading.grid_rowconfigure(i, weight=1)

    ui.texto_estado = tkinter.StringVar()

    state_label = tkinter.Label(ui.downloading, textvariable=ui.texto_estado, font=ui.main_font, bg="#1e1e1e", fg="white", width=40, justify="center")
    state_label.grid(row=1, column=1, pady=(20, 20))

    ui.download_button.config(state='disabled')
    ui.texto_estado.set("Iniciando descarga...")
    
    # Ruta local a ffmpeg
    ruta_ffmpeg = data.script_directory + "\\tools\\ffmpeg.exe"

    if ui.download_option_var.get() == "Audio":
        opciones = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
                }],
            'outtmpl': data.script_directory + '\\%(title)s.%(ext)s',
            'progress_hooks': [mi_hook],
            'ffmpeg_location': ruta_ffmpeg
        }
    else:
        opciones = {
            'format': 'bv*[height>=1080][ext=mp4]+ba[ext=m4a]/bestvideo[height>=1080]+bestaudio',
            'merge_output_format': 'mp4',
            'outtmpl': data.script_directory + '\\%(title)s.%(ext)s',
            'noplaylist': True,  # por si la URL es de una playlist
            'quiet': False,      # mostrará mensajes de progreso
            'verbose': True,     # para ver más información
            'progress_hooks': [mi_hook],
            'ffmpeg_location': ruta_ffmpeg
        }
    
    def hilo_descarga():
            try:
                with yt_dlp.YoutubeDL(opciones) as ydl:
                    ydl.download([ui.url.get()])
            except yt_dlp.DownloadError as e:
                ui.downloading.destroy
                error_message("URL Inválida")
                ui.texto_estado.set("Error durante la descarga")
                ui.downloading.destroy
            except Exception as e:
                 ui.downloading.destroy
                 error_message("Fallo inesperado")
                 ui.texto_estado.set("Fallo inesperado")
            finally:
                ui.download_button.config(state='normal')
    
    threading.Thread(target=hilo_descarga).start()


##***************# # # # # # # # # #*******************##
##               #   Error WINDOW  #                   ##
## # # # # # # # # # # # # # # # # # # # # # # # # # # ##

def error_message(a): # download_window call this
    error = tkinter.Toplevel() # Crea la ventana

    error.title("Error") # Título de la ventana 
    width, height = 250, 100 # Tamaño de la ventana

    ui.ventana.update_idletasks() # Obtine el tamaño de la ventana principal
    x_main = ui.ventana.winfo_x() #
    y_main = ui.ventana.winfo_y() #
    width_main = ui.ventana.winfo_width() #
    height_main = ui.ventana.winfo_height() #
        
    # Calcular posición centrada
    x = x_main + (width_main - width) // 2
    y = y_main + (height_main - height) // 2
        
    error.geometry(f"{width}x{height}+{x}+{y}")

    error.configure(bg=ui.colors["MAIN_BG"])
        
    error.iconbitmap(ui.icons["empty_ico"])

    error.resizable(False, False)

    columns = 3
    for i in range(columns):
        error.grid_columnconfigure(i, weight=1)
    
    rows = 3
    for i in range(rows):
        error.grid_rowconfigure(i, weight=1)

    error_label = tkinter.Label(error, text=a, font=ui.main_font, bg=ui.colors["MAIN_BG"], fg="white", width=40, justify="center")
    error_label.grid(row=1, column=1, pady=(20, 20))

    error_button = tkinter.Button(error, text="Continuar", font=ui.main_font, command= error.destroy, justify="center")
    error_button.grid(row=2, column=1, pady=(10, 10))

    winsound.MessageBeep(winsound.MB_ICONHAND)


##***************# # # # # # # # # #*******************##
##               #     Fuctions    #                   ##
## # # # # # # # # # # # # # # # # # # # # # # # # # # ## 

def admin() -> bool: # main_window call this
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def mi_hook(a): # download_window call this
    if a['status'] == 'downloading':
        porcentaje = a.get('_percent_str', '').strip()
        eta = a.get('_eta_str', '').strip()
        downloaded_bytes = a.get('_downloaded_bytes_str', '').strip()
        estimated_bytes = a.get('_total_bytes_estimate_str', '').strip()

        ui.texto_estado.set(f"Descargando: {porcentaje}\n{downloaded_bytes}/{estimated_bytes}\nTiempo restante: {eta}")
    elif a['status'] == 'finished':
        return

def clear_url(): # main_window call this
    ui.url.delete(0, tkinter.END)


main_window()

if __name__ == "__main__":
    pass