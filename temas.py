# =========================================================
# MODULO DE TEMAS
# chatbot/temas.py
# =========================================================

import random
import re

# =========================================================
# PALABRAS CLAVE POR TEMA
# =========================================================

PALABRAS_CLAVE = {

    "programacion": [

        "python",
        "java",
        "c++",
        "c#",
        "javascript",
        "html",
        "css",
        "programacion",
        "algoritmo",
        "variable",
        "funcion",
        "clase",
        "objeto",
        "codigo",
        "compilar",
        "software",
        "programa",
        "desarrollo",
        "backend",
        "frontend"
    ],

    "ia": [

        "ia",
        "inteligencia",
        "artificial",
        "machine",
        "learning",
        "deep",
        "red",
        "neuronal",
        "chatbot",
        "modelo",
        "datos",
        "openai",
        "automatizacion",
        "robot",
        "vision",
        "lenguaje"
    ],

    "redes": [

        "red",
        "router",
        "switch",
        "ip",
        "tcp",
        "udp",
        "wifi",
        "internet",
        "lan",
        "wan",
        "servidor",
        "cliente",
        "dns",
        "dhcp",
        "ethernet",
        "subred",
        "vlsm",
        "paquete"
    ],

    "hardware": [

        "hardware",
        "procesador",
        "cpu",
        "ram",
        "ssd",
        "hdd",
        "gpu",
        "tarjeta",
        "placa",
        "monitor",
        "teclado",
        "mouse",
        "computador",
        "pc",
        "fuente",
        "memoria",
        "disco"
    ],

    "ciberseguridad": [

        "virus",
        "hackeo",
        "hacker",
        "seguridad",
        "firewall",
        "phishing",
        "malware",
        "ransomware",
        "contraseña",
        "autenticacion",
        "ciberseguridad",
        "encriptacion",
        "vpn",
        "ataque",
        "proteccion"
    ]
}

# =========================================================
# LIMPIAR TEXTO
# =========================================================

def limpiar_texto(texto):

    texto = texto.lower()

    texto = re.sub(
        r"[^\wáéíóúüñ\s]",
        " ",
        texto
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()

# =========================================================
# CONTAR COINCIDENCIAS
# =========================================================

def contar_coincidencias(
    palabras_usuario,
    palabras_tema
):

    coincidencias = 0

    for palabra in palabras_usuario:

        if palabra in palabras_tema:

            coincidencias += 1

    return coincidencias

# =========================================================
# DETECTAR TEMA
# =========================================================

def detectar_tema(texto):

    texto = limpiar_texto(texto)

    palabras_usuario = texto.split()

    puntuaciones = {}

    # =====================================================
    # CALCULAR PUNTUACIÓN
    # =====================================================

    for tema, palabras_clave in (
        PALABRAS_CLAVE.items()
    ):

        puntuacion = contar_coincidencias(
            palabras_usuario,
            palabras_clave
        )

        puntuaciones[tema] = puntuacion

    # =====================================================
    # MEJOR TEMA
    # =====================================================

    mejor_tema = max(
        puntuaciones,
        key=puntuaciones.get
    )

    # =====================================================
    # SI NO HAY COINCIDENCIAS
    # =====================================================

    if puntuaciones[mejor_tema] == 0:

        return random.choice(
            list(PALABRAS_CLAVE.keys())
        )

    return mejor_tema

# =========================================================
# OBTENER PALABRAS CLAVE
# =========================================================

def obtener_palabras_clave():

    return PALABRAS_CLAVE

# =========================================================
# OBTENER TEMAS DISPONIBLES
# =========================================================

def obtener_temas():

    return list(
        PALABRAS_CLAVE.keys()
    )

# =========================================================
# RESUMEN DEL TEMA
# =========================================================

def descripcion_tema(tema):

    descripciones = {

        "programacion":
        "💻 Programación y desarrollo de software",

        "ia":
        "🤖 Inteligencia Artificial y automatización",

        "redes":
        "🌐 Redes y comunicaciones",

        "hardware":
        "🖥️ Hardware y componentes físicos",

        "ciberseguridad":
        "🔐 Seguridad informática y protección digital"
    }

    return descripciones.get(
        tema,
        "📚 Tema general"
    )

# =========================================================
# OBTENER ICONO
# =========================================================

def icono_tema(tema):

    iconos = {

        "programacion": "💻",
        "ia": "🤖",
        "redes": "🌐",
        "hardware": "🖥️",
        "ciberseguridad": "🔐"
    }

    return iconos.get(
        tema,
        "📚"
    )
