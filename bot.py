from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
import random

from datetime import datetime, timedelta
from collections import defaultdict, deque, Counter
from openai import OpenAI
import os

TOKEN = "8996485412:AAEtyvBbfY4nuIBo1XTYe6lajs1f1Oigh5g"
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

    "me voy": [
        "Otro caído en combate social 😔",
        "No soportó la interacción humana 💀",
        "Duró menos que una conversación en Tinder 😭"
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

for trigger in respuestas:
        if trigger in mensaje:
            respuesta = random.choice(respuestas[trigger])
            await update.message.reply_text(respuesta)
            return

if random.randint(1, 300) == 1:
        await update.message.reply_text(random.choice(preguntas_random))

if mensaje.startswith("!pregunta") or mensaje.startswith("/pregunta"):
        await update.message.reply_text(random.choice(preguntas))

if mensaje.startswith("!batalla") or mensaje.startswith("/batalla"):
        await update.message.reply_text(random.choice(batallas))

if mensaje.startswith("!confesion") or mensaje.startswith("/confesion"):
        await update.message.reply_text(random.choice(confesiones))
if mensaje in ["!corte", "/corte"]:
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        if update.effective_user.id not in admin_ids:
            await update.message.reply_text("Este botón rojo solo lo pueden pulsar los admins 😭")
            

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

MINUTOS_SILENCIO = 45
historial_chats = defaultdict(lambda: deque(maxlen=120))
contador_mensajes = {}
ultimo_mensaje_usuario = {}
nombres_usuarios = {}
usuarios_presentados = {}
mensajes_usuario = {}
async def revisar_silencios(context: ContextTypes.DEFAULT_TYPE):
    ahora = datetime.now()

    for chat_id, ultima in list(ultima_actividad.items()):
        tiempo_silencio = ahora - ultima
        ultimo_aviso = ultimo_empujon.get(chat_id)

        if tiempo_silencio >= timedelta(minutes=MINUTOS_SILENCIO):
            if not ultimo_aviso or ahora - ultimo_aviso >= timedelta(minutes=MINUTOS_SILENCIO):
                pregunta = random.choice(preguntas_random)
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"El grupo lleva un rato demasiado tranquilo 😭\n\n{pregunta}"
                )
                ultimo_empujon[chat_id] = ahora
app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, responder))

print("Bot funcionando 😭")
app.job_queue.run_repeating(revisar_silencios, interval=600, first=600)
app.run_polling()
