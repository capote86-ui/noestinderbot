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
MAX_RONDAS_VOTACION = 2

CARPETA_DATOS = "/data" if os.path.isdir("/data") else "."
ARCHIVO_RANKING = os.path.join(CARPETA_DATOS, "ranking_impostor.json")

impostores_activos: dict[int, dict[str, Any]] = {}


def nombre_usuario(user) -> str:
    if user.username:
        return f"@{user.username}"
    return user.first_name or "Alguien"


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )
    return re.sub(r"\s+", " ", texto).strip()


def contiene_palabra_prohibida(texto: str, palabra: str) -> bool:
    """
    Detecta la palabra exacta y también derivados evidentes.

    Ejemplos:
    - "café" detecta "café" y "cafetera".
    - "pizza" detecta "pizzería".
    """
    texto_normalizado = normalizar(texto)
    palabra_normalizada = normalizar(palabra)

    patron_exacto = (
        r"(?<!\w)"
        + re.escape(palabra_normalizada)
        + r"(?!\w)"
    )

    if re.search(patron_exacto, texto_normalizado):
        return True

    tokens = re.findall(r"\w+", texto_normalizado)

    # En palabras muy cortas, buscar derivados generaría demasiados falsos positivos.
    if len(palabra_normalizada) < 4:
        return False

    for token in tokens:
        if token.startswith(palabra_normalizada):
            return True

        # Permite detectar variantes muy cercanas, como pizza -> pizzeria.
        raiz = palabra_normalizada[:-1]
        if len(raiz) >= 4 and token.startswith(raiz):
            return True

    return False


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
            json.dump(
                ranking_impostor,
                archivo,
                ensure_ascii=False,
                indent=2,
            )

        os.replace(temporal, ARCHIVO_RANKING)

    except OSError as error:
        print(f"No se pudo guardar el ranking del Impostor: {error}")


def estadisticas_usuario(user_id: int, nombre: str) -> dict[str, Any]:
    datos = ranking_impostor.setdefault(
        str(user_id),
        {
            "nombre": nombre,
            "puntos": 0,
            "partidas": 0,
            "victorias": 0,
            "veces_impostor": 0,
            "impostores_descubiertos": 0,
            "palabras_acertadas": 0,
            "votos_correctos": 0,
        },
    )

    datos["nombre"] = nombre

    # Compatibilidad con rankings creados por versiones anteriores.
    valores_por_defecto = {
        "puntos": 0,
        "partidas": 0,
        "victorias": 0,
        "veces_impostor": 0,
        "impostores_descubiertos": 0,
        "palabras_acertadas": 0,
        "votos_correctos": 0,
    }

    for clave, valor in valores_por_defecto.items():
        datos.setdefault(clave, valor)

    return datos


def nombre_job(tipo: str, chat_id: int, ronda: int = 0) -> str:
    return f"impostor_{tipo}_{chat_id}_{ronda}"


def cancelar_jobs(context, chat_id: int) -> None:
    if not context.job_queue:
        return

    for tipo in ("pistas", "votacion", "adivinar"):
        for ronda in range(20):
            nombre = nombre_job(tipo, chat_id, ronda)

            for job in context.job_queue.get_jobs_by_name(nombre):
                job.schedule_removal()


def teclado_inscripcion(chat_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Participar",
                    callback_data=f"imp_join:{chat_id}",
                ),
                InlineKeyboardButton(
                    "🚪 Salir",
                    callback_data=f"imp_leave:{chat_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    "▶️ Empezar",
                    callback_data=f"imp_start:{chat_id}",
                )
            ],
        ]
    )


async def iniciar_impostor(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    admin_ids: list[int],
) -> None:
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "🎭 El juego debe iniciarse dentro del grupo."
        )
        return

    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden abrir una partida."
        )
        return

    if chat_id in impostores_activos:
        await update.message.reply_text(
            "🎭 Ya hay una partida de El Impostor abierta."
        )
        return

    mensaje = await update.message.reply_text(
        "🎭 EL IMPOSTOR — NO ES TINDER\n\n"
        "Todos recibirán una palabra por privado, menos una persona: "
        "el impostor.\n"
        "Después tendréis que dar una pista sin revelar la palabra "
        "y votar al sospechoso.\n\n"
        f"👥 Mínimo: {MINIMO_JUGADORES} jugadores.\n\n"
        "Participantes: nadie todavía.",
        reply_markup=teclado_inscripcion(chat_id),
    )

    impostores_activos[chat_id] = {
        "estado": "inscripcion",
        "jugadores": {},
        "mensaje_id": mensaje.message_id,
        "categoria": None,
        "palabra": None,
        "impostor_id": None,
        "pistas": {},
        "votos": {},
        "candidatos": [],
        "ronda_votacion": 0,
        "resolviendo": False,
    }


