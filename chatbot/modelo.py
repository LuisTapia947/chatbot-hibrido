# =========================================================
# modelo PRINCIPAL DEL CHATBOT
# chatbot/modelo.py
# =========================================================

from chatbot.matematicas import (
    es_operacion_matematica,
    resolver_operacion
)

from chatbot.conocimiento import (
    buscar_respuesta
)

from chatbot.respuestas import (
    respuesta_especial,
    construir_respuesta,
    mensaje_sin_respuesta,
    es_comando_salida,
    mensaje_despedida
)

from chatbot.temas import (
    detectar_tema
)

from chatbot.historial import (
    guardar_chat,
    obtener_historiales
)

# =========================================================
# PROCESAR MENSAJE
# =========================================================

def procesar_mensaje(

    mensaje_usuario,

    memoria,
    preguntas,
    temas
):

    # =====================================================
    # LIMPIAR TEXTO
    # =====================================================

    texto = (
        mensaje_usuario
        .lower()
        .strip()
    )

    # =====================================================
    # DETECTAR TEMA
    # =====================================================

    tema_detectado = detectar_tema(
        texto
    )

    # =====================================================
    # RESPUESTA BASE
    # =====================================================

    respuesta = {

        "tipo": None,

        "mensaje": "",

        "tema": tema_detectado,

        "cerrar_chat": False
    }

    # =====================================================
    # COMANDO SALIR
    # =====================================================

    if es_comando_salida(texto):

        respuesta["tipo"] = "salida"

        respuesta["mensaje"] = (
            mensaje_despedida()
        )

        respuesta["cerrar_chat"] = True

        return respuesta

    # =====================================================
    # RESPUESTAS ESPECIALES
    # =====================================================

    especial = respuesta_especial(
        texto
    )

    if especial:

        respuesta["tipo"] = "especial"

        respuesta["mensaje"] = especial

        return respuesta

    # =====================================================
    # OPERACIONES MATEMÁTICAS
    # =====================================================

    if es_operacion_matematica(
        texto
    ):

        resultado = resolver_operacion(
            texto
        )

        respuesta["tipo"] = (
            "matematica"
        )

        respuesta["mensaje"] = (
            resultado["respuesta"]
        )

        return respuesta

    # =====================================================
    # BÚSQUEDA EN CONOCIMIENTO
    # =====================================================

    resultado_busqueda = (
        buscar_respuesta(
            texto,
            memoria,
            preguntas
        )
    )

    # =====================================================
    # RESPUESTA ENCONTRADA
    # =====================================================

    if resultado_busqueda["respuesta"]:

        respuesta["tipo"] = (
            "conocimiento"
        )

        respuesta["mensaje"] = (
            construir_respuesta(
                resultado_busqueda[
                    "respuesta"
                ],
                resultado_busqueda[
                    "score"
                ]
            )
        )

        return respuesta

    # =====================================================
    # SIN RESPUESTA
    # =====================================================

    respuesta["tipo"] = (
        "sin_respuesta"
    )

    respuesta["mensaje"] = (
        mensaje_sin_respuesta()
    )

    return respuesta

# =========================================================
# INICIALIZAR CHAT
# =========================================================

def inicializar_chat(st, temas):

    # =====================================================
    # CHAT
    # =====================================================

    if "chat" not in st.session_state:

        st.session_state.chat = []

    # =====================================================
    # CHAT CERRADO
    # =====================================================

    if (
        "chat_cerrado"
        not in st.session_state
    ):

        st.session_state.chat_cerrado = (
            False
        )

    # =====================================================
    # TEMA ACTUAL
    # =====================================================

    if (
        "tema_actual"
        not in st.session_state
    ):

        st.session_state.tema_actual = (
            list(temas.keys())[0]
        )

# =========================================================
# AGREGAR MENSAJE
# =========================================================

def agregar_mensaje(

    st,
    tipo,
    mensaje
):

    st.session_state.chat.append(
        (
            tipo,
            mensaje
        )
    )

# =========================================================
# REINICIAR CHAT
# =========================================================

def reiniciar_chat(st):

    st.session_state.chat = []

    st.session_state.chat_cerrado = (
        False
    )

# =========================================================
# CHAT CERRADO
# =========================================================

def chat_esta_cerrado(st):

    return (
        st.session_state.chat_cerrado
    )

# =========================================================
# CERRAR CHAT
# =========================================================

def cerrar_chat(st):

    st.session_state.chat_cerrado = (
        True
    )
