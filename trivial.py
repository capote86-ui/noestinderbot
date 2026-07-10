import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from preguntas_trivial import preguntas_trivial

trivials_activos = {}
ranking_trivial = {}


def nombre_usuario(user):
    if user.username:
        return f"@{user.username}"
    return user.first_name or "Alguien"


def estrellas(dificultad):
    try:
        dificultad = int(dificultad)
    except Exception:
        dificultad = 1

    if dificultad <= 1:
        return "⭐ Fácil"
    if dificultad == 2:
        return "⭐⭐ Media"
    if dificultad == 3:
        return "⭐⭐⭐ Difícil"
    return "⭐⭐⭐⭐ Experto"


def preparar_pregunta(pregunta):
    opciones = pregunta["opciones"].copy()

    correcta = pregunta["correcta"]

    # Compatible con formato antiguo: correcta = "A", "B", "C" o "D"
    if correcta in ["A", "B", "C", "D"]:
        correcta_texto = pregunta["opciones"]["ABCD".index(correcta)]
    else:
        correcta_texto = correcta

    random.shuffle(opciones)

    letras = ["A", "B", "C", "D"]
    opciones_mezcladas = dict(zip(letras, opciones))

    letra_correcta = None
    for letra, texto in opciones_mezcladas.items():
        if texto == correcta_texto:
            letra_correcta = letra
            break

    return opciones_mezcladas, correcta_texto, letra_correcta


async def iniciar_trivial(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int, admin_ids: list):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text("🚫 Solo los administradores pueden iniciar un trivial.")
        return

    if chat_id in trivials_activos:
        await update.message.reply_text("Ya hay un trivial activo en este grupo.")
        return

    preguntas_partida = random.sample(
        preguntas_trivial,
        min(15, len(preguntas_trivial))
    )

    trivials_activos[chat_id] = {
        "indice": 0,
        "preguntas": preguntas_partida,
        "jugadores": {},
        "puntos": {},
        "respuestas": {},
        "mensaje_id": None,
        "estado": "inscripcion",
        "ronda": 0,
        "opciones_actuales": {},
        "correcta_texto": None,
        "letra_correcta": None
    }

    teclado = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Participar", callback_data=f"trivia_join:{chat_id}"),
        InlineKeyboardButton("▶️ Empezar", callback_data=f"trivia_start:{chat_id}")
    ]])

    mensaje = await update.message.reply_text(
        "🧠 TRIVIAL NO ES TINDER\n\n"
        "Partida de 15 preguntas random.\n\n"
        "✅ Pulsa Participar para apuntarte.\n"
        "▶️ Cuando estéis listos, un admin pulsa Empezar.\n\n"
        "Participantes: nadie todavía.",
        reply_markup=teclado
    )

    trivials_activos[chat_id]["mensaje_id"] = mensaje.message_id


async def actualizar_mensaje_inscripcion(context, chat_id):
    partida = trivials_activos.get(chat_id)
    if not partida:
        return

    jugadores = partida["jugadores"]

    if jugadores:
        lista = "\n".join([f"• {nombre}" for nombre in jugadores.values()])
    else:
        lista = "nadie todavía."

    teclado = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Participar", callback_data=f"trivia_join:{chat_id}"),
        InlineKeyboardButton("▶️ Empezar", callback_data=f"trivia_start:{chat_id}")
    ]])

    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=partida["mensaje_id"],
        text=(
            "🧠 TRIVIAL NO ES TINDER\n\n"
            "Partida de 15 preguntas random.\n\n"
            "✅ Pulsa Participar para apuntarte.\n"
            "▶️ Cuando estéis listos, un admin pulsa Empezar.\n\n"
            f"Participantes:\n{lista}"
        ),
        reply_markup=teclado
    )


