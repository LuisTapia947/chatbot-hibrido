# =========================================================
# MODULO MATEMÁTICO
# chatbot/matematicas.py
# =========================================================

import math
import re

# =========================================================
# FRASES DE INTRODUCCIÓN A ELIMINAR
# =========================================================

FRASES_PREFIJO = [
    "por favor calcula",
    "por favor resuelve",
    "puedes calcular",
    "puedes resolver",
    "puedes decirme cuanto es",
    "puedes decirme cuanto da",
    "dime cuanto es",
    "dime cuanto da",
    "dime el resultado de",
    "cuanto da la operacion",
    "cuanto da la",
    "cuanto es el resultado de",
    "cual es el resultado de",
    "cuál es el resultado de",
    "cual es el valor de",
    "cuál es el valor de",
    "resultado de la operacion",
    "resultado de",
    "cuanto es",
    "cuanto da",
    "calcula",
    "resuelve",
    "cuál es",
    "cual es",
    "opera",
    "evalua",
    "evalúa",
    "haz la operacion",
    "haz la operación",
]

# =========================================================
# PALABRAS DE RELLENO A ELIMINAR (DESPUÉS DE LAS FRASES)
# =========================================================

PALABRAS_RELLENO = [
    "operacion",
    "operación",
    "siguiente",
    "esto",
    "esta",
    "valor",
    "numero",
    "número",
    "siguiente",
    "por",
    "favor",
    "por favor",
    "dime",
    "puedes",
    "el",
    "la",
    "de",
    "lo",
    "que",
]

# =========================================================
# EXTRAER OPERACIÓN
# =========================================================

def extraer_operacion(texto):

    texto = texto.lower().strip()

    # =====================================================
    # ELIMINAR SIGNOS DE PUNTUACIÓN Y CARACTERES EXTRAÑOS
    # =====================================================

    texto = re.sub(r'[¿?¡!,;:\.]', '', texto)

    # =====================================================
    # ORDENAR FRASES DE MÁS LARGA A MÁS CORTA
    # para evitar que "cuanto es" elimine parte de
    # "cuanto es el resultado de" antes de que esta se evalúe
    # =====================================================

    frases_ordenadas = sorted(
        FRASES_PREFIJO,
        key=len,
        reverse=True
    )

    for frase in frases_ordenadas:

        if texto.startswith(frase):
            texto = texto[len(frase):]
            break

        texto = texto.replace(frase, "")

    # =====================================================
    # ELIMINAR PALABRAS DE RELLENO QUE QUEDAN SUELTAS
    # Solo al inicio del texto para no tocar la expresión
    # =====================================================

    palabras_relleno_ordenadas = sorted(
        PALABRAS_RELLENO,
        key=len,
        reverse=True
    )

    cambio = True

    while cambio:

        cambio = False

        for palabra in palabras_relleno_ordenadas:

            patron = r'^\s*' + re.escape(palabra) + r'\s+'

            nuevo = re.sub(patron, '', texto)

            if nuevo != texto:

                texto = nuevo
                cambio = True

    # =====================================================
    # LIMPIAR ESPACIOS DOBLES Y RESIDUOS FINALES
    # =====================================================

    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto

# =========================================================
# DETECTAR OPERACIÓN MATEMÁTICA
# =========================================================

