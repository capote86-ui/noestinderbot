from telegram.ext import Application, MessageHandler, CallbackQueryHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import CallbackQueryHandler
import random

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from collections import defaultdict, deque, Counter
from openai import OpenAI
import os

from tribunal import (
    activar_tribunal,
    desactivar_tribunal,
    lanzar_tribunal_manual,
    cancelar_tribunal,
    botones_tribunal,
    publicar_tribunal
)
from trivial import iniciar_trivial, cancelar_trivial, mostrar_ranking_trivial, botones_trivial
from fichas import guardar_ficha_admin, mostrar_ficha, borrar_ficha_admin
from cumpleanos import (
    activar_cumpleanos,
    desactivar_cumpleanos,
    mostrar_proximos_cumpleanos,
    mostrar_cumpleanos_mes,
    revisar_cumpleanos
)
from misa_domingo import (
    activar_misa,
    desactivar_misa,
    lanzar_misa_manual,
    cancelar_misa,
    aviso_misa_30,
    aviso_misa_10,
    aviso_misa_2,
    publicar_misa_automatica
)
from tests import (
    activar_tests,
    desactivar_tests,
    lanzar_test_manual,
    publicar_test_automatico,
    cancelar_test_admin,
    botones_tests,
)
TOKEN = os.getenv("BOT_TOKEN")
print("TOKEN CARGADO:", bool(TOKEN))
print("API:", os.getenv("OPENAI_API_KEY"))
respuestas = {

"buenos dias": [
    "☕ Buenos días. Ya podéis empezar a fingir que sois adultos funcionales.",
    "🌞 Buenos días, habitantes del caos.",
    "📢 Reiniciando el servidor humano...",
    "☕ Café, dignidad y suerte para todos.",
    "👀 Buenos días a los que escriben y a los que espían.",
    "😴 ¿Ya estamos despiertos o seguimos negociándolo?",
    "🌤️ Otro día más evitando responsabilidades.",
    "📱 Telegram sigue aquí. Nosotros también.",
    "☕ Buenos días. Que hoy no os toque ningún evento canónico.",
    "😎 A ver qué desastre colectivo nos espera hoy."
],

"buenas tardes": [
    "🌇 Buenas tardes. Ya hemos sobrevivido a media jornada.",
    "☕ Hora oficial de bajar la productividad.",
    "😴 Buenas tardes a los presentes y a los que deberían estar trabajando.",
    "📢 Se abre el turno de procrastinación.",
    "🌤️ Buenas tardes, criaturas del algoritmo.",
    "👀 Los observadores silenciosos siguen ahí.",
    "🍿 ¿Qué drama nos perdimos hoy?",
    "😎 Siguen sin pagarnos por estar aquí.",
    "🫠 Ya es tarde para ser productivos.",
    "☀️ Aún quedan horas para tomar malas decisiones."
],

"buenas noches": [
    "🌙 Buenas noches. Que vuestros pensamientos os dejen dormir.",
    "😴 Hora de apagar el cerebro. O intentarlo.",
    "🌜 Descansen, leyendas del desastre.",
    "🛌 No reviséis conversaciones antiguas.",
    "👀 Que el cringe del pasado no os visite esta noche.",
    "💀 Hora de recordar momentos vergonzosos aleatorios.",
    "🌙 Cerrando sesión hasta nuevo aviso.",
    "😴 No alimentéis pensamientos intrusivos.",
    "🛸 Si os secuestran extraterrestres, avisad mañana.",
    "🌌 El caos seguirá aquí al despertar."
],

"hola buenas": [
    "👋 Educación premium detectada.",
    "😎 Bienvenido al caos organizado.",
    "📢 Buenos modales localizados.",
    "👀 Ya puedes empezar a cotillear."
],

"tinder": [
    "🚨 Trauma detectado.",
    "😭 Aquí intentamos recuperarnos de eso.",
    "💀 Palabra prohibida en territorio seguro.",
    "🫠 No invoques ese mal.",
    "⚠️ Recuerdo de Vietnam desbloqueado."
],

"me aburr": [
    "🎭 El entretenimiento eres tú.",
    "📢 Pues genera contenido.",
    "👀 NPC detectado esperando evento aleatorio.",
    "🍿 Empieza un drama, una encuesta o un debate.",
    "😎 El grupo no incluye animadores profesionales.",
    "🎲 Lanza un tema random y observa qué pasa.",
    "🚨 Nivel de aburrimiento crítico detectado.",
    "🤝 Interactúa con otros humanos. Riesgo asumible."
],

"toy aburr": [
    "🎭 El entretenimiento eres tú.",
    "👀 NPC detectado esperando contenido.",
    "📢 Pues anima el cotarro.",
    "🍿 Estamos esperando tu aportación."
],

"grupo muerto": [
    "⚰️ No está muerto. Está cargando.",
    "😴 Está en modo ahorro de energía.",
    "👀 Hay más gente leyendo que hablando.",
    "📡 Actividad vital mínima detectada.",
    "🫠 Todos esperan que escriba otro.",
    "☕ El grupo está tomando café mentalmente.",
    "📱 60 personas mirando. 0 escribiendo.",
    "💀 Grupo muerto desde 2019. Mismos síntomas."
],

"tengo hambre": [
    "🍕 El tema más serio del grupo.",
    "🌮 Proceda a ingerir alimentos.",
    "🍔 Tu cuerpo te está enviando una sugerencia.",
    "🍟 Todos acabamos hablando de comida.",
    "🌯 Ahora yo también tengo hambre.",
    "🍕 Otra vez la pizza ganando.",
    "🍜 ¿Y qué vas a pedir?"
],

"alguien": [
    "👀 Seguro que sí. Otra cosa es que responda.",
    "📢 Hay gente. Lo prometo.",
    "🫠 Todos están esperando que responda otro.",
    "🤔 Estadísticamente debería haber alguien.",
    "📡 Presencia humana probable.",
    "👻 Hay actividad paranormal suficiente.",
    "📱 60 personas observando desde las sombras."
],

"que hacen": [
    "😎 Sobreviviendo.",
    "☕ Posponiendo cosas importantes.",
    "📱 Mirando Telegram mientras hacen otra cosa.",
    "🎭 Improvisando la vida.",
    "👀 Observando sin participar.",
    "🫠 Intentando parecer adultos funcionales.",
    "🍿 Esperando contenido interesante."
],

"ayuda": [
    "🆘 Describe tu evento canónico.",
    "😭 No somos psicólogos pero hacemos lo que podemos.",
    "🤔 Cuéntanos el desastre.",
    "📢 Necesitamos contexto."
],

"triste": [
    "🫂 Abrazo grupal virtual.",
    "💀 El lore del personaje continúa.",
    "🌈 Mañana probablemente será menos raro.",
    "🤝 Te mandamos energía de la buena."
],

"banco": [
    "🏦 Tema delicado en España últimamente.",
    "💸 Nunca trae buenas noticias.",
    "😭 Ya estoy nervioso."
],

"pedo": [
    "💀 Telegram nunca decepciona.",
    "🫠 Era cuestión de tiempo.",
    "📢 Se abrió la caja de Pandora."
],

"mimir": [
    "😴 Hora de cerrar los ojos.",
    "🌙 Que descanses.",
    "💀 Hora de recordar momentos vergonzosos.",
    "🛌 Buena suerte negociando con tu cerebro."
],

"lunes": [
    "☕ Mis condolencias.",
    "😭 Nadie pidió esto.",
    "💀 El boss final de la semana.",
    "🫠 Mucha fuerza."
],

"viernes": [
    "🎉 Se logró.",
    "🍻 Sobrevivimos otra semana.",
    "😎 Ahora sí empieza la vida.",
    "🚀 Modo fin de semana activado."
],

"curro": [
    "💼 Palabra fea.",
    "☕ Mucha fuerza.",
    "😭 Que sea leve.",
    "📊 Simulando productividad."
],

"trabajo": [
    "💼 Tema sensible.",
    "☕ Mucha fuerza.",
    "😭 Nadie quiere hablar de eso.",
    "📊 Estamos todos igual."
],

"pizza": [
    "🍕 Por fin un tema importante.",
    "😎 La respuesta suele ser pizza.",
    "🍕 Nunca decepciona.",
    "🤝 Une más que la política."
],

"cafe": [
    "☕ Combustible oficial del grupo.",
    "😎 Café y a seguir.",
    "☕ La verdadera bebida energética.",
    "💀 Sin café no hay conversación."
],

"ex": [
    "🚨 Peligro detectado.",
    "💀 No abras esa puerta.",
    "🫠 Lore desbloqueado.",
    "😭 Ya empezamos."
],

"telegram": [
    "📱 Hogar de los NPCs observadores.",
    "👀 Aquí seguimos.",
    "😎 La red social de los supervivientes.",
    "💀 Más adictivo de lo que parece."
]


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
    "¿Quién es más probable que convierta cualquier plan tranquilo en una aventura?",
        "¿Quién es más probable que se quede dormido viendo una película en el cine?",
    "¿Quién es más probable que llegue tarde a su propia boda?",
    "¿Quién es más probable que se compre algo que no necesita por una oferta?",
    "¿Quién es más probable que se haga amigo del camarero en cinco minutos?",
    "¿Quién es más probable que sobreviva una semana sin móvil?",
    "¿Quién es más probable que envíe un mensaje al grupo equivocado?",
    "¿Quién es más probable que se deje la cartera en casa?",
    "¿Quién es más probable que termine cantando en un karaoke sin querer?",
    "¿Quién es más probable que se coma el último trozo de pizza sin preguntar?",
    "¿Quién es más probable que tenga una colección rarísima en casa?",
    "¿Quién es más probable que se quede atrapado viendo vídeos de gatos durante horas?",
    "¿Quién es más probable que adopte un animal exótico?",
    "¿Quién es más probable que se apunte a un reality show?",
    "¿Quién es más probable que gane un concurso de excusas?",
    "¿Quién es más probable que aparezca en televisión por accidente?",
    "¿Quién es más probable que haga una maleta una hora antes del vuelo?",
    "¿Quién es más probable que olvide un cumpleaños importante?",
    "¿Quién es más probable que se pierda en un centro comercial?",
    "¿Quién es más probable que se haga influencer sin pretenderlo?",
    "¿Quién es más probable que monte un negocio loco y que funcione?",
    "¿Quién es más probable que tenga una historia increíble para cualquier tema?",
    "¿Quién es más probable que sobreviva mejor en una isla desierta?",
    "¿Quién es más probable que se quede sin batería todos los días?",
    "¿Quién es más probable que se quede hablando hasta las 5 de la mañana?",
    "¿Quién es más probable que organice una quedada y luego no vaya?",
    "¿Quién es más probable que compre un billete para el día equivocado?",
    "¿Quién es más probable que se convierta en detective por aburrimiento?",
    "¿Quién es más probable que se enamore de alguien por cómo escribe?",
    "¿Quién es más probable que diga 'no voy a salir' y acabar de fiesta?",
    "¿Quién es más probable que llore viendo anuncios de Navidad?",
    "¿Quién es más probable que gane una discusión aunque no tenga razón?",
    "¿Quién es más probable que se quede atrapado en un ascensor?",
    "¿Quién es más probable que haga reír incluso cuando está enfadado?",
    "¿Quién es más probable que sobreviva a un apocalipsis con una chancla?",
    "¿Quién es más probable que se apunte a una actividad rara por curiosidad?",
    "¿Quién es más probable que encuentre dinero en la calle?",
    "¿Quién es más probable que tenga más memes guardados en el móvil?",
    "¿Quién es más probable que se quede dormido en una videollamada?",
    "¿Quién es más probable que se haga viral por un motivo absurdo?",
    "¿Quién es más probable que se haga amigo de un desconocido en un viaje?",
    "¿Quién es más probable que sepa más cotilleos del grupo?",
    "¿Quién es más probable que aparezca con un cambio de look radical?",
    "¿Quién es más probable que termine viviendo en otro país?",
    "¿Quién es más probable que convenza al grupo para hacer una locura?",
    "¿Quién es más probable que se presente a un concurso de televisión?",
    "¿Quién es más probable que llegue a una cita un día antes por error?",
    "¿Quién es más probable que mande un audio de más de diez minutos?",
    "¿Quién es más probable que se quede leyendo comentarios en internet durante horas?",
    "¿Quién es más probable que tenga más suerte en los sorteos?",
    "¿Quién es más probable que gane una guerra de memes?",
    "¿Quién es más probable que adopte una cabra porque le dio pena?",
    "¿Quién es más probable que compre algo por AliExpress a las tres de la mañana?",
    "¿Quién es más probable que monte una fiesta improvisada en casa?",
    "¿Quién es más probable que se convierta en leyenda del grupo?",
    "¿Quién es más probable que desaparezca una semana y volver como si nada?",
    "¿Quién es más probable que encuentre pareja primero?",
    "¿Quién es más probable que termine escribiendo un libro?",
    "¿Quién es más probable que tenga una teoría conspiranoica favorita?",
    "¿Quién es más probable que gane un concurso de comer pizza?",
    "¿Quién es más probable que llegue tarde incluso estando al lado?",
    "¿Quién es más probable que olvide por qué abrió la nevera?",
    "¿Quién es más probable que se quede atrapado viendo reels durante tres horas?",
    "¿Quién es más probable que haga una compra impulsiva gigantesca?",
    "¿Quién es más probable que acabe presentando un programa de televisión?",
    "¿Quién es más probable que se disfrace sin necesidad de carnaval?",
    "¿Quién es más probable que sobreviva más tiempo en un videojuego de terror?",
    "¿Quién es más probable que tenga un talento oculto que nadie conoce?",
    "¿Quién es más probable que acabe hablando con un famoso por casualidad?",
    "¿Quién es más probable que convierta una anécdota de cinco minutos en una historia de media hora?",
    "¿Quién es más probable que adopte una alpaca si pudiera?",
    "¿Quién es más probable que se quede atrapado viendo documentales absurdos?",
    "¿Quién es más probable que haga amigos en una cola del supermercado?",
    "¿Quién es más probable que gane un concurso de cultura inútil?",
    "¿Quién es más probable que se pierda siguiendo un GPS?",
    "¿Quién es más probable que encuentre una oferta imposible?",
    "¿Quién es más probable que se monte una película por un mensaje ambiguo?",
    "¿Quién es más probable que sea el primero en responder en el grupo?",
    "¿Quién es más probable que aparezca con una mascota inesperada?",
    "¿Quién es más probable que termine viviendo en una furgoneta camper?",
    "¿Quién es más probable que se haga astronauta si pudiera?",
    "¿Quién es más probable que convenza a alguien de casi cualquier cosa?",
    "¿Quién es más probable que tenga la mejor excusa preparada?",
    "¿Quién es más probable que se quede dormido en el transporte público?",
    "¿Quién es más probable que sobreviva a una semana sin internet?",
    "¿Quién es más probable que haga una lista para absolutamente todo?",
    "¿Quién es más probable que se convierta en meme del grupo?",
    "¿Quién es más probable que tenga la historia más surrealista del año?",
    "¿Quién es más probable que se apunte a una aventura sin preguntar detalles?",
    "¿Quién es más probable que gane este propio juego de '¿Quién es más?'?"
]

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text.lower().strip()

    chat_id = update.effective_chat.id
    
    if mensaje.startswith("/") or mensaje.startswith("!"):
        comando = mensaje.split()[0]
        comando = comando.lstrip("/!").split("@")[0]

        if comando in COMANDOS_SOLO_ADMINS:
            admins = await context.bot.get_chat_administrators(chat_id)
            admin_ids = [admin.user.id for admin in admins]

            if update.effective_user.id not in admin_ids:
                await update.message.reply_text(
                    "🚫 Este comando solo pueden utilizarlo los administradores."
                )
                return
    
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
    if mensaje == "!ranking" or mensaje == "/ranking":
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

            "1️⃣ Preséntate para entrar.\n"
            "Indica tu nombre o apodo, edad y de dónde eres. Además, envía un audio breve (5-15 segundos) saludando al grupo para que podamos ponerte voz. 😊\n\n"

            "2️⃣ Es obligatorio tener foto de perfil.\n"
            "No tiene que ser una foto tuya; puede ser cualquier imagen. Las cuentas sin foto podrán ser expulsadas por seguridad y confianza del grupo.\n\n"

            "3️⃣ Respeto ante todo.\n"
            "Nada de insultos, faltas de respeto, acoso ni comportamientos que generen mal ambiente.\n\n"

            "4️⃣ Prohibido:\n"
            "• Decir BRO y derivados.\n"
            "• Menores de 18 años.\n"
            "• Spam y publicidad.\n"
            "• Venta o promoción de contenido sexual o pornográfico.\n"
            "• Agregar al privado sin permiso.\n"
            "• Política, religión y temas que puedan generar conflicto.\n\n"

            "5️⃣ Este grupo está pensado para conocer gente, hacer amistades y pasar un buen rato.\n\n"

            "6️⃣ Si alguien te molesta o incumple las normas, avisa a un moderador o administrador.\n\n"

            "7️⃣ Participa.\n"
            "Este no es un grupo para quedarse de espectador. Cuanto más participes, mejor será la experiencia para todos.\n\n"

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

        if update.effective_user.id != RAQUEL_ID:
            await update.message.reply_text(
                "🚫 Solo Raquel puede iniciar un '¿Quién es más...?'."
            )
            return

        pregunta = random.choice(preguntas_quienesmas)

        quienesmas_activo[chat_id] = pregunta
        quienesmas_votos[chat_id] = {}

        await update.message.reply_text(
            f"👀 ¿Quién es más probable...?\n\n"
            f"{pregunta}\n\n"
            f"🗳️ Para votar, escribe únicamente el @usuario de la persona elegida.\n"
            f"Ejemplo: @usuario\n\n"
            f"✅ Solo cuentan mensajes que sean exactamente un @usuario.\n"
            f"🛑 Para cerrar la votación utiliza /cerrarquienes"
        )
        return
    if mensaje.startswith("!cerrarquienes") or mensaje.startswith("/cerrarquienes"):

        if update.effective_user.id != RAQUEL_ID:
            await update.message.reply_text(
                "🚫 Solo Raquel puede cerrar esta votación."
            )
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

    if chat_id in quienesmas_activo:
        texto_voto = update.message.text.strip()
        votante_id = update.effective_user.id

        if not texto_voto.startswith("@"):
            return

        if " " in texto_voto:
            return

        quienesmas_votos[chat_id][votante_id] = texto_voto

        return

    if mensaje.startswith("!miid") or mensaje.startswith("/miid"):
        await update.message.reply_text(
            f"Tu ID numérico de Telegram es: {update.effective_user.id}"
        )
        return

    if mensaje.startswith("!trivial") or mensaje.startswith("/trivial"):
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]
        await iniciar_trivial(update, context, chat_id, admin_ids)
        return

    if mensaje.startswith("!cancelartrivial") or mensaje.startswith("/cancelartrivial"):
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]
        await cancelar_trivial(update, chat_id, admin_ids)
        return

    if mensaje == "!rankingtrivial" or mensaje == "/rankingtrivial":
        await mostrar_ranking_trivial(update)
        return
    if (
        mensaje.startswith("/guardarficha ")
        or mensaje.startswith("!guardarficha ")
        or mensaje == "/guardarficha"
        or mensaje == "!guardarficha"
    ):
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        await guardar_ficha_admin(update, admin_ids)
        return

    if (
        mensaje == "/ficha"
        or mensaje == "!ficha"
        or mensaje.startswith("/ficha ")
        or mensaje.startswith("!ficha ")
    ):
        await mostrar_ficha(
            update,
            contador_mensajes,
            ultimo_mensaje_usuario
        )
        return

    if mensaje == "/borrarficha" or mensaje == "!borrarficha":
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        await borrar_ficha_admin(update, admin_ids)
        return

    if texto == "/test":
    await lanzar_test_manual(
        update,
        context,
        admin_ids
    )
    return
    if texto == "/activartests":
    await activar_tests(
        update,
        admin_ids
    )
    return
    if texto == "/desactivartests":
    await desactivar_tests(
        update,
        admin_ids
    )
    return
    if texto == "/cancelartest":
    await cancelar_test_admin(
        update,
        context,
        admin_ids
    )
    return

    if mensaje == "/activarcumples" or mensaje == "!activarcumples":
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        await activar_cumpleanos(update, admin_ids)
        return

    if mensaje == "/desactivarcumples" or mensaje == "!desactivarcumples":
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        await desactivar_cumpleanos(update, admin_ids)
        return

    if mensaje == "/cumples" or mensaje == "!cumples":
        await mostrar_proximos_cumpleanos(update)
        return

    if mensaje == "/cumplesmes" or mensaje == "!cumplesmes":
        await mostrar_cumpleanos_mes(update)
        return

    if mensaje == "/activartribunal" or mensaje == "!activartribunal":
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        await activar_tribunal(update, admin_ids)
        return

    if mensaje == "/desactivartribunal" or mensaje == "!desactivartribunal":
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        await desactivar_tribunal(update, admin_ids)
        return

    if mensaje == "/tribunal" or mensaje == "!tribunal":
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        await lanzar_tribunal_manual(
            update,
            context,
            admin_ids
        )
        return

    if mensaje == "/cancelartribunal" or mensaje == "!cancelartribunal":
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        await cancelar_tribunal(
            update,
            context,
            admin_ids
        )
        return

    if mensaje == "/nuevo" or mensaje == "!nuevo":
        await update.message.reply_text(
            "👋 ¡Bienvenido/a!\n\n"
            "Antes de participar, completa estos 4 pasos:\n\n"
            "📝 Preséntate indicando tu nombre o apodo, edad y de dónde eres.\n\n"
            "🖼️ Pon una foto de perfil (no hace falta que sea tu cara, cualquier imagen sirve).\n\n"
            "🎙️ Envía un audio breve (5-15 segundos) saludando al grupo.\n\n"
            "🤝 ¡Y ya está! Ahora solo queda participar y disfrutar del grupo. 😊"
        )
        return

    if mensaje == "/activarmisa" or mensaje == "!activarmisa":
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        await activar_misa(update, admin_ids)
        return

    if mensaje == "/desactivarmisa" or mensaje == "!desactivarmisa":
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        await desactivar_misa(update, admin_ids)
        return

    if mensaje == "/misa" or mensaje == "!misa":
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        await lanzar_misa_manual(
            update,
            context,
            admin_ids
        )
        return

    if mensaje == "/cancelarmisa" or mensaje == "!cancelarmisa":
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        await cancelar_misa(
            update,
            context,
            admin_ids
        )
        return
    saludos_automaticos = [
        "hola",
        "hola buenas",
        "buenos dias",
        "buenas tardes",
        "buenas noches"
    ]

    for trigger in respuestas:
        if trigger in mensaje:

            # Los saludos se responden solo 1 de cada 10 veces.
            if trigger in saludos_automaticos:
                if random.randint(1, 10) != 1:
                    return

            # El resto de respuestas automáticas salen solo 1 de cada 15 veces.
            else:
                if random.randint(1, 15) != 1:
                    return

            respuesta = random.choice(respuestas[trigger])
            await update.message.reply_text(respuesta)
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
MINUTOS_SILENCIO = 360
historial_chats = defaultdict(lambda: deque(maxlen=120))

