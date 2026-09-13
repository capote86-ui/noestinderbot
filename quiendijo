import json
import random
from pathlib import Path
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

_BASE = Path(__file__).resolve().parent
with (_BASE / "quiendijo_frases.json").open(encoding="utf-8") as f:
    FRASES = json.load(f)

AUTORES = {}
for frase in FRASES:
    AUTORES[frase["author_id"]] = frase["author"]


def _elegir_frase(context):
    usadas = context.chat_data.setdefault("quiendijo_usadas", [])
    disponibles = [i for i in range(len(FRASES)) if i not in usadas]
    if not disponibles:
        usadas.clear()
        disponibles = list(range(len(FRASES)))
    indice = random.choice(disponibles)
    usadas.append(indice)
    return indice, FRASES[indice]


async def quien_dijo(update, context):
    indice, frase = _elegir_frase(context)
    correcto = frase["author_id"]

    otros = [aid for aid in AUTORES if aid != correcto]
    distractores = random.sample(otros, k=min(3, len(otros)))
    opciones = distractores + [correcto]
    random.shuffle(opciones)

    estado = context.chat_data.setdefault("quiendijo_partidas", {})
    estado[str(indice)] = {
        "correcto": correcto,
        "opciones": opciones,
        "respondieron": [],
        "resuelto": False,
    }

    teclado = [
        [InlineKeyboardButton(AUTORES[aid], callback_data=f"qd_{indice}_{pos}")]
        for pos, aid in enumerate(opciones)
    ]

    texto = (
        "🗣️ ¿QUIÉN DIJO?\n\n"
        f"«{frase['text']}»\n\n"
        "👀 ¿Quién soltó esta maravilla?"
    )
    await update.message.reply_text(texto, reply_markup=InlineKeyboardMarkup(teclado))


async def botones_quien_dijo(update, context):
    query = update.callback_query
    await query.answer()

    try:
        _, indice_s, pos_s = query.data.split("_")
        indice = int(indice_s)
        pos = int(pos_s)
    except (ValueError, IndexError):
        return

    estado = context.chat_data.get("quiendijo_partidas", {}).get(str(indice))
    if not estado:
        await query.answer("Esta ronda ya no está disponible.", show_alert=True)
        return
    if estado.get("resuelto"):
        await query.answer("Esta ronda ya está resuelta 😏", show_alert=True)
        return

    uid = str(query.from_user.id)
    if uid in estado["respondieron"]:
        await query.answer("Ya has respondido en esta ronda 👀", show_alert=True)
        return
    estado["respondieron"].append(uid)

    try:
        elegido = estado["opciones"][pos]
    except IndexError:
        return

    if elegido != estado["correcto"]:
        await query.answer("❌ No era esa persona. Has gastado tu intento 😈", show_alert=True)
        return

    estado["resuelto"] = True
    frase = FRASES[indice]
    nombre_ganador = query.from_user.first_name or "Alguien"

    ranking = context.chat_data.setdefault("ranking_quiendijo", {})
    ranking[uid] = ranking.get(uid, {"nombre": nombre_ganador, "puntos": 0})
    ranking[uid]["nombre"] = nombre_ganador
    ranking[uid]["puntos"] += 1

    texto = (
        "🗣️ ¿QUIÉN DIJO?\n\n"
        f"«{frase['text']}»\n\n"
        f"✅ Lo dijo: {frase['author']}\n"
        f"📅 {frase['date']}\n\n"
        f"🏆 {nombre_ganador} acertó y suma 1 punto."
    )
    await query.edit_message_text(texto)


async def ranking_quien_dijo(update, context):
    ranking = context.chat_data.get("ranking_quiendijo", {})
    if not ranking:
        await update.message.reply_text("🏆 Todavía no hay puntos en ¿Quién dijo?")
        return
    orden = sorted(ranking.values(), key=lambda x: x["puntos"], reverse=True)[:10]
    lineas = ["🏆 RANKING · ¿QUIÉN DIJO?", ""]
    medallas = ["🥇", "🥈", "🥉"]
    for i, dato in enumerate(orden):
        icono = medallas[i] if i < 3 else f"{i+1}."
        lineas.append(f"{icono} {dato['nombre']} — {dato['puntos']} punto{'s' if dato['puntos'] != 1 else ''}")
    await update.message.reply_text("\n".join(lineas))
