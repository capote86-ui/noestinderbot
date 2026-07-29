import json
import os
import random
import re
import unicodedata
from typing import Any, Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest, Forbidden, TelegramError
from telegram.ext import ContextTypes

from palabras_impostor import PALABRAS_IMPOSTOR

MINIMO_JUGADORES = 5
TIEMPO_PISTAS = 120
TIEMPO_VOTACION = 60
TIEMPO_ADIVINAR = 30

CARPETA_DATOS = "/data" if os.path.isdir("/data") else "."
ARCHIVO_RANKING = os.path.join(CARPETA_DATOS, "ranking_impostor.json")

impostores_activos: dict[int, dict[str, Any]] = {}


def nombre_usuario(user) -> str:
    if user.username:
        return f"@{user.username}"
    return user.first_name or "Alguien"


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", texto).strip()


def contiene_palabra_prohibida(texto: str, palabra: str) -> bool:
    patron = r"(?<!\w)" + re.escape(normalizar(palabra)) + r"(?!\w)"
    return re.search(patron, normalizar(texto)) is not None


def cargar_ranking() -> dict[str, dict[str, Any]]:
    if not os.path.exists(ARCHIVO_RANKING):
        return {}
    try:
        with open(ARCHIVO_RANKING, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return datos if isinstance(datos, dict) else {}
    except (OSError, json.JSONDecodeError, TypeError):
        return {}


ranking_impostor = cargar_ranking()


def guardar_ranking() -> None:
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    temporal = f"{ARCHIVO_RANKING}.tmp"
    try:
        with open(temporal, "w", encoding="utf-8") as archivo:
            json.dump(ranking_impostor, archivo, ensure_ascii=False, indent=2)
        os.replace(temporal, ARCHIVO_RANKING)
    except OSError as error:
        print(f"No se pudo guardar el ranking del Impostor: {error}")


def estadisticas_usuario(user_id: int, nombre: str) -> dict[str, Any]:
    datos = ranking_impostor.setdefault(str(user_id), {
        "nombre": nombre, "puntos": 0, "partidas": 0, "victorias": 0,
        "veces_impostor": 0, "impostores_descubiertos": 0,
        "palabras_acertadas": 0, "votos_correctos": 0,
    })
    datos["nombre"] = nombre
    return datos


def nombre_job(tipo: str, chat_id: int, ronda: int = 0) -> str:
    return f"impostor_{tipo}_{chat_id}_{ronda}"


def cancelar_jobs(context, chat_id: int) -> None:
    for tipo in ("pistas", "votacion", "adivinar"):
        for ronda in range(20):
            for job in context.job_queue.get_jobs_by_name(nombre_job(tipo, chat_id, ronda)):
                job.schedule_removal()


def teclado_inscripcion(chat_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Participar", callback_data=f"imp_join:{chat_id}"),
         InlineKeyboardButton("🚪 Salir", callback_data=f"imp_leave:{chat_id}")],
        [InlineKeyboardButton("▶️ Empezar", callback_data=f"imp_start:{chat_id}")],
    ])


async def iniciar_impostor(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int, admin_ids: list[int]) -> None:
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text("🚫 Solo los administradores pueden abrir una partida.")
        return
    if chat_id in impostores_activos:
        await update.message.reply_text("🎭 Ya hay una partida de El Impostor abierta.")
        return
    mensaje = await update.message.reply_text(
        "🎭 EL IMPOSTOR — NO ES TINDER\n\n"
        "Todos recibirán una palabra por privado, menos una persona: el impostor.\n"
        "Después tendréis que dar una pista sin revelar la palabra y votar al sospechoso.\n\n"
        f"👥 Mínimo: {MINIMO_JUGADORES} jugadores.\n\nParticipantes: nadie todavía.",
        reply_markup=teclado_inscripcion(chat_id),
    )
    impostores_activos[chat_id] = {
        "estado": "inscripcion", "jugadores": {}, "mensaje_id": mensaje.message_id,
        "categoria": None, "palabra": None, "impostor_id": None, "pistas": {},
        "votos": {}, "candidatos": [], "ronda_votacion": 0,
    }


async def actualizar_inscripcion(context, chat_id: int) -> None:
    partida = impostores_activos.get(chat_id)
    if not partida or partida["estado"] != "inscripcion":
        return
    lista = "\n".join(f"• {n}" for n in partida["jugadores"].values()) or "nadie todavía."
    try:
        await context.bot.edit_message_text(
            chat_id=chat_id, message_id=partida["mensaje_id"],
            text=("🎭 EL IMPOSTOR — NO ES TINDER\n\n"
                  "Todos recibirán una palabra por privado, menos una persona: el impostor.\n"
                  "Después tendréis que dar una pista sin revelar la palabra y votar al sospechoso.\n\n"
                  f"👥 Mínimo: {MINIMO_JUGADORES} jugadores.\n\n"
                  f"Participantes ({len(partida['jugadores'])}):\n{lista}"),
            reply_markup=teclado_inscripcion(chat_id),
        )
    except BadRequest as error:
        if "message is not modified" not in str(error).lower():
            print(error)


