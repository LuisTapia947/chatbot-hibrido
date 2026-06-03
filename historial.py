# =========================================================
# HISTORIAL DE CHATS
# =========================================================

import os
from datetime import datetime

# =========================================================
# GUARDAR CHAT
# =========================================================

def guardar_chat(chat):

    carpeta = "historial"

    os.makedirs(
        carpeta,
        exist_ok=True
    )

    fecha = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    archivo = os.path.join(
        carpeta,
        f"chat_{fecha}.txt"
    )

    with open(
        archivo,
        "w",
        encoding="utf-8"
    ) as f:

        for tipo, mensaje in chat:

            if tipo == "usuario":

                f.write(
                    f"USUARIO:\n{mensaje}\n\n"
                )

            else:

                f.write(
                    f"CHATBOT:\n{mensaje}\n\n"
                )

    return archivo

# =========================================================
# LISTAR HISTORIALES
# =========================================================

def obtener_historiales():

    carpeta = "historial"

    if not os.path.exists(carpeta):

        return []

    archivos = sorted(
        os.listdir(carpeta),
        reverse=True
    )

    return archivos