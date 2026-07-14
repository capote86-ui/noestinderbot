import json
import os
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from casos_tribunal import casos_tribunal


CARPETA_DATOS = "/data" if os.path.isdir("/data") else "."
ARCHIVO_TRIBUNAL = os.path.join(CARPETA_DATOS, "tribunal.json")


def cargar_datos():
    if not os.path.exists(ARCHIVO_TRIBUNAL):
        return {
            "chat_ids": [],
            "contador": 0,
            "casos_recientes": [],
            "activos": {}
        }

    try:
        with open(ARCHIVO_TRIBUNAL, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return {
            "chat_ids": [],
            "contador": 0,
            "casos_recientes": [],
            "activos": {}
        }


datos_tribunal = cargar_datos()
tribunales_activos = datos_tribunal.setdefault("activos", {})

def guardar_datos():
    with open(ARCHIVO_TRIBUNAL, "w", encoding="utf-8") as archivo:
        json.dump(
            datos_tribunal,
            archivo,
            ensure_ascii=False,
            indent=2
        )


def elegir_caso():
    recientes = datos_tribunal.get("casos_recientes", [])

    disponibles = [
        indice
        for indice in range(len(casos_tribunal))
        if indice not in recientes
    ]

    if not disponibles:
        recientes.clear()
        disponibles = list(range(len(casos_tribunal)))

    indice_elegido = random.choice(disponibles)

    recientes.append(indice_elegido)

    limite_recientes = min(20, len(casos_tribunal) - 1)

    if len(recientes) > limite_recientes:
        recientes.pop(0)

    datos_tribunal["casos_recientes"] = recientes
    guardar_datos()

    return indice_elegido, casos_tribunal[indice_elegido]


async def activar_tribunal(update: Update, admin_ids):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden activar el Tribunal."
        )
        return

    chat_id = update.effective_chat.id
    chat_ids = datos_tribunal.setdefault("chat_ids", [])

    if chat_id in chat_ids:
        await update.message.reply_text(
            "⚖️ El Tribunal ya está activado en este grupo."
        )
        return

    chat_ids.append(chat_id)
    guardar_datos()

    await update.message.reply_text(
        "✅ Tribunal de No es Tinder activado.\n\n"
        "Cada día a las 20:30 se publicará automáticamente un nuevo caso."
    )


async def desactivar_tribunal(update: Update, admin_ids):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden desactivar el Tribunal."
        )
        return

    chat_id = update.effective_chat.id
    chat_ids = datos_tribunal.setdefault("chat_ids", [])

    if chat_id not in chat_ids:
        await update.message.reply_text(
            "El Tribunal no estaba activado en este grupo."
        )
        return

    chat_ids.remove(chat_id)
    guardar_datos()

    await update.message.reply_text(
        "🛑 Tribunal automático desactivado."
    )


async def iniciar_tribunal_en_chat(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int
):
    clave_chat = str(chat_id)

    if clave_chat in tribunales_activos:
        return

    indice_caso, caso = elegir_caso()

    datos_tribunal["contador"] = datos_tribunal.get("contador", 0) + 1
    numero_caso = datos_tribunal["contador"]
    guardar_datos()

    teclado = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "A",
            callback_data=f"tribunal_voto:A:{chat_id}:{numero_caso}"
        ),
        InlineKeyboardButton(
            "B",
            callback_data=f"tribunal_voto:B:{chat_id}:{numero_caso}"
        ),
        InlineKeyboardButton(
            "C",
            callback_data=f"tribunal_voto:C:{chat_id}:{numero_caso}"
        ),
        InlineKeyboardButton(
            "D",
            callback_data=f"tribunal_voto:D:{chat_id}:{numero_caso}"
        )
    ]])

    texto = (
        f"⚖️ TRIBUNAL DE NO ES TINDER\n"
        f"📂 Caso nº {numero_caso}\n\n"
        f"{caso['pregunta']}\n\n"
        f"A) {caso['opciones'][0]}\n"
        f"B) {caso['opciones'][1]}\n"
        f"C) {caso['opciones'][2]}\n"
        f"D) {caso['opciones'][3]}\n\n"
        f"⏱️ Tenéis 30 minutos para votar.\n"
        f"El voto es individual y no llena el chat."
    )

    mensaje = await context.bot.send_message(
        chat_id=chat_id,
        text=texto,
        reply_markup=teclado
    )

    tribunales_activos[clave_chat] = {
        "numero_caso": numero_caso,
        "indice_caso": indice_caso,
        "mensaje_id": mensaje.message_id,
        "votos": {}
    }