async def actualizar_inscripcion(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
) -> None:
    partida = impostores_activos.get(chat_id)

    if not partida or partida["estado"] != "inscripcion":
        return

    lista = (
        "\n".join(
            f"• {nombre}"
            for nombre in partida["jugadores"].values()
        )
        or "nadie todavía."
    )

    try:
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=partida["mensaje_id"],
            text=(
                "🎭 EL IMPOSTOR — NO ES TINDER\n\n"
                "Todos recibirán una palabra por privado, menos una "
                "persona: el impostor.\n"
                "Después tendréis que dar una pista sin revelar la "
                "palabra y votar al sospechoso.\n\n"
                f"👥 Mínimo: {MINIMO_JUGADORES} jugadores.\n\n"
                f"Participantes ({len(partida['jugadores'])}):\n"
                f"{lista}"
            ),
            reply_markup=teclado_inscripcion(chat_id),
        )

    except BadRequest as error:
        if "message is not modified" not in str(error).lower():
            print(f"No se pudo actualizar la inscripción: {error}")


def elegir_palabra() -> tuple[str, str]:
    categorias = [
        categoria
        for categoria, palabras in PALABRAS_IMPOSTOR.items()
        if palabras
    ]

    if not categorias:
        raise ValueError(
            "PALABRAS_IMPOSTOR no contiene categorías con palabras."
        )

    categoria = random.choice(categorias)
    palabra = random.choice(PALABRAS_IMPOSTOR[categoria])

    return categoria, palabra


async def depurar_jugadores_activos(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    partida: dict[str, Any],
) -> list[str]:
    """
    Elimina de la partida a usuarios que ya no pertenecen al grupo.
    Devuelve sus nombres.
    """
    eliminados: list[str] = []

    for user_id, nombre in list(partida["jugadores"].items()):
        try:
            miembro = await context.bot.get_chat_member(chat_id, user_id)

            if miembro.status in {"left", "kicked"}:
                partida["jugadores"].pop(user_id, None)
                partida["pistas"].pop(user_id, None)
                partida["votos"].pop(user_id, None)
                eliminados.append(nombre)

        except TelegramError:
            # Ante un error puntual de Telegram, no expulsamos al jugador.
            continue

    return eliminados


async def avisar_cancelacion_privada(
    context: ContextTypes.DEFAULT_TYPE,
    partida: dict[str, Any],
    texto: str,
) -> None:
    for user_id in partida["jugadores"]:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=texto,
            )
        except TelegramError:
            continue


async def cancelar_por_abandono(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    eliminados: list[str],
) -> None:
    partida = impostores_activos.get(chat_id)

    if not partida:
        return

    nombres = "\n".join(f"• {nombre}" for nombre in eliminados)

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "🛑 La partida ha sido cancelada porque uno o varios "
            "participantes ya no están en el grupo:\n\n"
            f"{nombres}\n\n"
            f"Se necesitan al menos {MINIMO_JUGADORES} jugadores activos."
        ),
    )

    await avisar_cancelacion_privada(
        context,
        partida,
        "🛑 La partida de El Impostor ha sido cancelada en el grupo.",
    )

    cancelar_jobs(context, chat_id)
    impostores_activos.pop(chat_id, None)