def es_operacion_matematica(texto):

    expr = extraer_operacion(texto)

    # =====================================================
    # DESCARTAR TEXTOS QUE SON CLARAMENTE LENGUAJE NATURAL
    # Si después de extraer queda algo sin números ni
    # funciones matemáticas, no es una operación
    # =====================================================

    if not expr:
        return False

    # =====================================================
    # SÍMBOLOS MATEMÁTICOS
    # =====================================================

    simbolos = [
        "+",
        "*",
        "/",
        "^",
    ]

    # =====================================================
    # PATRONES DE FUNCIONES MATEMÁTICAS
    # =====================================================

    patrones_funciones = [
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
        r'\be\b',
    ]

    tiene_numero = bool(re.search(r'\d', expr))

    # =====================================================
    # REGLA 1: número + operador aritmético básico
    # =====================================================

    if tiene_numero and any(s in expr for s in simbolos):
        return True

    # =====================================================
    # REGLA 2: resta explícita entre dos números
    # (separada para evitar falsos positivos con guiones)
    # =====================================================

    if tiene_numero and re.search(r'\d\s*-\s*\d', expr):
        return True

    # =====================================================
    # REGLA 3: paréntesis con número adentro
    # =====================================================

    if tiene_numero and re.search(r'\(\s*\d', expr):
        return True

    # =====================================================
    # REGLA 4: función matemática reconocida
    # =====================================================

    if any(re.search(patron, expr) for patron in patrones_funciones):
        return True

    # =====================================================
    # REGLA 5: expresión que es solo un número
    # (ej: el usuario escribe "25" solo — no es operación)
    # =====================================================

    return False

# =========================================================
# CONVERTIR EXPRESIÓN
# =========================================================

def convertir_expresion(expr):

    expr = expr.lower().strip()

    # =====================================================
    # POTENCIAS
    # =====================================================

    expr = expr.replace("^", "**")

    # =====================================================
    # RAÍZ
    # =====================================================

    expr = re.sub(r'raiz\(', 'sqrt(', expr)

    # =====================================================
    # SENO
    # =====================================================

    expr = re.sub(r'sen\(', 'sin(', expr)

    # =====================================================
    # MULTIPLICACIÓN IMPLÍCITA: 2pi → 2*pi, 3e → 3*e
    # =====================================================

    expr = re.sub(r'(\d)(pi|e\b)', r'\1*\2', expr)

    # =====================================================
    # FUNCIONES DISPONIBLES PARA eval()
    # =====================================================

    funciones = {

        "__builtins__": {},

        "sqrt":     math.sqrt,
        "log":      math.log10,
        "ln":       math.log,
        "sin":      lambda x: math.sin(math.radians(x)),
        "cos":      lambda x: math.cos(math.radians(x)),
        "tan":      lambda x: math.tan(math.radians(x)),
        "factorial": math.factorial,
        "pi":       math.pi,
        "e":        math.e,
        "abs":      abs,
    }

    return expr, funciones

# =========================================================
# FORMATEAR NÚMEROS
# =========================================================

def formatear_numero(valor):

    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))

    return str(round(valor, 6))

# =========================================================
# EXPLICAR OPERACIÓN PASO A PASO
# =========================================================

