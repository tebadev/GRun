import os
from locale import getdefaultlocale, 

# Directorios
directorios = ["/usr/share/applications", "~/.local/share/applications"]

# Comprueba si el directorio existe
def comprobar_dir(directorios):
    directorios_filtrados = []

    for directorio in directorios:
        if os.path.exists(directorio):
            directorios_filtrados.append(directorio)

    return directorios_filtrados

# Comprueba si es un archivo .desktop
def filtrar_desktops(directorios):
    ficheros_filtrados = []

    for directorio in directorios:
        ficheros = os.listdir(directorio)

        for fichero in ficheros:
            if ".desktop" in fichero:
                ruta_completa = os.path.join(directorio, fichero)
                ficheros_filtrados.append(ruta_completa)

    return ficheros_filtrados

def leer_desktops (ficheros):
    contenido_ficheros = {
        "nombre": [],
        "ruta": []
    }

    for fichero in ficheros:
        with open(fichero, "r") as conteniido:
            if "[Desktop Entry]" in conteniido.readline():
                for linea in conteniido:
                    pass

print (getdefaultlocale())


