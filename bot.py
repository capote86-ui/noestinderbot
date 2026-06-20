from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
import random

from datetime import datetime, timedelta
from collections import defaultdict, deque, Counter
from openai import OpenAI
import os

TOKEN = "8996485412:AAF_SJkLwA3-3xtMUGj59TUJNGcF17J9LV0"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("API:", os.getenv("OPENAI_API_KEY"))
respuestas = {
    
    "buenos dias": [
        "Buenos días, supervivientes de Telegram ☕",
        "Otro día más evitando red flags 😭",
        "Buenos días a los presentes y a los que solo observan 👀"
    ],

    "buenas tardes": [
        "Buenas tardes, habitantes del caos 😭",
        "La productividad murió, pero nosotros seguimos 💀"
        "Buenas tardes a los presentes y a los mirones 👀"
    ],

    "buenas noches": [
        "Descansen, criaturas del caos 😭",
        "Hora de sobrepensar eventos de 2017 💀",
        "Que el cringe no les persiga esta noche 👀"
    ],

    "tinder": [
        "🚨 Trauma detectado 🚨",
        "Aquí intentamos recuperarnos de eso 😭",
        "Palabra prohibida en territorio seguro 💀"
    ],

    "me aburr": [
        "Pues habla 😭",
        "Literalmente estás en un grupo de Telegram 💀",
        "El entretenimiento eres tú 👀"
    ],

    "grupo muerto": [
        "Está hibernando 😭",
        "Silencio administrativo detectado 💀",
        "La gente está leyendo escondida 👀"
    ],

    "tengo hambre": [
        "Pide comida y comparte 😭",
        "Todos pensando en pizza otra vez 💀",
        "El verdadero tema serio del grupo 🍕"
    ],

    "alguien": [
        "No sé, ¿personas? 😭",
        "Hay 60 personas observando en silencio 👀",
        "Probablemente sí, pero nadie quiere escribir primero 💀"
    ],

    "xd": [
        "2009 vibes detectadas 😭",
        "Ese xd viene con historia 💀"
    ],

    "toy aburr": [
        "Pues anima el cotarro 😭",
        "NPC detectado esperando contenido 👀"
    ],

    "que hacen": [
        "Sobreviviendo 😭",
        "Intentando mantener este grupo vivo 💀"
    ],

    "ayuda": [
        "No somos psicólogos pero hacemos lo que podemos 😭",
        "Describe tu evento canónico 💀"
    ],

    "triste": [
        "Abrazo grupal virtual 😭",
        "El lore del personaje continúa 💀"
    ],

    "banco": [
        "Tema delicado en España últimamente 😭"
    ],

    "pedo": [
        "Telegram nunca decepciona 💀"
    ],

    "mimir": [
        "Hora de cerrar los ojos y recordar momentos vergonzosos 😭"
    ],

    "hola buenas": [
        "Educación detectada 👀",
        "Bienvenido al caos organizado 😭"
    ],
}

