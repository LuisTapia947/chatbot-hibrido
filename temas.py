# chatbot/temas.py

# =========================================================

# MODULO DE TEMAS

# chatbot/temas.py

# =========================================================

import random

from chatbot.conocimiento import (
limpiar_texto
)

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

# DETECTAR TEMA

# =========================================================

def detectar_tema(texto,temas):


 texto = limpiar_texto(texto)

 puntuaciones = {}

 for tema, lista_preguntas in temas.items():

    puntuacion = 0

    for pregunta in lista_preguntas:

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

# =====================================================
# EVITAR DETECCIONES VACÍAS
# =====================================================

 if puntuaciones[tema_detectado] == 0:

    return "programacion"

 return tema_detectado


# =========================================================

# OBTENER SUGERENCIAS

# =========================================================

def obtener_sugerencias(
tema,
temas,
usadas=None,
cantidad=6
):


 if usadas is None:

    usadas = []

 disponibles = [

    pregunta

    for pregunta in temas.get(tema, [])

    if pregunta not in usadas
]

# =====================================================
# REINICIAR SI YA SE USARON TODAS
# =====================================================

 if len(disponibles) < cantidad:

    usadas.clear()

    disponibles = temas.get(
        tema,
        []
    )

 if not disponibles:

    return []

 return random.sample(
    disponibles,
    min(cantidad, len(disponibles))
)