async def comenzar_partida(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
) -> None:
    partida = impostores_activos.get(chat_id)

    if not partida or partida.get("estado") != "inscripcion":
        return

    eliminados = await depurar_jugadores_activos(
        context,
        chat_id,
        partida,
    )

    if eliminados:
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "ℹ️ Se han eliminado de la inscripción usuarios que ya "
                "no están en el grupo:\n"
                + "\n".join(f"• {nombre}" for nombre in eliminados)
            ),
        )

    if len(partida["jugadores"]) < MINIMO_JUGADORES:
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"❌ Ya no hay suficientes jugadores. Hacen falta al "
                f"menos {MINIMO_JUGADORES}."
            ),
        )
        await actualizar_inscripcion(context, chat_id)
        return

    try:
        categoria, palabra = elegir_palabra()
    except ValueError as error:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"❌ No se pudo iniciar la partida: {error}",
        )
        return

    impostor_id = random.choice(
        list(partida["jugadores"].keys())
    )

    partida.update(
        {
            "estado": "enviando_roles",
            "categoria": categoria,
            "palabra": palabra,
            "impostor_id": impostor_id,
            "pistas": {},
            "votos": {},
            "candidatos": list(partida["jugadores"].keys()),
            "ronda_votacion": 0,
            "resolviendo": False,
        }
    )

    fallos: list[str] = []
    roles_enviados: list[int] = []

    for user_id, nombre in partida["jugadores"].items():
        if user_id == impostor_id:
            texto = (
                "🕵️ ERES EL IMPOSTOR\n\n"
                f"📚 Categoría: {categoria}\n\n"
                "No conoces la palabra. Lee las pistas, intenta pasar "
                "desapercibido y dedúcela."
            )
        else:
            texto = (
                "🎭 TU PALABRA ES:\n\n"
                f"🔐 {palabra.upper()}\n"
                f"📚 Categoría: {categoria}\n\n"
                "No la escribas. Cuando empiece la ronda, manda una "
                "sola pista al grupo."
            )

        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=texto,
            )
            roles_enviados.append(user_id)

        except (Forbidden, TelegramError):
            fallos.append(nombre)

    if fallos:
        for user_id in roles_enviados:
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=(
                        "⚠️ La partida no ha podido empezar porque el bot "
                        "no pudo enviar el rol a todos los participantes. "
                        "El rol recibido queda anulado."
                    ),
                )
            except TelegramError:
                continue

        partida.update(
            {
                "estado": "inscripcion",
                "categoria": None,
                "palabra": None,
                "impostor_id": None,
                "pistas": {},
                "votos": {},
                "candidatos": [],
                "ronda_votacion": 0,
                "resolviendo": False,
            }
        )

        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "❌ No puedo empezar porque no he podido enviar el rol "
                "por privado a:\n"
                + "\n".join(f"• {nombre}" for nombre in fallos)
                + "\n\nDeben abrir el chat privado del bot, pulsar "
                "START y volver a intentarlo."
            ),
        )

        await actualizar_inscripcion(context, chat_id)
        return

    partida["estado"] = "pistas"

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "🎭 ¡EMPIEZA LA RONDA!\n\n"
            "Cada participante debe escribir UNA sola pista en el grupo.\n"
            "❌ No podéis decir la palabra.\n"
            f"⏱️ Tenéis {TIEMPO_PISTAS} segundos.\n\n"
            "Que empiece la actuación."
        ),
    )

    if context.job_queue:
        context.job_queue.run_once(
            cerrar_pistas_por_tiempo,
            when=TIEMPO_PISTAS,
            data={"chat_id": chat_id},
            name=nombre_job("pistas", chat_id),
        )


async def procesar_mensaje_impostor(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> bool:
    if not update.message or not update.message.text:
        return False

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    texto = update.message.text.strip()

    # Los comandos deben continuar hacia responder() y no contar como pistas.
    if texto.startswith("/") or texto.startswith("!"):
        return False

    if update.effective_chat.type == "private":
        for grupo_id, partida in list(impostores_activos.items()):
            if (
                partida.get("estado") == "adivinar_palabra"
                and partida.get("impostor_id") == user_id
            ):
                await resolver_adivinanza(
                    context,
                    grupo_id,
                    texto,
                )
                return True

        return False

    partida = impostores_activos.get(chat_id)

    if (
        not partida
        or partida.get("estado") != "pistas"
        or user_id not in partida["jugadores"]
    ):
        return False

    if user_id in partida["pistas"]:
        await update.message.reply_text(
            f"{nombre_usuario(update.effective_user)}, "
            "ya has enviado tu pista."
        )
        return True

    if contiene_palabra_prohibida(
        texto,
        partida["palabra"],
    ):
        try:
            await update.message.delete()
        except TelegramError:
            pass

        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"🚫 {nombre_usuario(update.effective_user)}, "
                "no puedes decir la palabra ni un derivado evidente."
            ),
        )
        return True

    partida["pistas"][user_id] = texto

    faltan = (
        len(partida["jugadores"])
        - len(partida["pistas"])
    )

    await update.message.reply_text(
        f"✅ Pista registrada. Faltan {faltan} participante(s)."
    )

    if faltan == 0 and partida.get("estado") == "pistas":
        partida["estado"] = "preparando_votacion"

        if context.job_queue:
            for job in context.job_queue.get_jobs_by_name(
                nombre_job("pistas", chat_id)
            ):
                job.schedule_removal()

        await iniciar_votacion(context, chat_id)

    return True


