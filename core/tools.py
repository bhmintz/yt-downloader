#import requests, datetime, data
import data, subprocess
from rich.console import Console
#from rich.layout import Layout
#from rich.panel import Panel
from rich.prompt import Prompt
from colorama import Fore, Style
#from datetime import datetime, timedelta
#from zoneinfo import ZoneInfo

version = "0.1.2"

# Detecta el sistema y guarda el valor correcto para vaciar consola según el sistema corriendo
debug, debug_c = False, "clear" if data.os.name == "posix" else "cls"

# Variable de verificacion de tiempo
verify_time = False

def clear():
    if debug == False: data.os.system(debug_c)

COLOR_MAP_TERM = {
    "green": Fore.GREEN,
    "red": Fore.RED,
    "blue": Fore.BLUE,
    "yellow": Fore.YELLOW,
    "cyan": Fore.CYAN,
    "magenta": Fore.MAGENTA,
    "black": Fore.BLACK,
    "white": Fore.WHITE,
    "lgreen": Fore.LIGHTGREEN_EX,
    "lred": Fore.LIGHTRED_EX,
    "lblue": Fore.LIGHTBLUE_EX,
    "lyellow": Fore.LIGHTYELLOW_EX,
    "lcyan": Fore.LIGHTCYAN_EX,
    "lmagenta": Fore.LIGHTMAGENTA_EX,
    "lblack": Fore.LIGHTBLACK_EX,
    "lwhite": Fore.LIGHTWHITE_EX
}
COLOR_MAP_HEX = {
    # Basics
    "green": "#008000",
    "red": "#FF0000",
    "blue": "#0000FF",
    "yellow": "#FFFF00",
    "orange": "#FFA500",
    "cyan": "#00FFFF",
    "magenta": "#FF00FF",
    "pink": "#FFC0CB",
    "black": "#000000",
    "white": "#FFFFFF",

    # Light
    "lgreen": "#90EE90",
    "lred": "#FF474C",
    "lblue": "#ADD8E6",
    "lyellow": "#FFFAA0",
    "lorange": "#FFD580",
    "lcyan": "#00FFF0",
    "lmagenta": "#FF80FF",
    "lpink": "#FFB6C1",
    "lblack": "#454545",
    "lwhite": "#FFFFF7",

    # Bright
    "brgreen": "#AAFF00",
    "brred": "#EE4B2B",
    "brblue": "#0096FF",
    "bryellow": "#CFFF04",
    "brorange": "#FF5C00",
    "brcyan": "#0AFFFF",
    "brmagenta": "#FF08E8",
    "brpink": "#FF007F",
    "brblack": "#222024",
    "brwhite": "#FFFFFF"
}

def color(color_value, terminal=True):
    if terminal: return COLOR_MAP_TERM.get(color_value, Fore.GREEN)
    else: return COLOR_MAP_HEX.get(color_value, "#FFFFFF")

def texto(texto, color_value, terminal=True, style=""):
    clear = Style.RESET_ALL
    if terminal:
        colorr = color(color_value)
        print(colorr + texto + clear)
    else:
        colorr = color(color_value, False)
        Console().print(f"[{style}{colorr}]{texto}[/{style}{colorr}]")

def inp_texto(texto, color_value, terminal=True, style=""):
    colorr = color(color_value, terminal)
    if terminal:
        clear = Style.RESET_ALL
        input_value = input(colorr + texto + clear)
    else:
        input_value = Prompt.ask(f"[{style}{colorr}]{texto}[/{style}{colorr}]")
    return input_value

def comprobacion(texto, colorr, terminal=True, style=""):
    confirm = inp_texto(texto, colorr, terminal)
    confirm = confirm.lower()

    if confirm == "y" or confirm == "yes":
        retorno = True
    elif confirm == "n" or confirm == "no":
        retorno = False
    else:
        retorno = False

    return retorno

'''
def verify_time_func():
    global verify_time, configs

    if verify_time is False: return

    clear()

    title()

    zona_local = ""

    ### Obtener el horario en internet y si falla detener el script ==================================================
    try:    
        # Obteniendo zona horaria a travez de su ip publica
        datas = requests.get("https://ipinfo.io", timeout=5).json()
        zona_local = datas.get("timezone", None)

        # Obteniendo el horario de internet segun su zona horaria
        url = f"https://api.timezonedb.com/v2.1/get-time-zone?key=YKS5BCDRP1VM&format=json&by=zone&zone={zona_local}"
        response = requests.get(url)
        data = response.json()
        hora_internet = datetime.strptime(data["formatted"], "%Y-%m-%d %H:%M:%S")
    except requests.exceptions.RequestException as e:
        clear()

        title()

        print("")
        texto("Advertencia: No se pudo realizar la verificación por internet de el horario de su sistema.", "red", 2)
        print("")
        texto("PRO TIP: Comprueba que estes conectado a internet y vuelva a ejecutar el script. ツ", "brgreen", 2)
        inp_texto("Presiona ENTER para salir", "white", 2)
        return exit()
    ### ===============================================================================================================

    # Obtener horario del sistema
    hora_local_sistema = datetime.now()

    # Comparar ambos horarios
    if hora_local_sistema.strftime("%H:%M") == hora_internet.strftime("%H:%M"):
        # Desactivar verificacion de horario al entrar
        verify_time = False

        # Guardar el valor de la variable en configs.json
        configs["verify_time"] = verify_time
        save(filepath_configs, configs)

        # Imprimir en consola en modo dev
        if debug:
            print("")
            texto("EXITO: Se verificó el horario del sistema correctamente.", "brgreen", 2)
            print("")
        
        # Vaciar consola
        clear()
    else:
        clear()
        texto("Advertencia: El horario de su sistema no coincide con el horario de internet de su zona horaria actual.", "red", 2)
        print("")
        texto(f"Horario en internet de su zona horaria ({zona_local}): {hora_internet.strftime("%H:%M")}", "white", 2)
        texto(f"Horario de su sistema: {hora_local_sistema.strftime("%H:%M")}", "white", 2)
        print("")
        texto("PRO TIP: Ajuste el reloj de su sistema correctamente en configuración y vuelva a ejecutar el script. ツ", "brgreen", 2)
        inp_texto("Presiona ENTER para salir", "white", 2)
        return exit()
'''

if __name__ == "__main__":
    pass
