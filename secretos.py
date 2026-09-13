import json
import os
import random
import time
from typing import Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from misiones_secretos import MISIONES_SECRETOS


CARPETA_DATOS = "/data" if os.path.isdir("/data") else "."
ARCHIVO_SECRETOS = os.path.join(CARPETA_DATOS, "secretos.json")

MIN_JUGADORES = 4
MAX_JUGADORES = 15
DURACION_PARTIDA = 20 * 60
AVISO_FINAL = 2 * 60
PUNTOS_MISION = 5
PUNTOS_ACIERTO = 3
PUNTOS_FALLO = -2
PUNTOS_LADRON = 2
MAX_ACUSACIONES_NORMAL = 2
MAX_ACUSACIONES_LADRON = 4


def _datos_vacios() -> dict[str, Any]:
    return {"partidas": {}, "ranking": {}}


def _cargar_datos() -> dict[str, Any]:
    if not os.path.exists(ARCHIVO_SECRETOS):
        return _datos_vacios()
    try:
        with open(ARCHIVO_SECRETOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        if not isinstance(datos, dict):
            return _datos_vacios()
        datos.setdefault("partidas", {})
        datos.setdefault("ranking", {})
        return datos
    except (OSError, json.JSONDecodeError, TypeError):
        return _datos_vacios()


datos_secretos = _cargar_datos()


def _guardar_datos() -> None:
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    temporal = f"{ARCHIVO_SECRETOS}.tmp"
    try:
        with open(temporal, "w", encoding="utf-8") as archivo:
            json.dump(datos_secretos, archivo, ensure_ascii=False, indent=2)
        os.replace(temporal, ARCHIVO_SECRETOS)
    except OSError as error:
        print(f"No se pudieron guardar los datos de Secretos: {error}")


def _partida(chat_id: int) -> dict[str, Any] | None:
    return datos_secretos.get("partidas", {}).get(str(chat_id))


def _nombre_usuario(usuario) -> str:
    if getattr(usuario, "username", None):
        return f"@{usuario.username}"
    return usuario.first_name or "Jugador"


def _teclado_inscripcion(bot_username: str | None = None) -> InlineKeyboardMarkup:
    filas = [
        [
            InlineKeyboardButton("🎭 Me apunto", callback_data="sec_join"),
            InlineKeyboardButton("🚪 Me bajo", callback_data="sec_leave"),
        ],
        [
            InlineKeyboardButton("🚀 Empezar", callback_data="sec_start"),
            InlineKeyboardButton("🛑 Cancelar", callback_data="sec_cancel"),
        ],
    ]
    if bot_username:
        filas.append([
            InlineKeyboardButton(
                "🔐 Abrir privado del bot",
                url=f"https://t.me/{bot_username}?start=secretos",
            )
        ])
    return InlineKeyboardMarkup(filas)


def _texto_inscripcion(partida: dict[str, Any]) -> str:
    jugadores = partida.get("jugadores", {})
    nombres = [j.get("nombre", "Jugador") for j in jugadores.values()]
    lista = "\n".join(f"• {n}" for n in nombres) if nombres else "• Nadie todavía"
    return (
        "🎭 EL JUEGO DE LOS SECRETOS\n\n"
        "Cada jugador recibirá por privado una misión secreta. "
        "Tendrás que cumplirla sin que el resto descubra qué estás intentando hacer.\n\n"
        "🕵️ Uno de vosotros será EL LADRÓN: no tendrá una misión normal y deberá descubrir las de los demás.\n\n"
        f"👥 Jugadores: {len(jugadores)}/{MAX_JUGADORES}\n{lista}\n\n"
        f"✅ Mínimo: {MIN_JUGADORES} jugadores\n"
        "⏱️ Partida: 20 minutos\n"
        "🔐 IMPORTANTE: antes de apuntarte, abre el privado de No es Tinderbot y pulsa /start."
    )


async def inicio_privado_secretos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.type != "private":
        return
    await update.message.reply_text(
        "✅ Privado de No es Tinderbot activado.\n\n"
        "Ya puedo enviarte misiones secretas cuando participes en 🎭 El juego de los secretos.\n"
        "Vuelve al grupo y pulsa «Me apunto»."
    )


async def iniciar_secretos(update: Update, context: ContextTypes.DEFAULT_TYPE, admin_ids) -> None:
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text("🚫 Solo los administradores pueden abrir una partida.")
        return

    chat_id = update.effective_chat.id
    existente = _partida(chat_id)
    if existente and existente.get("estado") in {"inscripcion", "jugando", "finalizando"}:
        await update.message.reply_text("🎭 Ya hay una partida de Secretos abierta en este grupo.")
        return

    me = await context.bot.get_me()
    partida = {
        "chat_id": chat_id,
        "estado": "inscripcion",
        "creada_ts": int(time.time()),
        "jugadores": {},
        "mensaje_inscripcion_id": None,
        "fin_ts": None,
        "aviso_enviado": False,
        "ranking_aplicado": False,
    }
    datos_secretos.setdefault("partidas", {})[str(chat_id)] = partida
    _guardar_datos()

    mensaje = await update.message.reply_text(
        _texto_inscripcion(partida),
        reply_markup=_teclado_inscripcion(me.username),
    )
    partida["mensaje_inscripcion_id"] = mensaje.message_id
    _guardar_datos()


async def cancelar_secretos(update: Update, context: ContextTypes.DEFAULT_TYPE, admin_ids) -> None:
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text("🚫 Solo los administradores pueden cancelar la partida.")
        return

    chat_id = update.effective_chat.id
    partida = _partida(chat_id)
    if not partida or partida.get("estado") not in {"inscripcion", "jugando", "finalizando"}:
        await update.message.reply_text("No hay ninguna partida de Secretos activa.")
        return

    _eliminar_jobs(context, chat_id)
    partida["estado"] = "cancelada"
    _guardar_datos()
    await update.message.reply_text("🛑 Partida de Secretos cancelada por administración.")


async def ranking_secretos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ranking = datos_secretos.get("ranking", {})
    if not ranking:
        await update.message.reply_text("🏆 Todavía no hay ranking de Secretos. Hay que delinquir primero.")
        return

    orden = sorted(
        ranking.values(),
        key=lambda x: (int(x.get("puntos", 0)), int(x.get("victorias", 0))),
        reverse=True,
    )[:10]

    texto = "🏆 RANKING · JUEGO DE LOS SECRETOS\n\n"
    for pos, ficha in enumerate(orden, start=1):
        texto += (
            f"{pos}. {ficha.get('nombre', 'Jugador')} — "
            f"{int(ficha.get('puntos', 0))} pts · "
            f"{int(ficha.get('victorias', 0))} victoria(s)\n"
        )
    await update.message.reply_text(texto)


def _eliminar_jobs(context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> None:
    for prefijo in (f"secretos_aviso_{chat_id}", f"secretos_fin_{chat_id}"):
        for job in context.job_queue.get_jobs_by_name(prefijo):
            job.schedule_removal()


def _programar_jobs(context: ContextTypes.DEFAULT_TYPE, chat_id: int, fin_ts: int) -> None:
    _eliminar_jobs(context, chat_id)
    ahora = int(time.time())
    segundos_fin = max(1, fin_ts - ahora)
    segundos_aviso = fin_ts - AVISO_FINAL - ahora

    if segundos_aviso > 0:
        context.job_queue.run_once(
            aviso_ronda_final,
            when=segundos_aviso,
            data={"chat_id": chat_id},
            name=f"secretos_aviso_{chat_id}",
        )

    context.job_queue.run_once(
        finalizar_secretos_job,
        when=segundos_fin,
        data={"chat_id": chat_id},
        name=f"secretos_fin_{chat_id}",
    )


async def _actualizar_inscripcion(query, context, partida: dict[str, Any]) -> None:
    try:
        me = await context.bot.get_me()
        await query.edit_message_text(
            _texto_inscripcion(partida),
            reply_markup=_teclado_inscripcion(me.username),
        )
    except TelegramError:
        pass


async def _es_admin(context, chat_id: int, user_id: int) -> bool:
    try:
        admins = await context.bot.get_chat_administrators(chat_id)
        return user_id in [a.user.id for a in admins]
    except TelegramError:
        return False


async def _comenzar_partida(query, context, partida: dict[str, Any]) -> None:
    chat_id = int(partida["chat_id"])
    jugadores = partida.get("jugadores", {})
    if len(jugadores) < MIN_JUGADORES:
        await query.answer(f"Hacen falta al menos {MIN_JUGADORES} jugadores.", show_alert=True)
        return

    ids = list(jugadores.keys())
    ladron_id = random.choice(ids)
    indices_disponibles = list(range(len(MISIONES_SECRETOS)))
    random.shuffle(indices_disponibles)
    necesarios = len(ids) - 1
    if necesarios > len(indices_disponibles):
        await query.answer("No hay suficientes misiones configuradas.", show_alert=True)
        return

    mision_pos = 0
    for uid in ids:
        ficha = jugadores[uid]
        ficha["rol"] = "ladron" if uid == ladron_id else "jugador"
        ficha["mision_idx"] = None if uid == ladron_id else indices_disponibles[mision_pos]
        if uid != ladron_id:
            mision_pos += 1
        ficha["mision_cumplida"] = False
        ficha["puntos"] = 0
        ficha["acusaciones"] = 0
        ficha["descubiertos"] = []

    ahora = int(time.time())
    partida["estado"] = "jugando"
    partida["inicio_ts"] = ahora
    partida["fin_ts"] = ahora + DURACION_PARTIDA
    partida["aviso_enviado"] = False
    partida["ranking_aplicado"] = False
    _guardar_datos()

    errores = []
    for uid, ficha in jugadores.items():
        user_id = int(uid)
        if ficha["rol"] == "ladron":
            texto = (
                "🕵️ ERES EL LADRÓN\n\n"
                "No tienes una misión normal. Tu objetivo es descubrir las misiones de los demás sin que sepan quién eres.\n\n"
                f"✅ Cada misión que descubras: +{PUNTOS_LADRON} puntos.\n"
                f"❌ Cada acusación fallida: {PUNTOS_FALLO} puntos.\n"
                f"🔎 Puedes hacer hasta {MAX_ACUSACIONES_LADRON} acusaciones durante la partida.\n\n"
                "Compórtate como si tú también tuvieras una misión. 😈"
            )
            teclado = InlineKeyboardMarkup([[
                InlineKeyboardButton("🔎 Acusar a alguien", callback_data=f"sec_accuse:{chat_id}")
            ]])
        else:
            mision = MISIONES_SECRETOS[int(ficha["mision_idx"])]
            texto = (
                "🎯 TU MISIÓN SECRETA\n\n"
                f"{mision}\n\n"
                "Tienes 20 minutos. Intenta conseguirlo sin que los demás descubran qué estás haciendo.\n\n"
                f"✅ Si la cumples: +{PUNTOS_MISION} puntos.\n"
                f"🔎 También puedes intentar descubrir misiones ajenas (+{PUNTOS_ACIERTO}/"
                f"{PUNTOS_FALLO} puntos)."
            )
            teclado = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ He cumplido mi misión", callback_data=f"sec_claim:{chat_id}")],
                [InlineKeyboardButton("🔎 Acusar a alguien", callback_data=f"sec_accuse:{chat_id}")],
            ])
        try:
            await context.bot.send_message(user_id, texto, reply_markup=teclado)
        except TelegramError:
            errores.append(ficha.get("nombre", str(uid)))

    if errores:
        partida["estado"] = "inscripcion"
        partida["fin_ts"] = None
        _guardar_datos()
        await context.bot.send_message(
            chat_id,
            "⚠️ No he podido enviar la misión por privado a: " + ", ".join(errores) +
            ".\nQue abran No es Tinderbot, pulsen /start y vuelvan a apuntarse."
        )
        return

    _programar_jobs(context, chat_id, int(partida["fin_ts"]))
    await query.edit_message_text(
        "🎭 EL JUEGO DE LOS SECRETOS HA EMPEZADO\n\n"
        "🔐 Ya tenéis vuestra misión por privado.\n"
        "🕵️ Entre vosotros hay un Ladrón.\n"
        "⏱️ Tenéis 20 minutos.\n\n"
        "Hablad con normalidad, cumplid vuestra misión, desconfiad de todos y no os delatéis. 😈\n\n"
        "No es Tinderbot se encargará del tiempo, las acusaciones, los puntos y el final."
    )