async def cerrar_pistas_por_tiempo(
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    chat_id = int(context.job.data["chat_id"])
    partida = impostores_activos.get(chat_id)

    if not partida or partida.get("estado") != "pistas":
        return

    sin_pista = [
        nombre
        for user_id, nombre in partida["jugadores"].items()
        if user_id not in partida["pistas"]
    ]

    if sin_pista:
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "⏰ Tiempo terminado.\n\n"
                "No enviaron pista:\n"
                + "\n".join(
                    f"• {nombre}"
                    for nombre in sin_pista
                )
            ),
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="⏰ Tiempo terminado.",
        )

    partida["estado"] = "preparando_votacion"
    await iniciar_votacion(context, chat_id)


def teclado_votacion(
    partida: dict[str, Any],
    chat_id: int,
) -> InlineKeyboardMarkup:
    botones = []

    for user_id in partida["candidatos"]:
        nombre = partida["jugadores"].get(
            user_id,
            "Alguien",
        )[:40]

        botones.append(
            [
                InlineKeyboardButton(
                    nombre,
                    callback_data=(
                        f"imp_vote:{chat_id}:{user_id}:"
                        f"{partida['ronda_votacion']}"
                    ),
                )
            ]
        )

    return InlineKeyboardMarkup(botones)


async def iniciar_votacion(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    candidatos: Optional[list[int]] = None,
) -> None:
    partida = impostores_activos.get(chat_id)

    if not partida:
        return

    if partida.get("estado") not in {
        "pistas",
        "preparando_votacion",
        "votacion",
    }:
        return

    eliminados = await depurar_jugadores_activos(
        context,
        chat_id,
        partida,
    )

    if eliminados:
        if partida.get("impostor_id") not in partida["jugadores"]:
            await cancelar_por_abandono(
                context,
                chat_id,
                eliminados,
            )
            return

        if len(partida["jugadores"]) < MINIMO_JUGADORES:
            await cancelar_por_abandono(
                context,
                chat_id,
                eliminados,
            )
            return

        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "ℹ️ Se han retirado de la partida jugadores que ya no "
                "están en el grupo:\n"
                + "\n".join(
                    f"• {nombre}"
                    for nombre in eliminados
                )
            ),
        )

    candidatos_validos = (
        candidatos
        if candidatos is not None
        else list(partida["jugadores"].keys())
    )

    candidatos_validos = [
        user_id
        for user_id in candidatos_validos
        if user_id in partida["jugadores"]
    ]

    if not candidatos_validos:
        await context.bot.send_message(
            chat_id=chat_id,
            text="🛑 No quedan candidatos válidos. Partida cancelada.",
        )
        cancelar_jobs(context, chat_id)
        impostores_activos.pop(chat_id, None)
        return

    partida["estado"] = "votacion"
    partida["votos"] = {}
    partida["ronda_votacion"] += 1
    partida["candidatos"] = candidatos_validos
    partida["resolviendo"] = False

    pistas = (
        "\n".join(
            f"• {partida['jugadores'].get(user_id, 'Alguien')}: {pista}"
            for user_id, pista in partida["pistas"].items()
            if user_id in partida["jugadores"]
        )
        or "Nadie mandó ninguna pista."
    )

    texto_ronda = (
        "🗳️ HORA DE VOTAR"
        if partida["ronda_votacion"] == 1
        else "⚖️ DESEMPATE"
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            f"{texto_ronda}\n\n"
            f"Pistas:\n{pistas}\n\n"
            "¿Quién es el impostor?"
        ),
        reply_markup=teclado_votacion(
            partida,
            chat_id,
        ),
    )

    ronda = partida["ronda_votacion"]

    if context.job_queue:
        context.job_queue.run_once(
            cerrar_votacion_por_tiempo,
            when=TIEMPO_VOTACION,
            data={
                "chat_id": chat_id,
                "ronda": ronda,
            },
            name=nombre_job(
                "votacion",
                chat_id,
                ronda,
            ),
        )


