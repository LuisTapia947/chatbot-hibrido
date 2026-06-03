# =========================================================
# MODULO DE RESPUESTAS
# chatbot/respuestas.py
# =========================================================

from datetime import datetime
import random

# =========================================================
# FRASES DE INTRODUCCIÓN
# =========================================================

INTRODUCCIONES = [

    "Encontré información relacionada con tu consulta.",

    "Esta es la explicación más adecuada para tu pregunta.",

    "Analicé tu pregunta y encontré la siguiente respuesta.",

    "Puedo ayudarte con esta información.",

    "Aquí tienes una explicación clara sobre el tema."
]

# =========================================================
# FRASES DE CONTINUACIÓN
# =========================================================

CONTINUAR = [

    "¿Deseas realizar otra consulta?",

    "Puedes seguir preguntando si lo necesitas.",

    "Estoy disponible para ayudarte nuevamente.",

    "Si tienes otra duda, puedes escribirla.",

    "Puedo ayudarte con más preguntas si deseas."
]

# =========================================================
# RESPUESTAS ESPECIALES
# =========================================================

def respuesta_especial(texto):

    texto = texto.lower().strip()

    # =====================================================
    # HORA
    # =====================================================

    if (
        "hora" in texto
        or "qué hora es" in texto
        or "que hora es" in texto
    ):

        hora_actual = datetime.now().strftime(
            "%H:%M"
        )

        return (
            "🕒 La hora actual es "
            f"**{hora_actual}**."
        )

    # =====================================================
    # FECHA
    # =====================================================

    if (
        "fecha" in texto
        or "qué fecha es" in texto
        or "que fecha es" in texto
    ):

        fecha_actual = datetime.now().strftime(
            "%d/%m/%Y"
        )

        return (
            "📅 La fecha actual es "
            f"**{fecha_actual}**."
        )

    # =====================================================
    # IDENTIDAD
    # =====================================================

    if (
        "quien eres" in texto
        or "qué eres" in texto
        or "que eres" in texto
    ):

        return (
            "🤖 Soy un chatbot híbrido educativo "
            "desarrollado con Python y Streamlit. "
            "Puedo responder preguntas de conocimiento "
            "y resolver operaciones matemáticas."
        )

    # =====================================================
    # ESTADO
    # =====================================================

    if (
        "como estas" in texto
        or "cómo estás" in texto
    ):

        return (
            "✅ Estoy funcionando correctamente "
            "y preparado para ayudarte."
        )

    # =====================================================
    # FUNCIONES
    # =====================================================

    if (
        "que puedes hacer" in texto
        or "qué puedes hacer" in texto
    ):

        return (
            "📚 Puedo ayudarte con preguntas "
            "sobre programación, redes, hardware, "
            "inteligencia artificial y ciberseguridad. "
            "También puedo resolver operaciones matemáticas."
        )

    # =====================================================
    # SALUDO
    # =====================================================

    saludos = [
        "hola",
        "buenas",
        "buenos dias",
        "buenas tardes",
        "buenas noches"
    ]

    if texto in saludos:

        return (
            "👋 Hola, bienvenido al chatbot híbrido educativo. "
            "Puedes hacer preguntas de conocimiento "
            "o escribir operaciones matemáticas."
        )

    return None

# =========================================================
# MENSAJE DE DESPEDIDA
# =========================================================

def mensaje_despedida():

    return """

### 👋 Sesión finalizada

El chatbot híbrido educativo cerró la conversación correctamente.

Gracias por utilizar el sistema inteligente de consultas educativas y matemáticas.

Puedes reiniciar la conversación desde el panel lateral si deseas volver a comenzar.

"""

# =========================================================
# GENERAR RESPUESTA NORMAL
# =========================================================

def construir_respuesta(
    respuesta,
    similitud=1.0
):

    texto = (
        random.choice(
            INTRODUCCIONES
        )
        + "\n\n"
        + respuesta
        + "\n\n"
        + random.choice(
            CONTINUAR
        )
    )

    # =====================================================
    # COINCIDENCIA APROXIMADA
    # =====================================================

    if similitud < 1:

        texto += (
            "\n\n"
            f"🔎 Coincidencia aproximada: "
            f"{similitud*100:.0f}%"
        )

    return texto

# =========================================================
# MENSAJE SIN RESPUESTA
# =========================================================

def mensaje_sin_respuesta():

    mensajes = [

        "No encontré información suficiente para responder esa consulta.",

        "No tengo información exacta sobre ese tema todavía.",

        "La pregunta no coincide con mi base de conocimiento actual.",

        "Intenta formular la pregunta de otra manera."
    ]

    return random.choice(
        mensajes
    )

# =========================================================
# VALIDAR COMANDO SALIR
# =========================================================

def es_comando_salida(texto):

    texto = texto.lower().strip()

    comandos = [

        "salir",
        "cerrar",
        "quiero salir",
        "finalizar",
        "terminar chat",
        "cerrar chat"
    ]

    return texto in comandos