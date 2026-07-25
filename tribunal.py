import json
import os
import random
from datetime import datetime, timezone
from typing import Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest, TelegramError
from telegram.ext import ContextTypes

from casos_tribunal import casos_tribunal


CARPETA_DATOS = "/data" if os.path.isdir("/data") else "."
ARCHIVO_TRIBUNAL = os.path.join(CARPETA_DATOS, "tribunal.json")
DURACION_VOTACION_SEGUNDOS = 30 * 60
LETRAS = ("A", "B", "C", "D")


def datos_vacios() -> dict[str, Any]:
    return {
        "chat_ids": [],
        "contador": 0,
        "casos_recientes": [],
        "activos": {},
    }


def cargar_datos() -> dict[str, Any]:
    if not os.path.exists(ARCHIVO_TRIBUNAL):
        return datos_vacios()

    try:
        with open(ARCHIVO_TRIBUNAL, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (json.JSONDecodeError, OSError, TypeError):
        return datos_vacios()

    if not isinstance(datos, dict):
        return datos_vacios()

    datos.setdefault("chat_ids", [])
    datos.setdefault("contador", 0)
    datos.setdefault("casos_recientes", [])
    datos.setdefault("activos", {})

    if not isinstance(datos["chat_ids"], list):
        datos["chat_ids"] = []

    if not isinstance(datos["casos_recientes"], list):
        datos["casos_recientes"] = []

    if not isinstance(datos["activos"], dict):
        datos["activos"] = {}

    return datos


datos_tribunal = cargar_datos()
tribunales_activos = datos_tribunal["activos"]


def guardar_datos() -> None:
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    archivo_temporal = f"{ARCHIVO_TRIBUNAL}.tmp"

    try:
        with open(archivo_temporal, "w", encoding="utf-8") as archivo:
            json.dump(
                datos_tribunal,
                archivo,
                ensure_ascii=False,
                indent=2,
            )

        os.replace(archivo_temporal, ARCHIVO_TRIBUNAL)

    except OSError as error:
        print(f"No se pudieron guardar los datos del Tribunal: {error}")

        try:
            if os.path.exists(archivo_temporal):
                os.remove(archivo_temporal)
        except OSError:
            pass


def ahora_utc_timestamp() -> int:
    return int(datetime.now(timezone.utc).timestamp())


def elegir_caso() -> tuple[int, dict[str, Any]]:
    if not casos_tribunal:
        raise RuntimeError("No hay casos disponibles en casos_tribunal.py")

    recientes = datos_tribunal.setdefault("casos_recientes", [])

    recientes_validos = [
        indice
        for indice in recientes
        if isinstance(indice, int) and 0 <= indice < len(casos_tribunal)
    ]

    disponibles = [
        indice
        for indice in range(len(casos_tribunal))
        if indice not in recientes_validos
    ]

    if not disponibles:
        recientes_validos = []
        disponibles = list(range(len(casos_tribunal)))

    indice_elegido = random.choice(disponibles)
    recientes_validos.append(indice_elegido)

    limite_recientes = min(20, max(0, len(casos_tribunal) - 1))

    if limite_recientes == 0:
        recientes_validos = []
    else:
        recientes_validos = recientes_validos[-limite_recientes:]

    datos_tribunal["casos_recientes"] = recientes_validos
    guardar_datos()

    return indice_elegido, casos_tribunal[indice_elegido]


def crear_teclado(
    chat_id: int,
    numero_caso: int,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                letra,
                callback_data=(
                    f"tribunal_voto:{letra}:{chat_id}:{numero_caso}"
                ),
            )
            for letra in LETRAS
        ]]
    )


def nombre_job(chat_id: int, numero_caso: int) -> str:
    return f"tribunal_{chat_id}_{numero_caso}"


def programar_cierre(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    numero_caso: int,
    segundos: int,
) -> None:
    nombre = nombre_job(chat_id, numero_caso)

    for job in context.job_queue.get_jobs_by_name(nombre):
        job.schedule_removal()

    context.job_queue.run_once(
        cerrar_tribunal_por_tiempo,
        when=max(1, segundos),
        data={
            "chat_id": chat_id,
            "numero_caso": numero_caso,
        },
        name=nombre,
    )


async def activar_tribunal(update: Update, admin_ids) -> None:
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