async def cerrar_votacion_por_tiempo(
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    chat_id = int(context.job.data["chat_id"])
    ronda = int(context.job.data["ronda"])

    partida = impostores_activos.get(chat_id)

    if (
        partida
        and partida.get("estado") == "votacion"
        and partida.get("ronda_votacion") == ronda
    ):
        await resolver_votacion(
            context,
            chat_id,
        )


async def resolver_votacion(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
) -> None:
    partida = impostores_activos.get(chat_id)

    if (
        not partida
        or partida.get("estado") != "votacion"
        or partida.get("resolviendo")
    ):
        return

    partida["resolviendo"] = True

    conteo = {
        user_id: 0
        for user_id in partida["candidatos"]
    }

    for candidato in partida["votos"].values():
        if candidato in conteo:
            conteo[candidato] += 1

    if not partida["votos"]:
        await context.bot.send_message(
            chat_id=chat_id,
            text="💀 No votó nadie. El impostor gana.",
        )
        await finalizar_partida(
            context,
            chat_id,
            True,
            "sin_votos",
        )
        return

    max_votos = max(conteo.values())

    empatados = [
        user_id
        for user_id, total in conteo.items()
        if total == max_votos
    ]

    if len(empatados) > 1:
        if partida["ronda_votacion"] >= MAX_RONDAS_VOTACION:
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    "⚖️ El desempate ha vuelto a terminar en empate.\n\n"
                    "🕵️ El impostor sobrevive y gana la partida."
                ),
            )
            await finalizar_partida(
                context,
                chat_id,
                True,
                "empate_final",
            )
            return

        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "⚖️ Hay empate. Se repite la votación solo entre "
                "los empatados."
            ),
        )

        partida["resolviendo"] = False

        await iniciar_votacion(
            context,
            chat_id,
            empatados,
        )
        return

    acusado = empatados[0]

    if acusado != partida["impostor_id"]:
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"❌ {partida['jugadores'].get(acusado, 'Alguien')} "
                "no era.\n"
                f"🕵️ El impostor era "
                f"{partida['jugadores'].get(partida['impostor_id'], 'Alguien')}.\n"
                f"🔐 La palabra era {partida['palabra'].upper()}."
            ),
        )

        await finalizar_partida(
            context,
            chat_id,
            True,
            "no_descubierto",
        )
        return

    partida["estado"] = "adivinar_palabra"
    partida["resolviendo"] = False

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            f"🎯 Habéis descubierto a "
            f"{partida['jugadores'].get(acusado, 'Alguien')}.\n\n"
            "Tiene una última oportunidad para adivinar la palabra "
            "por privado."
        ),
    )

    try:
        await context.bot.send_message(
            chat_id=partida["impostor_id"],
            text=(
                "🕵️ Te han descubierto.\n\n"
                "Escribe únicamente la palabra que crees que tenían "
                f"los demás. Tienes {TIEMPO_ADIVINAR} segundos."
            ),
        )

    except TelegramError:
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "❌ No he podido contactar con el impostor por privado. "
                "Ganan los civiles."
            ),
        )
        await finalizar_partida(
            context,
            chat_id,
            False,
            "sin_respuesta",
        )
        return

    if context.job_queue:
        context.job_queue.run_once(
            cerrar_adivinanza_por_tiempo,
            when=TIEMPO_ADIVINAR,
            data={"chat_id": chat_id},
            name=nombre_job(
                "adivinar",
                chat_id,
            ),
        )


async def resolver_adivinanza(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    respuesta: str,
) -> None:
    partida = impostores_activos.get(chat_id)

    if (
        not partida
        or partida.get("estado") != "adivinar_palabra"
        or partida.get("resolviendo")
    ):
        return

    partida["resolviendo"] = True

    acierta = (
        normalizar(respuesta)
        == normalizar(partida["palabra"])
    )

    if context.job_queue:
        for job in context.job_queue.get_jobs_by_name(
            nombre_job("adivinar", chat_id)
        ):
            job.schedule_removal()

    if acierta:
        texto = (
            f"😈 Ha acertado: {partida['palabra'].upper()}.\n\n"
            "Gana el impostor."
        )
        motivo = "palabra_acertada"
    else:
        texto = (
            f"❌ Respondió «{respuesta}».\n"
            f"La palabra era {partida['palabra'].upper()}.\n\n"
            "Ganan los civiles."
        )
        motivo = "palabra_fallada"

    await context.bot.send_message(
        chat_id=chat_id,
        text=texto,
    )

    await finalizar_partida(
        context,
        chat_id,
        acierta,
        motivo,
    )