def elegir_palabra() -> tuple[str, str]:
    categorias = [c for c, lista in PALABRAS_IMPOSTOR.items() if lista]
    categoria = random.choice(categorias)
    return categoria, random.choice(PALABRAS_IMPOSTOR[categoria])


async def comenzar_partida(context, chat_id: int) -> None:
    partida = impostores_activos.get(chat_id)
    if not partida:
        return
    categoria, palabra = elegir_palabra()
    impostor_id = random.choice(list(partida["jugadores"].keys()))
    partida.update({"estado": "enviando_roles", "categoria": categoria, "palabra": palabra,
                    "impostor_id": impostor_id, "pistas": {}, "votos": {},
                    "candidatos": list(partida["jugadores"].keys()), "ronda_votacion": 0})
    fallos = []
    for user_id, nombre in partida["jugadores"].items():
        try:
            texto = (f"🕵️ ERES EL IMPOSTOR\n\n📚 Categoría: {categoria}\n\n"
                     "No conoces la palabra. Lee las pistas, intenta pasar desapercibido y dedúcela.") if user_id == impostor_id else (
                     f"🎭 TU PALABRA ES:\n\n🔐 {palabra.upper()}\n📚 Categoría: {categoria}\n\n"
                     "No la escribas. Cuando empiece la ronda, manda una sola pista al grupo.")
            await context.bot.send_message(chat_id=user_id, text=texto)
        except (Forbidden, TelegramError):
            fallos.append(nombre)
    if fallos:
        partida.update({"estado": "inscripcion", "categoria": None, "palabra": None, "impostor_id": None})
        await context.bot.send_message(chat_id=chat_id, text=(
            "❌ No puedo empezar porque no he podido enviar el rol por privado a:\n" +
            "\n".join(f"• {n}" for n in fallos) +
            "\n\nDeben abrir el chat privado del bot, pulsar START y volver a intentarlo."))
        return
    partida["estado"] = "pistas"
    await context.bot.send_message(chat_id=chat_id, text=(
        "🎭 ¡EMPIEZA LA RONDA!\n\nCada participante debe escribir UNA sola pista en el grupo.\n"
        "❌ No podéis decir la palabra.\n⏱️ Tenéis 120 segundos.\n\nQue empiece la actuación."))
    context.job_queue.run_once(cerrar_pistas_por_tiempo, when=TIEMPO_PISTAS,
                               data={"chat_id": chat_id}, name=nombre_job("pistas", chat_id))


async def procesar_mensaje_impostor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if not update.message or not update.message.text:
        return False
    user_id, chat_id, texto = update.effective_user.id, update.effective_chat.id, update.message.text.strip()
    if update.effective_chat.type == "private":
        for grupo_id, partida in list(impostores_activos.items()):
            if partida.get("estado") == "adivinar_palabra" and partida.get("impostor_id") == user_id:
                await resolver_adivinanza(context, grupo_id, texto)
                return True
        return False
    partida = impostores_activos.get(chat_id)
    if not partida or partida.get("estado") != "pistas" or user_id not in partida["jugadores"]:
        return False
    if user_id in partida["pistas"]:
        await update.message.reply_text(f"{nombre_usuario(update.effective_user)}, ya has enviado tu pista.")
        return True
    if contiene_palabra_prohibida(texto, partida["palabra"]):
        try:
            await update.message.delete()
        except TelegramError:
            pass
        await context.bot.send_message(chat_id=chat_id, text=f"🚫 {nombre_usuario(update.effective_user)}, no puedes decir la palabra.")
        return True
    partida["pistas"][user_id] = texto
    faltan = len(partida["jugadores"]) - len(partida["pistas"])
    await update.message.reply_text(f"✅ Pista registrada. Faltan {faltan} participante(s).")
    if faltan == 0:
        for job in context.job_queue.get_jobs_by_name(nombre_job("pistas", chat_id)):
            job.schedule_removal()
        await iniciar_votacion(context, chat_id)
    return True


async def cerrar_pistas_por_tiempo(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = int(context.job.data["chat_id"])
    partida = impostores_activos.get(chat_id)
    if not partida or partida.get("estado") != "pistas":
        return
    await iniciar_votacion(context, chat_id)


def teclado_votacion(partida: dict[str, Any], chat_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(partida["jugadores"].get(uid, "Alguien")[:40],
        callback_data=f"imp_vote:{chat_id}:{uid}:{partida['ronda_votacion']}")] for uid in partida["candidatos"]])


