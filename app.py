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
    layout="centered"
)

# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #f5f7fb;
}

.main {
    background-color: #f5f7fb;
    color: #111827;
}

.block-container {
    max-width: 950px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1 {
    text-align: center;
    color: #2563eb;
    font-size: 3rem;
    margin-bottom: 5px;
}

.subtitulo {
    text-align: center;
    color: #475569;
    font-size: 1.1rem;
    margin-bottom: 30px;
}

.chat-user {
    background-color: #dbeafe;
    color: #111827;
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 12px;
    border-left: 5px solid #2563eb;
}

.chat-bot {
    background-color: white;
    color: #111827;
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 18px;
    border-left: 5px solid #10b981;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

div.stTextInput input {
    border-radius: 14px;
    border: 2px solid #cbd5e1;
    padding: 14px;
    background-color: white;
    color: black;
}

div.stButton > button {
    width: 100%;
    border-radius: 14px;
    height: 48px;
    font-size: 15px;
    font-weight: bold;
    background-color: #2563eb;
    color: white;
    border: none;
}

div.stButton > button:hover {
    background-color: #1d4ed8;
}

.codigo {
    background-color: #e2e8f0;
    padding: 10px;
    border-radius: 10px;
    font-family: monospace;
    color: black;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO
# =========================================================

st.markdown("""
<h1>🤖 Chatbot Híbrido Educativo</h1>

<p class="subtitulo">
Sistema inteligente de preguntas educativas y operaciones matemáticas avanzadas
</p>
""", unsafe_allow_html=True)

# =========================================================
# MEMORIA
# =========================================================

memoria = {}

temas = {
    "programacion": [],
    "ia": [],
    "redes": [],
    "hardware": [],
    "ciberseguridad": []
}

# =========================================================
# CARGAR ARCHIVOS
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

        nombre_tema = archivo.replace(
            ".txt",
            ""
        )

        for linea in lineas:

            if "?r:" in linea:

                pregunta, respuesta = linea.split("?r:")

                pregunta = pregunta.replace(
                    "p:",
                    ""
                ).strip().lower()

                respuesta = respuesta.strip()

                memoria[pregunta] = respuesta

                temas[nombre_tema].append(
                    pregunta
                )

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

    st.subheader("🧮 Operaciones matemáticas")

    st.markdown("""
Puedes escribir operaciones como:
""")

    st.markdown("""
<div class="codigo">
2+5*8<br>
raiz(144)<br>
2^8<br>
log(100)<br>
ln(20)<br>
sen(90)<br>
cos(0)<br>
tan(45)<br>
factorial(5)<br>
pi*2
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    st.info(
        "También puedes escribir preguntas naturales como:\n\n"
        "• ¿Qué es Python?\n"
        "• ¿Qué es una red LAN?\n"
        "• ¿Qué es inteligencia artificial?"
    )

    if st.button("🗑️ Reiniciar conversación"):

        st.session_state.chat = []

        st.session_state.tema_actual = None

        st.rerun()

# =========================================================
# FRASES
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
            "desarrollado con Python y Streamlit."
        )

    if "como estas" in texto:

        return (
            "Estoy funcionando correctamente "
            "y preparado para ayudarte."
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

    simbolos = [
        "+",
        "-",
        "*",
        "/",
        "^",
        "(",
        ")"
    ]

    funciones = [
        "raiz",
        "sqrt",
        "log",
        "ln",
        "sen",
        "sin",
        "cos",
        "tan",
        "factorial",
        "pi",
        "e"
    ]

    if any(s in expr for s in simbolos):

        return True

    if any(f in expr for f in funciones):

        return True

    if re.search(r'\d', expr):

        return True

    return False

# =========================================================
# CONVERTIR EXPRESIÓN
# =========================================================

def convertir_expresion(expr):

    expr = expr.lower().strip()

    expr = expr.replace("^", "**")

    expr = re.sub(
        r'raiz\(',
        'sqrt(',
        expr
    )

    expr = re.sub(
        r'sen\(',
        'sin(',
        expr
    )

    funciones = {
        "sqrt": math.sqrt,
        "log": math.log10,
        "ln": math.log,
        "sin": lambda x: math.sin(math.radians(x)),
        "cos": lambda x: math.cos(math.radians(x)),
        "tan": lambda x: math.tan(math.radians(x)),
        "factorial": math.factorial,
        "pi": math.pi,
        "e": math.e,
        "abs": abs
    }

    return expr, funciones

# =========================================================
# EXPLICAR OPERACIÓN
# =========================================================

def explicar_operacion(expresion):

    try:

        original = extraer_operacion(
            expresion
        )

        expr, funciones = convertir_expresion(
            original
        )

        resultado = eval(
            expr,
            {"__builtins__": {}},
            funciones
        )

        texto = (
            "Para resolver esta expresión "
            "se aplicó el orden matemático "
            "correcto."
        )

        detalles = []

        if "(" in original:

            detalles.append(
                "primero se resolvieron "
                "los paréntesis"
            )

        if "^" in original:

            detalles.append(
                "después se calcularon "
                "las potencias"
            )

        if "*" in original or "/" in original:

            detalles.append(
                "luego se realizaron "
                "multiplicaciones y divisiones"
            )

        if "+" in original or "-" in original[1:]:

            detalles.append(
                "y finalmente se efectuaron "
                "las sumas y restas"
            )

        if "raiz" in original:

            detalles.append(
                "incluyendo raíces cuadradas"
            )

        if (
            "sen" in original
            or "cos" in original
            or "tan" in original
        ):

            detalles.append(
                "utilizando funciones trigonométricas"
            )

        if detalles:

            texto += (
                ", donde "
                + ", ".join(detalles)
                + "."
            )

        return (
            f"### 🧮 Operación ingresada\n\n"
            f"`{original}`\n\n"
            f"{texto}\n\n"
            f"### ✅ Resultado final\n\n"
            f"**{resultado}**"
        )

    except Exception as e:

        return (
            "❌ No fue posible resolver "
            "la operación matemática.\n\n"
            f"{e}"
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
# DETECTAR TEMA
# =========================================================

def detectar_tema(texto):

    texto = texto.lower()

    for tema, lista in temas.items():

        for pregunta in lista:

            if any(
                palabra in pregunta
                for palabra in texto.split()
            ):

                return tema

    return random.choice(
        list(temas.keys())
    )

# =========================================================
# SESSION STATE
# =========================================================

if "chat" not in st.session_state:

    st.session_state.chat = []

if "tema_actual" not in st.session_state:

    st.session_state.tema_actual = random.choice(
        list(temas.keys())
    )

# =========================================================
# INPUT
# =========================================================

with st.form(
    "form_chat",
    clear_on_submit=True
):

    pregunta = st.text_input(
        "💬 Escribe tu pregunta o una operación matemática:"
    )

    enviar = st.form_submit_button(
        "Enviar consulta"
    )

# =========================================================
# PROCESAR MENSAJE
# =========================================================

if enviar and pregunta:

    texto = pregunta.lower().strip()

    st.session_state.chat.append(
        ("usuario", pregunta)
    )

    tema_detectado = detectar_tema(
        texto
    )

    st.session_state.tema_actual = (
        tema_detectado
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
# PREGUNTAS SUGERIDAS
# =========================================================

st.markdown("---")

st.subheader("💡 Preguntas sugeridas")

tema_actual = st.session_state.tema_actual

preguntas_sugeridas = random.sample(
    temas[tema_actual],
    min(6, len(temas[tema_actual]))
)

col1, col2 = st.columns(2)

for i, pregunta_sug in enumerate(
    preguntas_sugeridas
):

    col = col1 if i % 2 == 0 else col2

    if col.button(
        pregunta_sug,
        key=f"sug_{i}"
    ):

        st.session_state.chat.append(
            ("usuario", pregunta_sug)
        )

        respuesta, score = buscar_respuesta(
            pregunta_sug
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
# ERRORES
# =========================================================

if errores:

    with st.expander(
        "⚠️ Ver errores del sistema"
    ):

        for e in errores:

            st.error(e)