async def cerrar_adivinanza_por_tiempo(
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    chat_id = int(context.job.data["chat_id"])
    partida = impostores_activos.get(chat_id)

    if (
        not partida
        or partida.get("estado") != "adivinar_palabra"
        or partida.get("resolviendo")
    ):
        return

    partida["resolviendo"] = True

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "⏰ No respondió a tiempo.\n"
            f"La palabra era {partida['palabra'].upper()}.\n\n"
            "Ganan los civiles."
        ),
    )

    await finalizar_partida(
        context,
        chat_id,
        False,
        "tiempo_agotado",
    )


async def finalizar_partida(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    gana_impostor: bool,
    motivo: str,
) -> None:
    partida = impostores_activos.get(chat_id)

    if not partida:
        return

    # Evita dobles cierres y dobles puntuaciones.
    if partida.get("estado") == "finalizado":
        return

    partida["estado"] = "finalizado"

    impostor_id = partida["impostor_id"]

    for user_id, nombre in partida["jugadores"].items():
        datos = estadisticas_usuario(
            user_id,
            nombre,
        )
        datos["partidas"] += 1

        if user_id == impostor_id:
            datos["veces_impostor"] += 1

    # Estadísticas de votos.
    for votante_id, candidato_id in partida["votos"].items():
        if candidato_id == impostor_id:
            datos_votante = estadisticas_usuario(
                votante_id,
                partida["jugadores"].get(
                    votante_id,
                    "Alguien",
                ),
            )
            datos_votante["votos_correctos"] += 1

    if gana_impostor:
        datos_impostor = estadisticas_usuario(
            impostor_id,
            partida["jugadores"].get(
                impostor_id,
                "Alguien",
            ),
        )

        datos_impostor["victorias"] += 1
        datos_impostor["puntos"] += 15

        if motivo == "palabra_acertada":
            datos_impostor["palabras_acertadas"] += 1
            datos_impostor["puntos"] += 5

    else:
        for user_id, nombre in partida["jugadores"].items():
            if user_id == impostor_id:
                continue

            datos = estadisticas_usuario(
                user_id,
                nombre,
            )
            datos["victorias"] += 1
            datos["puntos"] += 10
            datos["impostores_descubiertos"] += 1

        # Los civiles que votaron correctamente reciben 5 puntos extra.
        for votante_id, candidato_id in partida["votos"].items():
            if (
                candidato_id == impostor_id
                and votante_id != impostor_id
            ):
                datos_votante = estadisticas_usuario(
                    votante_id,
                    partida["jugadores"].get(
                        votante_id,
                        "Alguien",
                    ),
                )
                datos_votante["puntos"] += 5

    guardar_ranking()
    cancelar_jobs(context, chat_id)
    impostores_activos.pop(chat_id, None)


async def cancelar_impostor(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    admin_ids: list[int],
) -> None:
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden cancelar la partida."
        )
        return

    partida = impostores_activos.get(chat_id)

    if not partida:
        await update.message.reply_text(
            "No hay ninguna partida activa."
        )
        return

    await avisar_cancelacion_privada(
        context,
        partida,
        "🛑 La partida de El Impostor ha sido cancelada por un administrador.",
    )

    cancelar_jobs(context, chat_id)
    impostores_activos.pop(chat_id, None)

    await update.message.reply_text(
        "🛑 Partida de El Impostor cancelada. "
        "Los participantes también han sido avisados por privado."
    )


async def mostrar_ranking_impostor(
    update: Update,
) -> None:
    if not ranking_impostor:
        await update.message.reply_text(
            "Todavía no hay ranking de El Impostor."
        )
        return

    ordenado = sorted(
        ranking_impostor.values(),
        key=lambda datos: (
            datos.get("puntos", 0),
            datos.get("victorias", 0),
        ),
        reverse=True,
    )[:10]

    lineas = []

    for posicion, datos in enumerate(ordenado, 1):
        lineas.append(
            f"{posicion}. {datos.get('nombre', 'Alguien')} — "
            f"{datos.get('puntos', 0)} puntos · "
            f"{datos.get('victorias', 0)} victoria(s)"
        )

    texto = (
        "🎭 RANKING DE EL IMPOSTOR\n\n"
        + "\n".join(lineas)
    )

    await update.message.reply_text(texto)


