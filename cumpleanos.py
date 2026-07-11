import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Update
from telegram.ext import ContextTypes

from fichas import fichas_usuarios


CARPETA_DATOS = "/data" if os.path.isdir("/data") else "."
ARCHIVO_CONFIG = os.path.join(CARPETA_DATOS, "config_cumpleanos.json")

ZONA_CANARIAS = ZoneInfo("Atlantic/Canary")


def cargar_configuracion():
    if not os.path.exists(ARCHIVO_CONFIG):
        return {"chat_ids": []}

    try:
        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return {"chat_ids": []}


def guardar_configuracion():
    with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as archivo:
        json.dump(
            configuracion_cumpleanos,
            archivo,
            ensure_ascii=False,
            indent=2
        )


configuracion_cumpleanos = cargar_configuracion()


def convertir_fecha(cumpleanos):
    if not cumpleanos:
        return None

    try:
        return datetime.strptime(cumpleanos, "%d/%m")
    except ValueError:
        return None


def nombre_ficha(ficha):
    usuario = ficha.get("usuario")

    if usuario:
        return f"@{usuario}"

    return ficha.get("nombre", "Alguien")


async def activar_cumpleanos(
    update: Update,
    admin_ids
):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden activar los cumpleaños."
        )
        return

    chat_id = update.effective_chat.id
    chat_ids = configuracion_cumpleanos.setdefault("chat_ids", [])

    if chat_id in chat_ids:
        await update.message.reply_text(
            "🎂 Los avisos de cumpleaños ya están activados en este grupo."
        )
        return

    chat_ids.append(chat_id)
    guardar_configuracion()

    await update.message.reply_text(
        "✅ Avisos de cumpleaños activados.\n\n"
        "El bot comprobará cada día a las 09:00, hora canaria, "
        "si algún miembro está de cumpleaños."
    )


async def desactivar_cumpleanos(
    update: Update,
    admin_ids
):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden desactivar los cumpleaños."
        )
        return

    chat_id = update.effective_chat.id
    chat_ids = configuracion_cumpleanos.setdefault("chat_ids", [])

    if chat_id not in chat_ids:
        await update.message.reply_text(
            "Los avisos de cumpleaños no estaban activados."
        )
        return

    chat_ids.remove(chat_id)
    guardar_configuracion()

    await update.message.reply_text(
        "🛑 Avisos de cumpleaños desactivados."
    )


async def mostrar_proximos_cumpleanos(update: Update):
    hoy = datetime.now(ZONA_CANARIAS)
    proximos = []

    for ficha in fichas_usuarios.values():
        fecha = convertir_fecha(ficha.get("cumpleanos"))

        if not fecha:
            continue

        cumple_este_ano = datetime(
            hoy.year,
            fecha.month,
            fecha.day,
            tzinfo=ZONA_CANARIAS
        )

        if cumple_este_ano.date() < hoy.date():
            cumple_este_ano = datetime(
                hoy.year + 1,
                fecha.month,
                fecha.day,
                tzinfo=ZONA_CANARIAS
            )

        dias = (cumple_este_ano.date() - hoy.date()).days

        proximos.append(
            (
                dias,
                nombre_ficha(ficha),
                fecha.strftime("%d/%m")
            )
        )

    if not proximos:
        await update.message.reply_text(
            "Todavía no hay cumpleaños registrados en las fichas."
        )
        return

    proximos.sort(key=lambda elemento: elemento[0])

    texto = "🎂 Próximos cumpleaños\n\n"

    for dias, nombre, fecha in proximos[:10]:
        if dias == 0:
            cuando = "¡Hoy!"
        elif dias == 1:
            cuando = "Mañana"
        else:
            cuando = f"Dentro de {dias} días"

        texto += f"• {nombre} — {fecha} · {cuando}\n"

    await update.message.reply_text(texto)


async def mostrar_cumpleanos_mes(update: Update):
    ahora = datetime.now(ZONA_CANARIAS)
    cumpleanos_mes = []

    for ficha in fichas_usuarios.values():
        fecha = convertir_fecha(ficha.get("cumpleanos"))

        if not fecha or fecha.month != ahora.month:
            continue

        cumpleanos_mes.append(
            (
                fecha.day,
                nombre_ficha(ficha),
                fecha.strftime("%d/%m")
            )
        )

    if not cumpleanos_mes:
        await update.message.reply_text(
            "🎂 No hay cumpleaños registrados este mes."
        )
        return

    cumpleanos_mes.sort(key=lambda elemento: elemento[0])

    texto = "🎉 Cumpleaños de este mes\n\n"

    for _, nombre, fecha in cumpleanos_mes:
        texto += f"• {nombre} — {fecha}\n"

    await update.message.reply_text(texto)


async def revisar_cumpleanos(
    context: ContextTypes.DEFAULT_TYPE
):
    ahora = datetime.now(ZONA_CANARIAS)
    fecha_actual = ahora.strftime("%d/%m")

    cumpleaneros = []

    for ficha in fichas_usuarios.values():
        if ficha.get("cumpleanos") == fecha_actual:
            cumpleaneros.append(nombre_ficha(ficha))

    if not cumpleaneros:
        return

    if len(cumpleaneros) == 1:
        texto = (
            f"🎉🎂 ¡Hoy está de cumpleaños {cumpleaneros[0]}!\n\n"
            "Todo el grupo a felicitarle como corresponde. "
            "No aceptamos silencios administrativos en un día así 🥳"
        )
    else:
        nombres = "\n".join(
            f"• {nombre}" for nombre in cumpleaneros
        )

        texto = (
            "🎉🎂 ¡Hoy tenemos varios cumpleaños!\n\n"
            f"{nombres}\n\n"
            "Que empiece la lluvia de felicitaciones 🥳"
        )

    for chat_id in configuracion_cumpleanos.get("chat_ids", []):
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=texto
            )
        except Exception as error:
            print(
                f"No se pudo enviar el cumpleaños a {chat_id}: {error}"
            )
