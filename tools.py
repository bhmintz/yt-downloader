#import requests, datetime, data
import data, subprocess
from rich.console import Console
#from rich.layout import Layout
#from rich.panel import Panel
from rich.prompt import Prompt
from colorama import Fore, Style
#from datetime import datetime, timedelta
#from zoneinfo import ZoneInfo

version = "0.1.0"

# Detecta el sistema y guarda el valor correcto para vaciar consola según el sistema corriendo
debug, debug_c = False, "clear" if data.os.name == "posix" else "cls",

# Variable de verificacion de tiempo
verify_time = False

def clear():
    if debug == False:
        data.os.system(debug_c)

def color(color_value, module=1):
    if module == 1:
        match color_value:
            case "green": color_value = Fore.GREEN
            case "red": color_value = Fore.RED
            case "blue": color_value = Fore.BLUE
            case "yellow": color_value = Fore.YELLOW
            case "cyan": color_value = Fore.CYAN
            case "magenta": color_value = Fore.MAGENTA
            case "black": color_value = Fore.BLACK
            case "white": color_value = Fore.WHITE
            case "lgreen": color_value = Fore.LIGHTGREEN_EX
            case "lred": color_value = Fore.LIGHTRED_EX
            case "lblue": color_value = Fore.LIGHTBLUE_EX
            case "lyellow": color_value = Fore.LIGHTYELLOW_EX
            case "lcyan": color_value = Fore.LIGHTCYAN_EX
            case "lmagenta": color_value = Fore.LIGHTMAGENTA_EX
            case "lblack": color_value = Fore.LIGHTBLACK_EX
            case "lwhite": color_value = Fore.LIGHTWHITE_EX
            case None: color_value = Fore.GREEN
    else:
        match color_value:
            # Basics
            case "green": color_value = "#008000"
            case "red": color_value = "#FF0000"
            case "blue": color_value = "#0000FF"
            case "yellow": color_value = "#FFFF00"
            case "orange": color_value = "#FFA500"
            case "cyan": color_value = "#00FFFF"
            case "magenta": color_value = "#FF00FF"
            case "pink": color_value = "#FFC0CB"
            case "black": color_value = "#000000"
            case "white": color_value = "#FFFFFF"

            # Light
            case "lgreen": color_value = "#90EE90"
            case "lred": color_value = "#FF474C"
            case "lblue": color_value = "#ADD8E6"
            case "lyellow": color_value = "#FFFAA0"
            case "lorange": color_value = "#FFD580"
            case "lcyan": color_value = "#00FFF0"
            case "lmagenta": color_value = "#FF80FF"
            case "lpink": color_value = "#FFB6C1"
            case "lblack": color_value = "#454545"
            case "lwhite": color_value = "#FFFFF7"

            # Bright
            case "brgreen": color_value = "#AAFF00"
            case "brred": color_value = "#EE4B2B"
            case "brblue": color_value = "#0096FF"
            case "bryellow": color_value = "#CFFF04"
            case "brorange": color_value = "#FF5C00"
            case "brcyan": color_value = "#0AFFFF"
            case "brmagenta": color_value = "#FF08E8"
            case "brpink": color_value = "#FF007F"
            case "brblack": color_value = "#222024"
            case "lwhite": color_value = "#FFFFFF"

            case None: color_value = "#008000"
    return color_value

def texto(texto, color_value, module=1, style=""):
    if module == 1:
            clear_color = Style.RESET_ALL
            colorr = color(color_value)
            print(colorr + texto + clear_color)
    else:
        colorr = color(color_value, 2)
        Console().print(f"[{style}{colorr}]{texto}[/{style}{colorr}]")

def inp_texto(texto, color_value, module=1, style=""):
    colorr = color(color_value, module)
    if module == 1:
        clear_color = Style.RESET_ALL
        input_value = input(colorr + texto + clear_color)
    else:
        input_value = Prompt.ask(f"[{style}{colorr}]{texto}[/{style}{colorr}]")
    return input_value

def comprobacion(texto, colorr, module=1, style=""):
    confirm = inp_texto(texto, colorr, module, style)
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