preguntas_random = [
      "Pregunta seria: ¿qué red flag os hace salir corriendo? 😭",
    "¿Cuál ha sido vuestra peor primera impresión de alguien? 💀",
    "¿Qué cosa pequeña os hace perder interés automáticamente? 👀",
    "¿Qué palabra os da cringe instantáneo? 😭",
    "¿Cuál es vuestra opinión más funable? 💀",
    "¿Qué red social borraríais mañana mismo? 👀",
    "¿Cuál ha sido vuestro evento canónico más lamentable? 😭",
    "¿Qué secreto absurdo os llevaríais a la tumba? 💀",
    "¿Qué persona famosa sería insoportable como pareja? 👀",
    "Debate serio: ¿audio largo sí o cárcel? 🎙️",
    "¿Qué cosa os da vergüenza admitir que os gusta? 😭",
    "¿Qué emoji usa demasiado la gente? 💀",
    "¿Cuál ha sido vuestra conversación más incómoda? 👀",
    "¿Qué serie os parece sobrevaloradísima? 😭",
    "¿Qué hábito raro tenéis cuando estáis solos? 💀",
    "¿Qué app os roba más tiempo? 👀",
    "¿Qué frase os hace pensar automáticamente 'red flag'? 😭",
    "¿Qué persona del grupo sobreviviría mejor a un apocalipsis? 💀",
    "¿Qué es peor: ghostear o volver como si nada? 👀",
    "¿Qué manía ajena no soportáis? 😭",
    "¿Qué comida defenderíais aunque os juzguen? 💀",
    "¿Qué cosa hacéis y jamás admitiriais en persona? 👀",
    "¿Qué fue lo más raro que os dijeron para ligar? 😭",
    "¿Cuál ha sido vuestra peor cita? 💀",
    "¿Qué cosa os arruina automáticamente el día? 👀",
    "¿Qué teoría absurda tenéis sobre las relaciones? 😭",
    "¿Qué personaje ficticio sería insoportable en la vida real? 💀",
    "¿Qué canción os da vergüenza admitir que os gusta? 👀",
    "¿Cuál es vuestra red flag más absurda? 😭",
    "¿Qué es más sospechoso: responder demasiado rápido o demasiado lento? 💀",
    "¿Qué opinión os guardáis para evitar peleas? 👀",
    "¿Qué fue lo más ridículo que hicisteis por alguien? 😭",
    "¿Qué cosa os parece atractiva aunque sea rara? 💀",
    "¿Qué es peor: cancelar planes o llegar tarde? 👀",
    "¿Qué palabra debería desaparecer de internet? 😭",
    "¿Qué situación os hizo querer desaparecer del planeta? 💀",
    "¿Qué persona famosa creéis que sería un desastre en Telegram? 👀",
    "¿Qué cosa os parece insoportable en los grupos? 😭",
    "¿Qué fue lo último que os hizo pensar 'qué vergüenza ajena'? 💀",
    "¿Qué edad mental real creéis que tiene este grupo? 👀",
    "¿Qué plan os parece aburridísimo pero todo el mundo ama? 😭",
    "¿Qué película defendéis aunque sepáis que es mala? 💀",
    "¿Qué cosa os da ansiedad social instantánea? 👀",
    "¿Qué mensaje habéis enviado y os arrepentisteis inmediatamente? 😭",
    "¿Qué moda de internet os parece terrible? 💀",
    "¿Qué persona del grupo parece más sospechosa? 👀",
    "¿Qué es más red flag: no usar memes o abusar de ellos? 😭",
    "¿Qué sería peor: quedarse sin música o sin memes? 💀",
    "¿Qué cosa hacéis para evitar conversaciones incómodas? 👀",
    "¿Cuál ha sido vuestro momento más NPC? 😭",
    "¿Qué costumbre rara tiene vuestra familia? 💀",
    "¿Qué mentira absurda habéis dicho para salir de una situación? 👀",
    "¿Qué frase define perfectamente vuestro estado mental hoy? 😭",
    "¿Qué tema siempre acaba en discusión? 💀",
    "¿Qué persona del grupo parece tener más lore oculto? 👀",
    "¿Qué cosa os da miedo admitir públicamente? 😭",
    "¿Qué conversación os dejó pensando días después? 💀",
    "¿Qué haríais si mañana desapareciera internet? 👀",
    "¿Qué es más difícil: ligar o mantener conversación? 😭",
    "¿Qué habilidad inútil tenéis? 💀",
    "¿Qué cosa hacéis cuando nadie os responde? 👀",
    "¿Qué app define mejor vuestro caos mental? 😭",
    "¿Qué cosa os parece sospechosa en una persona demasiado perfecta? 💀",
    "¿Qué cosa normal os parece rarísima? 👀",
    "¿Qué fue lo último que os hizo reír muchísimo solos? 😭",
    "¿Qué frase diría perfectamente este grupo? 💀",
    "¿Qué persona del grupo parece más capaz de desaparecer 3 meses? 👀",
    "¿Qué situación os da vergüenza recordar antes de dormir? 😭",
    "¿Qué red flag vuestra defendéis igualmente? 💀",
    "¿Qué es más peligroso: aburrirse o sobrepensar? 👀",
    "¿Qué cosa os hace parecer bordes sin querer? 😭",
    "¿Qué tema jamás debería tocarse después de las 2am? 💀",
    "¿Qué persona famosa tendría más probabilidades de acabar en este grupo? 👀"
]
quienesmas_activo = {}
quienesmas_votos = {}
quienesmas_resultados = []