def explicar_operacion(expresion):

    try:

        # =================================================
        # EXPRESIÓN ORIGINAL LIMPIA
        # =================================================

        original = extraer_operacion(expresion)

        expr, funciones = convertir_expresion(original)

        pasos = []

        pasos.append(
            "🧮 **Operación ingresada**\n\n"
            f"`{original}`"
        )

        expresion_actual = original

        # =================================================
        # PASO A PASO: FUNCIONES ESPECIALES PRIMERO
        # (se resuelven antes que los paréntesis generales)
        # =================================================

        DESCRIPCIONES = {
            "raiz":      "Raíz cuadrada: se busca el número que multiplicado por sí mismo da {arg}",
            "sqrt":      "Raíz cuadrada: se busca el número que multiplicado por sí mismo da {arg}",
            "log":       "Logaritmo base 10: ¿a qué potencia hay que elevar 10 para obtener {arg}?",
            "ln":        "Logaritmo natural: ¿a qué potencia hay que elevar e (≈2.718) para obtener {arg}?",
            "sen":       "Seno: razón trigonométrica del ángulo {arg}°",
            "sin":       "Seno: razón trigonométrica del ángulo {arg}°",
            "cos":       "Coseno: razón trigonométrica del ángulo {arg}°",
            "tan":       "Tangente: razón trigonométrica del ángulo {arg}°",
            "factorial": "Factorial: se multiplica {arg} × ({arg}-1) × ({arg}-2) × ... × 1",
        }

        funciones_especiales = [
            ("raiz",      r'raiz\((.*?)\)'),
            ("log",       r'log\((.*?)\)'),
            ("ln",        r'ln\((.*?)\)'),
            ("sen",       r'sen\((.*?)\)'),
            ("cos",       r'cos\((.*?)\)'),
            ("tan",       r'tan\((.*?)\)'),
            ("factorial", r'factorial\((.*?)\)'),
        ]

        for nombre, patron in funciones_especiales:

            encontrados = re.findall(patron, original)

            for argumento in encontrados:

                try:

                    operacion      = f"{nombre}({argumento})"
                    operacion_eval = (
                        operacion
                        .replace("^", "**")
                        .replace("raiz", "sqrt")
                        .replace("sen",  "sin")
                    )

                    resultado  = eval(operacion_eval, funciones)
                    res_txt    = formatear_numero(resultado)
                    descripcion = DESCRIPCIONES.get(nombre, "").format(arg=argumento)

                    pasos.append(
                        f"📌 **Paso — {nombre.capitalize()}**\n\n"
                        f"> {descripcion}\n\n"
                        f"`{operacion}` = **{res_txt}**"
                    )

                except:
                    pass

                # =================================================
        # PASO A PASO: PARÉNTESIS ANIDADOS
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
                contenido_eval = contenido.replace("^", "**")

                try:

                    valor = eval(contenido_eval, funciones)
                    valor_txt = formatear_numero(valor)

                    # Ignorar paréntesis que contienen solo un número
                    es_numero_simple = bool(
                        re.fullmatch(
                            r'\s*-?\d+(\.\d+)?\s*',
                            contenido
                        )
                    )

                    # Detectar si pertenece a una función ya explicada
                    es_funcion_especial = any(
                        re.search(
                            r'\b' + fn + r'\s*$',
                            expresion_actual[:expresion_actual.index(grupo)]
                        )
                        for fn in [
                            "sqrt",
                            "sin",
                            "cos",
                            "tan",
                            "log",
                            "ln",
                            "factorial"
                        ]
                        if grupo in expresion_actual
                    )

                    if not es_numero_simple and not es_funcion_especial:

                        pasos.append(
                            f"📌 **Paso — Subexpresión entre paréntesis**\n\n"
                            f"`({contenido})` → se resuelve primero por jerarquía\n\n"
                            f"`{contenido}` = **{valor_txt}**"
                        )

                    expresion_actual = expresion_actual.replace(
                        grupo,
                        valor_txt,
                        1
                    )

                    hubo_cambio = True

                except:
                    pass

            if not hubo_cambio:
                break



        # =================================================
        # PASO A PASO: POTENCIAS
        # =================================================

        coincidencias_pot = re.findall(
            r'(\d+\.?\d*)\s*\^\s*(\d+\.?\d*)',
            original
        )

        for base, exponente in coincidencias_pot:

            resultado = float(base) ** float(exponente)

            pasos.append(
                f"📌 **Paso — Potencia**\n\n"
                f"> Se multiplica {base} por sí mismo {exponente} veces\n\n"
                f"`{base}^{exponente}` = **{formatear_numero(resultado)}**"
            )

               # =================================================
        # PASO A PASO: JERARQUÍA ARITMÉTICA
        # Explica el orden en que se resuelve la expresión
        # =================================================

        tiene_mult_div = bool(re.search(r'[\*\/]', expr))
        tiene_suma_res = bool(
            re.search(r'(?<!\*\*)\d+\.?\d*\s*[\+\-]\s*\d+\.?\d*', expr)
        )

        if tiene_mult_div and tiene_suma_res:

            pasos.append(
                "📋 **Jerarquía de operaciones**\n\n"
                "> Por orden de operaciones: primero `×` y `÷`, luego `+` y `−`"
            )

            expr_simplificada = expr

            # =========================================
            # Multiplicaciones y divisiones
            # =========================================

            partes = re.split(
                r'(\d+\.?\d*\s*[\*\/]\s*\d+\.?\d*)',
                expr
            )

            for parte in partes:

                parte_limpia = parte.strip()

                if re.match(
                    r'^\d+\.?\d*\s*[\*\/]\s*\d+\.?\d*$',
                    parte_limpia
                ):

                    try:

                        val = eval(parte_limpia, funciones)
                        val_txt = formatear_numero(val)

                        simbolo = "×" if "*" in parte_limpia else "÷"
                        nums = re.split(r'[\*\/]', parte_limpia)

                        pasos.append(
                            f"📌 **Paso — {'Multiplicación' if simbolo == '×' else 'División'}**\n\n"
                            f"`{nums[0].strip()} {simbolo} {nums[1].strip()}` = **{val_txt}**"
                        )

                        expr_simplificada = expr_simplificada.replace(
                            parte_limpia,
                            val_txt,
                            1
                        )

                    except:
                        pass

            # =========================================
            # Suma o resta final
            # =========================================

            try:

                if re.search(
                    r'\d+\.?\d*\s*[\+\-]\s*\d+\.?\d*',
                    expr_simplificada
                ):

                    resultado_final_operacion = eval(
                        expr_simplificada,
                        funciones
                    )

                    simbolo = "+" if "+" in expr_simplificada else "−"

                    if simbolo == "+":
                        nums = expr_simplificada.split("+")
                    else:
                        nums = expr_simplificada.split("-")

                    if len(nums) == 2:

                        pasos.append(
                            f"📌 **Paso — {'Suma' if simbolo == '+' else 'Resta'}**\n\n"
                            f"`{nums[0].strip()} {simbolo} {nums[1].strip()}` = "
                            f"**{formatear_numero(resultado_final_operacion)}**"
                        )

            except:
                pass

        elif tiene_mult_div:

            partes = re.split(
                r'(\d+\.?\d*\s*[\*\/]\s*\d+\.?\d*)',
                expr
            )

            for parte in partes:

                parte_limpia = parte.strip()

                if re.match(
                    r'^\d+\.?\d*\s*[\*\/]\s*\d+\.?\d*$',
                    parte_limpia
                ):

                    try:

                        val = eval(parte_limpia, funciones)
                        val_txt = formatear_numero(val)

                        simbolo = "×" if "*" in parte_limpia else "÷"
                        nums = re.split(r'[\*\/]', parte_limpia)

                        pasos.append(
                            f"📌 **Paso — {'Multiplicación' if simbolo == '×' else 'División'}**\n\n"
                            f"`{nums[0].strip()} {simbolo} {nums[1].strip()}` = **{val_txt}**"
                        )

                    except:
                        pass

        elif tiene_suma_res:

            partes = re.split(
                r'(\d+\.?\d*\s*[\+\-]\s*\d+\.?\d*)',
                expr
            )

            for parte in partes:

                parte_limpia = parte.strip()

                if re.match(
                    r'^\d+\.?\d*\s*[\+\-]\s*\d+\.?\d*$',
                    parte_limpia
                ):

                    try:

                        val = eval(parte_limpia, funciones)
                        val_txt = formatear_numero(val)

                        simbolo = "+" if "+" in parte_limpia else "−"
                        nums = re.split(r'[\+\-]', parte_limpia)

                        pasos.append(
                            f"📌 **Paso — {'Suma' if simbolo == '+' else 'Resta'}**\n\n"
                            f"`{nums[0].strip()} {simbolo} {nums[1].strip()}` = **{val_txt}**"
                        )

                    except:
                        pass
        # =================================================
        # RESULTADO FINAL
        # =================================================

        resultado_final = eval(expr, funciones)
        resultado_final = formatear_numero(resultado_final)

        pasos.append("\n✅ **Resultado final**")
        pasos.append(f"## {resultado_final}")

        return "\n\n".join(pasos)

    except Exception as e:

        return (
            "❌ No fue posible resolver la operación matemática.\n\n"
            f"Detalle del error: `{e}`"
        )