async def enviar_pregunta_trivial(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    partida = trivials_activos.get(chat_id)
    if not partida:
        return

    indice = partida["indice"]

    if indice >= len(partida["preguntas"]):
        await finalizar_trivial(context, chat_id)
        return

    pregunta = partida["preguntas"][indice]

    opciones_mezcladas, correcta_texto, letra_correcta = preparar_pregunta(pregunta)

    partida["respuestas"] = {}
    partida["estado"] = "pregunta"
    partida["ronda"] += 1
    partida["opciones_actuales"] = opciones_mezcladas
    partida["correcta_texto"] = correcta_texto
    partida["letra_correcta"] = letra_correcta

    ronda_actual = partida["ronda"]

    categoria = pregunta.get("categoria", "Random")
    dificultad = estrellas(pregunta.get("dificultad", 1))

    texto = (
        f"🧠 TRIVIAL NO ES TINDER\n\n"
        f"Pregunta {indice + 1}/15\n"
        f"📚 Categoría: {categoria}\n"
        f"{dificultad}\n"
        f"⏱️ Tenéis 20 segundos para responder.\n\n"
        f"{pregunta['pregunta']}\n\n"
        f"A) {opciones_mezcladas['A']}\n"
        f"B) {opciones_mezcladas['B']}\n"
        f"C) {opciones_mezcladas['C']}\n"
        f"D) {opciones_mezcladas['D']}"
    )

    teclado = InlineKeyboardMarkup([[
        InlineKeyboardButton("A", callback_data=f"trivia_respuesta:A:{chat_id}:{ronda_actual}"),
        InlineKeyboardButton("B", callback_data=f"trivia_respuesta:B:{chat_id}:{ronda_actual}"),
        InlineKeyboardButton("C", callback_data=f"trivia_respuesta:C:{chat_id}:{ronda_actual}"),
        InlineKeyboardButton("D", callback_data=f"trivia_respuesta:D:{chat_id}:{ronda_actual}")
    ]])

    mensaje = await context.bot.send_message(
        chat_id=chat_id,
        text=texto,
        reply_markup=teclado
    )

    partida["mensaje_id"] = mensaje.message_id

    context.job_queue.run_once(
        cerrar_pregunta_por_tiempo,
        when=20,
        data={"chat_id": chat_id, "ronda": ronda_actual},
        name=f"trivial_{chat_id}_{ronda_actual}"
    )


async def cerrar_pregunta_por_tiempo(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data["chat_id"]
    ronda = context.job.data["ronda"]

    partida = trivials_activos.get(chat_id)
    if not partida:
        return

    if partida.get("ronda") != ronda:
        return

    if partida.get("estado") != "pregunta":
        return

    await cerrar_pregunta_trivial(context, chat_id)


async def cerrar_pregunta_trivial(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    partida = trivials_activos.get(chat_id)
    if not partida:
        return

    partida["estado"] = "cerrando"

    indice = partida["indice"]
    pregunta = partida["preguntas"][indice]

    correcta_texto = partida["correcta_texto"]
    letra_correcta = partida["letra_correcta"]

    acertantes = []

    for user_id, respuesta_texto in partida["respuestas"].items():
        if respuesta_texto == correcta_texto:
            partida["puntos"][user_id] = partida["puntos"].get(user_id, 0) + 1
            acertantes.append(partida["jugadores"].get(user_id, "Alguien"))

    texto = (
        f"✅ Respuesta correcta: {letra_correcta}) {correcta_texto}\n\n"
    )

    explicacion = pregunta.get("explicacion")
    if explicacion:
        texto += f"📖 {explicacion}\n\n"

    if acertantes:
        texto += "🎯 Han acertado:\n"
        for nombre in acertantes:
            texto += f"• {nombre}\n"
    else:
        texto += "💀 No ha acertado nadie. Dolor académico.\n"

    texto += "\n🏆 Marcador actual:\n"

    ranking = sorted(partida["puntos"].items(), key=lambda x: x[1], reverse=True)

    if ranking:
        for user_id, puntos in ranking:
            nombre = partida["jugadores"].get(user_id, "Alguien")
            texto += f"• {nombre}: {puntos} punto(s)\n"
    else:
        texto += "• Nadie ha puntuado todavía.\n"

    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=partida["mensaje_id"],
        text=texto
    )

    partida["indice"] += 1

    await enviar_pregunta_trivial(context, chat_id)


async def finalizar_trivial(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    partida = trivials_activos.get(chat_id)
    if not partida:
        return

    texto = "🏁 FINAL DEL TRIVIAL\n\n"

    ranking = sorted(partida["puntos"].items(), key=lambda x: x[1], reverse=True)

    if not ranking:
        texto += "Nadie ha puntuado. Esto ha sido un simulacro emocional 😭"
    else:
        for i, (user_id, puntos) in enumerate(ranking, start=1):
            nombre = partida["jugadores"].get(user_id, "Alguien")
            texto += f"{i}. {nombre} — {puntos}/15\n"
            ranking_trivial[user_id] = ranking_trivial.get(user_id, 0) + puntos

        ganador_id = ranking[0][0]
        ganador = partida["jugadores"].get(ganador_id, "Alguien")
        texto += f"\n👑 Ganador/a: {ganador}"

    trivials_activos.pop(chat_id, None)

    await context.bot.send_message(chat_id=chat_id, text=texto)


async def cancelar_trivial(update: Update, chat_id: int, admin_ids: list):
    if update.effective_user.id not in admin_ids:
        return

    if chat_id in trivials_activos:
        trivials_activos.pop(chat_id, None)
        await update.message.reply_text("🛑 Trivial cancelado.")
    else:
        await update.message.reply_text("No hay trivial activo.")


async def mostrar_ranking_trivial(update: Update):
    if not ranking_trivial:
        await update.message.reply_text("Todavía no hay ranking de trivial.")
        return

    ranking = sorted(ranking_trivial.items(), key=lambda x: x[1], reverse=True)[:10]

    texto = "🏆 Ranking histórico del trivial\n\n"

    for i, (user_id, puntos) in enumerate(ranking, start=1):
        texto += f"{i}. Usuario {user_id} — {puntos} puntos\n"

    await update.message.reply_text(texto)


async def botones_trivial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    datos = query.data.split(":")
    accion = datos[0]

    if accion == "trivia_join":
        chat_id = int(datos[1])

        if chat_id not in trivials_activos:
            await query.answer("No hay trivial activo.", show_alert=True)
            return

        partida = trivials_activos[chat_id]

        if partida["estado"] != "inscripcion":
            await query.answer("La partida ya empezó.", show_alert=True)
            return

        user_id = query.from_user.id
        nombre = nombre_usuario(query.from_user)

        partida["jugadores"][user_id] = nombre
        partida["puntos"][user_id] = 0

        await query.answer("Te has apuntado al trivial 🧠", show_alert=True)
        await actualizar_mensaje_inscripcion(context, chat_id)
        return

    if accion == "trivia_start":
        chat_id = int(datos[1])

        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        if query.from_user.id not in admin_ids:
            await query.answer("Solo los admins pueden empezar la partida.", show_alert=True)
            return

        if chat_id not in trivials_activos:
            await query.answer("No hay trivial preparado.", show_alert=True)
            return

        if not trivials_activos[chat_id]["jugadores"]:
            await query.answer("Aún no se ha apuntado nadie.", show_alert=True)
            return

        await query.answer("Empieza el trivial 🧠", show_alert=True)
        await query.message.edit_text("🧠 Empieza el trivial. Que gane el menos NPC.")
        await enviar_pregunta_trivial(context, chat_id)
        return

    if accion == "trivia_respuesta":
        respuesta_letra = datos[1]
        chat_id = int(datos[2])
        ronda = int(datos[3])

        if chat_id not in trivials_activos:
            await query.answer("Esta partida ya terminó.", show_alert=True)
            return

        partida = trivials_activos[chat_id]

        if partida.get("ronda") != ronda:
            await query.answer("Esta pregunta ya no está activa.", show_alert=True)
            return

        if partida.get("estado") != "pregunta":
            await query.answer("Esta pregunta ya está cerrada.", show_alert=True)
            return

        user_id = query.from_user.id

        if user_id not in partida["jugadores"]:
            await query.answer("No estás apuntado/a a esta partida.", show_alert=True)
            return

        if user_id in partida["respuestas"]:
            await query.answer("Ya has respondido esta pregunta.", show_alert=True)
            return

        respuesta_texto = partida["opciones_actuales"].get(respuesta_letra)

        partida["respuestas"][user_id] = respuesta_texto

        await query.answer(f"Respuesta registrada: {respuesta_letra}", show_alert=True)

        if len(partida["respuestas"]) >= len(partida["jugadores"]):
            await cerrar_pregunta_trivial(context, chat_id)