async def botones_impostor(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query or not query.data:
        return

    partes = query.data.split(":")
    accion = partes[0]

    if accion in {
        "imp_join",
        "imp_leave",
        "imp_start",
    }:
        if len(partes) != 2:
            await query.answer(
                "Botón no válido.",
                show_alert=True,
            )
            return

        try:
            chat_id = int(partes[1])
        except ValueError:
            await query.answer(
                "Botón no válido.",
                show_alert=True,
            )
            return

        partida = impostores_activos.get(chat_id)

        if not partida:
            await query.answer(
                "Esta partida ya no existe.",
                show_alert=True,
            )
            return

        if partida["estado"] != "inscripcion":
            await query.answer(
                "La partida ya ha empezado.",
                show_alert=True,
            )
            return

        user_id = query.from_user.id

        if accion == "imp_join":
            partida["jugadores"][user_id] = nombre_usuario(
                query.from_user
            )

            await query.answer(
                "Te has apuntado 🎭",
                show_alert=True,
            )
            await actualizar_inscripcion(
                context,
                chat_id,
            )
            return

        if accion == "imp_leave":
            partida["jugadores"].pop(
                user_id,
                None,
            )

            await query.answer(
                "Has salido.",
                show_alert=True,
            )
            await actualizar_inscripcion(
                context,
                chat_id,
            )
            return

        try:
            admins = await context.bot.get_chat_administrators(
                chat_id
            )
        except TelegramError:
            await query.answer(
                "No he podido comprobar los administradores.",
                show_alert=True,
            )
            return

        admin_ids = [
            admin.user.id
            for admin in admins
        ]

        if user_id not in admin_ids:
            await query.answer(
                "Solo un administrador puede empezar.",
                show_alert=True,
            )
            return

        if len(partida["jugadores"]) < MINIMO_JUGADORES:
            await query.answer(
                f"Hacen falta al menos {MINIMO_JUGADORES} jugadores.",
                show_alert=True,
            )
            return

        await query.answer(
            "Repartiendo roles…",
            show_alert=True,
        )

        try:
            await query.message.edit_reply_markup(
                reply_markup=None
            )
        except BadRequest:
            pass

        await comenzar_partida(
            context,
            chat_id,
        )
        return

    if accion == "imp_vote":
        if len(partes) != 4:
            await query.answer(
                "Voto no válido.",
                show_alert=True,
            )
            return

        try:
            chat_id = int(partes[1])
            candidato_id = int(partes[2])
            ronda = int(partes[3])
        except ValueError:
            await query.answer(
                "Voto no válido.",
                show_alert=True,
            )
            return

        partida = impostores_activos.get(chat_id)

        if (
            not partida
            or partida.get("estado") != "votacion"
            or partida.get("ronda_votacion") != ronda
            or partida.get("resolviendo")
        ):
            await query.answer(
                "La votación ya terminó.",
                show_alert=True,
            )
            return

        user_id = query.from_user.id

        if user_id not in partida["jugadores"]:
            await query.answer(
                "Solo votan los participantes.",
                show_alert=True,
            )
            return

        if candidato_id not in partida["candidatos"]:
            await query.answer(
                "Ese candidato ya no está disponible.",
                show_alert=True,
            )
            return

        if user_id == candidato_id:
            await query.answer(
                "No puedes votarte a ti mismo.",
                show_alert=True,
            )
            return

        if user_id in partida["votos"]:
            await query.answer(
                "Ya has votado.",
                show_alert=True,
            )
            return

        partida["votos"][user_id] = candidato_id

        await query.answer(
            "Has votado a "
            f"{partida['jugadores'].get(candidato_id, 'Alguien')}.",
            show_alert=True,
        )

        if len(partida["votos"]) >= len(partida["jugadores"]):
            await resolver_votacion(
                context,
                chat_id,
            )

        return

    await query.answer(
        "Botón no reconocido.",
        show_alert=True,
    )