async def iniciar_votacion(context: ContextTypes.DEFAULT_TYPE, chat_id: int, candidatos: Optional[list[int]] = None) -> None:
    partida = impostores_activos.get(chat_id)
    if not partida:
        return
    partida["estado"], partida["votos"], partida["ronda_votacion"] = "votacion", {}, partida["ronda_votacion"] + 1
    partida["candidatos"] = candidatos or list(partida["jugadores"].keys())
    pistas = "\n".join(f"• {partida['jugadores'].get(uid, 'Alguien')}: {p}" for uid, p in partida["pistas"].items()) or "Nadie mandó ninguna pista."
    await context.bot.send_message(chat_id=chat_id, text=f"🗳️ HORA DE VOTAR\n\nPistas:\n{pistas}\n\n¿Quién es el impostor?",
                                   reply_markup=teclado_votacion(partida, chat_id))
    ronda = partida["ronda_votacion"]
    context.job_queue.run_once(cerrar_votacion_por_tiempo, when=TIEMPO_VOTACION,
        data={"chat_id": chat_id, "ronda": ronda}, name=nombre_job("votacion", chat_id, ronda))


async def cerrar_votacion_por_tiempo(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id, ronda = int(context.job.data["chat_id"]), int(context.job.data["ronda"])
    partida = impostores_activos.get(chat_id)
    if partida and partida.get("estado") == "votacion" and partida.get("ronda_votacion") == ronda:
        await resolver_votacion(context, chat_id)


async def resolver_votacion(context, chat_id: int) -> None:
    partida = impostores_activos.get(chat_id)
    if not partida or partida.get("estado") != "votacion":
        return
    conteo = {uid: 0 for uid in partida["candidatos"]}
    for candidato in partida["votos"].values():
        if candidato in conteo:
            conteo[candidato] += 1
    if not partida["votos"]:
        await context.bot.send_message(chat_id=chat_id, text="💀 No votó nadie. El impostor gana.")
        await finalizar_partida(context, chat_id, True, "sin_votos")
        return
    max_votos = max(conteo.values())
    empatados = [uid for uid, total in conteo.items() if total == max_votos]
    if len(empatados) > 1:
        await context.bot.send_message(chat_id=chat_id, text="⚖️ Hay empate. Se repite la votación solo entre los empatados.")
        await iniciar_votacion(context, chat_id, empatados)
        return
    acusado = empatados[0]
    if acusado != partida["impostor_id"]:
        await context.bot.send_message(chat_id=chat_id, text=(f"❌ {partida['jugadores'].get(acusado)} no era.\n"
            f"🕵️ El impostor era {partida['jugadores'].get(partida['impostor_id'])}.\n"
            f"🔐 La palabra era {partida['palabra'].upper()}."))
        await finalizar_partida(context, chat_id, True, "no_descubierto")
        return
    partida["estado"] = "adivinar_palabra"
    await context.bot.send_message(chat_id=chat_id, text=f"🎯 Habéis descubierto a {partida['jugadores'].get(acusado)}. Tiene una última oportunidad por privado.")
    try:
        await context.bot.send_message(chat_id=partida["impostor_id"], text=f"🕵️ Te han descubierto. Adivina la palabra. Tienes {TIEMPO_ADIVINAR} segundos.")
    except TelegramError:
        await finalizar_partida(context, chat_id, False, "sin_respuesta")
        return
    context.job_queue.run_once(cerrar_adivinanza_por_tiempo, when=TIEMPO_ADIVINAR,
                               data={"chat_id": chat_id}, name=nombre_job("adivinar", chat_id))


async def resolver_adivinanza(context, chat_id: int, respuesta: str) -> None:
    partida = impostores_activos.get(chat_id)
    if not partida or partida.get("estado") != "adivinar_palabra":
        return
    acierta = normalizar(respuesta) == normalizar(partida["palabra"])
    await context.bot.send_message(chat_id=chat_id, text=(
        f"😈 Ha acertado: {partida['palabra'].upper()}. Gana el impostor." if acierta else
        f"❌ Respondió «{respuesta}». La palabra era {partida['palabra'].upper()}. Ganan los civiles."))
    await finalizar_partida(context, chat_id, acierta, "palabra_acertada" if acierta else "palabra_fallada")


async def cerrar_adivinanza_por_tiempo(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = int(context.job.data["chat_id"])
    partida = impostores_activos.get(chat_id)
    if partida and partida.get("estado") == "adivinar_palabra":
        await context.bot.send_message(chat_id=chat_id, text=f"⏰ No respondió. La palabra era {partida['palabra'].upper()}. Ganan los civiles.")
        await finalizar_partida(context, chat_id, False, "tiempo_agotado")


async def finalizar_partida(context, chat_id: int, gana_impostor: bool, motivo: str) -> None:
    partida = impostores_activos.get(chat_id)
    if not partida:
        return
    imp = partida["impostor_id"]
    for uid, nombre in partida["jugadores"].items():
        datos = estadisticas_usuario(uid, nombre)
        datos["partidas"] += 1
        if uid == imp:
            datos["veces_impostor"] += 1
    if gana_impostor:
        d = estadisticas_usuario(imp, partida["jugadores"].get(imp, "Alguien")); d["victorias"] += 1; d["puntos"] += 15
        if motivo == "palabra_acertada": d["palabras_acertadas"] += 1; d["puntos"] += 5
    else:
        for uid, nombre in partida["jugadores"].items():
            if uid != imp:
                d = estadisticas_usuario(uid, nombre); d["victorias"] += 1; d["puntos"] += 10
    guardar_ranking(); cancelar_jobs(context, chat_id); impostores_activos.pop(chat_id, None)


async def cancelar_impostor(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int, admin_ids: list[int]) -> None:
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text("🚫 Solo los administradores pueden cancelar la partida."); return
    if chat_id not in impostores_activos:
        await update.message.reply_text("No hay ninguna partida activa."); return
    cancelar_jobs(context, chat_id); impostores_activos.pop(chat_id, None)
    await update.message.reply_text("🛑 Partida de El Impostor cancelada.")


async def mostrar_ranking_impostor(update: Update) -> None:
    if not ranking_impostor:
        await update.message.reply_text("Todavía no hay ranking de El Impostor."); return
    ordenado = sorted(ranking_impostor.values(), key=lambda d: (d.get("puntos", 0), d.get("victorias", 0)), reverse=True)[:10]
    texto = "🎭 RANKING DE EL IMPOSTOR\n\n" + "\n".join(
        f"{i}. {d.get('nombre', 'Alguien')} — {d.get('puntos', 0)} puntos · {d.get('victorias', 0)} victoria(s)"
        for i, d in enumerate(ordenado, 1))
    await update.message.reply_text(texto)


async def botones_impostor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return
    partes, accion = query.data.split(":"), query.data.split(":")[0]
    if accion in ("imp_join", "imp_leave", "imp_start"):
        chat_id = int(partes[1]); partida = impostores_activos.get(chat_id)
        if not partida:
            await query.answer("Esta partida ya no existe.", show_alert=True); return
        if partida["estado"] != "inscripcion":
            await query.answer("La partida ya ha empezado.", show_alert=True); return
        uid = query.from_user.id
        if accion == "imp_join":
            partida["jugadores"][uid] = nombre_usuario(query.from_user); await query.answer("Te has apuntado 🎭", show_alert=True); await actualizar_inscripcion(context, chat_id); return
        if accion == "imp_leave":
            partida["jugadores"].pop(uid, None); await query.answer("Has salido.", show_alert=True); await actualizar_inscripcion(context, chat_id); return
        admins = await context.bot.get_chat_administrators(chat_id)
        if uid not in [a.user.id for a in admins]:
            await query.answer("Solo un administrador puede empezar.", show_alert=True); return
        if len(partida["jugadores"]) < MINIMO_JUGADORES:
            await query.answer(f"Hacen falta al menos {MINIMO_JUGADORES} jugadores.", show_alert=True); return
        await query.answer("Repartiendo roles…", show_alert=True); await query.message.edit_reply_markup(reply_markup=None); await comenzar_partida(context, chat_id); return
    if accion == "imp_vote":
        chat_id, candidato, ronda = int(partes[1]), int(partes[2]), int(partes[3]); partida = impostores_activos.get(chat_id)
        if not partida or partida.get("estado") != "votacion" or partida.get("ronda_votacion") != ronda:
            await query.answer("La votación ya terminó.", show_alert=True); return
        uid = query.from_user.id
        if uid not in partida["jugadores"]:
            await query.answer("Solo votan los participantes.", show_alert=True); return
        if uid == candidato:
            await query.answer("No puedes votarte a ti mismo.", show_alert=True); return
        if uid in partida["votos"]:
            await query.answer("Ya has votado.", show_alert=True); return
        partida["votos"][uid] = candidato; await query.answer(f"Has votado a {partida['jugadores'].get(candidato)}.", show_alert=True)
        if len(partida["votos"]) >= len(partida["jugadores"]):
            await resolver_votacion(context, chat_id)
