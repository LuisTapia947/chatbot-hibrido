# =========================================================
# CHATBOT HÍBRIDO 
# =========================================================

import streamlit as st
from difflib import get_close_matches
import random
import os
import re
from datetime import datetime

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Chatbot Híbrido IA",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

h1 {
    text-align: center;
    color: #38bdf8;
}

div.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITULO
# =========================================================

st.title("🤖 Chatbot Híbrido Educativo")

st.markdown("""
### Funciones del chatbot

✅ Preguntas de conocimiento  
✅ Coincidencias inteligentes  
✅ Resolución matemática  
✅ Explicación de operaciones  
✅ Sugerencias automáticas  
✅ Respuestas educadas  
""")

# =========================================================
# MEMORIA
# =========================================================

memoria = {}

# =========================================================
# CARGAR ARCHIVOS TXT
# =========================================================

carpeta_actual = os.path.dirname(
    os.path.abspath(__file__)
)

archivos = [
    "programacion.txt",
    "ia.txt",
    "redes.txt",
    "hardware.txt",
    "ciberseguridad.txt"
]

errores = []

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

            txt = f.read().strip()

        lineas = [
            l for l in txt.split("\n")
            if l
        ]

        for l in lineas:

            if "?r:" in l:

                q, r = l.split("?r:")

                pregunta = q.replace(
                    "p:",
                    ""
                ).strip().lower()

                respuesta = r.strip()

                if pregunta and respuesta:

                    memoria[pregunta] = respuesta

    except Exception as e:

        errores.append(
            f"Error cargando {archivo}: {e}"
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
    "Estoy procesando tu pregunta."
]

continuar = [
    "¿Deseas preguntar algo más?",
    "¿Puedo ayudarte nuevamente?",
    "¿Tienes otra consulta?"
]

# =========================================================
# RESPUESTAS ESPECIALES
# =========================================================

def respuesta_especial(q):

    q = q.lower()

    if "hora" in q:

        return (
            f"La hora actual es "
            f"{datetime.now().strftime('%H:%M')}."
        )

    if "fecha" in q:

        return (
            f"La fecha actual es "
            f"{datetime.now().strftime('%d/%m/%Y')}."
        )

    if "quien eres" in q:

        return (
            "Soy un chatbot híbrido educativo "
            "desarrollado en Python y Streamlit."
        )

    if "como estas" in q:

        return (
            "Estoy funcionando correctamente "
            "y listo para ayudarte."
        )

    if "que puedes hacer" in q:

        return (
            "Puedo responder preguntas sobre "
            "programación, inteligencia artificial, "
            "redes, hardware y ciberseguridad."
        )

    return None

# =========================================================
# OPERACIONES MATEMÁTICAS AVANZADAS
# =========================================================

import math

# =========================================================
# EXTRAER OPERACIÓN
# =========================================================

def extraer_operacion(texto):

    texto = texto.lower()

    texto = texto.replace("cuanto es", "")
    texto = texto.replace("calcula", "")
    texto = texto.replace("resuelve", "")
    texto = texto.replace("resultado de", "")

    return texto.strip()

# =========================================================
# DETECTAR OPERACIÓN
# =========================================================

def es_operacion_matematica(texto):

    expresion = extraer_operacion(texto)

    permitidos = (
        "0123456789+-*/().,^ "
        "abcdefghijklmnopqrstuvwxyz"
    )

    for c in expresion:

        if c.lower() not in permitidos:

            return False

    return True