async def desactivar_tribunal(update: Update, admin_ids) -> None:
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
    chat_id: int,
) -> None:
    clave_chat = str(chat_id)
    tribunal_anterior = tribunales_activos.get(clave_chat)

    if tribunal_anterior:
        fecha_cierre = int(tribunal_anterior.get("fecha_cierre", 0))

        if fecha_cierre and fecha_cierre <= ahora_utc_timestamp():
            await cerrar_tribunal(
                context,
                chat_id,
                int(tribunal_anterior["numero_caso"]),
            )
        else:
            return

    indice_caso, caso = elegir_caso()

    datos_tribunal["contador"] = int(
        datos_tribunal.get("contador", 0)
    ) + 1
    numero_caso = datos_tribunal["contador"]
    fecha_cierre = ahora_utc_timestamp() + DURACION_VOTACION_SEGUNDOS

    texto = (
        f"⚖️ TRIBUNAL DE NO ES TINDER\n"
        f"📂 Caso nº {numero_caso}\n\n"
        f"{caso['pregunta']}\n\n"
        f"A) {caso['opciones'][0]}\n"
        f"B) {caso['opciones'][1]}\n"
        f"C) {caso['opciones'][2]}\n"
        f"D) {caso['opciones'][3]}\n\n"
        f"⏱️ Tenéis 30 minutos para votar.\n"
        f"Podéis cambiar vuestro voto mientras el caso siga abierto.\n"
        f"El voto es privado y no llena el chat."
    )

    mensaje = await context.bot.send_message(
        chat_id=chat_id,
        text=texto,
        reply_markup=crear_teclado(chat_id, numero_caso),
    )

    tribunales_activos[clave_chat] = {
        "numero_caso": numero_caso,
        "indice_caso": indice_caso,
        "mensaje_id": mensaje.message_id,
        "votos": {},
        "fecha_cierre": fecha_cierre,
    }

    guardar_datos()

    programar_cierre(
        context,
        chat_id,
        numero_caso,
        DURACION_VOTACION_SEGUNDOS,
    )


async def publicar_tribunal(
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    for chat_id in list(datos_tribunal.get("chat_ids", [])):
        try:
            await iniciar_tribunal_en_chat(context, int(chat_id))
        except Exception as error:
            print(
                f"No se pudo publicar el Tribunal en {chat_id}: {error}"
            )


async def lanzar_tribunal_manual(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    admin_ids,
) -> None:
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden abrir el Tribunal."
        )
        return

    chat_id = update.effective_chat.id
    clave_chat = str(chat_id)
    tribunal = tribunales_activos.get(clave_chat)

    if tribunal:
        fecha_cierre = int(tribunal.get("fecha_cierre", 0))

        if fecha_cierre and fecha_cierre <= ahora_utc_timestamp():
            await cerrar_tribunal(
                context,
                chat_id,
                int(tribunal["numero_caso"]),
            )
        else:
            await update.message.reply_text(
                "⚖️ Ya hay un caso del Tribunal abierto."
            )
            return

    try:
        await iniciar_tribunal_en_chat(context, chat_id)
    except Exception as error:
        print(f"No se pudo abrir el Tribunal manualmente: {error}")
        await update.message.reply_text(
            "❌ No se pudo abrir el Tribunal. Revisa los registros del bot."
        )


