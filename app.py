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
# ESTILOS VISUALES
# =========================================================

st.markdown("""
<style>

/* ======================================================
GENERAL
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
CONTENEDOR
====================================================== */

.block-container {

    max-width: 1200px;

    padding-top: 1.5rem;

    padding-bottom: 8rem;
}

/* ======================================================
TITULO
====================================================== */

.titulo {

    text-align: center;

    font-size: 3.4rem;

    font-weight: 800;

    color: #1e3a8a;

    margin-bottom: 10px;
}

.subtitulo {

    text-align: center;

    color: #475569;

    font-size: 1.1rem;

    margin-bottom: 35px;
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

    margin-left: 120px;

    margin-bottom: 16px;

    box-shadow:
    0 6px 18px rgba(37,99,235,0.22);

    animation: aparecer 0.2s ease;
}

/* ======================================================
CHAT BOT
====================================================== */

.chat-bot {

    background: white;

    color: #111827;

    padding: 20px;

    border-radius: 24px;

    margin-right: 120px;

    margin-bottom: 18px;

    border: 1px solid #e2e8f0;

    box-shadow:
    0 5px 18px rgba(0,0,0,0.05);

    animation: aparecer 0.2s ease;
}

/* ======================================================
ANIMACION
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
BOTONES
====================================================== */

div.stButton > button {

    width: 100%;

    border-radius: 16px;

    min-height: 55px;

    font-size: 14px;

    font-weight: 600;

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

    transition: 0.2s;
}

div.stButton > button:hover {

    transform: translateY(-2px);
}

/* ======================================================
CAJA CODIGO
====================================================== */

.codigo {

    background: #0f172a;

    color: #f8fafc;

    padding: 16px;

    border-radius: 14px;

    font-family: monospace;

    line-height: 1.8;

    font-size: 14px;
}

/* ======================================================
CHAT INPUT
====================================================== */

[data-testid="stChatInput"] {

    position: fixed;

    bottom: 15px;

    left: 22rem;

    right: 2rem;

    z-index: 1000;
}

[data-testid="stChatInput"] textarea {

    border-radius: 18px !important;

    border: 2px solid #dbeafe !important;

    padding: 14px !important;

    box-shadow:
    0 2px 12px rgba(0,0,0,0.06);
}

/* ======================================================
TARJETAS
====================================================== */

.card {

    background: white;

    padding: 18px;

    border-radius: 18px;

    border: 1px solid #e2e8f0;

    box-shadow:
    0 4px 14px rgba(0,0,0,0.05);

    margin-bottom: 16px;
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
# TITULO
# =========================================================

st.markdown("""

<div class="titulo">
🤖 Chatbot Híbrido
</div>

<div class="subtitulo">
Sistema educativo inteligente con búsqueda híbrida y resolución matemática avanzada
</div>

""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🤖 Panel del Sistema")

    st.markdown(f"""

<div class="card">

### 📊 Estadísticas

- Total preguntas: {estadisticas['total']}
- Programación: {estadisticas['programacion']}
- IA: {estadisticas['ia']}
- Redes: {estadisticas['redes']}
- Hardware: {estadisticas['hardware']}
- Ciberseguridad: {estadisticas['ciberseguridad']}

</div>

""", unsafe_allow_html=True)

    st.markdown("### 📚 Áreas disponibles")

    st.markdown("""
💻 Programación  
🤖 Inteligencia Artificial  
🌐 Redes  
🖥️ Hardware  
🔐 Ciberseguridad
""")

    st.markdown("---")

    st.markdown("### 🧮 Ejemplos Matemáticos")

    st.markdown("""
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
""", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🕘 Historial")

    historiales = obtener_historiales()

    if historiales:

        for archivo in historiales[:10]:

            st.markdown(f"""
<div class="card">
📄 {archivo}
</div>
""", unsafe_allow_html=True)

    else:

        st.info(
            "Aún no hay conversaciones guardadas."
        )

    st.markdown("---")

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