guardar_datos()

    context.job_queue.run_once(
        cerrar_tribunal_por_tiempo,
        when=1800,
        data={
            "chat_id": chat_id,
            "numero_caso": numero_caso
        },
        name=f"tribunal_{chat_id}_{numero_caso}"
    )


async def publicar_tribunal(
    context: ContextTypes.DEFAULT_TYPE
):
    for chat_id in datos_tribunal.get("chat_ids", []):
        try:
            await iniciar_tribunal_en_chat(context, chat_id)
        except Exception as error:
            print(
                f"No se pudo publicar el Tribunal en {chat_id}: {error}"
            )


async def lanzar_tribunal_manual(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    admin_ids
):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden abrir el Tribunal."
        )
        return

    chat_id = update.effective_chat.id

    if str(chat_id) in tribunales_activos:
        await update.message.reply_text(
            "⚖️ Ya hay un caso del Tribunal abierto."
        )
        return

    await iniciar_tribunal_en_chat(context, chat_id)


async def botones_tribunal(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    datos = query.data.split(":")

    if len(datos) != 4:
        await query.answer()
        return

    accion, respuesta, chat_id_texto, numero_texto = datos

    if accion != "tribunal_voto":
        await query.answer()
        return

    chat_id = int(chat_id_texto)
    numero_caso = int(numero_texto)

    tribunal = tribunales_activos.get(str(chat_id))

    if not tribunal:
        await query.answer(
            "Esta votación ya terminó.",
            show_alert=True
        )
        return

    if tribunal["numero_caso"] != numero_caso:
        await query.answer(
            "Este caso ya no está activo.",
            show_alert=True
        )
        return

    user_id = query.from_user.id

    if str(user_id) in tribunal["votos"]:
        await query.answer(
            "Ya has votado en este caso.",
            show_alert=True
        )
        return

    tribunal["votos"][str(user_id)] = respuesta
    guardar_datos()

    await query.answer(
        f"Voto registrado: opción {respuesta}",
        show_alert=True
    )


async def cerrar_tribunal_por_tiempo(
    context: ContextTypes.DEFAULT_TYPE
):
    chat_id = context.job.data["chat_id"]
    numero_caso = context.job.data["numero_caso"]

    await cerrar_tribunal(
        context,
        chat_id,
        numero_caso
    )


async def cerrar_tribunal(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    numero_caso: int
):
    clave_chat = str(chat_id)
    tribunal = tribunales_activos.get(clave_chat)

    if not tribunal:
        return

    if tribunal["numero_caso"] != numero_caso:
        return

    caso = casos_tribunal[tribunal["indice_caso"]]
    votos = tribunal["votos"]

    conteo = {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0
    }

    for respuesta in votos.values():
        if respuesta in conteo:
            conteo[respuesta] += 1

    total = len(votos)

    def porcentaje(letra):
        if total == 0:
            return 0

        return round((conteo[letra] / total) * 100)

    texto = (
        f"⚖️ VEREDICTO DEL TRIBUNAL\n"
        f"📂 Caso nº {numero_caso}\n\n"
        f"{caso['pregunta']}\n\n"
        f"A) {caso['opciones'][0]} — {conteo['A']} voto(s) "
        f"· {porcentaje('A')} %\n\n"
        f"B) {caso['opciones'][1]} — {conteo['B']} voto(s) "
        f"· {porcentaje('B')} %\n\n"
        f"C) {caso['opciones'][2]} — {conteo['C']} voto(s) "
        f"· {porcentaje('C')} %\n\n"
        f"D) {caso['opciones'][3]} — {conteo['D']} voto(s) "
        f"· {porcentaje('D')} %\n\n"
        f"👥 Participación total: {total}\n\n"
        f"🏛️ El grupo ha hablado.\n"
        f"Ahora podéis defender vuestra postura. "
        f"Debate sí; puñaladas, no."
    )

    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=tribunal["mensaje_id"],
        text=texto
    )

    tribunales_activos.pop(clave_chat, None)
    guardar_datos()


async def cancelar_tribunal(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    admin_ids
):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden cancelar el Tribunal."
        )
        return

    chat_id = update.effective_chat.id
    clave_chat = str(chat_id)
    tribunal = tribunales_activos.get(clave_chat)

    if not tribunal:
        await update.message.reply_text(
            "No hay ningún caso activo ahora mismo."
        )
        return

    nombre_job = (
        f"tribunal_{chat_id}_{tribunal['numero_caso']}"
    )

    for job in context.job_queue.get_jobs_by_name(nombre_job):
        job.schedule_removal()

    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=tribunal["mensaje_id"],
        text=(
            f"🛑 Caso nº {tribunal['numero_caso']} cancelado "
            f"por administración."
        )
    )

    tribunales_activos.pop(chat_id, None)
