# =========================================================
# MODULO DE SUGERENCIAS
# chatbot/sugerencias.py
# =========================================================

import random

# =========================================================
# CANTIDAD DE SUGERENCIAS
# =========================================================

MAX_SUGERENCIAS = 6

# =========================================================
# OBTENER SUGERENCIAS POR TEMA
# =========================================================

def obtener_sugerencias(
    tema,
    temas,
    cantidad=MAX_SUGERENCIAS
):

    # =====================================================
    # VALIDAR TEMA
    # =====================================================

    if tema not in temas:

        return []

    preguntas = temas[tema]

    # =====================================================
    # VALIDAR LISTA VACÍA
    # =====================================================

    if not preguntas:

        return []

    # =====================================================
    # LIMITAR CANTIDAD
    # =====================================================

    cantidad = min(
        cantidad,
        len(preguntas)
    )

    # =====================================================
    # RETORNAR ALEATORIAS
    # =====================================================

    return random.sample(
        preguntas,
        cantidad
    )

# =========================================================
# ACTUALIZAR SUGERENCIAS
# =========================================================

def actualizar_sugerencias(
    st,
    tema_actual,
    temas
):

    # =====================================================
    # PRIMERA CARGA
    # =====================================================

    if "tema_sugerencias" not in st.session_state:

        st.session_state.tema_sugerencias = (
            tema_actual
        )

    # =====================================================
    # PRIMERA LISTA
    # =====================================================

    if "preguntas_sugeridas" not in st.session_state:

        st.session_state.preguntas_sugeridas = (
            obtener_sugerencias(
                tema_actual,
                temas
            )
        )

    # =====================================================
    # CAMBIO DE TEMA
    # =====================================================

    if (
        st.session_state.tema_sugerencias
        != tema_actual
    ):

        st.session_state.tema_sugerencias = (
            tema_actual
        )

        st.session_state.preguntas_sugeridas = (
            obtener_sugerencias(
                tema_actual,
                temas
            )
        )

# =========================================================
# MOSTRAR BOTONES
# =========================================================

def mostrar_sugerencias(
    st,
    preguntas_sugeridas
):

    if not preguntas_sugeridas:

        return None

    st.markdown("---")

    st.subheader(
        "💡 Preguntas sugeridas"
    )

    col1, col2 = st.columns(2)

    pregunta_seleccionada = None

    # =====================================================
    # CREAR BOTONES
    # =====================================================

    for i, pregunta in enumerate(
        preguntas_sugeridas
    ):

        columna = (
            col1
            if i % 2 == 0
            else col2
        )

        if columna.button(
            pregunta,
            key=f"sugerencia_{i}",
            use_container_width=True
        ):

            pregunta_seleccionada = (
                pregunta
            )

    return pregunta_seleccionada

# =========================================================
# REINICIAR SUGERENCIAS
# =========================================================

def reiniciar_sugerencias(
    st,
    tema,
    temas
):

    st.session_state.tema_sugerencias = (
        tema
    )

    st.session_state.preguntas_sugeridas = (
        obtener_sugerencias(
            tema,
            temas
        )
    )

# =========================================================
# OBTENER TEMA ALEATORIO
# =========================================================

def obtener_tema_aleatorio(
    temas
):

    lista_temas = list(
        temas.keys()
    )

    if not lista_temas:

        return "programacion"

    return random.choice(
        lista_temas
    )

# =========================================================
# GENERAR SUGERENCIAS INICIALES
# =========================================================

def generar_sugerencias_iniciales(
    temas
):

    tema = obtener_tema_aleatorio(
        temas
    )

    preguntas = obtener_sugerencias(
        tema,
        temas
    )

    return tema, preguntas
