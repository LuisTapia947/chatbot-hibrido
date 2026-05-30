# =========================================================
# CHATBOT HÍBRIDO 
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
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ESTILOS VISUALES MODERNOS
# =========================================================

st.markdown("""
<style>

/* ======================================================
FUENTE Y FONDO GENERAL
====================================================== */

html, body, [class*="css"] {

    font-family: 'Inter', sans-serif;

    background:
    linear-gradient(
        180deg,
        #f8fafc 0%,
        #eef2ff 100%
    );
}

/* ======================================================
CONTENEDOR PRINCIPAL
====================================================== */

.main {

    color: #111827;
}

.block-container {

    max-width: 1150px;

    padding-top: 1.5rem;

    padding-bottom: 2rem;
}

/* ======================================================
TÍTULO
====================================================== */

.titulo-principal {

    text-align: center;

    font-size: 3.5rem;

    font-weight: 800;

    color: #1e3a8a;

    margin-bottom: 10px;
}

.subtitulo {

    text-align: center;

    color: #475569;

    font-size: 1.15rem;

    margin-bottom: 40px;
}

/* ======================================================
CHAT USUARIO
====================================================== */

.chat-user {

    background:
    linear-gradient(
        135deg,
        #2563eb 0%,
        #3b82f6 100%
    );

    color: white;

    padding: 18px;

    border-radius: 24px;

    margin-left: 100px;

    margin-bottom: 15px;

    box-shadow:
    0 5px 18px rgba(37,99,235,0.20);

    animation: aparecer 0.25s ease;
}

/* ======================================================
CHAT BOT
====================================================== */

.chat-bot {

    background: white;

    color: #111827;

    padding: 20px;

    border-radius: 24px;

    margin-right: 100px;

    margin-bottom: 18px;

    border: 1px solid #e2e8f0;

    box-shadow:
    0 4px 18px rgba(0,0,0,0.05);

    animation: aparecer 0.25s ease;
}

/* ======================================================
ANIMACIÓN
====================================================== */

@keyframes aparecer {

    from {

        opacity: 0;

        transform: translateY(10px);
    }

    to {

        opacity: 1;

        transform: translateY(0px);
    }
}

/* ======================================================
INPUT
====================================================== */

div.stTextInput input {

    background: white;

    border: 2px solid #dbeafe;

    border-radius: 20px;

    padding: 16px;

    font-size: 16px;

    color: #111827;

    box-shadow:
    0 2px 12px rgba(0,0,0,0.05);
}

div.stTextInput input:focus {

    border: 2px solid #2563eb;

    box-shadow:
    0 0 0 4px rgba(37,99,235,0.15);
}

/* ======================================================
BOTONES
====================================================== */

div.stButton > button {

    width: 100%;

    border-radius: 18px;

    height: 52px;

    font-size: 15px;

    font-weight: 700;

    border: none;

    color: white;

    background:
    linear-gradient(
        135deg,
        #2563eb 0%,
        #1d4ed8 100%
    );

    box-shadow:
    0 4px 15px rgba(37,99,235,0.25);

    transition: all 0.2s ease;
}

div.stButton > button:hover {

    transform: translateY(-2px);

    background:
    linear-gradient(
        135deg,
        #1d4ed8 0%,
        #1e40af 100%
    );
}

/* ======================================================
SIDEBAR
====================================================== */

section[data-testid="stSidebar"] {

    background:
    linear-gradient(
        180deg,
        #0f172a 0%,
        #1e293b 100%
    );
}

section[data-testid="stSidebar"] * {

    color: white !important;
}

/* ======================================================
TARJETAS
====================================================== */

.card {

    background: white;

    border-radius: 20px;

    padding: 18px;

    margin-bottom: 18px;

    border: 1px solid #e2e8f0;

    box-shadow:
    0 3px 10px rgba(0,0,0,0.05);
}

/* ======================================================
CÓDIGO
====================================================== */

.codigo {

    background: #0f172a;

    color: #f8fafc;

    padding: 16px;

    border-radius: 14px;

    font-family: monospace;

    font-size: 14px;

    line-height: 1.8;
}

/* ======================================================
SCROLL
====================================================== */

::-webkit-scrollbar {

    width: 10px;
}

::-webkit-scrollbar-track {

    background: #e2e8f0;
}

::-webkit-scrollbar-thumb {

    background: #94a3b8;

    border-radius: 20px;
}

::-webkit-scrollbar-thumb:hover {

    background: #64748b;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO PRINCIPAL
# =========================================================

st.markdown("""

<div class="titulo-principal">
🤖 Chatbot Híbrido 
</div>

<div class="subtitulo">
Sistema inteligente de búsqueda híbrida,
preguntas educativas y resolución matemática avanzada
</div>

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
# CARGAR ARCHIVOS TXT
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
# SIDEBAR MODERNO
# =========================================================

with st.sidebar:

    st.markdown("""
    ## 🤖 Panel del Sistema
    """)

    st.success(
        f"Preguntas cargadas: {len(preguntas)}"
    )

    st.markdown("---")

    st.markdown("""
    ### 📚 Áreas de conocimiento

    💻 Programación  
    🤖 Inteligencia Artificial  
    🌐 Redes  
    🖥️ Hardware  
    🔐 Ciberseguridad  
    """)

    st.markdown("---")

    st.markdown("""
    ### 🧮 Operaciones Matemáticas
    """)

    st.markdown("""
    <div class="codigo">

    2+5*8

    raiz(144)

    2^8

    log(100)

    ln(20)

    sen(90)

    cos(0)

    tan(45)

    factorial(5)

    pi*2

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.info(
        "También puedes hacer preguntas naturales como:\n\n"
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

if "chat_cerrado" not in st.session_state:

    st.session_state.chat_cerrado = False

# =========================================================
# CHAT FINALIZADO
# =========================================================

if st.session_state.chat_cerrado:

    st.markdown("""

    <div class="chat-bot">

    <h2>👋 Sesión finalizada</h2>

    <p>
    El chatbot híbrido educativo cerró la conversación correctamente.
    </p>

    <p>
    Puedes reiniciar la conversación desde el panel lateral.
    </p>

    </div>

    """, unsafe_allow_html=True)

    st.stop()

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

    # GUARDAR MENSAJE USUARIO
    st.session_state.chat.append(
        ("usuario", pregunta)
    )

    # DETECTAR TEMA
    tema_detectado = detectar_tema(
        texto
    )

    st.session_state.tema_actual = (
        tema_detectado
    )

    # =====================================================
    # SALIR DEL CHAT
    # =====================================================

    if texto in ["salir", "quiero salir"]:

        respuesta_final = """

### 👋 Sesión finalizada

El chatbot híbrido educativo ha cerrado la conversación correctamente.

Gracias por utilizar el sistema inteligente de consultas educativas y matemáticas.

Puedes reiniciar la conversación desde el panel lateral si deseas volver a comenzar.

        """

        st.session_state.chat.append(
            ("bot", respuesta_final)
        )

        st.session_state.chat_cerrado = True

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

        respuesta_final = explicar_operacion(
            texto
        )

    # =====================================================
    # RESPUESTAS GENERALES
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

    # =====================================================
    # GUARDAR RESPUESTA
    # =====================================================

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

# =========================================================
# GUARDAR SUGERENCIAS
# =========================================================

if "tema_sugerencias" not in st.session_state:

    st.session_state.tema_sugerencias = tema_actual

if "preguntas_sugeridas" not in st.session_state:

    st.session_state.preguntas_sugeridas = (
        random.sample(
            temas[tema_actual],
            min(6, len(temas[tema_actual]))
        )
    )

# =========================================================
# CAMBIAR SOLO SI CAMBIA EL TEMA
# =========================================================

if (
    st.session_state.tema_sugerencias
    != tema_actual
):

    st.session_state.tema_sugerencias = (
        tema_actual
    )

    st.session_state.preguntas_sugeridas = (
        random.sample(
            temas[tema_actual],
            min(6, len(temas[tema_actual]))
        )
    )

preguntas_sugeridas = (
    st.session_state.preguntas_sugeridas
)

# =========================================================
# MOSTRAR BOTONES
# =========================================================

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

