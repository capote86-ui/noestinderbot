import json
import os
import random
import secrets
from collections import Counter
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from tests_base import TESTS, obtener_test_por_id


CARPETA_DATOS = "/data" if os.path.isdir("/data") else "."
ARCHIVO_CONFIGURACION = os.path.join(CARPETA_DATOS, "tests_config.json")

# Número de tests recientes que el bot evita repetir.
VENTANA_ANTIRREPETICION = 8

# Sesiones activas. Cada usuario tiene su propio mensaje de preguntas.
sesiones_tests = {}


def cargar_configuracion():
    configuracion = {
        "chat_ids": [],
        "historial": {}
    }

    if not os.path.exists(ARCHIVO_CONFIGURACION):
        return configuracion

    try:
        with open(ARCHIVO_CONFIGURACION, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, dict):
            return configuracion

        datos.setdefault("chat_ids", [])
        datos.setdefault("historial", {})
        return datos

    except (json.JSONDecodeError, OSError, TypeError):
        return configuracion


configuracion_tests = cargar_configuracion()


def guardar_configuracion():
    os.makedirs(CARPETA_DATOS, exist_ok=True)

    with open(ARCHIVO_CONFIGURACION, "w", encoding="utf-8") as archivo:
        json.dump(
            configuracion_tests,
            archivo,
            ensure_ascii=False,
            indent=2
        )


def nombre_usuario(user):
    if user.username:
        return f"@{user.username}"

    return user.full_name or "Participante"


def elegir_test(chat_id):
    historial_chat = configuracion_tests.setdefault(
        "historial",
        {}
    ).setdefault(str(chat_id), [])

    ids_recientes = set(historial_chat[-VENTANA_ANTIRREPETICION:])
    disponibles = [
        test for test in TESTS
        if test["id"] not in ids_recientes
    ]

    if not disponibles:
        disponibles = TESTS[:]

    elegido = random.choice(disponibles)

    historial_chat.append(elegido["id"])
    configuracion_tests["historial"][str(chat_id)] = historial_chat[-50:]
    guardar_configuracion()

    return elegido


def teclado_publicacion(test_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "▶️ Hacer el test",
                callback_data=f"test_start:{test_id}"
            )
        ]
    ])


def texto_publicacion(test):
    return (
        "📝 TEST DE NO ES TINDER\n\n"
        f"{test['categoria']}\n"
        f"🎯 {test['titulo']}\n\n"
        f"{test['descripcion']}\n\n"
        f"Consta de {len(test['preguntas'])} preguntas.\n"
        "Pulsa el botón para descubrir tu resultado."
    )


async def activar_tests(update: Update, admin_ids):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden activar los tests."
        )
        return

    chat_id = update.effective_chat.id
    chat_ids = configuracion_tests.setdefault("chat_ids", [])

    if chat_id in chat_ids:
        await update.message.reply_text(
            "📝 Los tests semanales ya estaban activados."
        )
        return

    chat_ids.append(chat_id)
    guardar_configuracion()

    await update.message.reply_text(
        "✅ Tests semanales activados.\n\n"
        "El bot publicará un test automáticamente cada semana."
    )


async def desactivar_tests(update: Update, admin_ids):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden desactivar los tests."
        )
        return

    chat_id = update.effective_chat.id
    chat_ids = configuracion_tests.setdefault("chat_ids", [])

    if chat_id not in chat_ids:
        await update.message.reply_text(
            "Los tests semanales no estaban activados."
        )
        return

    chat_ids.remove(chat_id)
    guardar_configuracion()

    await update.message.reply_text(
        "🛑 Tests semanales desactivados."
    )


async def publicar_test_en_chat(context, chat_id, test=None):
    if test is None:
        test = elegir_test(chat_id)

    await context.bot.send_message(
        chat_id=chat_id,
        text=texto_publicacion(test),
        reply_markup=teclado_publicacion(test["id"])
    )


async def publicar_test_automatico(
    context: ContextTypes.DEFAULT_TYPE
):
    for chat_id in configuracion_tests.get("chat_ids", []):
        try:
            await publicar_test_en_chat(context, chat_id)
        except Exception as error:
            print(
                f"No se pudo publicar un test automático "
                f"en {chat_id}: {error}"
            )


async def lanzar_test_manual(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    admin_ids
):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden lanzar un test."
        )
        return

    test = elegir_test(update.effective_chat.id)

    await publicar_test_en_chat(
        context,
        update.effective_chat.id,
        test
    )


def crear_teclado_pregunta(session_id, pregunta):
    filas = []

    for indice, opcion in enumerate(pregunta["opciones"]):
        filas.append([
            InlineKeyboardButton(
                opcion["texto"],
                callback_data=f"test_ans:{session_id}:{indice}"
            )
        ])

    filas.append([
        InlineKeyboardButton(
            "❌ Abandonar",
            callback_data=f"test_cancel:{session_id}"
        )
    ])

    return InlineKeyboardMarkup(filas)


def texto_pregunta(test, indice_pregunta, usuario):
    pregunta = test["preguntas"][indice_pregunta]

    return (
        f"📝 Test de {usuario}\n\n"
        f"{test['categoria']} {test['titulo']}\n\n"
        f"Pregunta {indice_pregunta + 1}/"
        f"{len(test['preguntas'])}\n\n"
        f"❓ {pregunta['texto']}"
    )


def obtener_clave_ganadora(puntuaciones, test, session_id):
    maximo = max(puntuaciones.values())
    empatados = [
        perfil
        for perfil, puntos in puntuaciones.items()
        if puntos == maximo
    ]

    if len(empatados) == 1:
        return empatados[0]

    # Desempate estable para que no cambie si Telegram repite el callback.
    rng = random.Random(session_id)
    return rng.choice(empatados)


