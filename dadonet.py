import random

SALSEO = [
    "¿Quién del grupo te cayó mejor desde el primer día?",
    "¿Quién del grupo te cayó peor al principio y ahora te cae mejor?",
    "¿Quién te cayó bien al principio y ahora te genera más dudas?",
    "¿Quién del grupo crees que habla por privado con más gente de la que reconoce?",
    "¿Quién crees que se hace más el inocente de lo que realmente es?",
    "¿Quién del grupo te genera más curiosidad aunque apenas hayas hablado con esa persona?",
    "¿Con quién del grupo crees que tendrías una conversación de horas sin aburrirte?",
    "¿Quién del grupo crees que podría sorprenderte muchísimo en persona?",
    "¿Quién crees que tiene una personalidad muy distinta por privado que en el grupo?",
    "¿Quién del grupo crees que sabe más salseos de los que cuenta?",
    "¿Quién crees que observa mucho más de lo que participa?",
    "¿Quién del grupo crees que tiene más facilidad para ligar sin proponérselo?",
    "¿Quién crees que tiene más gente detrás de lo que aparenta?",
    "¿Quién del grupo sería tu compañero/a perfecto/a para una noche de fiesta?",
    "¿Con quién del grupo te irías de viaje un fin de semana sin conocerlo mucho más?",
    "¿Quién crees que sería capaz de desaparecer del grupo y volver un mes después como si nada?",
    "¿Quién del grupo crees que se mete en más líos sentimentales?",
    "¿Quién crees que podría acabar emparejado con alguien del grupo?",
    "¿Quién del grupo crees que tiene más paciencia para aguantar dramas?",
    "¿Quién sería la peor persona para confiarle un secreto pequeño?",
    "¿Quién del grupo te parece más difícil de conocer de verdad?",
    "¿Quién crees que tiene más doble vida entre lo que cuenta aquí y su vida real?",
    "¿Quién del grupo crees que es más celoso/a de lo que reconoce?",
    "¿Quién crees que se engancha emocionalmente más rápido?",
    "¿Quién del grupo crees que tarda menos en cansarse de alguien?",
    "¿Quién crees que tiene más posibilidades de enamorarse de alguien del grupo?",
    "¿Quién del grupo crees que podría tener una relación secreta y nadie se enteraría?",
    "¿Quién te parece más probable que haya cotilleado el perfil entero de alguien del grupo?",
    "¿Quién crees que borra mensajes después de mandarlos porque se arrepiente?",
    "¿Quién del grupo sería capaz de montar una película mental por un simple 'visto'?",
    "¿Quién crees que más disimula cuando alguien le gusta?",
    "¿Quién del grupo crees que se pica más cuando le llevan la contraria?",
    "¿Quién crees que tendría más éxito organizando una quedada del grupo?",
    "¿Quién del grupo crees que sería más divertido/a de conocer cara a cara?",
    "¿Quién crees que podría acabar siendo tu mejor amigo/a de aquí?",
    "¿A quién del grupo le preguntarías primero si quisieras enterarte de un salseo?",
]

