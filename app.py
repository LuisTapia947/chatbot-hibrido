# =========================================================
# CHATBOT HÍBRIDO EDUCATIVO AVANZADO
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
    layout="wide"
)

# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

h1, h2, h3 {
    color: #38bdf8;
}

.stChatMessage {
    border-radius: 15px;
    padding: 10px;
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
}

textarea {
    border-radius: 12px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO
# =========================================================

st.title("🤖 Chatbot Híbrido Educativo")

st.markdown("""
### Funciones del sistema

✅ Respuestas educativas  
✅ Búsqueda inteligente  
✅ Coincidencias aproximadas  
✅ Matemática avanzada  
✅ Explicación de resultados  
✅ Funciones científicas  
✅ Sugerencias automáticas  
""")

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

    st.header("📚 Información")

    st.success(
        f"Preguntas cargadas: {len(preguntas)}"
    )

    st.markdown("---")

    st.subheader("📖 Temáticas")

    st.write("💻 Programación")
    st.write("🧠 Inteligencia Artificial")
    st.write("🌐 Redes")
    st.write("🖥️ Hardware")
    st.write("🔐 Ciberseguridad")

    st.markdown("---")

    if st.button("🗑️ Limpiar conversación"):

        st.session_state.chat = []

        st.session_state.cerrado = False

        st.rerun()

# =========================================================
# FRASES NATURALES
# =========================================================

introducciones = [
    "Excelente pregunta.",
    "Claro, aquí tienes la información.",
    "Con gusto responderé tu consulta.",
    "Estoy procesando tu pregunta.",
    "Encontré información relevante."
]

continuar = [
    "¿Deseas preguntar algo más?",
    "¿Puedo ayudarte nuevamente?",
    "¿Tienes otra consulta?"
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
            "y listo para ayudarte."
        )

    if "que puedes hacer" in texto:

        return (
            "Puedo responder preguntas educativas "
            "y resolver operaciones matemáticas."
        )

    return None

# =========================================================
# MATEMÁTICAS
# =========================================================

def extraer_operacion(texto):

    texto = texto.lower()

    reemplazos = [
        "cuanto es",
        "calcula",
        "resuelve",
        "resultado de"
    ]

    for r in reemplazos:

        texto = texto.replace(r, "")

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

    expr = expr.replace(
        "raiz(",
        "math.sqrt("
    )

    expr = expr.replace(
        "sqrt(",
        "math.sqrt("
    )

    expr = expr.replace(
        "log(",
        "math.log10("
    )

    expr = expr.replace(
        "ln(",
        "math.log("
    )

    expr = expr.replace(
        "sen(",
        "math.sin(math.radians("
    )

    expr = expr.replace(
        "sin(",
        "math.sin(math.radians("
    )

    expr = expr.replace(
        "cos(",
        "math.cos(math.radians("
    )

    expr = expr.replace(
        "tan(",
        "math.tan(math.radians("
    )

    expr = expr.replace(
        "factorial(",
        "math.factorial("
    )

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
# EXPLICAR OPERACIÓN
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

        pasos = []

        pasos.append(
            f"📌 Operación:\n\n{original}"
        )

        pasos.append(
            "\n📖 Desarrollo:"
        )

        if "(" in original:

            pasos.append(
                "\n• Primero se resolvieron "
                "las operaciones dentro "
                "de los paréntesis."
            )

        if "^" in original:

            pasos.append(
                "\n• Se calcularon las potencias."
            )

        if (
            "*" in original
            or "/" in original
        ):

            pasos.append(
                "\n• Luego se realizaron "
                "las multiplicaciones y divisiones."
            )

        if (
            "+" in original
            or "-" in original[1:]
        ):

            pasos.append(
                "\n• Finalmente se resolvieron "
                "las sumas y restas."
            )

        if "raiz" in original:

            pasos.append(
                "\n• Se identificó una raíz cuadrada."
            )

        if "log" in original:

            pasos.append(
                "\n• Se identificó un logaritmo."
            )

        if (
            "sen" in original
            or "cos" in original
            or "tan" in original
        ):

            pasos.append(
                "\n• Se utilizaron funciones trigonométricas."
            )

        pasos.append(
            f"\n\n🧮 Resultado:\n\n{resultado}"
        )

        pasos.append(
            "\n✅ La operación fue resuelta correctamente."
        )

        return "".join(pasos)

    except Exception as e:

        return (
            f"❌ Error matemático:\n\n{e}"
        )

# =========================================================
# RESOLVER OPERACIÓN
# =========================================================

def resolver_operacion(expresion):

    return explicar_operacion(
        expresion
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

if "cerrado" not in st.session_state:

    st.session_state.cerrado = False

if "input_usuario" not in st.session_state:

    st.session_state.input_usuario = ""

# =========================================================
# CERRAR CHAT
# =========================================================

if st.session_state.cerrado:

    st.warning(
        "El chatbot fue cerrado correctamente."
    )

    st.stop()

# =========================================================
# BOTONES MATEMÁTICOS
# =========================================================

st.markdown("## 🧮 Herramientas Matemáticas")

fila1 = st.columns(6)

if fila1[0].button("√"):
    st.session_state.input_usuario += "raiz("

if fila1[1].button("^"):
    st.session_state.input_usuario += "^"

if fila1[2].button("π"):
    st.session_state.input_usuario += "pi"

if fila1[3].button("log"):
    st.session_state.input_usuario += "log("

if fila1[4].button("ln"):
    st.session_state.input_usuario += "ln("

if fila1[5].button("!"):
    st.session_state.input_usuario += "factorial("

fila2 = st.columns(6)

if fila2[0].button("sen"):
    st.session_state.input_usuario += "sen("

if fila2[1].button("cos"):
    st.session_state.input_usuario += "cos("

if fila2[2].button("tan"):
    st.session_state.input_usuario += "tan("

if fila2[3].button("("):
    st.session_state.input_usuario += "("

if fila2[4].button(")"):
    st.session_state.input_usuario += ")"

if fila2[5].button("%"):
    st.session_state.input_usuario += "/100"

# =========================================================
# INPUT
# =========================================================

pregunta = st.text_input(
    "💬 Escribe tu pregunta:",
    value=st.session_state.input_usuario
)

enviar = st.button("📨 Enviar")

# =========================================================
# PROCESAR MENSAJE
# =========================================================

if enviar and pregunta:

    st.session_state.input_usuario = ""

    texto = pregunta.lower().strip()

    st.session_state.chat.append(
        ("usuario", pregunta)
    )

    # SALIR
    if texto in ["salir", "quiero salir"]:

        respuesta_final = (
            "Hasta luego. "
            "El chatbot se cerrará correctamente."
        )

        st.session_state.chat.append(
            ("bot", respuesta_final)
        )

        st.session_state.cerrado = True

        st.rerun()

    # RESPUESTAS ESPECIALES
    elif respuesta_especial(texto):

        respuesta_final = (
            respuesta_especial(texto)
            + "\n\n"
            + random.choice(continuar)
        )

    # MATEMÁTICAS
    elif es_operacion_matematica(texto):

        respuesta_final = resolver_operacion(
            texto
        )

    # PREGUNTAS NORMALES
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
                "No encontré información suficiente. "
                "Intenta formular la pregunta de otra manera."
            )

    st.session_state.chat.append(
        ("bot", respuesta_final)
    )

# =========================================================
# MOSTRAR CHAT
# =========================================================

for tipo, mensaje in st.session_state.chat:

    if tipo == "usuario":

        with st.chat_message("user"):

            st.markdown(mensaje)

    else:

        with st.chat_message("assistant"):

            st.markdown(mensaje)

# =========================================================
# PREGUNTAS SUGERIDAS
# =========================================================

st.markdown("---")

st.subheader("💡 Preguntas sugeridas")

if "sugerencias" not in st.session_state:

    st.session_state.sugerencias = random.sample(
        preguntas,
        min(8, len(preguntas))
    )

col1, col2 = st.columns(2)

for i, pregunta_sugerida in enumerate(
    st.session_state.sugerencias
):

    col = col1 if i % 2 == 0 else col2

    if col.button(
        pregunta_sugerida,
        key=f"sug_{i}"
    ):

        st.session_state.input_usuario = (
            pregunta_sugerida
        )

        st.rerun()

# =========================================================
# ERRORES
# =========================================================

if errores:

    with st.expander(
        "⚠️ Ver errores del sistema"
    ):

        for e in errores:

            st.error(e)