async def iniciar_test_desde_boton(
    query,
    context,
    test_id
):
    test = obtener_test_por_id(test_id)

    if not test:
        await query.answer(
            "Ese test ya no está disponible.",
            show_alert=True
        )
        return

    user_id = query.from_user.id
    chat_id = query.message.chat.id

    # Cancela silenciosamente la sesión anterior del mismo usuario en el chat.
    clave_usuario = (chat_id, user_id)
    sesion_anterior = sesiones_tests.get(clave_usuario)

    if sesion_anterior:
        sesiones_tests.pop(clave_usuario, None)

    session_id = secrets.token_hex(4)

    sesion = {
        "session_id": session_id,
        "chat_id": chat_id,
        "user_id": user_id,
        "test_id": test_id,
        "pregunta": 0,
        "puntuaciones": Counter(
            {perfil: 0 for perfil in test["perfiles"]}
        ),
        "message_id": None
    }

    sesiones_tests[clave_usuario] = sesion

    mensaje = await context.bot.send_message(
        chat_id=chat_id,
        reply_to_message_id=query.message.message_id,
        text=texto_pregunta(
            test,
            0,
            nombre_usuario(query.from_user)
        ),
        reply_markup=crear_teclado_pregunta(
            session_id,
            test["preguntas"][0]
        )
    )

    sesion["message_id"] = mensaje.message_id

    await query.answer("Tu test ha comenzado.")


async def procesar_respuesta(
    query,
    context,
    session_id,
    indice_opcion
):
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    clave_usuario = (chat_id, user_id)
    sesion = sesiones_tests.get(clave_usuario)

    if not sesion or sesion["session_id"] != session_id:
        await query.answer(
            "Esta sesión ya terminó o no te pertenece.",
            show_alert=True
        )
        return

    test = obtener_test_por_id(sesion["test_id"])

    if not test:
        sesiones_tests.pop(clave_usuario, None)
        await query.answer(
            "No se pudo recuperar el test.",
            show_alert=True
        )
        return

    indice_pregunta = sesion["pregunta"]
    pregunta = test["preguntas"][indice_pregunta]

    if indice_opcion < 0 or indice_opcion >= len(pregunta["opciones"]):
        await query.answer("Respuesta no válida.", show_alert=True)
        return

    opcion = pregunta["opciones"][indice_opcion]
    sesion["puntuaciones"][opcion["perfil"]] += 1
    sesion["pregunta"] += 1

    if sesion["pregunta"] < len(test["preguntas"]):
        siguiente = test["preguntas"][sesion["pregunta"]]

        try:
            await query.edit_message_text(
                text=texto_pregunta(
                    test,
                    sesion["pregunta"],
                    nombre_usuario(query.from_user)
                ),
                reply_markup=crear_teclado_pregunta(
                    session_id,
                    siguiente
                )
            )
        except BadRequest as error:
            if "Message is not modified" not in str(error):
                raise

        await query.answer()
        return

    clave_ganadora = obtener_clave_ganadora(
        sesion["puntuaciones"],
        test,
        session_id
    )
    resultado = test["perfiles"][clave_ganadora]

    puntuacion_ordenada = sorted(
        sesion["puntuaciones"].items(),
        key=lambda elemento: elemento[1],
        reverse=True
    )

    resumen_puntos = " · ".join(
        f"{test['perfiles'][clave]['nombre']} {puntos}"
        for clave, puntos in puntuacion_ordenada
    )

    texto_resultado = (
        f"📝 RESULTADO DE {nombre_usuario(query.from_user)}\n\n"
        f"{test['categoria']} {test['titulo']}\n\n"
        f"{resultado['nombre']}\n\n"
        f"{resultado['texto']}\n\n"
        f"📊 Puntuación: {resumen_puntos}"
    )

    sesiones_tests.pop(clave_usuario, None)

    try:
        await query.edit_message_text(text=texto_resultado)
    except BadRequest as error:
        if "Message is not modified" not in str(error):
            raise

    await query.answer("Test terminado.")


async def cancelar_test_desde_boton(
    query,
    session_id
):
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    clave_usuario = (chat_id, user_id)
    sesion = sesiones_tests.get(clave_usuario)

    if not sesion or sesion["session_id"] != session_id:
        await query.answer(
            "Esta sesión no te pertenece o ya terminó.",
            show_alert=True
        )
        return

    sesiones_tests.pop(clave_usuario, None)

    await query.edit_message_text(
        "❌ Test abandonado.\n\n"
        "Puedes volver a empezar desde la publicación del test."
    )
    await query.answer()


async def botones_tests(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    if not query or not query.data:
        return

    partes = query.data.split(":")
    accion = partes[0]

    if accion == "test_start" and len(partes) == 2:
        await iniciar_test_desde_boton(
            query,
            context,
            partes[1]
        )
        return

    if accion == "test_ans" and len(partes) == 3:
        try:
            indice = int(partes[2])
        except ValueError:
            await query.answer("Respuesta no válida.", show_alert=True)
            return

        await procesar_respuesta(
            query,
            context,
            partes[1],
            indice
        )
        return

    if accion == "test_cancel" and len(partes) == 2:
        await cancelar_test_desde_boton(
            query,
            partes[1]
        )
        return

    await query.answer("Acción no reconocida.", show_alert=True)


async def cancelar_test_admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    admin_ids
):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden cancelar tests."
        )
        return

    chat_id = update.effective_chat.id
    eliminadas = [
        clave for clave in sesiones_tests
        if clave[0] == chat_id
    ]

    for clave in eliminadas:
        sesiones_tests.pop(clave, None)

    await update.message.reply_text(
        f"🛑 Se han cancelado {len(eliminadas)} "
        "sesiones de test activas en este grupo."
    )