SIN_FILTRO = [
    "¿Quién del grupo te atrae más físicamente?",
    "¿A quién del grupo besarías si tuvieras que elegir ahora mismo?",
    "¿Con quién del grupo crees que tendrías más química en persona?",
    "¿Con quién del grupo tendrías una cita solo por curiosidad?",
    "¿Quién del grupo te parece más peligroso/a sentimentalmente?",
    "¿Quién crees que sería peor pareja?",
    "¿Quién crees que sería mejor pareja?",
    "¿Quién del grupo crees que rompería más corazones?",
    "¿Con quién del grupo jamás tendrías nada aunque te lo pusieran facilísimo?",
    "¿Quién crees que está más bueno/a de lo que enseñan sus fotos?",
    "¿Quién del grupo te genera más curiosidad sexual?",
    "¿Quién crees que sería mejor amante?",
    "¿Quién crees que sería peor amante?",
    "¿Con quién del grupo te liarías una noche sabiendo que al día siguiente no pasaría nada?",
    "¿Con quién del grupo no te importaría que surgiera algo inesperado?",
    "¿Quién del grupo crees que podría hacerte perder la cabeza?",
    "¿A quién del grupo bloquearías durante 24 horas solo por tocar los cojones?",
    "¿Quién del grupo te parece más probable que se haya fijado en alguien y no lo reconozca?",
    "¿Quién crees que está tonteando con alguien del grupo aunque diga que no?",
    "¿A quién del grupo le darías una oportunidad si te pidiera una cita?",
    "¿Quién del grupo te parece más probable que tenga un crush secreto?",
    "¿Quién crees que tendría más posibilidades contigo si se lo propusiera?",
    "¿Quién del grupo te parece más probable que ligue por mensaje privado?",
    "¿Quién crees que puede ser más intenso/a cuando le gusta alguien?",
    "¿Quién del grupo crees que se enamora peor?",
    "¿Quién crees que tarda menos en sustituir a una persona cuando una relación termina?",
    "¿Quién del grupo crees que volvería con un ex aunque jurara que jamás lo haría?",
    "¿Quién te parece más probable que haya enviado un mensaje borracho/a y se arrepintiera al día siguiente?",
    "¿Quién crees que sería capaz de tener dos conversaciones románticas abiertas al mismo tiempo?",
    "¿Quién del grupo crees que tiene más posibilidades de estar hablando con alguien del grupo por privado ahora mismo?",
    "¿A quién del grupo te costaría más decirle que no si se lanzara contigo?",
    "¿Quién del grupo te parece más atractivo/a por personalidad que por físico?",
    "¿Quién del grupo te parece más atractivo/a físicamente que por personalidad?",
    "¿Quién crees que podría gustarte mucho más después de conocerlo en persona?",
    "¿Quién crees que podría decepcionarte más al conocerlo en persona?",
    "¿Quién del grupo crees que tiene más posibilidades de ser tóxico/a en pareja?",
    "¿Quién crees que sería más posesivo/a?",
    "¿Quién crees que llevaría peor que su pareja tuviera mucha relación con otras personas del grupo?",
    "¿Quién crees que sería capaz de mirar el móvil de su pareja?",
    "¿Quién del grupo crees que perdonaría una infidelidad?",
    "¿Quién crees que jamás perdonaría una infidelidad?",
    "¿Quién del grupo crees que podría ser infiel y conseguir que nadie se enterara?",
    "¿Quién del grupo crees que tiene más secretos sentimentales?",
    "¿Con quién del grupo tendrías más miedo de engancharte emocionalmente?",
    "¿A quién del grupo te gustaría conocer mejor aunque nunca se lo hayas dicho?",
    "¿Quién del grupo te ha sorprendido para bien últimamente?",
    "¿Quién del grupo te ha decepcionado un poco últimamente?",
    "¿Quién crees que tiene una opinión sobre ti que nunca se atrevería a decirte?",
    "¿De quién del grupo te gustaría saber qué piensa realmente de ti?",
    "¿Quién crees que te juzgó mal cuando entraste al grupo?",
    "¿Quién del grupo crees que te conoce menos de lo que piensa?",
    "¿Quién del grupo crees que sabe exactamente cómo picarte?",
    "¿Quién podría hacerte enfadar más rápido?",
    "¿Con quién del grupo sería más probable que acabaras discutiendo y reconciliándote el mismo día?",
    "¿Quién crees que sería capaz de hacerse el/la duro/a y luego pillarse muchísimo?",
    "¿Quién del grupo crees que tiene más miedo al compromiso?",
    "¿Quién crees que tendría una relación más caótica?",
    "¿Quién del grupo crees que sería el primero en tener algo con otra persona del grupo?",
    "¿Quién te parece que está más acostumbrado/a a salirse con la suya?",
    "¿Quién del grupo crees que tiene más facilidad para manipular una situación a su favor?",
    "¿Quién crees que sería capaz de negar hasta la muerte que alguien le gusta aunque fuera evidente?",
]

