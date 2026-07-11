import json
import os
from datetime import datetime
from telegram import Update


CARPETA_DATOS = "/data" if os.path.isdir("/data") else "."
ARCHIVO_FICHAS = os.path.join(CARPETA_DATOS, "fichas.json")


def cargar_fichas():
    if not os.path.exists(ARCHIVO_FICHAS):
        return {}

    try:
        with open(ARCHIVO_FICHAS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return {}


def guardar_fichas():
    with open(ARCHIVO_FICHAS, "w", encoding="utf-8") as archivo:
        json.dump(
            fichas_usuarios,
            archivo,
            ensure_ascii=False,
            indent=2
        )


fichas_usuarios = cargar_fichas()


def nivel_participacion(total):
    if total >= 500:
        return "🔥 Leyenda del grupo"
    if total >= 250:
        return "🗣️ Muy activo/a"
    if total >= 100:
        return "💬 Activo/a"
    if total >= 30:
        return "🙂 Participación habitual"
    if total >= 10:
        return "👀 Participación ocasional"
    return "🫥 Modo observador"


def formatear_ultima_actividad(fecha):
    if not fecha:
        return "Sin actividad registrada"

    diferencia = datetime.now() - fecha
    minutos = int(diferencia.total_seconds() // 60)

    if minutos < 1:
        return "Hace unos segundos"
    if minutos < 60:
        return f"Hace {minutos} minuto(s)"

    horas = minutos // 60

    if horas < 24:
        return f"Hace {horas} hora(s)"

    dias = horas // 24
    return f"Hace {dias} día(s)"


def construir_ficha(
    user_id,
    contador_mensajes,
    ultimo_mensaje_usuario
):
    ficha = fichas_usuarios.get(str(user_id))

    if not ficha:
        return None

    total_mensajes = contador_mensajes.get(user_id, 0)
    ultima_actividad = ultimo_mensaje_usuario.get(user_id)

    usuario = ficha.get("usuario")
    usuario_texto = f"@{usuario}" if usuario else "Sin usuario público"

    edad = ficha.get("edad") or "No indicada"
    ciudad = ficha.get("ciudad") or "No indicada"
    pais = ficha.get("pais") or "No indicado"
    cumpleanos = ficha.get("cumpleanos") or "No indicado"

    if edad != "No indicada":
        edad = f"{edad} años"

    return (
        f"📋 FICHA DE {ficha['nombre'].upper()}\n\n"
        f"👤 Usuario: {usuario_texto}\n"
        f"🎂 Edad: {edad}\n"
        f"📍 Ciudad: {ciudad}\n"
        f"🌍 País: {pais}\n"
        f"🎉 Cumpleaños: {cumpleanos}\n\n"
        f"📊 Participación: {nivel_participacion(total_mensajes)}\n"
        f"💬 Mensajes registrados: {total_mensajes}\n"
        f"🕒 Última actividad: "
        f"{formatear_ultima_actividad(ultima_actividad)}"
    )


async def guardar_ficha_admin(
    update: Update,
    admin_ids
):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden crear o editar fichas."
        )
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "📋 Para crear una ficha, responde a un mensaje de esa persona "
            "con:\n\n"
            "/guardarficha Nombre | Edad | Ciudad | País | DD/MM\n\n"
            "Ejemplo:\n"
            "/guardarficha Raquel | 39 | Santa Cruz de Tenerife | "
            "España | 21/11\n\n"
            "Si no conoces un dato, escribe un guion: -"
        )
        return

    texto_original = update.message.text.strip()
    partes_comando = texto_original.split(maxsplit=1)

    if len(partes_comando) < 2:
        await update.message.reply_text(
            "❌ Faltan los datos.\n\n"
            "Formato:\n"
            "/guardarficha Nombre | Edad | Ciudad | País | DD/MM"
        )
        return

    datos = [dato.strip() for dato in partes_comando[1].split("|")]

    if len(datos) != 5:
        await update.message.reply_text(
            "❌ Debes separar exactamente cinco datos con barras verticales:\n\n"
            "Nombre | Edad | Ciudad | País | DD/MM"
        )
        return

    nombre, edad_texto, ciudad, pais, cumpleanos = datos

    if not nombre or nombre == "-":
        await update.message.reply_text(
            "❌ El nombre es obligatorio."
        )
        return

    if edad_texto == "-":
        edad = None
    else:
        try:
            edad = int(edad_texto)
        except ValueError:
            await update.message.reply_text(
                "❌ La edad debe ser un número o un guion."
            )
            return

        if edad < 18 or edad > 99:
            await update.message.reply_text(
                "❌ La edad debe estar entre 18 y 99 años."
            )
            return

    if cumpleanos == "-":
        cumpleanos = None
    else:
        try:
            datetime.strptime(cumpleanos, "%d/%m")
        except ValueError:
            await update.message.reply_text(
                "❌ El cumpleaños debe escribirse como DD/MM o con un guion."
            )
            return

    usuario_objetivo = update.message.reply_to_message.from_user
    user_id = usuario_objetivo.id

    fichas_usuarios[str(user_id)] = {
        "nombre": nombre,
        "edad": edad,
        "ciudad": None if ciudad == "-" else ciudad,
        "pais": None if pais == "-" else pais,
        "cumpleanos": cumpleanos,
        "usuario": usuario_objetivo.username,
        "telegram_nombre": usuario_objetivo.first_name,
        "actualizada_por": update.effective_user.id,
        "fecha_actualizacion": datetime.now().isoformat()
    }

    guardar_fichas()

    await update.message.reply_text(
        f"✅ Ficha de {nombre} guardada correctamente."
    )


async def mostrar_ficha(
    update: Update,
    contador_mensajes,
    ultimo_mensaje_usuario
):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id

    else:
        texto_original = update.message.text.strip()
        partes = texto_original.split(maxsplit=1)

        if len(partes) == 1:
            user_id = update.effective_user.id

        else:
            busqueda = partes[1].strip().lower().lstrip("@")
            user_id = None

            for ficha_id, ficha in fichas_usuarios.items():
                usuario = (ficha.get("usuario") or "").lower()
                nombre = (ficha.get("nombre") or "").lower()

                if busqueda == usuario or busqueda == nombre:
                    user_id = int(ficha_id)
                    break

            if user_id is None:
                await update.message.reply_text(
                    "No encuentro esa ficha.\n\n"
                    "También puedes responder al mensaje de la persona con /ficha."
                )
                return

    texto = construir_ficha(
        user_id,
        contador_mensajes,
        ultimo_mensaje_usuario
    )

    if not texto:
        await update.message.reply_text(
            "Esa persona todavía no tiene una ficha registrada."
        )
        return

    await update.message.reply_text(texto)


async def borrar_ficha_admin(
    update: Update,
    admin_ids
):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden borrar fichas."
        )
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Responde al mensaje de la persona con /borrarficha."
        )
        return

    user_id = update.message.reply_to_message.from_user.id

    if str(user_id) not in fichas_usuarios:
        await update.message.reply_text(
            "Esa persona no tiene una ficha guardada."
        )
        return

    nombre = fichas_usuarios[str(user_id)].get("nombre", "esa persona")

    fichas_usuarios.pop(str(user_id))
    guardar_fichas()

    await update.message.reply_text(
        f"🗑️ Ficha de {nombre} eliminada."
    )