async def botones_tribunal(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query or not query.data:
        return

    datos = query.data.split(":")

    if len(datos) != 4:
        await query.answer()
        return

    accion, respuesta, chat_id_texto, numero_texto = datos

    if accion != "tribunal_voto" or respuesta not in LETRAS:
        await query.answer()
        return

    try:
        chat_id = int(chat_id_texto)
        numero_caso = int(numero_texto)
    except ValueError:
        await query.answer()
        return

    tribunal = tribunales_activos.get(str(chat_id))

    if not tribunal:
        await query.answer(
            "Esta votación ya terminó.",
            show_alert=True,
        )
        return

    if int(tribunal.get("numero_caso", -1)) != numero_caso:
        await query.answer(
            "Este caso ya no está activo.",
            show_alert=True,
        )
        return

    fecha_cierre = int(tribunal.get("fecha_cierre", 0))

    if fecha_cierre and fecha_cierre <= ahora_utc_timestamp():
        await query.answer(
            "El tiempo para votar ya terminó.",
            show_alert=True,
        )
        await cerrar_tribunal(context, chat_id, numero_caso)
        return

    user_id = str(query.from_user.id)
    voto_anterior = tribunal.setdefault("votos", {}).get(user_id)
    tribunal["votos"][user_id] = respuesta
    guardar_datos()

    if voto_anterior and voto_anterior != respuesta:
        texto_respuesta = (
            f"Voto cambiado: {voto_anterior} → {respuesta}"
        )
    elif voto_anterior == respuesta:
        texto_respuesta = (
            f"Tu voto sigue siendo la opción {respuesta}."
        )
    else:
        texto_respuesta = (
            f"Voto registrado: opción {respuesta}."
        )

    await query.answer(
        texto_respuesta,
        show_alert=True,
    )


async def cerrar_tribunal_por_tiempo(
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if not context.job or not context.job.data:
        return

    chat_id = int(context.job.data["chat_id"])
    numero_caso = int(context.job.data["numero_caso"])

    await cerrar_tribunal(
        context,
        chat_id,
        numero_caso,
    )


async def cerrar_tribunal(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    numero_caso: int,
) -> None:
    clave_chat = str(chat_id)
    tribunal = tribunales_activos.get(clave_chat)

    if not tribunal:
        return

    if int(tribunal.get("numero_caso", -1)) != numero_caso:
        return

    indice_caso = int(tribunal.get("indice_caso", -1))

    if not 0 <= indice_caso < len(casos_tribunal):
        tribunales_activos.pop(clave_chat, None)
        guardar_datos()
        return

    caso = casos_tribunal[indice_caso]
    votos = tribunal.get("votos", {})

    conteo = {letra: 0 for letra in LETRAS}

    for respuesta in votos.values():
        if respuesta in conteo:
            conteo[respuesta] += 1

    total = sum(conteo.values())

    def porcentaje(letra: str) -> int:
        if total == 0:
            return 0

        return round((conteo[letra] / total) * 100)

    texto = (
        f"⚖️ VEREDICTO DEL TRIBUNAL\n"
        f"📂 Caso nº {numero_caso}\n\n"
        f"{caso['pregunta']}\n\n"
        f"A) {caso['opciones'][0]} — "
        f"{conteo['A']} voto(s) · {porcentaje('A')} %\n\n"
        f"B) {caso['opciones'][1]} — "
        f"{conteo['B']} voto(s) · {porcentaje('B')} %\n\n"
        f"C) {caso['opciones'][2]} — "
        f"{conteo['C']} voto(s) · {porcentaje('C')} %\n\n"
        f"D) {caso['opciones'][3]} — "
        f"{conteo['D']} voto(s) · {porcentaje('D')} %\n\n"
        f"👥 Participación total: {total}\n\n"
        f"🏛️ El grupo ha hablado.\n"
        f"Ahora podéis defender vuestra postura. "
        f"Debate sí; puñaladas, no."
    )

    mensaje_editado = False

    try:
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=int(tribunal["mensaje_id"]),
            text=texto,
            reply_markup=None,
        )
        mensaje_editado = True

    except BadRequest as error:
        texto_error = str(error).lower()

        if "message is not modified" in texto_error:
            mensaje_editado = True
        else:
            print(
                f"No se pudo editar el mensaje del Tribunal "
                f"{numero_caso}: {error}"
            )

    except TelegramError as error:
        print(
            f"Error de Telegram al cerrar el Tribunal "
            f"{numero_caso}: {error}"
        )

    if not mensaje_editado:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=texto,
            )
        except TelegramError as error:
            print(
                f"No se pudo publicar el veredicto del Tribunal "
                f"{numero_caso}: {error}"
            )

    tribunales_activos.pop(clave_chat, None)
    guardar_datos()


async def cancelar_tribunal(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    admin_ids,
) -> None:
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

    numero_caso = int(tribunal["numero_caso"])

    for job in context.job_queue.get_jobs_by_name(
        nombre_job(chat_id, numero_caso)
    ):
        job.schedule_removal()

    try:
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=int(tribunal["mensaje_id"]),
            text=(
                f"🛑 Caso nº {numero_caso} cancelado "
                f"por administración."
            ),
            reply_markup=None,
        )
    except TelegramError:
        await update.message.reply_text(
            f"🛑 Caso nº {numero_caso} cancelado por administración."
        )

    tribunales_activos.pop(clave_chat, None)
    guardar_datos()


async def restaurar_tribunales_pendientes(application) -> None:
    """
    Restaura los cierres pendientes después de un reinicio de Railway.

    Para utilizar esta protección, en bot.py hay que construir la aplicación así:

    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(restaurar_tribunales_pendientes)
        .build()
    )
    """
    ahora = ahora_utc_timestamp()

    for clave_chat, tribunal in list(tribunales_activos.items()):
        try:
            chat_id = int(clave_chat)
            numero_caso = int(tribunal["numero_caso"])
            fecha_cierre = int(tribunal.get("fecha_cierre", 0))
        except (KeyError, TypeError, ValueError):
            tribunales_activos.pop(clave_chat, None)
            continue

        if fecha_cierre <= 0:
            tribunales_activos.pop(clave_chat, None)
            continue

        segundos_restantes = fecha_cierre - ahora

        if segundos_restantes <= 0:
            application.job_queue.run_once(
                cerrar_tribunal_por_tiempo,
                when=1,
                data={
                    "chat_id": chat_id,
                    "numero_caso": numero_caso,
                },
                name=nombre_job(chat_id, numero_caso),
            )
        else:
            application.job_queue.run_once(
                cerrar_tribunal_por_tiempo,
                when=segundos_restantes,
                data={
                    "chat_id": chat_id,
                    "numero_caso": numero_caso,
                },
                name=nombre_job(chat_id, numero_caso),
            )

    guardar_datos()