BOMBA = [
    "Si tuvieras que acostarte con una persona del grupo, ¿a quién elegirías?",
    "Si tuvieras que besar a dos personas del grupo esta noche, ¿quiénes serían?",
    "¿Con quién del grupo tendrías sexo y con quién jamás aunque fueras la última persona del planeta?",
    "¿Quién del grupo crees que te atraería más si lo tuvieras delante ahora mismo?",
    "Si mañana despertaras en la cama con alguien del grupo, ¿con quién preferirías que fuera?",
    "¿A quién del grupo mandarías un mensaje de 'ven' a las tres de la mañana?",
    "¿Quién del grupo crees que tendría más posibilidades de hacerte ser infiel?",
    "¿Con quién del grupo tendrías una aventura que nadie pudiera descubrir?",
    "¿Quién del grupo crees que podría hacerte olvidar a alguien que todavía te importa?",
    "¿A quién del grupo le aceptarías una proposición indecente sin pensarlo demasiado?",
    "Si tuvieras que elegir pareja dentro del grupo durante un año entero, ¿a quién elegirías?",
    "¿A quién del grupo elegirías para una noche y a quién para una relación?",
    "¿Quién del grupo te parece demasiado atractivo/a como para ser buena idea?",
    "¿Quién crees que podría acabar siendo tu peor decisión sentimental?",
    "¿Con quién del grupo crees que habría más tensión sexual si os vierais en persona?",
    "Si pudieras leer un solo chat privado de alguien del grupo, ¿de quién sería?",
    "¿A quién del grupo jamás le dejarías leer tus conversaciones privadas?",
    "Si supieras que alguien del grupo está pillado por ti, ¿quién te gustaría que fuera?",
    "¿Quién del grupo te dolería más descubrir que habla mal de ti por privado?",
    "¿A quién del grupo eliminarías definitivamente si tuvieras que elegir a una persona?",
    "¿Quién del grupo crees que esconde la opinión más fuerte sobre otra persona del grupo?",
    "Di una persona del grupo con la que tendrías algo y una con la que ni de coña.",
    "¿Quién del grupo crees que tiene más posibilidades de acabar teniendo sexo con otra persona del grupo?",
    "¿Quién del grupo sería tu elección si te dijeran: 'o te lías con esta persona o abandonas el grupo'?",
    "Si esta noche hubiera una fiesta privada solo con gente del grupo, ¿con quién crees que acabarías tonteando?",
]

CATEGORIAS = {
    "🟡 SALSEO": SALSEO,
    "🔴 SIN FILTRO": SIN_FILTRO,
    "💣 BOMBA": BOMBA,
}

PESOS = {
    "🟡 SALSEO": 30,
    "🔴 SIN FILTRO": 50,
    "💣 BOMBA": 20,
}

ULTIMAS_A_EVITAR = 20

def _elegir_pregunta(context):
    categorias = list(CATEGORIAS.keys())
    pesos = [PESOS[c] for c in categorias]
    categoria = random.choices(categorias, weights=pesos, k=1)[0]

    usadas = context.chat_data.setdefault("dadonet_ultimas", [])
    disponibles = [p for p in CATEGORIAS[categoria] if p not in usadas]

    if not disponibles:
        disponibles = CATEGORIAS[categoria][:]

    pregunta = random.choice(disponibles)

    usadas.append(pregunta)
    if len(usadas) > ULTIMAS_A_EVITAR:
        del usadas[:-ULTIMAS_A_EVITAR]

    return categoria, pregunta

async def dadonet(update, context):
    categoria, pregunta = _elegir_pregunta(context)

    texto = (
        f"🎲 DADONET\n\n"
        f"{categoria}\n\n"
        f"{pregunta}\n\n"
        f"🎲 1–3 → Elige quién responde 😈\n"
        f"🎲 4–6 → Te toca responder a ti ☠️"
    )

    await update.message.reply_text(texto)