COMANDOS_SOLO_ADMINS = {
    "quienhabla",
    "ranking",
    "fantasmas",
    "analiza",
    "normas",
    "sinpresentar",
    "vigilar",
    "recordatorio",
    "limpieza",
    "foto",
    "quienesmas",
    "cerrarquienes",
    "miid",
    "trivial",
    "cancelartrivial",
    "rankingtrivial",
    "corte",
    "guardarficha",
    "borrarficha",
    "activarcumples",
    "desactivarcumples",
    "activartribunal",
    "desactivartribunal",
    "tribunal",
    "cancelartribunal",
    "nuevo",
    "activarmisa",
    "desactivarmisa",
    "misa",
    "cancelarmisa",
    "burla"
}

RAQUEL_ID = 1176046170
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

app.add_handler(
    CallbackQueryHandler(
        botones_trivial,
        pattern=r"^trivia_"
    )
)

app.add_handler(
    CallbackQueryHandler(
        botones_tribunal,
        pattern=r"^tribunal_"
    )
)

print("Bot funcionando 😭")

app.job_queue.run_repeating(
    revisar_silencios,
    interval=600,
    first=600
)

app.job_queue.run_daily(
    revisar_cumpleanos,
    time=datetime.strptime("09:00", "%H:%M")
        .replace(tzinfo=ZoneInfo("Atlantic/Canary"))
        .timetz()
)
app.job_queue.run_daily(
    publicar_tribunal,
    time=datetime.strptime("20:30", "%H:%M")
        .replace(tzinfo=ZoneInfo("Atlantic/Canary"))
        .timetz()
)
app.job_queue.run_daily(
    aviso_misa_30,
    time=datetime.strptime("11:00", "%H:%M")
        .replace(tzinfo=ZoneInfo("Atlantic/Canary"))
        .timetz(),
    days=(0,)
)

app.job_queue.run_daily(
    aviso_misa_10,
    time=datetime.strptime("11:20", "%H:%M")
        .replace(tzinfo=ZoneInfo("Atlantic/Canary"))
        .timetz(),
    days=(0,)
)

app.job_queue.run_daily(
    aviso_misa_2,
    time=datetime.strptime("11:28", "%H:%M")
        .replace(tzinfo=ZoneInfo("Atlantic/Canary"))
        .timetz(),
    days=(0,)
)

app.job_queue.run_daily(
    publicar_misa_automatica,
    time=datetime.strptime("11:30", "%H:%M")
        .replace(tzinfo=ZoneInfo("Atlantic/Canary"))
        .timetz(),
    days=(0,)
)
app.add_handler(
    CallbackQueryHandler(
        botones_tests,
        pattern=r"^test_"
    )
)
app.job_queue.run_daily(
    publicar_test_automatico,
    time=datetime.strptime("20:00", "%H:%M")
        .replace(tzinfo=ZoneInfo("Atlantic/Canary"))
        .timetz(),
    days=(3,)
)
app.run_polling()
