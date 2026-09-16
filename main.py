import os
import locale
import re

# Directorios de aplicaciones estándar en Linux
DIRECTORIOS = [
    "/usr/share/applications",
    "~/.local/share/applications"
]

def comprobar_directorios(directorios):
    """
    Comprueba qué directorios existen en el sistema.
    Usa expanduser para traducir '~' a la ruta del usuario (/home/usuario) para que pueda encontrar la carpeta 
    """
    directorios_validos = []
    for directorio in directorios:
        ruta_expandida = os.path.expanduser(directorio)
        if os.path.exists(ruta_expandida):
            directorios_validos.append(ruta_expandida)
    return directorios_validos

def filtrar_desktops(directorios):
    """
    Busca y devuelve las rutas completas de todos los archivos que
    terminan en '.desktop' usamos el endswith porque puede que haya backup o archivos desktop.old o quien sabe  pero es mejor filtar lo que buscas para evitar un proceso largo y hacerlo eficiente como mencionas
    """
    ficheros_desktop = []
    for directorio in directorios:
        for nombre_fichero in os.listdir(directorio):
            if nombre_fichero.endswith(".desktop"):
                ruta_completa = os.path.join(directorio, nombre_fichero)
                ficheros_desktop.append(ruta_completa)
    return ficheros_desktop

def leer_desktops(ficheros):

    # Detecta el idioma del sistema (ej: 'es_ES') y el idioma base (ej: 'es')
    idioma_actual, _ = locale.getlocale()
    idioma_default = idioma_actual.split("_")[0] if idioma_actual else "en"
    
    aplicaciones = []

    for ruta_fichero in ficheros:
        try:
            with open(ruta_fichero, "r", encoding="utf-8", errors="replace") as archivo:
                lineas = archivo.readlines()
        except OSError:
            continue

        en_seccion_desktop = False
        nombre_defecto = None
        nombre_idioma_exacto = None
        nombre_idioma_default = None
        comando_ejecutar = None
        no_mostrar = False
        oculto = False
        tipo_app = None

        for linea_cruda in lineas:
            linea = linea_cruda.strip()
            #por si hay líneas vacías o comentarios, tampoc tan necesario pero puede que algun .desktop inice con espacio o x cosa 
            if not linea or linea.startswith("#"):
                continue

            # Detectar encabezados de sección [NombreSeccion]
            if linea.startswith("[") and linea.endswith("]"):
                en_seccion_desktop = (linea == "[Desktop Entry]")
                continue

            # Solo nos interesa lo que esté dentro del bloque [Desktop Entry] no es obligatorio puede ser que no existan en tu caso si existen por eso te lo digo  y por eso te decia que no es obligatorio que tengan todos  en fin
            if not en_seccion_desktop or "=" not in linea:
                continue

            clave, valor = linea.split("=", 1)
            clave = clave.strip()
            valor = valor.strip()

            # Extraer las propiedades clave
            if clave == "Type":
                tipo_app = valor
            elif clave == "NoDisplay" and valor.lower() == "true":
                no_mostrar = True
            elif clave == "Hidden" and valor.lower() == "true":
                oculto = True
            elif clave == "Exec":
                # Limpia argumentos de Linux como %u, %f, %U, %F usando regex por eos import re arriba
                comando_ejecutar = re.sub(r"%[a-zA-Z]", "", valor).strip()
            elif clave == "Name":
                nombre_defecto = valor
            elif idioma_actual and clave == f"Name[{idioma_actual}]":
                nombre_idioma_exacto = valor
            elif clave == f"Name[{idioma_default}]":
                nombre_idioma_default = valor

        # Descartar si está oculta, si no es una Aplicación o si no tiene comando Exec
        if no_mostrar or oculto or tipo_app != "Application" or not comando_ejecutar:
            continue

        # Prioridad de idioma:
        # 1º Nombre exacto (ej: Name[es_ES])
        # 2º Nombre base (ej: Name[es]) lo que te decia de dividir aqui en dadao cas que no existe con el de arriba nos regresa este para usarlo ya que es español igual
        # 3º Nombre por defecto (Name en inglés) ya si de plano no existe nada en español sale le idoma abse EN o en
        nombre_final = nombre_idioma_exacto or nombre_idioma_default or nombre_defecto

        if nombre_final:
            aplicaciones.append({
                "nombre": nombre_final,
                "comando": comando_ejecutar,
                "ruta": ruta_fichero
            })

    # Ordenar las aplicaciones alfabéticamente por su nombre asi se ev mas bonito pero si no lo puedes quuitar, obvio esto es una demo 
    aplicaciones.sort(key=lambda app: app["nombre"].lower())
    return aplicaciones

if __name__ == "__main__":
    # 1. Filtrar directorios que existen
    dirs_validos = comprobar_directorios(DIRECTORIOS)

    # 2. Obtener lista de archivos .desktop osea los que nos interessan que son los de aplicacion la extension es .desktop por eso se llama asi por si no lo sabias 
    archivos_desktop = filtrar_desktops(dirs_validos)

    # 3. Leer y procesar las aplicaciones por eso se llama leer desktops  y obtener el idioma del sistema con locale.getlocale()  la funcionlocale esta arriba 
    lista_apps = leer_desktops(archivos_desktop)

    # 4. Mostrar información en consola por el momento se imprime todo en este caso 20 , cambia el 20 por otro numero si quieres ver mas o hasta el final usando len(lista_apps) osea todas las app si quieres 
    # Pero no recomiedo que le meuvas al 20 ya que te daria toda la lista de app y son muchas  pero como te digo esta demo es solo para mostrarte como funciona y no se crashee
    idioma, _ = locale.getlocale()
    print(f"Idioma del sistema: {idioma}")
    print(f"Total de aplicaciones encontradas: {len(lista_apps)}\n")
    print(f"Muestra de las primeras {len(lista_apps[:20])} aplicaciones:")
    print("-" * 60)
    for app in lista_apps[:20]:
        print(f"Nombre:   {app['nombre']}")
        print(f"Comando:  {app['comando']}")
        print(f"Archivo:  {app['ruta']}")
        print("-" * 20)
