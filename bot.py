from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
import random

TOKEN = "8996485412:AAEtyvBbfY4nuIBo1XTYe6lajs1f1Oigh5g"

respuestas = {
    "hola": [
        "Por fin alguien rompe el silencio administrativo 😭",
        "Milagro histórico: alguien ha hablado 🙌"
    ],
    "tinder": [
        "🚨 trauma detectado.",
        "Aquí intentamos recuperarnos de eso 😭"
    ],
    "me voy": [
        "Otro caído en combate social 😔",
        "No soportó la interacción humana 💀"
    ]
}

preguntas_random = [
    "Pregunta seria: ¿qué red flag os hace salir corriendo? 😭",
    "Confesión nocturna: decid algo rarísimo que hacéis.",
    "¿Cuál ha sido vuestro evento canónico de internet? 💀"
]

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text.lower()

    for trigger in respuestas:
        if trigger in mensaje:
            respuesta = random.choice(respuestas[trigger])
            await update.message.reply_text(respuesta)

    if random.randint(1, 40) == 1:
        await update.message.reply_text(random.choice(preguntas_random))

app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

print("Bot funcionando 😭")

app.run_polling()
