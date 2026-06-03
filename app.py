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

    font-family: 'Segoe UI', 'Inter', sans-serif;

    background:
    linear-gradient(
        135deg,
        #f8fafc 0%,
        #f1f5f9 50%,
        #e2e8f0 100%
    );

    color: #0f172a;
}

/* ======================================================
CONTENEDOR PRINCIPAL
====================================================== */

.block-container {

    max-width: 1200px;

    padding-top: 2rem;

    padding-bottom: 10rem;

    animation: fadein 0.35s ease-out;

    background: transparent;
}

/* ======================================================
ANIMACIONES
====================================================== */

@keyframes fadein {

    from {
        opacity: 0;
        transform: scale(0.98);
    }

    to {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes subir {

    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

@keyframes pulse-glow {

    0%, 100% {
        box-shadow:
        0 0 20px rgba(99, 102, 241, 0.20),
        0 10px 30px rgba(99, 102, 241, 0.10);
    }

    50% {
        box-shadow:
        0 0 40px rgba(99, 102, 241, 0.35),
        0 15px 40px rgba(99, 102, 241, 0.15);
    }
}

@keyframes float {

    0%, 100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-8px);
    }
}

/* ======================================================
HEADER
====================================================== */

.hero {
    background:
    linear-gradient(
        135deg,
        rgba(99, 102, 241, 0.15) 0%,
        rgba(168, 85, 247, 0.10) 50%,
        rgba(59, 130, 246, 0.12) 100%
    );
    border: 2px solid rgba(99, 102, 241, 0.25);
    border-radius: 32px;
    padding: 48px 40px;
    margin-bottom: 32px;
    box-shadow:
    0 20px 50px rgba(99, 102, 241, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
    position: relative;
    overflow: hidden;
    animation: float 4s ease-in-out infinite;
}

.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background:
    radial-gradient(
        circle,
        rgba(168, 85, 247, 0.15) 0%,
        transparent 70%
    );

    border-radius: 50%;
    z-index: 0;
}

.hero::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 350px;
    height: 350px;
    background:
    radial-gradient(
        circle,
        rgba(99, 102, 241, 0.12) 0%,
        transparent 70%
    );

    border-radius: 50%;

    z-index: 0;
}

.titulo {

    text-align: center;
    font-size: 3.8rem;
    font-weight: 900;
    background:
    linear-gradient(
        135deg,
        #6366f1 0%,
        #a855f7 50%,
        #3b82f6 100%
    );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    background-clip: text;

    margin-bottom: 15px;

    letter-spacing: -1px;

    position: relative;

    z-index: 1;
}

.subtitulo {

    text-align: center;

    color: #475569;

    font-size: 1.15rem;

    line-height: 1.8;

    font-weight: 500;

    position: relative;

    z-index: 1;
}

/* ======================================================
CHAT GENERAL
====================================================== */

.chat-wrapper {

    display: flex;

    width: 100%;

    margin-bottom: 20px;

    animation: subir 0.3s ease-out;
}

/* ======================================================
MENSAJE USUARIO
====================================================== */
.user-wrapper {
    display: flex;
    justify-content: flex-end;
    width: 100%;
}
.chat-user {
    max-width: 70%;
    margin-left: auto;

    background:
    linear-gradient(
        135deg,
        #6366f1 0%,
        #8b5cf6 100%
    );
    color: white;
    padding: 14px 18px;
    border-radius: 20px 20px 6px 20px;
    box-shadow:
    0 8px 20px rgba(99, 102, 241, 0.25);
    font-size: 15px;
    line-height: 1.7;
    border:
    1px solid rgba(255,255,255,0.15);

    transition: 0.2s ease;
}
.chat-user:hover {
    transform: translateY(-2px);
}

