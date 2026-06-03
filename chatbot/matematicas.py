# =========================================================
# MODULO MATEMÁTICO
# chatbot/matematicas.py
# =========================================================

import math
import re

# =========================================================
# EXTRAER OPERACIÓN
# =========================================================

def extraer_operacion(texto):

    texto = texto.lower().strip()

    palabras = [
        "cuanto es",
        "calcula",
        "resuelve",
        "resultado de",
        "cuál es",
        "cual es"
    ]

    for palabra in palabras:

        texto = texto.replace(
            palabra,
            ""
        )

    return texto.strip()

# =========================================================
# DETECTAR OPERACIÓN MATEMÁTICA
# =========================================================

def es_operacion_matematica(texto):

    expr = extraer_operacion(
        texto
    )

    # =====================================================
    # SÍMBOLOS
    # =====================================================

    simbolos = [
        "+",
        "-",
        "*",
        "/",
        "^",
        "(",
        ")"
    ]

    # =====================================================
    # FUNCIONES
    # =====================================================

    funciones = [

        r'\braiz\s*\(',
        r'\bsqrt\s*\(',
        r'\blog\s*\(',
        r'\bln\s*\(',
        r'\bsen\s*\(',
        r'\bsin\s*\(',
        r'\bcos\s*\(',
        r'\btan\s*\(',
        r'\bfactorial\s*\(',
        r'\bpi\b',
        r'\be\b'
    ]

    tiene_numero = bool(
        re.search(r'\d', expr)
    )

    # =====================================================
    # OPERADORES
    # =====================================================

    if (
        tiene_numero
        and any(
            s in expr
            for s in simbolos
        )
    ):

        return True

    # =====================================================
    # RESTA
    # =====================================================

    if (
        tiene_numero
        and re.search(
            r'\d\s*-\s*\d',
            expr
        )
    ):

        return True

    # =====================================================
    # FUNCIONES
    # =====================================================

    if any(
        re.search(patron, expr)
        for patron in funciones
    ):

        return True

    return False

# =========================================================
# CONVERTIR EXPRESIÓN
# =========================================================

def convertir_expresion(expr):

    expr = expr.lower().strip()

    # =====================================================
    # POTENCIAS
    # =====================================================

    expr = expr.replace(
        "^",
        "**"
    )

    # =====================================================
    # RAÍZ
    # =====================================================

    expr = re.sub(
        r'raiz\(',
        'sqrt(',
        expr
    )

    # =====================================================
    # SENO
    # =====================================================

    expr = re.sub(
        r'sen\(',
        'sin(',
        expr
    )

    # =====================================================
    # MULTIPLICACIÓN IMPLÍCITA
    # =====================================================

    expr = re.sub(
        r'(\d)(pi|e\b)',
        r'\1*\2',
        expr
    )

    # =====================================================
    # FUNCIONES DISPONIBLES
    # =====================================================

    funciones = {

        "__builtins__": {},

        "sqrt": math.sqrt,

        "log": math.log10,

        "ln": math.log,

        "sin": lambda x:
        math.sin(
            math.radians(x)
        ),

        "cos": lambda x:
        math.cos(
            math.radians(x)
        ),

        "tan": lambda x:
        math.tan(
            math.radians(x)
        ),

        "factorial":
        math.factorial,

        "pi": math.pi,

        "e": math.e,

        "abs": abs
    }

    return expr, funciones

# =========================================================
# FORMATEAR NÚMEROS
# =========================================================

def formatear_numero(valor):

    if (
        isinstance(valor, float)
        and valor.is_integer()
    ):

        return str(
            int(valor)
        )

    return str(
        round(valor, 6)
    )

# =========================================================
# EXPLICAR OPERACIÓN PASO A PASO
# =========================================================

def explicar_operacion(expresion):

    try:

        # =================================================
        # EXPRESIÓN ORIGINAL
        # =================================================

        original = extraer_operacion(
            expresion
        )

        expr, funciones = convertir_expresion(
            original
        )

        pasos = []

        pasos.append(
            "### 🧮 Operación ingresada\n\n"
            f"`{original}`"
        )

        expresion_actual = original

        # =================================================
        # PARÉNTESIS
        # =================================================

        while "(" in expresion_actual:

            coincidencias = re.findall(
                r'\([^()]+\)',
                expresion_actual
            )

            if not coincidencias:

                break

            hubo_cambio = False

            for grupo in coincidencias:

                contenido = grupo[1:-1]

                try:

                    contenido_eval = (
                        contenido
                        .replace("^", "**")
                    )

                    valor = eval(
                        contenido_eval,
                        funciones
                    )

                    valor_txt = (
                        formatear_numero(
                            valor
                        )
                    )

                    pasos.append(
                        f"📌 {contenido} = {valor_txt}"
                    )

                    expresion_actual = (
                        expresion_actual.replace(
                            grupo,
                            valor_txt,
                            1
                        )
                    )

                    hubo_cambio = True

                except:

                    pass

            if not hubo_cambio:

                break

        # =================================================
        # POTENCIAS
        # =================================================

        coincidencias_pot = re.findall(
            r'(\d+\.?\d*)\s*\^\s*(\d+\.?\d*)',
            original
        )

        for base, exponente in coincidencias_pot:

            resultado = (
                float(base)
                **
                float(exponente)
            )

            pasos.append(
                f"📌 {base}^{exponente} = "
                f"{formatear_numero(resultado)}"
            )

        # =================================================
        # FUNCIONES ESPECIALES
        # =================================================

        funciones_especiales = [

            ("raiz", r'raiz\((.*?)\)'),

            ("log", r'log\((.*?)\)'),

            ("ln", r'ln\((.*?)\)'),

            ("sen", r'sen\((.*?)\)'),

            ("cos", r'cos\((.*?)\)'),

            ("tan", r'tan\((.*?)\)'),

            ("factorial", r'factorial\((.*?)\)')
        ]

        for nombre, patron in funciones_especiales:

            encontrados = re.findall(
                patron,
                original
            )

            for valor in encontrados:

                try:

                    operacion = (
                        f"{nombre}({valor})"
                    )

                    operacion_eval = (
                        operacion
                        .replace("^", "**")
                        .replace("raiz", "sqrt")
                        .replace("sen", "sin")
                    )

                    resultado = eval(
                        operacion_eval,
                        funciones
                    )

                    pasos.append(
                        f"📌 {operacion} = "
                        f"{formatear_numero(resultado)}"
                    )

                except:

                    pass

        # =================================================
        # RESULTADO FINAL
        # =================================================

        resultado_final = eval(
            expr,
            funciones
        )

        resultado_final = (
            formatear_numero(
                resultado_final
            )
        )

        pasos.append(
            "\n### ✅ Resultado final"
        )

        pasos.append(
            f"## {resultado_final}"
        )

        return "\n\n".join(
            pasos
        )

    except Exception as e:

        return (
            "❌ No fue posible resolver "
            "la operación matemática.\n\n"
            f"Detalle del error: {e}"
        )
