# =========================================================
# CHATBOT HÍBRIDO IA + MATEMÁTICAS + IA SEMÁNTICA
# STREAMLIT VERSION PROFESIONAL
# =========================================================

import streamlit as st
from difflib import get_close_matches
import random
import os
import re
import numpy as np
from datetime import datetime

# IA SEMÁNTICA
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

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
✅ IA semántica inteligente  
✅ Resolución matemática  
✅ Explicación de operaciones  
✅ Sugerencias automáticas  
✅ Coincidencias aproximadas  
""")

# =========================================================
# MEMORIA
# =========================================================

memoria = {}

# =========================================================
# CARGAR TXT
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

                memoria[pregunta] = respuesta

    except Exception as e:

        errores.append(str(e))

preguntas = list(memoria.keys())

# =========================================================
# IA SEMÁNTICA
# =========================================================

st.sidebar.header("🧠 IA Semántica")

with st.spinner("Cargando modelo IA..."):

    fragmentos = []

    for p, r in memoria.items():

        fragmentos.append(
            f"Pregunta: {p}\nRespuesta: {r}"
        )

    modelo = SentenceTransformer(
        'paraphrase-multilingual-MiniLM-L12-v2'
    )

    embeddings = modelo.encode(
        fragmentos,
        show_progress_bar=False
    )

st.sidebar.success("Modelo IA cargado")

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("---")

    st.success(
        f"Preguntas cargadas: {len(preguntas)}"
    )

    st.markdown("---")

    st.subheader("📚 Temáticas")

    st.write("💻 Programación")
    st.write("🧠 Inteligencia Artificial")
    st.write("🌐 Redes")
    st.write("🖥️ Hardware")
    st.write("🔐 Ciberseguridad")

    st.markdown("---")

    if st.button("🗑️ Limpiar Chat"):

        st.session_state.chat = []

        st.rerun()

# =========================================================
# FRASES
# =========================================================

introducciones = [
    "Excelente pregunta.",
    "Claro, aquí tienes la información.",
    "Con gusto responderé.",
    "Estoy procesando tu consulta."
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

    return None

# =========================================================
# OPERACIONES MATEMÁTICAS
# =========================================================

def es_operacion_matematica(texto):

    patron = r'^[0-9\\+\\-\\*\\/\\.\\(\\) ]+$'

    return re.match(
        patron,
        texto
    )

def explicar_operacion(expresion, resultado):

    explicacion = (
        f"La operación matemática ingresada fue: "
        f"{expresion}. "
        f"Después de resolverla paso a paso, "
        f"el resultado obtenido es {resultado}. "
        f"El sistema evaluó correctamente los "
        f"operadores matemáticos y realizó el "
        f"cálculo respetando el orden de prioridad."
    )

    return explicacion

def resolver_operacion(expresion):

    try:

        resultado = eval(expresion)

        explicacion = explicar_operacion(
            expresion,
            resultado
        )

        return explicacion

    except:

        return (
            "Ocurrió un error al resolver "
            "la operación matemática."
        )

# =========================================================
# IA SEMÁNTICA
# =========================================================

def buscar_semantico(pregunta):

    emb_pregunta = modelo.encode([pregunta])

    similitudes = cosine_similarity(
        emb_pregunta,
        embeddings
    )[0]

    indice = np.argmax(similitudes)

    score = similitudes[indice]

    respuesta = fragmentos[indice]

    return respuesta, score

# =========================================================
# BÚSQUEDA NORMAL
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
# PROCESAR
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
    # BÚSQUEDA NORMAL
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

            # =============================================
            # IA SEMÁNTICA
            # =============================================

            respuesta_sem,
            score_sem = buscar_semantico(texto)

            if score_sem > 0.35:

                respuesta_final = (
                    "🧠 Respuesta obtenida "
                    "mediante IA semántica:\n\n"
                    f"{respuesta_sem}\n\n"
                    f"Nivel de confianza: "
                    f"{score_sem:.2f}"
                )

            else:

                respuesta_final = (
                    "No encontré información suficiente."
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

    with st.expander(
        "⚠️ Ver errores del sistema"
    ):

        for e in errores:

            st.error(e)

