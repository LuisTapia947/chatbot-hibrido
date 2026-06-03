# =========================================================
# APP PRINCIPAL 
# app.py
# =========================================================

import streamlit as st
import random

from chatbot.conocimiento import (
    cargar_conocimiento,
    buscar_respuesta,
    obtener_estadisticas
)

from chatbot.temas import (
    detectar_tema
)

from chatbot.matematicas import (
    es_operacion_matematica,
    explicar_operacion
)

from chatbot.respuestas import (
    respuesta_especial,
    obtener_intro,
    obtener_continuacion,
    es_comando_salida,
    mensaje_despedida,
    mensaje_sin_respuesta
)

from chatbot.historial import (
    guardar_chat,
    obtener_historiales
)

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
# ESTILOS VISUALES MEJORADOS
# =========================================================

st.markdown("""
<style>

/* ======================================================
FUENTE Y FONDO GLOBAL
====================================================== */

html,
body,
[class*="css"] {

    font-family: 'Inter', sans-serif;

    background:
    linear-gradient(
        180deg,
        #f8fafc 0%,
        #eef2ff 100%
    );

    color: #0f172a;
}

/* ======================================================
CONTENEDOR PRINCIPAL
====================================================== */

.block-container {

    max-width: 1180px;

    padding-top: 1.5rem;

    padding-bottom: 9rem;

    animation: fadein 0.25s ease;
}

/* ======================================================
ANIMACIONES
====================================================== */

@keyframes fadein {

    from {

        opacity: 0;
    }

    to {

        opacity: 1;
    }
}

@keyframes subir {

    from {

        opacity: 0;

        transform: translateY(12px);
    }

    to {

        opacity: 1;

        transform: translateY(0px);
    }
}

/* ======================================================
HEADER
====================================================== */

.hero {

    background:
    linear-gradient(
        135deg,
        rgba(37,99,235,0.10) 0%,
        rgba(59,130,246,0.05) 100%
    );

    border: 1px solid #dbeafe;

    border-radius: 28px;

    padding: 35px;

    margin-bottom: 30px;

    box-shadow:
    0 10px 30px rgba(37,99,235,0.08);
}

.titulo {

    text-align: center;

    font-size: 3.5rem;

    font-weight: 800;

    color: #1e3a8a;

    margin-bottom: 10px;

    letter-spacing: -1px;
}

.subtitulo {

    text-align: center;

    color: #475569;

    font-size: 1.1rem;

    line-height: 1.7;
}

/* ======================================================
CHAT GENERAL
====================================================== */

.chat-wrapper {

    display: flex;

    width: 100%;

    margin-bottom: 18px;

    animation: subir 0.22s ease;
}

/* ======================================================
MENSAJE USUARIO
====================================================== */

.user-wrapper {

    justify-content: flex-end;
}

.chat-user {

    width: fit-content;

    max-width: 75%;

    background:
    linear-gradient(
        135deg,
        #2563eb 0%,
        #3b82f6 100%
    );

    color: white;

    padding: 18px 20px;

    border-radius: 24px 24px 8px 24px;

    box-shadow:
    0 8px 24px rgba(37,99,235,0.25);

    font-size: 15px;

    line-height: 1.7;

    border: 1px solid rgba(255,255,255,0.15);
}

/* ======================================================
MENSAJE BOT
====================================================== */

.bot-wrapper {

    justify-content: flex-start;
}

.chat-bot {

    width: fit-content;

    max-width: 78%;

    background: rgba(255,255,255,0.90);

    backdrop-filter: blur(10px);

    color: #111827;

    padding: 20px 22px;

    border-radius: 24px 24px 24px 8px;

    border: 1px solid #e2e8f0;

    box-shadow:
    0 8px 24px rgba(15,23,42,0.06);

    line-height: 1.8;

    font-size: 15px;
}

/* ======================================================
ETIQUETAS
====================================================== */

.chat-label {

    font-size: 13px;

    font-weight: 700;

    margin-bottom: 10px;

    opacity: 0.9;
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

    border-right:
    1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {

    color: white !important;
}

/* ======================================================
SIDEBAR TARJETAS
====================================================== */

.sidebar-card {

    background:
    rgba(255,255,255,0.08);

    border:
    1px solid rgba(255,255,255,0.10);

    border-radius: 18px;

    padding: 16px;

    margin-bottom: 16px;

    backdrop-filter: blur(6px);
}

/* ======================================================
BOTONES
====================================================== */

div.stButton > button {

    width: 100%;

    border-radius: 16px;

    min-height: 54px;

    font-size: 14px;

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
    0 6px 18px rgba(37,99,235,0.22);

    transition: all 0.18s ease;
}

div.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
    0 10px 24px rgba(37,99,235,0.30);
}

/* ======================================================
CAJA DE CÓDIGO
====================================================== */

.codigo {

    background:
    linear-gradient(
        180deg,
        #0f172a 0%,
        #111827 100%
    );

    color: #f8fafc;

    padding: 18px;

    border-radius: 18px;

    font-family: monospace;

    line-height: 2;

    font-size: 14px;

    border: 1px solid rgba(255,255,255,0.06);

    overflow-x: auto;
}

/* ======================================================
CHAT INPUT
====================================================== */

[data-testid="stChatInput"] {

    position: fixed;

    bottom: 16px;

    left: 23rem;

    right: 2rem;

    z-index: 1000;
}

[data-testid="stChatInput"] > div {

    background: white;

    border-radius: 22px;

    padding: 6px;

    border: 1px solid #dbeafe;

    box-shadow:
    0 10px 30px rgba(15,23,42,0.10);
}

[data-testid="stChatInput"] textarea {

    border: none !important;

    box-shadow: none !important;

    font-size: 15px !important;

    padding: 14px !important;
}

/* ======================================================
SEPARADORES
====================================================== */

hr {

    border: none;

    height: 1px;

    background: #dbeafe;

    margin-top: 30px;

    margin-bottom: 30px;
}

/* ======================================================
SUBTITULOS
====================================================== */

h2, h3 {

    color: #1e293b;

    font-weight: 700;
}

/* ======================================================
SUGERENCIAS
====================================================== */

.sugerencias-box {

    background:
    rgba(255,255,255,0.75);

    border: 1px solid #dbeafe;

    border-radius: 24px;

    padding: 24px;

    margin-top: 20px;

    box-shadow:
    0 6px 20px rgba(0,0,0,0.04);
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

/* ======================================================
RESPONSIVE
====================================================== */

@media (max-width: 900px) {

    .chat-user,
    .chat-bot {

        max-width: 100%;
    }

    .titulo {

        font-size: 2.5rem;
    }

    [data-testid="stChatInput"] {

        left: 1rem;

        right: 1rem;
    }

    .hero {

        padding: 25px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# CARGAR CONOCIMIENTO
# =========================================================

memoria, preguntas, temas = (
    cargar_conocimiento()
)

estadisticas = obtener_estadisticas(
    memoria,
    temas
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

if "preguntas_usadas" not in st.session_state:

    st.session_state.preguntas_usadas = []

if "preguntas_sugeridas" not in st.session_state:

    disponibles = temas[
        st.session_state.tema_actual
    ]

    st.session_state.preguntas_sugeridas = (
        random.sample(
            disponibles,
            min(6, len(disponibles))
        )
    )

# =========================================================
# HEADER PRINCIPAL
# =========================================================

st.markdown(f"""

<div class="hero">

    <div class="titulo">
    🤖 Chatbot Híbrido
    </div>

    <div class="subtitulo">
    Sistema educativo inteligente con búsqueda híbrida,
    respuestas dinámicas y resolución matemática avanzada.
    </div>

</div>

""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # =====================================================
    # TITULO SIDEBAR
    # =====================================================

    st.markdown("""

    <div style="
        text-align:center;
        margin-bottom:25px;
    ">

    <h1 style="
        margin-bottom:0px;
        font-size:32px;
    ">
    🤖
    </h1>

    <h2 style="
        margin-top:5px;
        font-weight:800;
    ">
    Panel del Sistema
    </h2>

    <p style="
        opacity:0.8;
        font-size:14px;
    ">
    Chatbot educativo inteligente
    </p>

    </div>

    """, unsafe_allow_html=True)

    # =====================================================
    # ESTADISTICAS
    # =====================================================

    st.markdown(f"""

    <div class="sidebar-card">

    <h3 style="
        margin-top:0px;
        margin-bottom:18px;
    ">
    📊 Estadísticas
    </h3>

    <div style="
        display:flex;
        justify-content:space-between;
        margin-bottom:10px;
    ">
        <span>Total preguntas</span>
        <strong>{estadisticas['total']}</strong>
    </div>

    <div style="
        display:flex;
        justify-content:space-between;
        margin-bottom:10px;
    ">
        <span>💻 Programación</span>
        <strong>{estadisticas['programacion']}</strong>
    </div>

    <div style="
        display:flex;
        justify-content:space-between;
        margin-bottom:10px;
    ">
        <span>🤖 IA</span>
        <strong>{estadisticas['ia']}</strong>
    </div>

    <div style="
        display:flex;
        justify-content:space-between;
        margin-bottom:10px;
    ">
        <span>🌐 Redes</span>
        <strong>{estadisticas['redes']}</strong>
    </div>

    <div style="
        display:flex;
        justify-content:space-between;
        margin-bottom:10px;
    ">
        <span>🖥️ Hardware</span>
        <strong>{estadisticas['hardware']}</strong>
    </div>

    <div style="
        display:flex;
        justify-content:space-between;
    ">
        <span>🔐 Ciberseguridad</span>
        <strong>{estadisticas['ciberseguridad']}</strong>
    </div>

    </div>

    """, unsafe_allow_html=True)

    # =====================================================
    # AREAS
    # =====================================================

    st.markdown("""

    <div class="sidebar-card">

    <h3 style="
        margin-top:0px;
        margin-bottom:18px;
    ">
    📚 Áreas disponibles
    </h3>

    <div style="line-height:2; font-size:15px;">

    💻 Programación<br>
    🤖 Inteligencia Artificial<br>
    🌐 Redes<br>
    🖥️ Hardware<br>
    🔐 Ciberseguridad

    </div>

    </div>

    """, unsafe_allow_html=True)

    # =====================================================
    # EJEMPLOS MATEMATICOS
    # =====================================================

    st.markdown("""

    <div class="sidebar-card">

    <h3 style="
        margin-top:0px;
        margin-bottom:18px;
    ">
    🧮 Ejemplos Matemáticos
    </h3>

    <div class="codigo">

2+5*8

40-36*5

raiz(144)

2^8

log(100)

sen(90)

factorial(5)

pi*2

    </div>

    </div>

    """, unsafe_allow_html=True)

    # =====================================================
    # AYUDA
    # =====================================================

    st.markdown("""

    <div class="sidebar-card">

    <h3 style="
        margin-top:0px;
        margin-bottom:16px;
    ">
    💡 Ejemplos de preguntas
    </h3>

    <div style="
        line-height:1.9;
        font-size:14px;
        opacity:0.92;
    ">

    • ¿Qué es Python?<br>

    • ¿Qué es una red LAN?<br>

    • ¿Qué es inteligencia artificial?<br>

    • calcula 25*8+4<br>

    • raiz(625)

    </div>

    </div>

    """, unsafe_allow_html=True)

    # =====================================================
    # HISTORIAL
    # =====================================================

    st.markdown("""

    <div style="
        margin-top:10px;
        margin-bottom:10px;
    ">
    <h3>
    🕘 Historial reciente
    </h3>
    </div>

    """, unsafe_allow_html=True)

    historiales = obtener_historiales()

    if historiales:

        for archivo in historiales[:8]:

            st.markdown(f"""

            <div class="sidebar-card" style="
                padding:12px;
                margin-bottom:10px;
            ">

            📄 {archivo}

            </div>

            """, unsafe_allow_html=True)

    else:

        st.markdown("""

        <div class="sidebar-card">

        No hay conversaciones guardadas todavía.

        </div>

        """, unsafe_allow_html=True)

    # =====================================================
    # BOTON REINICIAR
    # =====================================================

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🗑️ Reiniciar conversación"):

        st.session_state.chat = []

        st.session_state.chat_cerrado = False

        st.session_state.preguntas_usadas = []

        st.session_state.tema_actual = random.choice(
            list(temas.keys())
        )

        disponibles = temas[
            st.session_state.tema_actual
        ]

        st.session_state.preguntas_sugeridas = (
            random.sample(
                disponibles,
                min(6, len(disponibles))
            )
        )

        st.rerun()

# =========================================================
# CHAT FINALIZADO
# =========================================================

if st.session_state.chat_cerrado:

    st.markdown(f"""

<div class="chat-bot">

{mensaje_despedida()}

</div>

""", unsafe_allow_html=True)

    st.stop()

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
# INPUT
# =========================================================

pregunta = st.chat_input(
    "Escribe tu pregunta..."
)

# =========================================================
# PROCESAR MENSAJE
# =========================================================

if pregunta:

    texto = pregunta.lower().strip()

    st.session_state.chat.append(
        ("usuario", pregunta)
    )

    # =====================================================
    # DETECTAR TEMA
    # =====================================================

    tema_detectado = detectar_tema(
        texto,
        temas
    )

    st.session_state.tema_actual = (
        tema_detectado
    )

    # =====================================================
    # SALIR
    # =====================================================

    if es_comando_salida(texto):

        respuesta_final = mensaje_despedida()

        st.session_state.chat.append(
            ("bot", respuesta_final)
        )

        guardar_chat(
            st.session_state.chat
        )

        st.session_state.chat_cerrado = True

        st.rerun()

    # =====================================================
    # RESPUESTAS ESPECIALES
    # =====================================================

    respuesta_esp = respuesta_especial(
        texto
    )

    if respuesta_esp:

        respuesta_final = (
            respuesta_esp
            + "\n\n"
            + obtener_continuacion()
        )

        st.session_state.chat.append(
            ("bot", respuesta_final)
        )

        st.rerun()

    # =====================================================
    # MATEMATICAS
    # =====================================================

    elif es_operacion_matematica(texto):

        respuesta_final = explicar_operacion(
            texto
        )

    # =====================================================
    # RESPUESTAS GENERALES
    # =====================================================

    else:

        resultado = buscar_respuesta(
            texto,
            memoria,
            preguntas
        )

        respuesta = resultado["respuesta"]

        score = resultado["score"]

        if respuesta:

            respuesta_final = (
                obtener_intro()
                + "\n\n"
                + respuesta
                + "\n\n"
                + obtener_continuacion()
            )

            if score < 1:

                respuesta_final += (
                    f"\n\n🔎 Coincidencia aproximada: "
                    f"{score*100:.0f}%"
                )

        else:

            respuesta_final = (
                mensaje_sin_respuesta()
            )

    st.session_state.chat.append(
        ("bot", respuesta_final)
    )

    st.rerun()

# =========================================================
# PREGUNTAS SUGERIDAS
# =========================================================

st.markdown("---")

st.subheader("💡 Preguntas sugeridas")

preguntas_sugeridas = (
    st.session_state.preguntas_sugeridas
)

col1, col2 = st.columns(2)

for i, pregunta_sug in enumerate(
    preguntas_sugeridas
):

    col = col1 if i % 2 == 0 else col2

    if col.button(
        pregunta_sug,
        key=f"sugerencia_{i}"
    ):

        st.session_state.preguntas_usadas.append(
            pregunta_sug
        )

        st.session_state.chat.append(
            ("usuario", pregunta_sug)
        )

        resultado = buscar_respuesta(
            pregunta_sug,
            memoria,
            preguntas
        )

        respuesta = resultado["respuesta"]

        score = resultado["score"]

        if respuesta:

            respuesta_final = (
                obtener_intro()
                + "\n\n"
                + respuesta
                + "\n\n"
                + obtener_continuacion()
            )

            if score < 1:

                respuesta_final += (
                    f"\n\n🔎 Coincidencia aproximada: "
                    f"{score*100:.0f}%"
                )

        else:

            respuesta_final = (
                mensaje_sin_respuesta()
            )

        st.session_state.chat.append(
            ("bot", respuesta_final)
        )

        # =================================================
        # CAMBIAR SUGERENCIAS
        # =================================================

        tema_actual = st.session_state.tema_actual

        disponibles = [

            p for p in temas[tema_actual]

            if p not in st.session_state.preguntas_usadas
        ]

        if len(disponibles) < 6:

            st.session_state.preguntas_usadas = []

            disponibles = temas[
                tema_actual
            ]

        st.session_state.preguntas_sugeridas = (
            random.sample(
                disponibles,
                min(6, len(disponibles))
            )
        )

        st.rerun()