/* ======================================================
MENSAJE BOT
====================================================== */
.bot-wrapper {
    width: 100%;
}
.chat-bot {
    width: 100%;
    box-sizing: border-box;
    background:
    rgba(255,255,255,0.95);
    color: #0f172a;
    padding: 18px 20px;
    border-radius: 20px;
    border:
    1px solid rgba(99,102,241,0.15);
    box-shadow:
    0 8px 24px rgba(0,0,0,0.08);
    line-height: 1.8;
    font-size: 15px;
    margin-bottom: 8px;
    transition: 0.2s ease;
}
.chat-bot:hover {
    border-color:
    rgba(99,102,241,0.25);
}
.chat-label {
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 10px;
    opacity: 0.8;
    text-transform: uppercase;

    letter-spacing: 0.8px;
}
/* ======================================================
SIDEBAR
====================================================== */
section[data-testid="stSidebar"] {
    background:
    linear-gradient(
        180deg,
        #f8fafc 0%,
        #f1f5f9 50%,
        #e2e8f0 100%
    );
    border-right: 1.5px solid rgba(99, 102, 241, 0.15);
}
section[data-testid="stSidebar"] * {
    color: #0f172a !important;
}
/* ======================================================
SIDEBAR TARJETAS
====================================================== */

.sidebar-card {
    background:
    linear-gradient(
        135deg,
        rgba(99, 102, 241, 0.06) 0%,
        rgba(139, 92, 246, 0.05) 100%
    );
    border: 1.5px solid rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 18px;
    backdrop-filter: blur(8px);
    transition: all 0.25s ease;
    box-shadow:
    0 6px 20px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.5);
}
.sidebar-card:hover {
    background:
    linear-gradient(
        135deg,
        rgba(99, 102, 241, 0.10) 0%,
        rgba(139, 92, 246, 0.08) 100%
    );
    border-color: rgba(99, 102, 241, 0.35);
    box-shadow:
    0 10px 28px rgba(99, 102, 241, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
    transform: translateY(-2px);
}

/* ======================================================
BOTONES
====================================================== */

div.stButton > button {
    width: 100%;
    border-radius: 18px;
    min-height: 48px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.5px;
    border: none;
    color: white;
    background:
    linear-gradient(
        135deg,
        #6366f1 0%,
        #8b5cf6 100%
    );
    box-shadow:
    0 8px 25px rgba(99, 102, 241, 0.30);
    transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    overflow: hidden;
}

div.stButton > button::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}
div.stButton > button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow:
    0 14px 35px rgba(99, 102, 241, 0.45),
    0 0 25px rgba(139, 92, 246, 0.25);
}
div.stButton > button:active {
    transform: translateY(-1px);
}

/* ======================================================
CAJA DE CÓDIGO
====================================================== */
.codigo {
    background:
    linear-gradient(
        180deg,
        #f1f5f9 0%,
        #e2e8f0 100%
    );
    color: #0f172a;
    padding: 20px 22px;
    border-radius: 16px;
    font-family: 'Courier New', monospace;
    line-height: 1.8;
    font-size: 14px;
    border: 1px solid rgba(99, 102, 241, 0.15);
    overflow-x: auto;
    box-shadow:
    0 8px 24px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
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
    background:
    linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.98) 0%,
        rgba(248, 250, 252, 0.98) 100%
    );
    border-radius: 24px;
    padding: 8px;
    border: 1.5px solid rgba(99, 102, 241, 0.2);
    box-shadow:
    0 12px 35px rgba(0, 0, 0, 0.10),
    0 0 25px rgba(99, 102, 241, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(15px);
}

[data-testid="stChatInput"] textarea {
    border: none !important;
    box-shadow: none !important;
    font-size: 15px !important;
    padding: 12px 18px !important;
    font-family: 'Segoe UI', sans-serif !important;
    color: #0f172a !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(15, 23, 42, 0.5) !important;
}
/* ======================================================
SEPARADORES
====================================================== */

