# =========================================================
# MODULO DE CONOCIMIENTO MEJORADO
# chatbot/conocimiento.py
# =========================================================

import os
import re
from difflib import get_close_matches

# =========================================================
# TEMAS DISPONIBLES
# =========================================================

TEMAS_DISPONIBLES = [
    "programacion",
    "ia",
    "redes",
    "hardware",
    "ciberseguridad"
]

# =========================================================
# LIMPIAR TEXTO
# =========================================================

def limpiar_texto(texto):

    texto = texto.lower().strip()

    # eliminar espacios dobles
    texto = re.sub(r"\s+", " ", texto)

    # eliminar símbolos innecesarios
    texto = re.sub(
        r"[¿?¡!.,;:]",
        "",
        texto
    )

    return texto

# =========================================================
# CARGAR CONOCIMIENTO
# =========================================================

def cargar_conocimiento():

    memoria = {}

    temas = {
        tema: []
        for tema in TEMAS_DISPONIBLES
    }

    errores = []

    # =====================================================
    # RUTA BASE
    # =====================================================

    carpeta_base = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    carpeta_data = os.path.join(
        carpeta_base,
        "data"
    )

    # =====================================================
    # VALIDAR CARPETA
    # =====================================================

    if not os.path.exists(carpeta_data):

        errores.append(
            "La carpeta data no existe."
        )

        return memoria, [], temas, errores

    # =====================================================
    # RECORRER ARCHIVOS
    # =====================================================

    for tema in TEMAS_DISPONIBLES:

        archivo = f"{tema}.txt"

        ruta = os.path.join(
            carpeta_data,
            archivo
        )

        # =================================================
        # VALIDAR ARCHIVO
        # =================================================

        if not os.path.exists(ruta):

            errores.append(
                f"No se encontró el archivo: {archivo}"
            )

            continue

        try:

            with open(
                ruta,
                "r",
                encoding="utf-8"
            ) as f:

                lineas = f.readlines()

            # =============================================
            # PROCESAR LÍNEAS
            # =============================================

            for numero, linea in enumerate(
                lineas,
                start=1
            ):

                linea = linea.strip()

                # ignorar líneas vacías
                if not linea:

                    continue

                # =========================================
                # FORMATO:
                # p:pregunta?r:respuesta
                # =========================================

                if "?r:" not in linea:

                    errores.append(
                        f"{archivo} "
                        f"(línea {numero}): "
                        f"Formato inválido."
                    )

                    continue

                try:

                    pregunta, respuesta = (
                        linea.split("?r:", 1)
                    )

                    pregunta = (
                        pregunta
                        .replace("p:", "")
                        .strip()
                    )

                    respuesta = (
                        respuesta.strip()
                    )

                    pregunta_limpia = (
                        limpiar_texto(
                            pregunta
                        )
                    )

                    # =====================================
                    # VALIDAR DATOS
                    # =====================================

                    if not pregunta_limpia:

                        errores.append(
                            f"{archivo} "
                            f"(línea {numero}): "
                            f"Pregunta vacía."
                        )

                        continue

                    if not respuesta:

                        errores.append(
                            f"{archivo} "
                            f"(línea {numero}): "
                            f"Respuesta vacía."
                        )

                        continue

                    # =====================================
                    # EVITAR DUPLICADOS
                    # =====================================

                    if pregunta_limpia in memoria:

                        errores.append(
                            f"{archivo} "
                            f"(línea {numero}): "
                            f"Pregunta duplicada."
                        )

                        continue

                    # =====================================
                    # GUARDAR
                    # =====================================

                    memoria[pregunta_limpia] = (
                        respuesta
                    )

                    temas[tema].append(
                        pregunta_limpia
                    )

                except Exception as e:

                    errores.append(
                        f"{archivo} "
                        f"(línea {numero}): {e}"
                    )

        except Exception as e:

            errores.append(
                f"Error cargando "
                f"{archivo}: {e}"
            )

    preguntas = list(
        memoria.keys()
    )

    return (
        memoria,
        preguntas,
        temas,
        errores
    )

# =========================================================
# ESTADISTICAS
# =========================================================

def obtener_estadisticas(
    memoria,
    temas
):

    estadisticas = {
        "total": len(memoria)
    }

    for tema in TEMAS_DISPONIBLES:

        estadisticas[tema] = len(
            temas.get(tema, [])
        )

    return estadisticas

# =========================================================
# CALCULAR SIMILITUD
# =========================================================

def calcular_similitud(
    texto1,
    texto2
):

    palabras1 = set(
        limpiar_texto(texto1).split()
    )

    palabras2 = set(
        limpiar_texto(texto2).split()
    )

    if not palabras1 or not palabras2:

        return 0

    coincidencias = (
        palabras1 & palabras2
    )

    return len(coincidencias) / max(
        len(palabras1),
        len(palabras2)
    )

# =========================================================
# BUSCAR RESPUESTA
# =========================================================

def buscar_respuesta(
    pregunta_usuario,
    memoria,
    preguntas,
    cutoff=0.55
):

    pregunta_usuario = limpiar_texto(
        pregunta_usuario
    )

    # =====================================================
    # COINCIDENCIA EXACTA
    # =====================================================

    if pregunta_usuario in memoria:

        return {
            "respuesta":
            memoria[pregunta_usuario],

            "score":
            1.0,

            "tipo":
            "exacta",

            "pregunta":
            pregunta_usuario
        }

    # =====================================================
    # COINCIDENCIA APROXIMADA
    # =====================================================

    coincidencias = get_close_matches(
        pregunta_usuario,
        preguntas,
        n=3,
        cutoff=cutoff
    )

    if coincidencias:

        mejor = coincidencias[0]

        similitud = calcular_similitud(
            pregunta_usuario,
            mejor
        )

        return {
            "respuesta":
            memoria[mejor],

            "score":
            similitud,

            "tipo":
            "aproximada",

            "pregunta":
            mejor
        }

    # =====================================================
    # SIN RESULTADOS
    # =====================================================

    return {
        "respuesta": None,
        "score": 0,
        "tipo": "sin_resultado",
        "pregunta": None
    }

# =========================================================
# DETECTAR TEMA
# =========================================================

def detectar_tema(
    texto,
    temas
):

    texto = limpiar_texto(texto)

    puntuaciones = {}

    for tema, preguntas in temas.items():

        puntuacion = 0

        for pregunta in preguntas:

            similitud = calcular_similitud(
                texto,
                pregunta
            )

            puntuacion += similitud

        puntuaciones[tema] = puntuacion

    tema_detectado = max(
        puntuaciones,
        key=puntuaciones.get
    )

    # evitar detecciones vacías
    if puntuaciones[tema_detectado] == 0:

        return "programacion"

    return tema_detectado