preguntas_quienesmas = [
    "¿Quién es más probable que defienda la pizza con piña?",
    "¿Quién es más probable que llegue tarde y diga que ya está llegando?",
    "¿Quién es más probable que se quede dormido en una cita?",
    "¿Quién es más probable que llore con Titanic?",
    "¿Quién es más probable que diga 'una copa y nos vamos' y vuelva de día?",
    "¿Quién es más probable que tenga 50 chats sin responder?",
    "¿Quién es más probable que sobreviva a un apocalipsis zombie?",
    "¿Quién es más probable que se enamore de una voz?",
    "¿Quién es más probable que se pierda usando Google Maps?",
    "¿Quién es más probable que pida postre diciendo que no tiene hambre?",
    "¿Quién es más probable que cante en la ducha como si estuviera en La Voz?",
    "¿Quién es más probable que compre algo absurdo por internet?",
    "¿Quién es más probable que se haga viral sin querer?",
    "¿Quién es más probable que diga 'yo no me enamoro' y caiga primero?",
    "¿Quién es más probable que tenga una historia surrealista para todo?",
    "¿Quién es más probable que organice un viaje entero?",
    "¿Quién es más probable que pierda el cargador del móvil?",
    "¿Quién es más probable que vea una temporada entera en un día?",
    "¿Quién es más probable que mande un audio de 7 minutos?",
    "¿Quién es más probable que convierta cualquier plan tranquilo en una aventura?"
]

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text.lower().strip()

    chat_id = update.effective_chat.id
    ultima_actividad[chat_id] = datetime.now()
    usuario = update.effective_user.first_name or "Alguien"
    historial_chats[chat_id].append((usuario, mensaje))

    user_id = update.effective_user.id
    nombres_usuarios[user_id] = usuario

    contador_mensajes[user_id] = contador_mensajes.get(user_id, 0) + 1
    ultimo_mensaje_usuario[user_id] = datetime.now()

    if user_id not in mensajes_usuario:
        mensajes_usuario[user_id] = []

    mensajes_usuario[user_id].append(mensaje)

    if len(mensajes_usuario[user_id]) > 80:
        mensajes_usuario[user_id] = mensajes_usuario[user_id][-80:]

    palabras_presentacion = [
        "soy ",
        "me llamo",
        "tengo ",
        "soy de",
        "vivo en",
        "me presento"
    ]

    if any(p in mensaje for p in palabras_presentacion):
        usuarios_presentados[user_id] = True
    if mensaje.startswith("!quienhabla") or mensaje.startswith("/quienhabla"):
        if not contador_mensajes:
            await update.message.reply_text("Aquí todavía no ha hablado ni el apuntador 😭")
            return

        ranking = sorted(contador_mensajes.items(), key=lambda x: x[1], reverse=True)[:10]

        texto = "📊 ¿Quién está dando más guerra?\n\n"

        for uid, total in ranking:
            nombre = nombres_usuarios.get(uid, "Alguien misterioso")
            texto += f"• {nombre}: {total} mensajes\n"

        await update.message.reply_text(texto)
        return
    if mensaje.startswith("!ranking") or mensaje.startswith("/ranking"):
        if not contador_mensajes:
            await update.message.reply_text("Todavía no tengo suficiente cotilleo estadístico 😭")
            return

        ranking = sorted(contador_mensajes.items(), key=lambda x: x[1], reverse=True)[:10]

        texto = "🏆 Ranking del caos\n\n"

        for i, (uid, total) in enumerate(ranking, start=1):
            nombre = nombres_usuarios.get(uid, "Alguien misterioso")
            texto += f"{i}. {nombre} - {total} mensajes\n"

        await update.message.reply_text(texto)
        return
    if mensaje.startswith("!fantasmas") or mensaje.startswith("/fantasmas"):
        if not ultimo_mensaje_usuario:
            await update.message.reply_text("Todavía no tengo fantasmas fichados 👻")
            return

        ahora = datetime.now()
        fantasmas = []

        for uid, fecha in ultimo_mensaje_usuario.items():
            horas = int((ahora - fecha).total_seconds() // 3600)

            if horas >= 24:
                nombre = nombres_usuarios.get(uid, "Alguien misterioso")
                dias = horas // 24
                fantasmas.append((nombre, dias))

        if not fantasmas:
            await update.message.reply_text("De momento no hay fantasmas. Milagro social 👻")
            return

        texto = "👻 Desaparecidos en combate\n\n"

        for nombre, dias in sorted(fantasmas, key=lambda x: x[1], reverse=True)[:10]:
            texto += f"• {nombre} - {dias} días sin hablar\n"

        await update.message.reply_text(texto)
        return
    if mensaje.startswith("!ficha") or mensaje.startswith("/ficha"):
        partes = mensaje.split(maxsplit=1)

        if len(partes) < 2:
            await update.message.reply_text("Dime de quién quieres la ficha. Ejemplo: !ficha Pedro")
            return

        buscado = partes[1].lower()
        encontrado = None

        for uid, nombre in nombres_usuarios.items():
            if buscado in nombre.lower():
                encontrado = uid
                break

        if not encontrado:
            await update.message.reply_text("No encuentro a esa criatura en mis archivos 😭")
            return

        nombre = nombres_usuarios.get(encontrado, "Alguien misterioso")
        total = contador_mensajes.get(encontrado, 0)
        presentado = "Sí" if usuarios_presentados.get(encontrado) else "No"
        ultimo = ultimo_mensaje_usuario.get(encontrado)

        if ultimo:
            horas = int((datetime.now() - ultimo).total_seconds() // 3600)
            ultimo_texto = f"hace {horas} horas" if horas > 0 else "hace nada"
        else:
            ultimo_texto = "no consta"

        if total >= 100:
            nivel = "protagonista absoluto del reality"
        elif total >= 50:
            nivel = "personaje recurrente con trama propia"
        elif total >= 10:
            nivel = "secundario con posibilidades"
        else:
            nivel = "figurante en prácticas"

        await update.message.reply_text(
            f"📋 Ficha de {nombre}\n\n"
            f"🕒 Mensajes enviados: {total}\n"
            f"🎂 Se presentó: {presentado}\n"
            f"💬 Último mensaje: {ultimo_texto}\n"
            f"🔥 Nivel de presencia: {nivel}"
        )
        return

        if mensaje.startswith("!presentados") or mensaje.startswith("/presentados"):
            presentados = [
            nombres_usuarios.get(uid, "Alguien misterioso")
            for uid in usuarios_presentados
            if usuarios_presentados.get(uid)
        ]

        if not presentados:
            await update.message.reply_text("De momento nadie se ha presentado como Dios manda 😭")
            return

        texto = "✅ Usuarios que parecen haberse presentado:\n\n"

        for nombre in presentados:
            texto += f"• {nombre}\n"

        await update.message.reply_text(texto)
        return
    if mensaje.startswith("!analiza") or mensaje.startswith("/analiza"):
        partes = mensaje.split(maxsplit=1)

        if len(partes) < 2:
            await update.message.reply_text("Dime a quién analizo. Ejemplo: !analiza Pedro")
            return

        buscado = partes[1].lower()
        encontrado = None

        for uid, nombre in nombres_usuarios.items():
            if buscado in nombre.lower():
                encontrado = uid
                break

        if not encontrado:
            await update.message.reply_text("No encuentro suficiente material de esa criatura 😭")
            return

        nombre = nombres_usuarios.get(encontrado, "Alguien misterioso")
        textos_usuario = mensajes_usuario.get(encontrado, [])[-30:]

        if not textos_usuario:
            await update.message.reply_text("No tengo suficiente historial para analizar a este espécimen 😭")
            return

        conversacion = "\n".join(textos_usuario)

        respuesta_ia = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres una IA sarcástica, divertida y con mala leche elegante. Analizas usuarios de un grupo de Telegram sin ser cruel ni insultar de forma grave. Sé breve, cómica y directa."
                },
                {
                    "role": "user",
                    "content": f"Analiza de forma divertida a {nombre} según estos últimos mensajes:\n\n{conversacion}"
                }
            ],
            max_tokens=180
        )

        analisis = respuesta_ia.choices[0].message.content

        await update.message.reply_text(f"🧠 Análisis de {nombre}\n\n{analisis}")
        return

    if mensaje.startswith("!normas") or mensaje.startswith("/normas"):

        texto_normas = (
            "📜 NORMAS DEL GRUPO\n\n"

            "1️⃣ Presentarte para entrar.\n"
            "Nombre, edad y de dónde eres.\n\n"

            "2️⃣ Es obligatorio tener foto de perfil.\n"
            "Las cuentas sin foto podrán ser expulsadas por seguridad y confianza del grupo.\n\n"

            "3️⃣ Respeto ante todo.\n"
            "Nada de insultos, faltas de respeto, acoso ni comportamientos que generen mal ambiente.\n\n"

            "4️⃣ Prohibido:\n"
            "• Menores de 18 años.\n"
            "• Spam y publicidad.\n"
            "• Venta o promoción de contenido sexual o pornográfico.\n"
            "• Agregar al privado sin permiso.\n"
            "• Política, religión y temas que puedan generar conflicto.\n\n"

            "5️⃣ Este grupo está pensado para conocer gente, hacer amistades y pasar un buen rato.\n\n"

            "6️⃣ Si alguien te molesta o incumple las normas, avisa a un moderador o administrador.\n\n"

            "7️⃣ Aquí venimos a charlar, reírnos y mantener un buen ambiente.\n\n"

            "8️⃣ El incumplimiento de las normas puede suponer la expulsión inmediata."
        )

        await update.message.reply_text(texto_normas)
        return
    if mensaje.startswith("!sinpresentar") or mensaje.startswith("/sinpresentar"):

        pendientes = []

        for uid, nombre in nombres_usuarios.items():
            if not usuarios_presentados.get(uid, False):
                pendientes.append(nombre)

        if not pendientes:
            await update.message.reply_text(
                "🎉 Todo el mundo parece haberse presentado. Milagro estadístico."
            )
            return

        texto = "👀 Usuarios pendientes de presentación\n\n"

        for nombre in pendientes:
            texto += f"• {nombre}\n"

        texto += "\n📢 Recordad presentaros con nombre, edad y de dónde sois."

        await update.message.reply_text(texto)
        return
    if mensaje.startswith("!vigilar") or mensaje.startswith("/vigilar"):

        sin_presentar = []
        poco_activos = []
        inactivos = []

        ahora = datetime.now()

        for uid, nombre in nombres_usuarios.items():
            total = contador_mensajes.get(uid, 0)
            presentado = usuarios_presentados.get(uid, False)
            ultimo = ultimo_mensaje_usuario.get(uid)

            if not presentado:
                sin_presentar.append(nombre)

            if total < 3:
                poco_activos.append((nombre, total))

            if ultimo:
                dias = int((ahora - ultimo).total_seconds() // 86400)
                if dias >= 7:
                    inactivos.append((nombre, dias))

        texto = "👮 Informe de vigilancia\n\n"

        texto += "📌 Sin presentar:\n"
        if sin_presentar:
            for nombre in sin_presentar[:10]:
                texto += f"• {nombre}\n"
        else:
            texto += "• Nadie pendiente. Milagro administrativo.\n"

        texto += "\n🫥 Con menos de 3 mensajes:\n"
        if poco_activos:
            for nombre, total in poco_activos[:10]:
                texto += f"• {nombre} — {total} mensajes\n"
        else:
            texto += "• Nadie en modo estatua.\n"

        texto += "\n👻 Inactivos +7 días:\n"
        if inactivos:
            for nombre, dias in inactivos[:10]:
                texto += f"• {nombre} — {dias} días sin hablar\n"
        else:
            texto += "• Sin fantasmas graves por ahora.\n"

        texto += "\nResumen: si alguien aparece en las tres listas, huele a decoración de grupo 😭"

        await update.message.reply_text(texto)
        return

    if mensaje.startswith("!recordatorio") or mensaje.startswith("/recordatorio"):

        texto = (
            "📢 Recordatorio del grupo\n\n"
            "Si todavía no te has presentado, hazlo con:\n"
            "• Nombre\n"
            "• Edad\n"
            "• De dónde eres\n\n"
            "También es obligatorio tener foto de perfil. Puede ser tuya, de una mascota, paisaje, meme o lo que quieras, pero algo que no parezca cuenta fantasma 👻\n\n"
            "Aquí venimos a charlar, reírnos y conocer gente. Si solo vienes a mirar desde la esquina, al menos trae pipas 😭"
        )

        await update.message.reply_text(texto)
        return

    if mensaje.startswith("!limpieza") or mensaje.startswith("/limpieza"):

        sin_presentar = []
        poco_activos = []
        inactivos = []

        ahora = datetime.now()

        for uid, nombre in nombres_usuarios.items():

            total = contador_mensajes.get(uid, 0)
            presentado = usuarios_presentados.get(uid, False)
            ultimo = ultimo_mensaje_usuario.get(uid)

            if not presentado:
                sin_presentar.append(nombre)

            if total < 3:
                poco_activos.append((nombre, total))

            if ultimo:
                dias = int((ahora - ultimo).total_seconds() // 86400)

                if dias >= 7:
                    inactivos.append((nombre, dias))

        texto = "🧹 INFORME DE LIMPIEZA\n\n"

        texto += f"👀 Sin presentar: {len(sin_presentar)}\n"
        texto += f"🗿 Menos de 3 mensajes: {len(poco_activos)}\n"
        texto += f"👻 Inactivos (+7 días): {len(inactivos)}\n\n"

        if sin_presentar:
            texto += "📌 Pendientes de presentación:\n"
            for nombre in sin_presentar[:10]:
                texto += f"• {nombre}\n"

        if poco_activos:
            texto += "\n🗿 Modo decoración:\n"
            for nombre, total in poco_activos[:10]:
                texto += f"• {nombre} ({total} mensajes)\n"

        if inactivos:
            texto += "\n👻 Fantasmas:\n"
            for nombre, dias in inactivos[:10]:
                texto += f"• {nombre} ({dias} días)\n"

        await update.message.reply_text(texto)
        return

    if mensaje.startswith("!foto") or mensaje.startswith("/foto"):

        texto = (
            "📸 Recordatorio de foto de perfil\n\n"
            "Por seguridad y confianza del grupo, es obligatorio tener foto de perfil.\n\n"
            "No hace falta que sea una foto tuya: puede ser una mascota, un paisaje, un meme, un peluche o lo que quieras.\n\n"
            "La idea es que la cuenta no parezca un perfil fantasma mirando desde la esquina 👻"
        )

        if update.message.reply_to_message:
            await update.message.reply_to_message.reply_text(texto)
        else:
            await update.message.reply_text(texto)

        return

    if mensaje.startswith("!quienesmas") or mensaje.startswith("/quienesmas"):
        pregunta = random.choice(preguntas_quienesmas)

        quienesmas_activo[chat_id] = pregunta
        quienesmas_votos[chat_id] = {}

        await update.message.reply_text(
            f"👀 ¿Quién es más probable...?\n\n"
            f"{pregunta}\n\n"
            f"🗳️ Para votar, escribe el @usuario de la persona elegida.\n"
            f"Ejemplo: @usuario\n\n"
            f"Solo cuentan los mensajes que tengan arroba.\n"
            f"Para cerrar la votación, un admin puede poner /cerrarquienes."
        )
        return

    if mensaje.startswith("!cerrarquienes") or mensaje.startswith("/cerrarquienes"):
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        if update.effective_user.id not in admin_ids:
            await update.message.reply_text("Solo los admins pueden cerrar la votación 😭")
            return

        if chat_id not in quienesmas_activo:
            await update.message.reply_text("No hay ninguna votación activa ahora mismo.")
            return

        votos = quienesmas_votos.get(chat_id, {})

        if not votos:
            await update.message.reply_text("Nadie ha votado. Democracia fallida 😭")
            quienesmas_activo.pop(chat_id, None)
            quienesmas_votos.pop(chat_id, None)
            return

        conteo = {}

        for votado in votos.values():
            conteo[votado] = conteo.get(votado, 0) + 1

        ranking = sorted(conteo.items(), key=lambda x: x[1], reverse=True)

        texto = "🏆 Resultado del '¿Quién es más...?'\n\n"

        for i, (nombre, total) in enumerate(ranking, start=1):
            texto += f"{i}. {nombre} — {total} voto(s)\n"

        ganador = ranking[0][0]

        texto += f"\n{ganador}, el grupo ha hablado. Proceda a defenderse 😭"

        quienesmas_resultados.append({
            "pregunta": quienesmas_activo[chat_id],
            "ganador": ganador,
            "votos": conteo
        })

        quienesmas_activo.pop(chat_id, None)
        quienesmas_votos.pop(chat_id, None)

        await update.message.reply_text(texto)
        return

    if chat_id in quienesmas_activo and "@" in update.message.text:
        texto_voto = update.message.text.strip()
        votante_id = update.effective_user.id

        partes = texto_voto.split()
        menciones = [p for p in partes if p.startswith("@")]

        if not menciones:
            return

        voto = menciones[0]

        quienesmas_votos[chat_id][votante_id] = voto

        await update.message.reply_text(f"🗳️ Voto registrado: {voto}")
        return

    if mensaje.startswith("!miid") or mensaje.startswith("/miid"):
        await update.message.reply_text(
        f"Tu ID numérico de Telegram es: {update.effective_user.id}"
    )
    return
    for trigger in respuestas:
        if trigger in mensaje:
            respuesta = random.choice(respuestas[trigger])
            await update.message.reply_text(respuesta)
            return

    if random.randint(1, 300) == 1:
        await update.message.reply_text(random.choice(preguntas_random))

    if mensaje.startswith("!pregunta") or mensaje.startswith("/pregunta"):
        await update.message.reply_text(random.choice(preguntas))

    if mensaje.startswith("!pregunta") or mensaje.startswith("/pregunta"):
        await update.message.reply_text(random.choice(preguntas))
        return

    if mensaje.startswith("!batalla") or mensaje.startswith("/batalla"):
        await update.message.reply_text(random.choice(batallas))
        return

    if mensaje.startswith("!confesion") or mensaje.startswith("/confesion"):
        await update.message.reply_text(random.choice(confesiones))
        return

    if mensaje in ["!corte", "/corte"]:
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        if update.effective_user.id not in admin_ids:
            await update.message.reply_text("Este botón rojo solo lo pueden pulsar los admins 😭")
            return

        corte = random.choice(cortes)

        if update.message.reply_to_message:
            await update.message.reply_to_message.reply_text(corte)
        else:
            await update.message.reply_text(corte)

        return

    if mensaje.startswith("!burla") or mensaje.startswith("/burla"):
        texto = mensaje.replace("!burla", "", 1).replace("/burla", "", 1).strip()

        if not texto and update.message.reply_to_message:
            texto = update.message.reply_to_message.text or ""

        if not texto:
            await update.message.reply_text("Tienes que escribir algo después de !burla o responder a un mensaje 😭")
            return

        burla = (
            texto.lower()
            .replace("a", "i")
            .replace("e", "i")
            .replace("o", "i")
            .replace("u", "i")
        )

        await update.message.reply_text(f"🫵 {burla} 😭")
        return 
        
    
preguntas = [
    "¿Qué red flag todo el mundo normaliza y tú no soportas? 🚩",
    "¿Cuál ha sido tu peor primera impresión de alguien? 😭",
    "¿Qué cosa te hace perder interés automáticamente? 💀",
    "¿Cuál ha sido la excusa más absurda que te han dado? 👀",
    "¿Qué opinión tienes que podría enfadar al grupo entero? 😭",
    "¿Qué cosa haces tú que sabes que es red flag? 💀",
    "¿Qué persona famosa sería insoportable como pareja? 👀",
    "¿Qué es peor: ghostear o volver como si nada? 😭",
    "¿Cuál ha sido tu conversación más incómoda? 💀",
    "¿Qué manía ajena no soportas? 👀",
    "¿Qué cosa te enamora aunque sea una tontería? 😭",
    "¿Qué es más red flag: seguir a demasiada gente o no seguir a nadie? 💀",
    "¿Qué fue lo más raro que te dijeron para ligar? 👀",
    "¿Qué palabra te da cringe instantáneo? 😭",
    "¿Qué serie o película te parece sobrevalorada? 💀",
    "¿Qué cosa pequeña te arruina el día? 👀",
    "¿Cuál es tu teoría más absurda sobre las relaciones? 😭",
    "¿Qué edad mental crees que tiene realmente el grupo? 💀",
    "¿Qué red social sacarías del planeta mañana mismo? 👀",
    "¿Cuál es la indirecta más obvia que no captaste? 😭",
    "¿Qué cosa haces cuando nadie te ve? 💀",
    "¿Qué canción pondrías para resumir tu vida amorosa? 👀",
    "¿Qué emoji usa demasiado la gente? 😭",
    "¿Qué te parece atractivo aunque sea raro? 💀",
    "¿Qué es peor: llegar tarde o cancelar planes? 👀",
]

batallas = [
    "Debate serio: ¿ducharse por la mañana o por la noche? 🚿",
    "¿Dormir con ruido o silencio absoluto? 😭",
    "¿Pizza con piña sí o expulsión inmediata? 🍍",
    "¿Audio largo o muro de texto? 💀",
    "¿TikTok ha destruido la atención de todos? 👀",
    "¿Responder rápido da necesidad o educación? 😭",
    "¿Dormir con calcetines es comodidad o delito? 🧦",
    "¿Ver series dobladas o subtituladas? 💀",
    "¿Café frío o crimen internacional? ☕",
    "¿La tortilla con cebolla o sin cebolla? 😭",
    "¿Los memes dan más conversación que las personas? 💀",
    "¿Llamar por teléfono debería prohibirse? 👀",
    "¿Instagram es postureo o diario personal? 😭",
    "¿Se puede ser amigo de un ex? 💀",
    "¿El visto debería desaparecer? 👀",
    "¿Es peor mentir o ocultar cosas? 😭",
    "¿Compartir ubicación da seguridad o miedo? 💀",
    "¿Las notas de voz deberían tener límite legal? 👀",
    "¿Plan tranquilo en casa o salir de fiesta? 😭",
    "¿La gente guapa lo tiene realmente más fácil? 💀",
]

confesiones = [
     "Confiesa una red flag tuya 😭",
    "¿Qué mentira absurda has dicho para quedar bien? 💀",
    "¿Qué cosa te da vergüenza admitir que te gusta? 👀",
    "¿Cuál ha sido tu evento canónico más lamentable? 😭",
    "¿Qué hiciste una vez y todavía te despiertas recordándolo? 💀",
    "¿Cuál ha sido tu peor ghosteo? 👀",
    "¿Qué es lo más tóxico que has hecho? 😭",
    "¿Cuál ha sido tu peor borrachera? 💀",
    "¿Qué persona no deberías haber vuelto a hablar nunca? 👀",
    "¿Qué fue lo más ridículo que hiciste por alguien? 😭",
    "¿Qué secreto absurdo tuyo descubriría el FBI? 💀",
    "¿Qué cosa infantil sigues haciendo? 👀",
    "¿Cuál ha sido tu momento más NPC? 😭",
    "¿Qué has stalkeado y jamás deberías haber visto? 💀",
    "¿Cuál ha sido tu peor mensaje enviado por error? 👀",
    "¿Qué opinión tuya ocultas para evitar peleas? 😭",
    "¿Qué hábito raro tienes cuando estás solo? 💀",
    "¿Cuál ha sido tu peor cita? 👀",
    "¿Qué excusa has usado para escapar de alguien? 😭",
    "¿Qué cosa haces y jamás admitirías en persona? 💀",
]
cortes = [
    "🚨 Alerta de intensidad innecesaria. Aquí se socializa, no se abre casting para OnlyFans.",
    "📸 Intercambio de fotos no solicitado detectado. Respira, hidrátate y compórtate como una persona funcional.",
    "🛑 Este grupo no es Wallapop emocional ni mercado negro de fotos.",
    "🚓 La patrulla antirraro ha sido avisada. Baja dos cambios.",
    "💀 Se ruega guardar la energía de depredador de Telegram en una carpeta y no traerla aquí.",
    "📢 Recordatorio amable: sin privados raros, sin pedir fotos y sin vender contenido. Qué locura pedir lo básico.",
    "🧯 Apagando incendio de cringe. Siguiente intento raro será gestionado por administración."
]

ultima_actividad = {}
ultimo_empujon = {}

mensajes_silencio = [
    "👀 ¿Seguís vivos o ya os habéis mudado todos a los privados?",
    "🪦 Minuto de silencio por esta conversación.",
    "🤖 Adelaida sospecha que os habéis quedado dormidos.",
    "📢 Recordatorio: esto es un grupo, no un documental de observación.",
    "🫥 Hay más gente leyendo que escribiendo. Sospechoso.",
    "☕ Aprovechad que nadie habla para confesar algún evento canónico.",
    "🚨 Detectado exceso de espectadores y escasez de protagonistas.",
    "📡 Buscando señales de vida inteligente...",
    "🎭 Este grupo tiene más extras que actores ahora mismo.",
    "👻 Si estáis aquí, haced una señal. Un parpadeo sirve."
]
MINUTOS_SILENCIO = 180
historial_chats = defaultdict(lambda: deque(maxlen=120))
contador_mensajes = {}
ultimo_mensaje_usuario = {}
nombres_usuarios = {}
usuarios_presentados = {}
mensajes_usuario = {}
async def revisar_silencios(context: ContextTypes.DEFAULT_TYPE):
    ahora = datetime.now()
    hora = ahora.hour

    if hora >= 23 or hora < 8:
        return
    
    for chat_id, ultima in list(ultima_actividad.items()):
        tiempo_silencio = ahora - ultima
        ultimo_aviso = ultimo_empujon.get(chat_id)

        if tiempo_silencio >= timedelta(minutes=MINUTOS_SILENCIO):
            if not ultimo_aviso or ahora - ultimo_aviso >= timedelta(minutes=MINUTOS_SILENCIO):
                pregunta = random.choice(preguntas_random)
                mensaje_silencio = random.choice(mensajes_silencio)
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"{mensaje_silencio}\n\n{pregunta}"
                )
                ultimo_empujon[chat_id] = ahora
app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, responder))

print("Bot funcionando 😭")
app.job_queue.run_repeating(revisar_silencios, interval=600, first=600)
app.run_polling()
