# =========================================================
# CHATBOT HÍBRIDO EDUCATIVO
# VERSIÓN MEJORADA VISUALMENTE
# =========================================================

import streamlit as st
from difflib import get_close_matches
from datetime import datetime
import random
import os
import re
import math

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Chatbot Híbrido IA",
    page_icon="🤖",
    layout="centered"
)

# =========================================================
# ESTILOS VISUALES
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.main {
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #111827 100%
    );
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 900px;
}

h1 {
    text-align: center;
    color: #38bdf8;
    font-size: 3rem;
    margin-bottom: 10px;
}

.subtitulo {
    text-align: center;
    color: #cbd5e1;
    font-size: 1.1rem;
    margin-bottom: 30px;
}

.chat-user {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
}

.chat-bot {
    background-color: #0f766e;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 15px;
}

div.stTextInput input {
    border-radius: 15px;
    padding: 12px;
    border: 2px solid #334155;
}

div.stButton > button {
    width: 100%;
    border-radius: 15px;
    height: 50px;
    font-size: 16px;
    font-weight: bold;
    background-color: #0ea5e9;
    color: white;
    border: none;
}

div.stButton > button:hover {
    background-color: #0284c7;
}

.sidebar .sidebar-content {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO
# =========================================================

st.markdown("""
<h1>🤖 Chatbot Híbrido Educativo</h1>
<p class="subtitulo">
Sistema inteligente de preguntas educativas y resolución matemática avanzada
</p>
""", unsafe_allow_html=True)

# =========================================================
# MEMORIA
# =========================================================

memoria = {}

# =========================================================
# CARGAR BASES DE CONOCIMIENTO
# =========================================================

archivos = [
    "programacion.txt",
    "ia.txt",
    "redes.txt",
    "hardware.txt",
    "ciberseguridad.txt"
]

errores = []

carpeta_actual = os.path.dirname(
    os.path.abspath(__file__)
)

for archivo in archivos:

    ruta = os.path.join(
        carpeta_actual,
        archivo
    )

    try:

        with open(
            ruta,
            "r",
            encoding="utf-8"
        ) as f:

            contenido = f.read().strip()

        lineas = contenido.split("\n")

        for linea in lineas:

            if "?r:" in linea:

                pregunta, respuesta = linea.split("?r:")

                pregunta = pregunta.replace(
                    "p:",
                    ""
                ).strip().lower()

                respuesta = respuesta.strip()

                if pregunta and respuesta:

                    memoria[pregunta] = respuesta

    except Exception as e:

        errores.append(
            f"{archivo}: {e}"
        )

preguntas = list(memoria.keys())

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📚 Información")

    st.success(
        f"Preguntas cargadas: {len(preguntas)}"
    )

    st.markdown("---")

    st.subheader("🧠 Áreas disponibles")

    st.write("💻 Programación")
    st.write("🤖 Inteligencia Artificial")
    st.write("🌐 Redes")
    st.write("🖥️ Hardware")
    st.write("🔐 Ciberseguridad")

    st.markdown("---")

    st.info(
        "También puedes resolver operaciones matemáticas avanzadas."
    )

    if st.button("🗑️ Reiniciar conversación"):

        st.session_state.chat = []

        st.rerun()

# =========================================================
# FRASES NATURALES
# =========================================================

introducciones = [
    "Encontré información relacionada con tu consulta.",
    "Esta es la explicación más adecuada para tu pregunta.",
    "Puedo ayudarte con la siguiente información.",
    "Analicé tu pregunta y encontré esta respuesta."
]

continuar = [
    "¿Te gustaría realizar otra consulta?",
    "Estoy disponible para ayudarte nuevamente.",
    "Puedes seguir preguntando si lo deseas."
]

# =========================================================
# RESPUESTAS ESPECIALES
# =========================================================

def respuesta_especial(texto):

    texto = texto.lower()

    if "hora" in texto:

        return (
            f"La hora actual es "
            f"{datetime.now().strftime('%H:%M')}."
        )

    if "fecha" in texto:

        return (
            f"La fecha actual es "
            f"{datetime.now().strftime('%d/%m/%Y')}."
        )

    if "quien eres" in texto:

        return (
            "Soy un chatbot híbrido educativo "
            "desarrollado en Python y Streamlit."
        )

    if "como estas" in texto:

        return (
            "Estoy funcionando correctamente "
            "y preparado para ayudarte."
        )

    if "que puedes hacer" in texto:

        return (
            "Puedo responder preguntas educativas "
            "y resolver operaciones matemáticas avanzadas."
        )

    return None

# =========================================================
# EXTRAER OPERACIÓN
# =========================================================

def extraer_operacion(texto):

    texto = texto.lower()

    palabras = [
        "cuanto es",
        "calcula",
        "resuelve",
        "resultado de"
    ]

    for p in palabras:

        texto = texto.replace(p, "")

    return texto.strip()

# =========================================================
# DETECTAR OPERACIÓN
# =========================================================

def es_operacion_matematica(texto):

    expr = extraer_operacion(texto)

    patron = r'^[0-9\+\-\*\/\.\(\)\,\^\%\ ]+[a-zA-Z]*.*$'

    return bool(
        re.match(patron, expr)
    )

# =========================================================
# CONVERTIR EXPRESIÓN
# =========================================================

def convertir_expresion(expr):

    expr = expr.replace("^", "**")

    reemplazos = {
        "raiz(": "math.sqrt(",
        "sqrt(": "math.sqrt(",
        "log(": "math.log10(",
        "ln(": "math.log(",
        "sen(": "math.sin(math.radians(",
        "sin(": "math.sin(math.radians(",
        "cos(": "math.cos(math.radians(",
        "tan(": "math.tan(math.radians(",
        "factorial(": "math.factorial("
    }

    for k, v in reemplazos.items():

        expr = expr.replace(k, v)

    expr = expr.replace(
        "pi",
        str(math.pi)
    )

    expr = expr.replace(
        "e",
        str(math.e)
    )

    return expr

# =========================================================
# EXPLICACIÓN MATEMÁTICA
# =========================================================

def explicar_operacion(expresion):

    try:

        original = extraer_operacion(
            expresion
        )

        expr = convertir_expresion(
            original
        )

        if "math.sin(math.radians(" in expr:
            expr += "))"

        if "math.cos(math.radians(" in expr:
            expr += "))"

        if "math.tan(math.radians(" in expr:
            expr += "))"

        resultado = eval(expr)

        explicacion = []

        explicacion.append(
            f"### 🧮 Operación matemática\n\n"
            f"`{original}`"
        )

        explicacion.append(
            "\n### 📖 Procedimiento aplicado"
        )

        if "(" in original:

            explicacion.append(
                "\n• Se resolvieron primero "
                "las operaciones agrupadas "
                "dentro de paréntesis."
            )

        if "^" in original:

            explicacion.append(
                "\n• Se calcularon las potencias "
                "utilizando prioridad matemática."
            )

        if "*" in original or "/" in original:

            explicacion.append(
                "\n• Posteriormente se realizaron "
                "las multiplicaciones y divisiones."
            )

        if "+" in original or "-" in original[1:]:

            explicacion.append(
                "\n• Finalmente se efectuaron "
                "las sumas y restas."
            )

        if "raiz" in original:

            explicacion.append(
                "\n• La expresión contiene "
                "una raíz cuadrada."
            )

        if "log" in original:

            explicacion.append(
                "\n• Se aplicó un logaritmo "
                "base 10."
            )

        if (
            "sen" in original
            or "cos" in original
            or "tan" in original
        ):

            explicacion.append(
                "\n• Se utilizaron funciones "
                "trigonométricas en grados."
            )

        explicacion.append(
            f"\n\n### ✅ Resultado obtenido\n\n"
            f"**{resultado}**"
        )

        return "".join(explicacion)

    except Exception as e:

        return (
            f"❌ Ocurrió un error al "
            f"resolver la operación.\n\n{e}"
        )

# =========================================================
# BUSCAR RESPUESTA
# =========================================================

def buscar_respuesta(
    pregunta_usuario,
    cutoff=0.55
):

    pregunta_usuario = (
        pregunta_usuario.lower().strip()
    )

    if pregunta_usuario in memoria:

        return memoria[pregunta_usuario], 1.0

    coincidencias = get_close_matches(
        pregunta_usuario,
        preguntas,
        n=1,
        cutoff=cutoff
    )

    if coincidencias:

        pregunta = coincidencias[0]

        similitud = len(
            set(pregunta_usuario)
            &
            set(pregunta)
        ) / max(
            len(pregunta_usuario),
            len(pregunta)
        )

        return memoria[pregunta], similitud

    return None, 0

# =========================================================
# SESSION STATE
# =========================================================

if "chat" not in st.session_state:

    st.session_state.chat = []

# =========================================================
# INPUT
# =========================================================

pregunta = st.text_input(
    "💬 Escribe tu pregunta o una operación matemática:"
)

enviar = st.button("Enviar consulta")

# =========================================================
# PROCESAR MENSAJE
# =========================================================

if enviar and pregunta:

    texto = pregunta.lower().strip()

    st.session_state.chat.append(
        ("usuario", pregunta)
    )

    # SALIR
    if texto in ["salir", "quiero salir"]:

        respuesta_final = (
            "La conversación fue finalizada correctamente."
        )

    # RESPUESTAS ESPECIALES
    elif respuesta_especial(texto):

        respuesta_final = (
            respuesta_especial(texto)
            + "\n\n"
            + random.choice(continuar)
        )

    # MATEMÁTICAS
    elif es_operacion_matematica(texto):

        respuesta_final = explicar_operacion(
            texto
        )

    # RESPUESTAS GENERALES
    else:

        respuesta, score = buscar_respuesta(
            texto
        )

        if respuesta:

            respuesta_final = (
                random.choice(introducciones)
                + "\n\n"
                + respuesta
                + "\n\n"
                + random.choice(continuar)
            )

            if score < 1:

                respuesta_final += (
                    f"\n\n🔎 Coincidencia aproximada: "
                    f"{score*100:.0f}%"
                )

        else:

            respuesta_final = (
                "No encontré información suficiente "
                "para responder esa consulta."
            )

    st.session_state.chat.append(
        ("bot", respuesta_final)
    )

# =========================================================
# MOSTRAR CHAT
# =========================================================

for tipo, mensaje in st.session_state.chat:

    if tipo == "usuario":

        st.markdown(
            f"""
            <div class="chat-user">
            <strong>👤 Tú:</strong><br><br>
            {mensaje}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="chat-bot">
            <strong>🤖 Chatbot:</strong><br><br>
            {mensaje}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# SUGERENCIAS
# =========================================================

st.markdown("---")

st.subheader("💡 Ejemplos de consultas")

ejemplos = [
    "¿Qué es Python?",
    "¿Qué es una red LAN?",
    "¿Qué es inteligencia artificial?",
    "cuanto es raiz(144)",
    "calcula 2^8",
    "sen(90)"
]

for e in ejemplos:

    st.markdown(f"• {e}")

# =========================================================
# ERRORES
# =========================================================

if errores:

    with st.expander(
        "⚠️ Ver errores del sistema"
    ):

        for e in errores:

            st.error(e)

