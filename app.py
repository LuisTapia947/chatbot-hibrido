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
# OPERACIONES MATEMÁTICAS INTELIGENTES
# =========================================================

def es_operacion_matematica(texto):

    patron = r'^[0-9\+\-\*\/\.\(\)\ ]+$'

    return re.match(
        patron,
        texto
    )

# =========================================================
# EXPLICAR OPERACION PASO A PASO
# =========================================================

def explicar_operacion(expresion):

    try:

        expr = expresion.replace(" ", "")

        explicacion = []

        explicacion.append(
            f"📌 Operación ingresada:\n\n{expr}"
        )

        explicacion.append(
            "\n📖 Desarrollo paso a paso:"
        )

        # ============================================
        # PASO 1
        # ============================================

        if "(" in expr:

            explicacion.append(
                "\n1️⃣ Primero se resuelven "
                "las operaciones dentro "
                "de los paréntesis."
            )

        # ============================================
        # POTENCIAS
        # ============================================

        if "**" in expr:

            explicacion.append(
                "\n2️⃣ Luego se calculan "
                "las potencias."
            )

        # ============================================
        # MULTIPLICACION Y DIVISION
        # ============================================

        if "*" in expr or "/" in expr:

            explicacion.append(
                "\n3️⃣ Después se realizan "
                "las multiplicaciones y divisiones "
                "de izquierda a derecha."
            )

        # ============================================
        # SUMAS Y RESTAS
        # ============================================

        if "+" in expr or "-" in expr[1:]:

            explicacion.append(
                "\n4️⃣ Finalmente se resuelven "
                "las sumas y restas."
            )

        # ============================================
        # RESULTADO
        # ============================================

        resultado = eval(expr)

        explicacion.append(
            f"\n🧮 Resultado final:\n\n{resultado}"
        )

        explicacion.append(
            "\n✅ La operación fue resuelta "
            "aplicando correctamente la jerarquía "
            "de operadores matemáticos."
        )

        return "".join(explicacion)

    except:

        return (
            "❌ Ocurrió un error al resolver "
            "la operación matemática."
        )

# =========================================================
# RESOLVER OPERACION
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

