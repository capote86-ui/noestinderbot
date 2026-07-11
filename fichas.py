import json
import os
from datetime import datetime
from telegram import Update


ARCHIVO_FICHAS = "fichas.json"


def cargar_fichas():
    if not os.path.exists(ARCHIVO_FICHAS):
        return {}

    try:
        with open(ARCHIVO_FICHAS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return {}


def guardar_fichas(fichas):
    archivo_temporal = f"{ARCHIVO_FICHAS}.tmp"

    with open(archivo_temporal, "w", encoding="utf-8") as archivo:
        json.dump(fichas, archivo, ensure_ascii=False, indent=2)

    os.replace(archivo_temporal, ARCHIVO_FICHAS)


fichas_usuarios = cargar_fichas()


def nivel_participacion(total_mensajes):
    if total_mensajes >= 500:
        return "🔥 Leyenda del grupo"
    if total_mensajes >= 250:
        return "🗣️ Muy activo/a"
    if total_mensajes >= 100:
        return "💬 Activo/a"
    if total_mensajes >= 30:
        return "🙂 Participación habitual"
    if total_mensajes >= 10:
        return "👀 Participación ocasional"
    return "🫥 Modo observador"


def tiempo_desde(fecha):
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


def construir_ficha(user_id, contador_mensajes, ultimo_mensaje_usuario):
    ficha = fichas_usuarios.get(str(user_id))

    if not ficha:
        return None

    total = contador_mensajes.get(user_id, 0)
    ultima_actividad = ultimo_mensaje_usuario.get(user_id)

    usuario = ficha.get("usuario")
    texto_usuario = f"@{usuario}" if usuario else "Sin nombre de usuario"

    return (
        f"📋 FICHA DE {ficha['nombre'].upper()}\n\n"
        f"👤 Usuario: {texto_usuario}\n"
        f"🎂 Edad: {ficha['edad']} años\n"
        f"📍 Ciudad: {ficha['ciudad']}\n"
        f"🌍 País: {ficha['pais']}\n"
        f"🎉 Cumpleaños: {ficha['cumpleanos']}\n\n"
        f"📊 Participación: {nivel_participacion(total)}\n"
        f"💬 Mensajes registrados: {total}\n"
        f"🕒 Última actividad: {tiempo_desde(ultima_actividad)}"
    )


async def registrar_ficha(update: Update):
    texto_original = update.message.text.strip()
    partes_comando = texto_original.split(maxsplit=1)

    if len(partes_comando) < 2:
        await update.message.reply_text(
            "📋 Para crear o actualizar tu ficha escribe:\n\n"
            "/ficharme Nombre | Edad | Ciudad | País | DD/MM\n\n"
            "Ejemplo:\n"
            "/ficharme Raquel | 39 | Santa Cruz de Tenerife | España | 21/11"
        )
        return

    datos = [dato.strip() for dato in partes_comando[1].split("|")]

    if len(datos) != 5:
        await update.message.reply_text(
            "❌ El formato no es correcto.\n\n"
            "Utiliza exactamente:\n"
            "/ficharme Nombre | Edad | Ciudad | País | DD/MM"
        )
        return

    nombre, edad_texto, ciudad, pais, cumpleanos = datos

    if not nombre or not ciudad or not pais:
        await update.message.reply_text(
            "❌ Nombre, ciudad y país no pueden estar vacíos."
        )
        return

    try:
        edad = int(edad_texto)
    except ValueError:
        await update.message.reply_text(
            "❌ La edad debe escribirse con números."
        )
        return

    if edad < 18 or edad > 99:
        await update.message.reply_text(
            "❌ La edad debe estar entre 18 y 99 años."
        )
        return

    try:
        datetime.strptime(cumpleanos, "%d/%m")
    except ValueError:
        await update.message.reply_text(
            "❌ El cumpleaños debe tener formato DD/MM.\n"
            "Ejemplo: 21/11"
        )
        return

    usuario = update.effective_user.username

    fichas_usuarios[str(update.effective_user.id)] = {
        "nombre": nombre,
        "edad": edad,
        "ciudad": ciudad,
        "pais": pais,
        "cumpleanos": cumpleanos,
        "usuario": usuario,
        "fecha_registro": datetime.now().isoformat()
    }

    guardar_fichas(fichas_usuarios)

    await update.message.reply_text(
        f"✅ Ficha guardada correctamente, {nombre}.\n\n"
        "Ya pueden consultarla con /ficha."
    )


async def mostrar_mi_ficha(
    update: Update,
    contador_mensajes,
    ultimo_mensaje_usuario
):
    texto = construir_ficha(
        update.effective_user.id,
        contador_mensajes,
        ultimo_mensaje_usuario
    )

    if not texto:
        await update.message.reply_text(
            "Todavía no tienes ficha.\n\n"
            "Créala con:\n"
            "/ficharme Nombre | Edad | Ciudad | País | DD/MM"
        )
        return

    await update.message.reply_text(texto)


async def mostrar_ficha(
    update: Update,
    contador_mensajes,
    ultimo_mensaje_usuario
):
    texto_original = update.message.text.strip()
    partes = texto_original.split(maxsplit=1)

    user_id_buscado = None

    if update.message.reply_to_message:
        user_id_buscado = update.message.reply_to_message.from_user.id

    elif len(partes) >= 2:
        busqueda = partes[1].strip().lower().lstrip("@")

        for user_id, ficha in fichas_usuarios.items():
            usuario = (ficha.get("usuario") or "").lower()
            nombre = ficha.get("nombre", "").lower()

            if busqueda == usuario or busqueda == nombre:
                user_id_buscado = int(user_id)
                break

    else:
        user_id_buscado = update.effective_user.id

    if not user_id_buscado:
        await update.message.reply_text(
            "No encuentro esa ficha.\n\n"
            "Puedes escribir:\n"
            "/ficha @usuario\n\n"
            "O responder a un mensaje con /ficha."
        )
        return

    texto = construir_ficha(
        user_id_buscado,
        contador_mensajes,
        ultimo_mensaje_usuario
    )

    if not texto:
        await update.message.reply_text(
            "Esa persona todavía no ha creado su ficha."
        )
        return

    await update.message.reply_text(texto)


async def borrar_mi_ficha(update: Update):
    user_id = str(update.effective_user.id)

    if user_id not in fichas_usuarios:
        await update.message.reply_text(
            "No tienes ninguna ficha guardada."
        )
        return

    fichas_usuarios.pop(user_id)
    guardar_fichas(fichas_usuarios)

    await update.message.reply_text(
        "🗑️ Tu ficha ha sido eliminada."
    )


async def borrar_ficha_admin(update: Update, admin_ids):
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text(
            "🚫 Solo los administradores pueden borrar fichas ajenas."
        )
        return

    texto_original = update.message.text.strip()
    partes = texto_original.split(maxsplit=1)

    user_id_buscado = None

    if update.message.reply_to_message:
        user_id_buscado = update.message.reply_to_message.from_user.id

    elif len(partes) >= 2:
        busqueda = partes[1].strip().lower().lstrip("@")

        for user_id, ficha in fichas_usuarios.items():
            usuario = (ficha.get("usuario") or "").lower()
            nombre = ficha.get("nombre", "").lower()

            if busqueda == usuario or busqueda == nombre:
                user_id_buscado = int(user_id)
                break

    if not user_id_buscado:
        await update.message.reply_text(
            "No encuentro esa ficha.\n\n"
            "Usa /borrarficha @usuario o responde a un mensaje."
        )
        return

    if str(user_id_buscado) not in fichas_usuarios:
        await update.message.reply_text(
            "Esa persona no tiene ficha guardada."
        )
        return

    fichas_usuarios.pop(str(user_id_buscado))
    guardar_fichas(fichas_usuarios)

    await update.message.reply_text(
        "🗑️ Ficha eliminada por administración."
    )
