from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
import random

from datetime import datetime, timedelta

TOKEN = "8996485412:AAEtyvBbfY4nuIBo1XTYe6lajs1f1Oigh5g"

respuestas = {
    "hola": [
        "Buenas criaturas 😭",
        "Por fin alguien rompe el silencio administrativo 💀",
        "Hola, ciudadano funcional 👀",
        "Se abre la sesión de terapia grupal 😭"
    ],

    "buenos dias": [
        "Buenos días, supervivientes de Telegram ☕",
        "Otro día más evitando red flags 😭",
        "Buenos días a los presentes y a los que solo observan 👀"
    ],

    "buenas tardes": [
        "Buenas tardes, habitantes del caos 😭",
        "La productividad murió, pero nosotros seguimos 💀"
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

    "jajaj": [
        "Me alegra entreteneros 😭",
        "Risas detectadas. Seguimos operativos 💀"
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

    "ola": [
        "El espíritu del 2012 vive 😭",
        "K ase criatura 💀"
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
    mensaje = update.message.text.lower()

    chat_id = update.effective_chat.id
    ultima_actividad[chat_id] = datetime.now()

    for trigger in respuestas:
        if trigger in mensaje:
            respuesta = random.choice(respuestas[trigger])
            await update.message.reply_text(respuesta)

    if random.randint(1, 20) == 1:
        await update.message.reply_text(random.choice(preguntas_random))

    if mensaje == "!pregunta":
        await update.message.reply_text(random.choice(preguntas))

    if mensaje == "!batalla":
        await update.message.reply_text(random.choice(batallas))

    if mensaje == "!confesion":
        await update.message.reply_text(random.choice(confesiones))

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
   
ultima_actividad = {}
ultimo_empujon = {}

MINUTOS_SILENCIO = 45

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

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

print("Bot funcionando 😭")
app.job_queue.run_repeating(revisar_silencios, interval=600, first=600)
app.run_polling()
