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

from chatbot.matematicas import (
    es_operacion_matematica,
    explicar_operacion
)

from chatbot.respuestas import (
    respuesta_especial,
    obtener_intro,
    obtener_continuacion
)

from chatbot.temas import (
    detectar_tema
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
# ESTILOS
# =========================================================

st.markdown("""
<style>

/* ======================================================
FONDO
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

    padding-top: 2rem;

    padding-bottom: 8rem;
}

/* ======================================================
TÍTULO
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
CÓDIGO
====================================================== */

.codigo {

    background: #0f172a;

    color: #f8fafc;

    padding: 16px;

    border-radius: 14px;

    font-family: monospace;

    line-height: 1.8;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# CARGAR CONOCIMIENTO
# =========================================================

memoria, preguntas, temas, errores = (
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

if "tema_sugerencias" not in st.session_state:

    st.session_state.tema_sugerencias = (
        st.session_state.tema_actual
    )

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
# TÍTULO
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

    st.success(
        f"Preguntas cargadas: "
        f"{estadisticas['total']}"
    )

    st.markdown("---")

    st.markdown("""
### 📚 Áreas disponibles

💻 Programación  
🤖 Inteligencia Artificial  
🌐 Redes  
🖥️ Hardware  
🔐 Ciberseguridad
""")

    st.markdown("---")

    st.markdown("### 🧮 Operaciones Matemáticas")

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
        "También puedes escribir:\n\n"
        "• cuanto es 10-40\n"
        "• calcula raiz(81)\n"
        "• que es python\n"
        "• que es una red lan"
    )

    st.markdown("---")

    st.subheader("🕘 Historial")

    historiales = obtener_historiales()

    if historiales:

        for archivo in historiales[:10]:

            st.caption(archivo)

    else:

        st.caption(
            "Aún no hay conversaciones guardadas."
        )

    st.markdown("---")

    if st.button("🗑️ Reiniciar conversación"):

        st.session_state.chat = []

        st.session_state.chat_cerrado = False

        st.session_state.tema_actual = random.choice(
            list(temas.keys())
        )

        st.session_state.preguntas_usadas = []

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
# CHAT CERRADO
# =========================================================

if st.session_state.chat_cerrado:

    st.markdown("""

    <div class="chat-bot">

    <h2>👋 Sesión finalizada</h2>

    <p>
    El chatbot cerró correctamente la conversación.
    </p>

    <p>
    Puedes iniciar una nueva conversación desde el panel lateral.
    </p>

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
# INPUT ABAJO
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
    # ACTUALIZAR SUGERENCIAS
    # =====================================================

    disponibles = [

        p for p in temas[tema_detectado]

        if p not in st.session_state.preguntas_usadas
    ]

    if len(disponibles) < 6:

        st.session_state.preguntas_usadas = []

        disponibles = temas[tema_detectado]

    st.session_state.preguntas_sugeridas = (
        random.sample(
            disponibles,
            min(6, len(disponibles))
        )
    )

    # =====================================================
    # SALIR
    # =====================================================

    if texto in ["salir", "quiero salir"]:

        respuesta_final = """

### 👋 Sesión finalizada

El chatbot híbrido educativo ha cerrado correctamente la conversación.

Gracias por utilizar el sistema.

Puedes reiniciar una nueva conversación desde el panel lateral.

        """

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

    elif respuesta_especial(texto):

        respuesta_final = (
            respuesta_especial(texto)
            + "\n\n"
            + obtener_continuacion()
        )

    # =====================================================
    # MATEMÁTICAS
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
                "No encontré información suficiente "
                "para responder esa consulta."
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

        else:

            respuesta_final = (
                "No encontré información suficiente."
            )

        st.session_state.chat.append(
            ("bot", respuesta_final)
        )

        # ================================================
        # NUEVAS SUGERENCIAS
        # ================================================

        tema_actual = st.session_state.tema_actual

        disponibles = [

            p for p in temas[tema_actual]

            if p not in st.session_state.preguntas_usadas
        ]

        if len(disponibles) < 6:

            st.session_state.preguntas_usadas = []

            disponibles = temas[tema_actual]

        st.session_state.preguntas_sugeridas = (
            random.sample(
                disponibles,
                min(6, len(disponibles))
            )
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