async def botones_secretos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return

    data = query.data
    partes = data.split(":")
    accion = partes[0]

    if accion in {"sec_join", "sec_leave", "sec_start", "sec_cancel"}:
        chat_id = query.message.chat.id
        partida = _partida(chat_id)
        if not partida or partida.get("estado") != "inscripcion":
            await query.answer("Esta inscripción ya no está activa.", show_alert=True)
            return

        uid = str(query.from_user.id)
        jugadores = partida.setdefault("jugadores", {})

        if accion == "sec_join":
            if uid in jugadores:
                await query.answer("Ya estás apuntado/a 😏", show_alert=True)
                return
            if len(jugadores) >= MAX_JUGADORES:
                await query.answer("La partida está completa.", show_alert=True)
                return
            try:
                await context.bot.send_message(
                    query.from_user.id,
                    "🔐 Privado comprobado. Ya puedes participar en El juego de los secretos."
                )
            except TelegramError:
                await query.answer(
                    "Primero abre el privado de No es Tinderbot y pulsa /start. Después vuelve a intentarlo.",
                    show_alert=True,
                )
                return

            jugadores[uid] = {
                "nombre": _nombre_usuario(query.from_user),
                "username": query.from_user.username,
            }
            _guardar_datos()
            await query.answer("🎭 Apuntado/a. No te fíes de nadie.")
            await _actualizar_inscripcion(query, context, partida)
            return

        if accion == "sec_leave":
            if uid not in jugadores:
                await query.answer("No estabas apuntado/a.", show_alert=True)
                return
            jugadores.pop(uid, None)
            _guardar_datos()
            await query.answer("🚪 Te has bajado de la partida.")
            await _actualizar_inscripcion(query, context, partida)
            return

        if not await _es_admin(context, chat_id, query.from_user.id):
            await query.answer("Solo un administrador puede hacer eso.", show_alert=True)
            return

        if accion == "sec_cancel":
            partida["estado"] = "cancelada"
            _guardar_datos()
            await query.edit_message_text("🛑 Partida de Secretos cancelada.")
            return

        if accion == "sec_start":
            await query.answer()
            await _comenzar_partida(query, context, partida)
            return

    if len(partes) < 2:
        await query.answer()
        return

    try:
        chat_id = int(partes[1])
    except ValueError:
        await query.answer()
        return

    partida = _partida(chat_id)
    if not partida or partida.get("estado") != "jugando":
        await query.answer("Esta partida ya no está activa.", show_alert=True)
        return

    uid = str(query.from_user.id)
    jugadores = partida.get("jugadores", {})
    jugador = jugadores.get(uid)
    if not jugador:
        await query.answer("No formas parte de esta partida.", show_alert=True)
        return

    if accion == "sec_claim":
        if jugador.get("rol") == "ladron":
            await query.answer("Tú eres el Ladrón. No tienes una misión normal que cumplir 😈", show_alert=True)
            return
        if jugador.get("mision_cumplida"):
            await query.answer("Tu misión ya figura como cumplida.", show_alert=True)
            return
        jugador["mision_cumplida"] = True
        jugador["puntos"] = int(jugador.get("puntos", 0)) + PUNTOS_MISION
        _guardar_datos()
        await query.answer(f"✅ Misión marcada como cumplida. +{PUNTOS_MISION} puntos.", show_alert=True)
        return

    if accion == "sec_accuse":
        max_acusaciones = MAX_ACUSACIONES_LADRON if jugador.get("rol") == "ladron" else MAX_ACUSACIONES_NORMAL
        if int(jugador.get("acusaciones", 0)) >= max_acusaciones:
            await query.answer("Ya has gastado todas tus acusaciones.", show_alert=True)
            return

        objetivos = [
            (otro_uid, ficha)
            for otro_uid, ficha in jugadores.items()
            if otro_uid != uid and otro_uid not in jugador.get("descubiertos", [])
        ]
        if not objetivos:
            await query.answer("No te queda nadie nuevo a quien acusar.", show_alert=True)
            return

        botones = []
        fila = []
        for otro_uid, ficha in objetivos:
            fila.append(InlineKeyboardButton(
                ficha.get("nombre", "Jugador")[:28],
                callback_data=f"sec_target:{chat_id}:{otro_uid}",
            ))
            if len(fila) == 2:
                botones.append(fila)
                fila = []
        if fila:
            botones.append(fila)

        await query.message.reply_text(
            "🔎 ¿A quién quieres acusar?",
            reply_markup=InlineKeyboardMarkup(botones),
        )
        await query.answer()
        return

    if accion == "sec_target" and len(partes) == 3:
        target_id = partes[2]
        if target_id == uid or target_id not in jugadores:
            await query.answer("Objetivo no válido.", show_alert=True)
            return

        objetivo = jugadores[target_id]
        if objetivo.get("rol") == "ladron":
            correcta = -1
        else:
            correcta = int(objetivo["mision_idx"])

        candidatas = [i for i in range(len(MISIONES_SECRETOS)) if i != correcta]
        falsas = random.sample(candidatas, 3)
        opciones = falsas + [correcta]
        random.shuffle(opciones)

        texto = f"🔎 ¿Qué crees que tiene {objetivo.get('nombre', 'ese jugador')}?\n\n"
        letras = ["A", "B", "C", "D"]
        filas = []
        for letra, opcion in zip(letras, opciones):
            descripcion = "🕵️ ES EL LADRÓN" if opcion == -1 else MISIONES_SECRETOS[opcion]
            texto += f"{letra}) {descripcion}\n\n"
            filas.append([InlineKeyboardButton(
                letra,
                callback_data=f"sec_guess:{chat_id}:{target_id}:{opcion}",
            )])

        await query.message.reply_text(texto, reply_markup=InlineKeyboardMarkup(filas))
        await query.answer()
        return

    if accion == "sec_guess" and len(partes) == 4:
        target_id = partes[2]
        try:
            elegida = int(partes[3])
        except ValueError:
            await query.answer()
            return

        objetivo = jugadores.get(target_id)
        if not objetivo or target_id == uid:
            await query.answer("Objetivo no válido.", show_alert=True)
            return

        max_acusaciones = MAX_ACUSACIONES_LADRON if jugador.get("rol") == "ladron" else MAX_ACUSACIONES_NORMAL
        if int(jugador.get("acusaciones", 0)) >= max_acusaciones:
            await query.answer("Ya has gastado todas tus acusaciones.", show_alert=True)
            return
        if target_id in jugador.get("descubiertos", []):
            await query.answer("A esa persona ya la descubriste.", show_alert=True)
            return

        jugador["acusaciones"] = int(jugador.get("acusaciones", 0)) + 1
        correcta = -1 if objetivo.get("rol") == "ladron" else int(objetivo["mision_idx"])

        if elegida == correcta:
            puntos = PUNTOS_LADRON if jugador.get("rol") == "ladron" else PUNTOS_ACIERTO
            jugador["puntos"] = int(jugador.get("puntos", 0)) + puntos
            jugador.setdefault("descubiertos", []).append(target_id)
            _guardar_datos()
            await query.answer(f"✅ ¡ACIERTO! +{puntos} puntos.", show_alert=True)
        else:
            jugador["puntos"] = int(jugador.get("puntos", 0)) + PUNTOS_FALLO
            _guardar_datos()
            await query.answer(f"❌ Fallaste. {PUNTOS_FALLO} puntos.", show_alert=True)
        return

    await query.answer()


