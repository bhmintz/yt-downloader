import os, sys
from tools import *

def is_compiled(): return os.path.splitext(sys.argv[0])[1].lower() == '.exe'

if is_compiled():
    script_directory = os.path.dirname(sys.executable)
else:
    script_directory = os.path.dirname(os.path.abspath(__file__))

# Abre CLI en caso de que no esté abierto
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")

filepath_config =  script_directory + '\\hook_process.ini'

linea1 = "## ARCHIVO DE CONFIGURACION DE PROCESS KILLER ##\n\n"
linea2 = "[process_names]\n"
linea3 = "## Pegar aquí los nombres de los ejecutables de los procesos a cerrar, en caso de que quieras identificar al proceso por nombre. Como se ve en el ejemplo pero sin usar ';'\n"
linea4 = "##\n## Por ejemplo:\n;programa basura 1\n;avast\n;CClibrary.exe\n" + "\n\n\n\n\n\n\n"
linea5 = "[pids]\n"
linea6 = "## Pegar aquí los nombres de los PIDs de los procesos a cerrar, en caso de que quieras identificar al proceso por PIDs. Como se ve en el ejemplo pero sin usar ';'\n"
linea7 = "##\n## Por ejemplo:\n;87251\n;76315\n;2376\n" + "\n\n\n\n\n\n\n"
content = linea1 + linea2 + linea3 + linea4 + linea5 + linea6 + linea7

def save_file():
    with open(filepath_config, 'w', encoding='utf-8') as buffer:
        buffer.write(content)

def load_file():
    secciones = {}
    seccion_actual = ""

    with open(filepath_config, 'r', encoding='utf-8') as buffer:
        for linea in buffer:
            linea = linea.strip()
            if not linea or linea.startswith(';') or linea.startswith('#'):
                continue  # Ignorar líneas vacías o comentarios
            if linea.startswith('[') and linea.endswith(']'):
                seccion_actual = linea[1:-1].strip()
                secciones[seccion_actual] = []
            else:
                if seccion_actual == "process_names":
                    linea_copy = str(linea)
                    linea_temp = ""
                    for line in linea_copy.splitlines():
                        if line[-4:] == ".exe":
                            # Tiene ".exe" al final de la linea
                            #texto(line + " tiene .exe", "white", 2)
                            linea_temp = linea_temp + line
                        else:
                            # No tiene ".exe" al final de la linea
                            #texto(line + " no tiene .exe", "white", 2)
                            linea_temp = linea_temp + line + '.exe'
                    # Modifica la variable de linea con el .exe agredado a las lineas sin .exe
                    linea = linea_temp

                    secciones[seccion_actual].append(str(linea))

                elif seccion_actual == "pids":
                    secciones[seccion_actual].append(int(linea))

                else:
                    # Líneas antes de la primera sección, opcionalmente ignorar o manejar
                    pass
    return secciones

def sub_main():
    if os.path.exists(filepath_config):
        return load_file()
    else:
        save_file()
        if not os.path.exists(filepath_config):
            texto("ERROR: El programa no tiene permisos de administrador :c", "red", 2)
            inp_texto("Preisone ENTER para continuar", "white", 2)
            return sys.exit()

        content_temp = ""

        while not content_temp == content:
            with open(filepath_config, 'r', encoding='utf-8') as buff:
               content_temp = buff.read()
            texto("Creando archivo de configuración...", "white", 2)
        
        texto("EXITO: Archivo de configuración creado correctamente", "brgreen", 2)
        return load_file()

if __name__ == "__main__":
    pass
