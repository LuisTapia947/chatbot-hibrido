# =========================================================
# HISTORIAL DE CHATS
# historial.py
# =========================================================

import os
import json

from datetime import datetime

# =========================================================
# CARPETA
# =========================================================

CARPETA_HISTORIAL = "historial"

os.makedirs(
    CARPETA_HISTORIAL,
    exist_ok=True
)

# =========================================================
# GUARDAR CHAT
# =========================================================

def guardar_chat(chat):

    fecha = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    archivo = os.path.join(
        CARPETA_HISTORIAL,
        f"chat_{fecha}.json"
    )

    datos = {
        "fecha": fecha,
        "mensajes": chat
    }

    with open(
        archivo,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            datos,
            f,
            ensure_ascii=False,
            indent=4
        )

    return archivo

# =========================================================
# LISTAR HISTORIALES
# =========================================================

def obtener_historiales():

    archivos = [

        archivo

        for archivo in os.listdir(
            CARPETA_HISTORIAL
        )

        if archivo.endswith(".json")
    ]

    archivos.sort(reverse=True)

    return archivos

# =========================================================
# CARGAR HISTORIAL
# =========================================================

def cargar_historial(nombre_archivo):

    archivo = os.path.join(
        CARPETA_HISTORIAL,
        nombre_archivo
    )

    if not os.path.exists(archivo):

        return []

    with open(
        archivo,
        "r",
        encoding="utf-8"
    ) as f:

        datos = json.load(f)

    return datos.get(
        "mensajes",
        []
    )

# =========================================================
# OBTENER INFO DEL HISTORIAL
# =========================================================

def obtener_info_historial(nombre_archivo):

    archivo = os.path.join(
        CARPETA_HISTORIAL,
        nombre_archivo
    )

    try:

        with open(
            archivo,
            "r",
            encoding="utf-8"
        ) as f:

            datos = json.load(f)

        mensajes = datos.get(
            "mensajes",
            []
        )

        total = len(mensajes)

        fecha = datos.get(
            "fecha",
            "Sin fecha"
        )

        return {
            "fecha": fecha,
            "total": total
        }

    except:

        return {
            "fecha": "Error",
            "total": 0
        }

# =========================================================
# ELIMINAR HISTORIAL
# =========================================================

def eliminar_historial(nombre_archivo):

    archivo = os.path.join(
        CARPETA_HISTORIAL,
        nombre_archivo
    )

    if os.path.exists(archivo):

        os.remove(archivo)

# =========================================================
# LIMPIAR TODO
# =========================================================

def limpiar_historiales():

    archivos = obtener_historiales()

    for archivo in archivos:

        eliminar_historial(
            archivo
        )