async def aviso_ronda_final(context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.job or not context.job.data:
        return
    chat_id = int(context.job.data["chat_id"])
    partida = _partida(chat_id)
    if not partida or partida.get("estado") != "jugando" or partida.get("aviso_enviado"):
        return

    partida["aviso_enviado"] = True
    _guardar_datos()
    try:
        await context.bot.send_message(
            chat_id,
            "⏰ RONDA FINAL\n\n"
            "Quedan 2 minutos. Última oportunidad para cumplir vuestra misión o lanzar una acusación. 👀\n"
            "Después No es Tinderbot levantará todas las cartas."
        )
    except TelegramError as error:
        print(f"No se pudo enviar el aviso final de Secretos: {error}")


async def finalizar_secretos_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.job or not context.job.data:
        return
    await finalizar_secretos(context, int(context.job.data["chat_id"]))


async def finalizar_secretos(context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> None:
    partida = _partida(chat_id)
    if not partida or partida.get("estado") not in {"jugando", "finalizando"}:
        return

    partida["estado"] = "finalizando"
    _guardar_datos()
    jugadores = partida.get("jugadores", {})
    if not jugadores:
        partida["estado"] = "finalizada"
        _guardar_datos()
        return

    orden = sorted(
        jugadores.items(),
        key=lambda item: int(item[1].get("puntos", 0)),
        reverse=True,
    )
    max_puntos = int(orden[0][1].get("puntos", 0))
    ganadores = [uid for uid, ficha in orden if int(ficha.get("puntos", 0)) == max_puntos]

    texto = "🎭 FIN DEL JUEGO DE LOS SECRETOS\n\n🔐 REVELACIÓN DE MISIONES\n\n"
    for uid, ficha in jugadores.items():
        nombre = ficha.get("nombre", "Jugador")
        if ficha.get("rol") == "ladron":
            secreto = "🕵️ ERA EL LADRÓN"
        else:
            idx = int(ficha.get("mision_idx", 0))
            estado = "✅ cumplida" if ficha.get("mision_cumplida") else "❌ no cumplida"
            secreto = f"🎯 {MISIONES_SECRETOS[idx]} ({estado})"
        texto += f"• {nombre}: {secreto}\n"

    texto += "\n🏆 PUNTUACIÓN\n"
    for pos, (uid, ficha) in enumerate(orden, start=1):
        corona = " 👑" if uid in ganadores else ""
        texto += f"{pos}. {ficha.get('nombre', 'Jugador')} — {int(ficha.get('puntos', 0))} pts{corona}\n"

    nombres_ganadores = ", ".join(jugadores[uid].get("nombre", "Jugador") for uid in ganadores)
    texto += f"\n👑 GANADOR/A: {nombres_ganadores}\n\nNo es Tinderbot lo sabe todo. Y ahora vosotros también. 😈"

    if not partida.get("ranking_aplicado"):
        ranking = datos_secretos.setdefault("ranking", {})
        for uid, ficha in jugadores.items():
            registro = ranking.setdefault(uid, {
                "nombre": ficha.get("nombre", "Jugador"),
                "puntos": 0,
                "victorias": 0,
                "partidas": 0,
            })
            registro["nombre"] = ficha.get("nombre", registro.get("nombre", "Jugador"))
            registro["puntos"] = int(registro.get("puntos", 0)) + int(ficha.get("puntos", 0))
            registro["partidas"] = int(registro.get("partidas", 0)) + 1
            if uid in ganadores:
                registro["victorias"] = int(registro.get("victorias", 0)) + 1
        partida["ranking_aplicado"] = True
        _guardar_datos()

    try:
        await context.bot.send_message(chat_id, texto)
    except TelegramError as error:
        print(f"No se pudo publicar el final de Secretos: {error}")

    partida["estado"] = "finalizada"
    partida["finalizada_ts"] = int(time.time())
    _guardar_datos()


async def restaurar_secretos_pendientes(application) -> None:
    """Restaura temporizadores de partidas activas después de reiniciar Railway."""
    if CARPETA_DATOS != "/data":
        print(
            "AVISO SECRETOS: /data no existe. La restauración funciona tras reinicios del proceso, "
            "pero para sobrevivir a redeploys de Railway necesitas un Volume montado en /data."
        )

    ahora = int(time.time())
    for chat_id_texto, partida in list(datos_secretos.get("partidas", {}).items()):
        estado = partida.get("estado")
        if estado not in {"jugando", "finalizando"}:
            continue
        try:
            chat_id = int(chat_id_texto)
            fin_ts = int(partida.get("fin_ts") or 0)
        except (TypeError, ValueError):
            continue

        if estado == "finalizando" or fin_ts <= ahora:
            application.job_queue.run_once(
                finalizar_secretos_job,
                when=1,
                data={"chat_id": chat_id},
                name=f"secretos_fin_{chat_id}",
            )
            continue

        if not partida.get("aviso_enviado") and fin_ts - AVISO_FINAL <= ahora:
            application.job_queue.run_once(
                aviso_ronda_final,
                when=1,
                data={"chat_id": chat_id},
                name=f"secretos_aviso_{chat_id}",
            )

        _programar_jobs(application, chat_id, fin_ts)

    _guardar_datos()
