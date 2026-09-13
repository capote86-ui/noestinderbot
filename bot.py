import json
import os
import random
import time

from telegram import Update
from telegram.ext import ContextTypes

from mensajes_misa import (
    AVISOS_30,
    AVISOS_10,
    AVISOS_2,
    APERTURAS,
    CONFESIONES,
    LECTURAS,
    EXAMENES,
    PENITENCIAS,
    CANONIZACIONES,
    CIERRES,
)


CARPETA_DATOS = "/data" if os.path.isdir("/data") else "."
ARCHIVO_MISA = os.path.join(CARPETA_DATOS, "misa_domingo.json")

misas_activas = {}


def cargar_configuracion():
    if not os.path.exists(ARCHIVO_MISA):
        return {"chat_ids": []}

    try:
        with open(ARCHIVO_MISA, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, dict):
            return {"chat_ids": []}

        datos.setdefault("chat_ids", [])
        return datos

    except (json.JSONDecodeError, OSError, TypeError):
        return {"chat_ids": []}


configuracion_misa = cargar_configuracion()


def guardar_configuracion():
    os.makedirs(CARPETA_DATOS, exist_ok=True)

    with open(ARCHIVO_MISA, "w", encoding="utf-8") as archivo:
        json.dump(
            configuracion_misa,
            archivo,
            ensure_ascii=False,
            indent=2
        )


async def activar_misa(update: Update, admin_ids):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden activar la Misa Dominical."
        )
        return

    chat_id = update.effective_chat.id
    chat_ids = configuracion_misa.setdefault("chat_ids", [])

    if chat_id in chat_ids:
        await update.message.reply_text(
            "⛪ La Misa Dominical ya está activada en este grupo."
        )
        return

    chat_ids.append(chat_id)
    guardar_configuracion()

    await update.message.reply_text(
        "✅ Misa Dominical v2 activada.\n\n"
        "Se celebrará los domingos:\n"
        "🕚 Primer aviso: 11:00, hora canaria.\n"
        "⛪ Inicio: 11:30, hora canaria.\n"
        "🏁 Final aproximado: 13:00, hora canaria.\n\n"
        "En la Península será una hora más."
    )


async def desactivar_misa(update: Update, admin_ids):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden desactivar la Misa Dominical."
        )
        return

    chat_id = update.effective_chat.id
    chat_ids = configuracion_misa.setdefault("chat_ids", [])

    if chat_id not in chat_ids:
        await update.message.reply_text(
            "La Misa Dominical no estaba activada."
        )
        return

    chat_ids.remove(chat_id)
    guardar_configuracion()

    await update.message.reply_text(
        "🛑 Misa Dominical automática desactivada."
    )


async def enviar_a_grupos(context, lista_mensajes):
    for chat_id in configuracion_misa.get("chat_ids", []):
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=random.choice(lista_mensajes)
            )
        except Exception as error:
            print(f"No se pudo enviar mensaje de misa a {chat_id}: {error}")


async def aviso_misa_30(context: ContextTypes.DEFAULT_TYPE):
    await enviar_a_grupos(context, AVISOS_30)


async def aviso_misa_10(context: ContextTypes.DEFAULT_TYPE):
    await enviar_a_grupos(context, AVISOS_10)


async def aviso_misa_2(context: ContextTypes.DEFAULT_TYPE):
    await enviar_a_grupos(context, AVISOS_2)


async def enviar_parte_misa(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data["chat_id"]
    identificador = context.job.data["identificador"]
    lista_mensajes = context.job.data["mensajes"]

    misa = misas_activas.get(chat_id)

    if not misa or misa["identificador"] != identificador:
        return

    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=random.choice(lista_mensajes)
        )
    except Exception as error:
        print(f"No se pudo enviar una parte de la misa a {chat_id}: {error}")


async def finalizar_misa(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data["chat_id"]
    identificador = context.job.data["identificador"]

    misa = misas_activas.get(chat_id)

    if not misa or misa["identificador"] != identificador:
        return

    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=random.choice(CIERRES)
        )
    except Exception as error:
        print(f"No se pudo cerrar la misa en {chat_id}: {error}")

    misas_activas.pop(chat_id, None)


async def iniciar_misa_en_chat(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int
):
    if chat_id in misas_activas:
        return False

    identificador = f"{chat_id}_{time.time_ns()}"

    misas_activas[chat_id] = {
        "identificador": identificador
    }

    await context.bot.send_message(
        chat_id=chat_id,
        text=random.choice(APERTURAS)
    )

    # Tiempos contados desde el comienzo de la misa:
    # 11:30 Apertura
    # 11:40 Confesión
    # 11:50 Lectura
    # 12:05 Examen de conciencia
    # 12:20 Penitencia
    # 12:35 Canonización
    # 13:00 Cierre
    partes = [
        (10 * 60, CONFESIONES, "confesion"),
        (20 * 60, LECTURAS, "lectura"),
        (35 * 60, EXAMENES, "examen"),
        (50 * 60, PENITENCIAS, "penitencia"),
        (65 * 60, CANONIZACIONES, "canonizacion"),
    ]

    for segundos, mensajes, nombre in partes:
        context.job_queue.run_once(
            enviar_parte_misa,
            when=segundos,
            data={
                "chat_id": chat_id,
                "identificador": identificador,
                "mensajes": mensajes
            },
            name=f"misa_{chat_id}_{identificador}_{nombre}"
        )

    context.job_queue.run_once(
        finalizar_misa,
        when=90 * 60,
        data={
            "chat_id": chat_id,
            "identificador": identificador
        },
        name=f"misa_{chat_id}_{identificador}_cierre"
    )

    return True


async def publicar_misa_automatica(
    context: ContextTypes.DEFAULT_TYPE
):
    for chat_id in configuracion_misa.get("chat_ids", []):
        try:
            await iniciar_misa_en_chat(context, chat_id)
        except Exception as error:
            print(f"No se pudo iniciar la misa en {chat_id}: {error}")


async def lanzar_misa_manual(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    admin_ids
):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden iniciar la misa."
        )
        return

    iniciada = await iniciar_misa_en_chat(
        context,
        update.effective_chat.id
    )

    if not iniciada:
        await update.message.reply_text(
            "⛪ Ya hay una misa en marcha."
        )


async def cancelar_misa(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    admin_ids
):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden cancelar la misa."
        )
        return

    chat_id = update.effective_chat.id
    misa = misas_activas.get(chat_id)

    if not misa:
        await update.message.reply_text(
            "No hay ninguna misa en marcha."
        )
        return

    identificador = misa["identificador"]

    for job in context.job_queue.jobs():
        if job.name and job.name.startswith(
            f"misa_{chat_id}_{identificador}_"
        ):
            job.schedule_removal()

    misas_activas.pop(chat_id, None)

    await update.message.reply_text(
        "🛑 Misa cancelada por administración.\n\n"
        "Los pecados quedan pendientes para el próximo domingo."
    )