hr {
    border: none;
    height: 2px;
    background:
    linear-gradient(
        90deg,
        transparent 0%,
        rgba(99, 102, 241, 0.2) 50%,
        transparent 100%
    );
    margin-top: 32px;
    margin-bottom: 32px;
}
/* =====================================================
TÍTULOS Y SUBTÍTULOS
====================================================== */
h1, h2, h3 {
    color: #0f172a;
    font-weight: 800;
    letter-spacing: -0.5px;
}

h2 {
    color: #1e293b;
    background: transparent;
    margin-top: 24px;
    margin-bottom: 16px;
}

h3 {
    color: #334155;
    font-size: 1.1rem;
    margin-top: 18px;
    margin-bottom: 12px;
}

input {
    background: rgba(255, 255, 255, 0.98) !important;
    border: 1.5px solid rgba(99, 102, 241, 0.25) !important;
    border-radius: 12px !important;
    color: #0f172a !important;
    transition: all 0.25s ease !important;
}

input:focus {
    border-color: rgba(99, 102, 241, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12) !important;
}

select {
    background: rgba(255, 255, 255, 0.98) !important;
    border: 1.5px solid rgba(99, 102, 241, 0.25) !important;
    border-radius: 12px !important;
    color: #0f172a !important;
    padding: 10px 12px !important;
}

a {
    color: #4f46e5 !important;
    text-decoration: none;
    transition: all 0.25s ease;
    font-weight: 600;
}

a:hover {

    color: #6366f1 !important;

    text-decoration: underline;
}


p {
    color: #475569;
    line-height: 1.7;
    font-size: 15px;
}

.badge {
    background:
    linear-gradient(
        135deg,
        rgba(99, 102, 241, 0.12) 0%,
        rgba(168, 85, 247, 0.10) 100%
    );

    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 12px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 700;
    color: #4f46e5;
    display: inline-block;
    margin: 4px;
}

.stat-box {
    background:
    linear-gradient(
        135deg,
        rgba(99, 102, 241, 0.05) 0%,
        rgba(168, 85, 247, 0.04) 100%
    );
    border: 1.5px solid rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
    box-shadow:
    0 6px 20px rgba(0, 0, 0, 0.03),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
}
.stat-box:hover {
    background:
    linear-gradient(
        135deg,
        rgba(99, 102, 241, 0.08) 0%,
        rgba(168, 85, 247, 0.06) 100%
    );
    border-color: rgba(99, 102, 241, 0.3);
    transform: translateY(-4px);
    box-shadow:
    0 10px 28px rgba(99, 102, 241, 0.10),
    inset 0 1px 0 rgba(255, 255, 255, 0.7);
}
.stat-value {
    font-size: 28px;
    font-weight: 900;
    background:
    linear-gradient(
        135deg,
        #6366f1 0%,
        #a855f7 100%
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
}
.stat-label {
    font-size: 13px;
    color: #64748b;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.sugerencias-box {
    background:
    linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.95) 0%,
        rgba(248, 250, 252, 0.95) 100%
    );
    border: 1.5px solid rgba(99, 102, 241, 0.15);
    border-radius: 24px;
    padding: 28px;
    margin-top: 24px;
    box-shadow:
    0 10px 30px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(8px);
    animation: subir 0.4s ease-out;
}

::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}
::-webkit-scrollbar-track {
    background:
    rgba(99, 102, 241, 0.06);
    border-radius: 20px;
}
::-webkit-scrollbar-thumb {
    background:
    linear-gradient(
        180deg,
        #6366f1 0%,
        #8b5cf6 100%
    );
    border-radius: 20px;
    border: 3px solid rgba(99, 102, 241, 0.06);
    transition: all 0.25s ease;
}

::-webkit-scrollbar-thumb:hover {
    background:
    linear-gradient(
        180deg,
        #4f46e5 0%,
        #7c3aed 100%
    );

    box-shadow: 0 0 10px rgba(99, 102, 241, 0.25);
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
