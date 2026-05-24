# =========================================================
# CHATBOT HÍBRIDO EDUCATIVO IA
# =========================================================

import streamlit as st
from difflib import get_close_matches
import random
import os
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
# CSS PERSONALIZADO
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

h1 {
    color: #38bdf8;
    text-align: center;
}

.stChatMessage {
    border-radius: 15px;
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

st.title("🤖 Chatbot Híbrido")

st.markdown("""
### Temáticas disponibles

- 💻 Programación
- 🧠 Inteligencia Artificial
- 🌐 Redes
- 🖥️ Hardware
- 🔐 Ciberseguridad
""")

# =========================================================
# MEMORIA
# =========================================================

memoria = {}

# =========================================================
# RUTA ACTUAL
# =========================================================

carpeta_actual = os.path.dirname(os.path.abspath(__file__))

archivos = [
    "programacion.txt",
    "ia.txt",
    "redes.txt",
    "hardware.txt",
    "ciberseguridad.txt"
]

# =========================================================
# CARGAR ARCHIVOS
# =========================================================

errores = []

for archivo in archivos:

    ruta = os.path.join(carpeta_actual, archivo)

    try:

        with open(ruta, 'r', encoding='utf-8') as f:

            txt = f.read().strip()

        lineas = [l for l in txt.split('\n') if l]

        for numero, l in enumerate(lineas, start=1):

            try:

                if '?r:' in l:

                    q, r = l.split('?r:')

                    pregunta = q.replace(
                        'p:',
                        ''
                    ).strip().lower()

                    respuesta = r.strip()

                    if pregunta and respuesta:

                        memoria[pregunta] = respuesta

                else:

                    errores.append(
                        f"Formato incorrecto en {archivo} línea {numero}"
                    )

            except:

                errores.append(
                    f"Error procesando {archivo} línea {numero}"
                )

    except Exception as e:

        errores.append(f"No se pudo cargar {archivo}")
        errores.append(str(e))

preguntas = list(memoria.keys())

# =========================================================
# VALIDAR
# =========================================================

if len(preguntas) == 0:

    st.error("No se cargaron preguntas.")

    st.stop()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📚 Información")

    st.success(f"Preguntas cargadas: {len(preguntas)}")

    

    if st.button("🗑️ Limpiar conversación"):

        st.session_state.chat = []

        st.rerun()

# =========================================================
# FRASES NATURALES
# =========================================================

introducciones = [
    "Excelente pregunta.",
    "Claro, aquí tienes la respuesta.",
    "Con gusto responderé tu consulta.",
    "Estoy analizando tu pregunta."
]

continuar = [
    "¿Deseas preguntar algo más?",
    "¿Tienes otra consulta?",
    "¿Puedo ayudarte nuevamente?"
]

# =========================================================
# RESPUESTAS ESPECIALES
# =========================================================

def respuesta_especial(q):

    q = q.lower()

    if "hora" in q:

        return (
            f"La hora actual aproximada es "
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
            "desarrollado en Python."
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
# BUSCAR RESPUESTA
# =========================================================

def buscar_respuesta(
    pregunta_usuario,
    cutoff=0.55
):

    pregunta_usuario = (
        pregunta_usuario.lower().strip()
    )

    # EXACTA
    if pregunta_usuario in memoria:

        return memoria[pregunta_usuario], 1.0

    # APROXIMADA
    coincidencias = get_close_matches(
        pregunta_usuario,
        preguntas,
        n=1,
        cutoff=cutoff
    )

    if coincidencias:

        pregunta_encontrada = coincidencias[0]

        similitud = len(
            set(pregunta_usuario) &
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
# SUGERENCIAS
# =========================================================

def obtener_sugerencias(texto):

    sugerencias = get_close_matches(
        texto.lower(),
        preguntas,
        n=5,
        cutoff=0.25
    )

    return sugerencias

# =========================================================
# SESSION STATE
# =========================================================

if "chat" not in st.session_state:

    st.session_state.chat = []

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

    especial = respuesta_especial(pregunta)

    if especial:

        respuesta_final = (
            especial
            + "\n\n"
            + random.choice(continuar)
        )

    else:

        respuesta, score = buscar_respuesta(
            pregunta
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
                "No encontré una respuesta exacta."
            )

            sugerencias = obtener_sugerencias(
                pregunta
            )

            if sugerencias:

                respuesta_final += (
                    "\n\nQuizá quisiste preguntar:\n"
                )

                for s in sugerencias:

                    respuesta_final += f"\n• {s}"

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
# SUGERENCIAS VISUALES
# =========================================================

st.markdown("---")

st.subheader("💡 Preguntas sugeridas")

ejemplos = random.sample(
    preguntas,
    min(8, len(preguntas))
)

col1, col2 = st.columns(2)

for i, ejemplo in enumerate(ejemplos):

    if i % 2 == 0:

        if col1.button(
            ejemplo,
            key=f"sug_{i}"
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

    else:

        if col2.button(
            ejemplo,
            key=f"sug_{i}"
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
# ERRORES
# =========================================================

if errores:

    with st.expander("⚠️ Ver errores del sistema"):

        for e in errores:

            st.error(e)