# =========================================================
# CONVERTIR EXPRESIONES
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
        "abs(",
        "abs("
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

    # cerrar parentesis extra para trigonometría
    expr = expr.replace(
        "math.sin(math.radians(",
        "math.sin(math.radians("
    )

    expr = expr.replace(
        "math.cos(math.radians(",
        "math.cos(math.radians("
    )

    expr = expr.replace(
        "math.tan(math.radians(",
        "math.tan(math.radians("
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

        # corregir trigonometría
        if "math.sin(math.radians(" in expr:
            expr += "))"

        if "math.cos(math.radians(" in expr:
            expr += "))"

        if "math.tan(math.radians(" in expr:
            expr += "))"

        resultado = eval(expr)

        pasos = []

        pasos.append(
            f"📌 La operación ingresada fue:\n\n{original}"
        )

        pasos.append(
            "\n📖 El sistema analizó "
            "la expresión matemática."
        )

        if "^" in original:

            pasos.append(
                "\n• Se identificó una potencia."
            )

        if "raiz" in original or "sqrt" in original:

            pasos.append(
                "\n• Se identificó una raíz cuadrada."
            )

        if "log" in original:

            pasos.append(
                "\n• Se identificó un logaritmo base 10."
            )

        if "ln" in original:

            pasos.append(
                "\n• Se identificó un logaritmo natural."
            )

        if (
            "sen" in original
            or "sin" in original
        ):

            pasos.append(
                "\n• Se identificó una función seno."
            )

        if "cos" in original:

            pasos.append(
                "\n• Se identificó una función coseno."
            )

        if "tan" in original:

            pasos.append(
                "\n• Se identificó una función tangente."
            )

        if "factorial" in original:

            pasos.append(
                "\n• Se identificó un factorial."
            )

        if "(" in original:

            pasos.append(
                "\n• Se resolvieron primero "
                "las operaciones dentro "
                "de los paréntesis."
            )

        pasos.append(
            f"\n\n🧮 Resultado obtenido:\n\n{resultado}"
        )

        pasos.append(
            "\n✅ La operación fue procesada "
            "correctamente."
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

    # COINCIDENCIA EXACTA
    if pregunta_usuario in memoria:

        return memoria[pregunta_usuario], 1.0

    # COINCIDENCIA APROXIMADA
    coincidencias = get_close_matches(
        pregunta_usuario,
        preguntas,
        n=1,
        cutoff=cutoff
    )

    if coincidencias:

        pregunta_encontrada = coincidencias[0]

        similitud = len(
            set(pregunta_usuario)
            &
            set(pregunta_encontrada)
        ) / max(
            len(pregunta_usuario),
            len(pregunta_encontrada)
        )

        return (
            memoria[pregunta_encontrada],
            similitud
        )

    return None, 0

# =========================================================
# SESSION STATE
# =========================================================

if "chat" not in st.session_state:

    st.session_state.chat = []

if "cerrado" not in st.session_state:

    st.session_state.cerrado = False

# =========================================================
# CERRAR CHAT
# =========================================================

if st.session_state.cerrado:

    st.warning(
        "El chatbot fue cerrado correctamente."
    )

    st.stop()

# =========================================================
# INPUT CHAT
# =========================================================

pregunta = st.chat_input(
    "Escribe una pregunta..."
)

# =========================================================
# PROCESAR MENSAJE
# =========================================================

if pregunta:

    st.session_state.chat.append(
        ("usuario", pregunta)
    )

    texto = pregunta.lower().strip()

    # =====================================================
    # SALIR
    # =====================================================

    if (
        texto == "salir"
        or texto == "quiero salir"
    ):

        respuesta_final = (
            "Hasta luego. "
            "El chatbot se cerrará correctamente."
        )

        st.session_state.chat.append(
            ("bot", respuesta_final)
        )

        st.session_state.cerrado = True

        st.rerun()

    # =====================================================
    # RESPUESTAS ESPECIALES
    # =====================================================

    elif respuesta_especial(texto):

        respuesta_final = (
            respuesta_especial(texto)
            + "\n\n"
            + random.choice(continuar)
        )

    # =====================================================
    # OPERACIONES MATEMÁTICAS
    # =====================================================

    elif es_operacion_matematica(texto):

        respuesta_final = resolver_operacion(
            texto
        )

    # =====================================================
    # RESPUESTAS NORMALES
    # =====================================================

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

            if score < 1.0:

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
# SUGERENCIAS FIJAS
# =========================================================

st.markdown("---")

st.subheader("💡 Preguntas sugeridas")

if "sugerencias_fijas" not in st.session_state:

    st.session_state.sugerencias_fijas = (
        random.sample(
            preguntas,
            min(8, len(preguntas))
        )
    )

ejemplos = st.session_state.sugerencias_fijas

col1, col2 = st.columns(2)

for i, ejemplo in enumerate(ejemplos):

    columna = col1 if i % 2 == 0 else col2

    if columna.button(
        ejemplo,
        key=f"sug_btn_{i}"
    ):

        st.session_state.chat.append(
            ("usuario", ejemplo)
        )

        respuesta, score = buscar_respuesta(
            ejemplo
        )

        respuesta_final = (
            random.choice(introducciones)
            + "\n\n"
            + respuesta
            + "\n\n"
            + random.choice(continuar)
        )

        st.session_state.chat.append(
            ("bot", respuesta_final)
        )

        st.rerun()

# =========================================================
# MOSTRAR ERRORES
# =========================================================

if errores:

    with st.expander(
        "⚠️ Ver errores del sistema"
    ):

        for e in errores:

            st.error(e)

