TESTS = [
    {
        "id": "comensal",
        "categoria": "🍝 Gastronomía",
        "titulo": "¿Qué tipo de comensal eres?",
        "descripcion": "Descubre cómo te comportas cuando hay una carta delante.",
        "perfiles": {
            "clasico": {
                "nombre": "🍲 Comensal clásico",
                "texto": "Tú no necesitas veinte ingredientes ni una explicación de cinco minutos. Sabes lo que te gusta, vuelves a ello y rara vez te arrepientes."
            },
            "aventurero": {
                "nombre": "🌶️ Comensal aventurero",
                "texto": "Lees la carta completa, preguntas qué es lo más raro y, si nadie se atreve a pedirlo, tú ya lo has elegido."
            },
            "gourmet": {
                "nombre": "🍷 Sibarita gastronómico",
                "texto": "Te importa el producto, el punto de cocción, la presentación y hasta el pan. Comer es un plan serio y tú has venido a disfrutarlo."
            },
            "practico": {
                "nombre": "🍟 Comensal práctico",
                "texto": "Quieres comer bien, rápido y sin convertir la cena en una oposición. Si está rico y llena, misión cumplida."
            }
        },
        "preguntas": [
            {
                "texto": "Te dan una carta enorme. ¿Qué haces?",
                "opciones": [
                    {"texto": "Busco mi plato de siempre", "perfil": "clasico"},
                    {"texto": "Elijo lo que no conozco", "perfil": "aventurero"},
                    {"texto": "Pregunto por el producto y la elaboración", "perfil": "gourmet"},
                    {"texto": "Voy directo a lo más sencillo", "perfil": "practico"}
                ]
            },
            {
                "texto": "El camarero recomienda algo poco habitual.",
                "opciones": [
                    {"texto": "Prefiero no arriesgar", "perfil": "clasico"},
                    {"texto": "Eso es exactamente lo que quiero", "perfil": "aventurero"},
                    {"texto": "Pregunto por ingredientes y maridaje", "perfil": "gourmet"},
                    {"texto": "¿Tarda mucho?", "perfil": "practico"}
                ]
            },
            {
                "texto": "Tu acompañamiento ideal es...",
                "opciones": [
                    {"texto": "Papas, arroz o ensalada de toda la vida", "perfil": "clasico"},
                    {"texto": "Algo picante o desconocido", "perfil": "aventurero"},
                    {"texto": "Lo que mejor equilibre el plato", "perfil": "gourmet"},
                    {"texto": "Lo que venga incluido", "perfil": "practico"}
                ]
            },
            {
                "texto": "Cuando compartís comida...",
                "opciones": [
                    {"texto": "Pido algo que guste a todos", "perfil": "clasico"},
                    {"texto": "Propongo probar varias cosas nuevas", "perfil": "aventurero"},
                    {"texto": "Organizo el orden de los platos", "perfil": "gourmet"},
                    {"texto": "Como de todo sin complicarme", "perfil": "practico"}
                ]
            },
            {
                "texto": "Tu mayor miedo en un restaurante es...",
                "opciones": [
                    {"texto": "Que cambien la receta de siempre", "perfil": "clasico"},
                    {"texto": "Que todo sea demasiado convencional", "perfil": "aventurero"},
                    {"texto": "Que el producto sea mediocre", "perfil": "gourmet"},
                    {"texto": "Que la comida tarde una eternidad", "perfil": "practico"}
                ]
            },
            {
                "texto": "El postre...",
                "opciones": [
                    {"texto": "Uno conocido y seguro", "perfil": "clasico"},
                    {"texto": "El más raro de la carta", "perfil": "aventurero"},
                    {"texto": "Solo si merece realmente la pena", "perfil": "gourmet"},
                    {"texto": "Café y seguimos", "perfil": "practico"}
                ]
            }
        ]
    },
    {
        "id": "plato",
        "categoria": "🍝 Gastronomía",
        "titulo": "¿Qué plato representa tu personalidad?",
        "descripcion": "Tu manera de ser servida en un plato.",
        "perfiles": {
            "paella": {
                "nombre": "🥘 Paella",
                "texto": "Eres social, generas reunión y funcionas mejor cuando hay gente alrededor. Tienes carácter y no admites que cualquiera te prepare."
            },
            "pizza": {
                "nombre": "🍕 Pizza",
                "texto": "Fácil de querer, adaptable y capaz de encajar en casi cualquier plan. Pareces simple, pero tienes muchas versiones."
            },
            "sushi": {
                "nombre": "🍣 Sushi",
                "texto": "Cuidadoso, detallista y selectivo. No todo el mundo te entiende al principio, pero quien conecta contigo repite."
            },
            "tacos": {
                "nombre": "🌮 Tacos",
                "texto": "Intenso, divertido y un poco caótico. Contigo siempre pasan cosas y rara vez hay una noche aburrida."
            }
        },
        "preguntas": [
            {
                "texto": "En un grupo nuevo tú...",
                "opciones": [
                    {"texto": "Intentas unir a todo el mundo", "perfil": "paella"},
                    {"texto": "Te adaptas enseguida", "perfil": "pizza"},
                    {"texto": "Observas antes de abrirte", "perfil": "sushi"},
                    {"texto": "Entras con energía", "perfil": "tacos"}
                ]
            },
            {
                "texto": "Tu plan favorito es...",
                "opciones": [
                    {"texto": "Comida larga con amigos", "perfil": "paella"},
                    {"texto": "Algo sencillo que apetezca a todos", "perfil": "pizza"},
                    {"texto": "Un sitio especial y tranquilo", "perfil": "sushi"},
                    {"texto": "Improvisar y ver qué pasa", "perfil": "tacos"}
                ]
            },
            {
                "texto": "Cuando surge un problema...",
                "opciones": [
                    {"texto": "Busco una solución conjunta", "perfil": "paella"},
                    {"texto": "Me adapto a lo que haya", "perfil": "pizza"},
                    {"texto": "Analizo cada detalle", "perfil": "sushi"},
                    {"texto": "Actúo rápido y con intensidad", "perfil": "tacos"}
                ]
            },
            {
                "texto": "Tu estilo personal es...",
                "opciones": [
                    {"texto": "Tradicional con carácter", "perfil": "paella"},
                    {"texto": "Cómodo y versátil", "perfil": "pizza"},
                    {"texto": "Cuidado y minimalista", "perfil": "sushi"},
                    {"texto": "Llamativo y espontáneo", "perfil": "tacos"}
                ]
            },
            {
                "texto": "La gente te busca porque...",
                "opciones": [
                    {"texto": "Haces sentir parte del grupo", "perfil": "paella"},
                    {"texto": "Contigo todo es fácil", "perfil": "pizza"},
                    {"texto": "Sabes escuchar y observar", "perfil": "sushi"},
                    {"texto": "Levantas cualquier ambiente", "perfil": "tacos"}
                ]
            },
            {
                "texto": "Tu defecto más probable es...",
                "opciones": [
                    {"texto": "Querer organizar a todos", "perfil": "paella"},
                    {"texto": "Decir que sí a demasiadas cosas", "perfil": "pizza"},
                    {"texto": "Ser demasiado selectivo", "perfil": "sushi"},
                    {"texto": "Pasarte de intensidad", "perfil": "tacos"}
                ]
            }
        ]
    },
    {
        "id": "personaje_cine",
        "categoria": "🎬 Cine",
        "titulo": "¿Qué papel tendrías en una película?",
        "descripcion": "Toda película necesita protagonistas, villanos y gente que sobreviva al desastre.",
        "perfiles": {
            "protagonista": {
                "nombre": "🎬 Protagonista caótico",
                "texto": "La historia gira a tu alrededor aunque nadie te haya dado permiso. Te metes en problemas, improvisas y, de alguna manera, llegas al final."
            },
            "villano": {
                "nombre": "🖤 Villano incomprendido",
                "texto": "Tienes presencia, argumentos y una paciencia limitada. Probablemente tu plan no era tan malo; lo explicaste con demasiada intensidad."
            },
            "secundario": {
                "nombre": "✨ Secundario que roba escenas",
                "texto": "No necesitas llevar el peso de la trama. Apareces, dices la mejor frase y todo el mundo termina hablando de ti."
            },
            "superviviente": {
                "nombre": "🔦 Superviviente sensato",
                "texto": "Mientras los demás investigan el ruido del sótano, tú ya has llamado a emergencias y estás a tres calles de distancia."
            }
        },
        "preguntas": [
            {
                "texto": "Se oye un ruido extraño en una casa abandonada.",
                "opciones": [
                    {"texto": "Entro a investigar", "perfil": "protagonista"},
                    {"texto": "Espero dentro; seguramente era mi plan", "perfil": "villano"},
                    {"texto": "Hago un comentario brillante y sigo al grupo", "perfil": "secundario"},
                    {"texto": "Me voy inmediatamente", "perfil": "superviviente"}
                ]
            },
            {
                "texto": "En una discusión importante...",
                "opciones": [
                    {"texto": "Doy un discurso improvisado", "perfil": "protagonista"},
                    {"texto": "Explico por qué todos están equivocados", "perfil": "villano"},
                    {"texto": "Suelto la frase que se hace meme", "perfil": "secundario"},
                    {"texto": "Busco la salida más segura", "perfil": "superviviente"}
                ]
            },
            {
                "texto": "Tu entrada en escena sería...",
                "opciones": [
                    {"texto": "Corriendo y con un problema detrás", "perfil": "protagonista"},
                    {"texto": "Lenta, elegante y con música inquietante", "perfil": "villano"},
                    {"texto": "Con una frase inolvidable", "perfil": "secundario"},
                    {"texto": "Llegando a tiempo y con un plan", "perfil": "superviviente"}
                ]
            },
            {
                "texto": "El grupo toma una mala decisión.",
                "opciones": [
                    {"texto": "La lidero sin querer", "perfil": "protagonista"},
                    {"texto": "La aprovecho a mi favor", "perfil": "villano"},
                    {"texto": "Lo aviso con humor", "perfil": "secundario"},
                    {"texto": "No participo", "perfil": "superviviente"}
                ]
            },
            {
                "texto": "Tu frase de película sería...",
                "opciones": [
                    {"texto": "Tengo una idea", "perfil": "protagonista"},
                    {"texto": "Esto era inevitable", "perfil": "villano"},
                    {"texto": "Yo solo vine por la comida", "perfil": "secundario"},
                    {"texto": "Os dije que no entráramos", "perfil": "superviviente"}
                ]
            },
            {
                "texto": "En los créditos finales...",
                "opciones": [
                    {"texto": "Salgo en todas las escenas extra", "perfil": "protagonista"},
                    {"texto": "Se descubre que sigo vivo", "perfil": "villano"},
                    {"texto": "Tengo el mejor blooper", "perfil": "secundario"},
                    {"texto": "Ya estoy en casa durmiendo", "perfil": "superviviente"}
                ]
            }
        ]
    },
    {
        "id": "genero_cine",
        "categoria": "🎬 Cine",
        "titulo": "¿Qué género cinematográfico eres?",
        "descripcion": "Tu vida también tiene banda sonora, giros y escenas innecesarias.",
        "perfiles": {
            "comedia": {
                "nombre": "😂 Comedia",
                "texto": "Conviertes los problemas en anécdotas y las situaciones incómodas en material. No siempre solucionas el caos, pero lo haces entretenido."
            },
            "drama": {
                "nombre": "🎭 Drama",
                "texto": "Sientes fuerte, recuerdas todo y sabes darle importancia hasta a un punto suspensivo. Tu vida tiene primeros planos."
            },
            "aventura": {
                "nombre": "🗺️ Aventura",
                "texto": "Te mueve la curiosidad. Necesitas cambios, planes y alguna historia que contar cuando vuelvas."
            },
            "misterio": {
                "nombre": "🕵️ Misterio",
                "texto": "Observas, conectas detalles y no sueltas toda la información de golpe. Contigo siempre parece que hay una segunda lectura."
            }
        },
        "preguntas": [
            {
                "texto": "Un plan se cancela en el último momento.",
                "opciones": [
                    {"texto": "Me río y monto otro", "perfil": "comedia"},
                    {"texto": "Me afecta más de lo que admitiré", "perfil": "drama"},
                    {"texto": "Aprovecho para improvisar algo distinto", "perfil": "aventura"},
                    {"texto": "Quiero saber el verdadero motivo", "perfil": "misterio"}
                ]
            },
            {
                "texto": "Tu conversación favorita tiene...",
                "opciones": [
                    {"texto": "Bromas y anécdotas", "perfil": "comedia"},
                    {"texto": "Emoción y confesiones", "perfil": "drama"},
                    {"texto": "Planes e ideas nuevas", "perfil": "aventura"},
                    {"texto": "Preguntas y teorías", "perfil": "misterio"}
                ]
            },
            {
                "texto": "Cuando conoces a alguien...",
                "opciones": [
                    {"texto": "Busco hacerle reír", "perfil": "comedia"},
                    {"texto": "Me fijo en la conexión emocional", "perfil": "drama"},
                    {"texto": "Propongo hacer algo", "perfil": "aventura"},
                    {"texto": "Observo antes de confiar", "perfil": "misterio"}
                ]
            },
            {
                "texto": "Tu fin de semana ideal...",
                "opciones": [
                    {"texto": "Gente divertida y cero solemnidad", "perfil": "comedia"},
                    {"texto": "Un plan especial con significado", "perfil": "drama"},
                    {"texto": "Una escapada improvisada", "perfil": "aventura"},
                    {"texto": "Algo tranquilo y con conversación", "perfil": "misterio"}
                ]
            },
            {
                "texto": "Tu mayor talento es...",
                "opciones": [
                    {"texto": "Quitar tensión", "perfil": "comedia"},
                    {"texto": "Entender emociones", "perfil": "drama"},
                    {"texto": "Mover a la gente", "perfil": "aventura"},
                    {"texto": "Detectar lo que no se dice", "perfil": "misterio"}
                ]
            },
            {
                "texto": "Una palabra para tu vida:",
                "opciones": [
                    {"texto": "Anécdota", "perfil": "comedia"},
                    {"texto": "Intensidad", "perfil": "drama"},
                    {"texto": "Movimiento", "perfil": "aventura"},
                    {"texto": "Intriga", "perfil": "misterio"}
                ]
            }
        ]
    },
    {
        "id": "serie",
        "categoria": "📺 Series",
        "titulo": "¿Qué personaje eres dentro de una serie?",
        "descripcion": "En cada temporada hay quien manda, quien observa y quien provoca el giro.",
        "perfiles": {
            "lider": {
                "nombre": "👑 Líder del reparto",
                "texto": "Tomas decisiones, organizas y acabas cargando con problemas que ni siquiera eran tuyos."
            },
            "cerebro": {
                "nombre": "🧠 Cerebro estratégico",
                "texto": "Ves conexiones, piensas varios pasos por delante y rara vez haces algo sin haber calculado el efecto."
            },
            "corazon": {
                "nombre": "❤️ Corazón del grupo",
                "texto": "Eres quien escucha, une y recuerda que detrás del drama hay personas. Sin ti, el reparto se rompe."
            },
            "caos": {
                "nombre": "🔥 Agente del caos",
                "texto": "Quizá no solucionas la trama, pero garantizas que haya trama. Contigo nunca existe una temporada de relleno."
            }
        },
        "preguntas": [
            {
                "texto": "El grupo tiene un problema.",
                "opciones": [
                    {"texto": "Reparto tareas", "perfil": "lider"},
                    {"texto": "Diseño el plan", "perfil": "cerebro"},
                    {"texto": "Calmo a todos", "perfil": "corazon"},
                    {"texto": "Propongo algo arriesgado", "perfil": "caos"}
                ]
            },
            {
                "texto": "Tu secreto narrativo sería...",
                "opciones": [
                    {"texto": "Llevo tiempo protegiendo al grupo", "perfil": "lider"},
                    {"texto": "Sabía la verdad desde el principio", "perfil": "cerebro"},
                    {"texto": "He perdonado algo importante", "perfil": "corazon"},
                    {"texto": "Yo provoqué el problema inicial", "perfil": "caos"}
                ]
            },
            {
                "texto": "Cuando dos amigos discuten...",
                "opciones": [
                    {"texto": "Pongo orden", "perfil": "lider"},
                    {"texto": "Analizo quién tiene razón", "perfil": "cerebro"},
                    {"texto": "Intento reconciliarlos", "perfil": "corazon"},
                    {"texto": "Pregunto qué pasó exactamente", "perfil": "caos"}
                ]
            },
            {
                "texto": "Tu escena característica sería...",
                "opciones": [
                    {"texto": "Un discurso que une al equipo", "perfil": "lider"},
                    {"texto": "Una revelación brillante", "perfil": "cerebro"},
                    {"texto": "Una conversación emocional", "perfil": "corazon"},
                    {"texto": "Una entrada que lo cambia todo", "perfil": "caos"}
                ]
            },
            {
                "texto": "En una misión tú llevas...",
                "opciones": [
                    {"texto": "La responsabilidad", "perfil": "lider"},
                    {"texto": "El mapa y el plan", "perfil": "cerebro"},
                    {"texto": "El botiquín", "perfil": "corazon"},
                    {"texto": "Algo que nadie pidió", "perfil": "caos"}
                ]
            },
            {
                "texto": "Tu final de temporada ideal:",
                "opciones": [
                    {"texto": "El grupo permanece unido", "perfil": "lider"},
                    {"texto": "Todo encaja", "perfil": "cerebro"},
                    {"texto": "Hay reconciliación", "perfil": "corazon"},
                    {"texto": "Un giro imposible", "perfil": "caos"}
                ]
            }
        ]
    },
    {
        "id": "energia_musical",
        "categoria": "🎵 Música",
        "titulo": "¿Qué energía musical transmites?",
        "descripcion": "No hace falta cantar bien para tener una energía sonora muy concreta.",
        "perfiles": {
            "pop": {
                "nombre": "✨ Pop magnético",
                "texto": "Accesible, expresivo y con facilidad para conectar. Tienes energía de estribillo que todo el mundo termina recordando."
            },
            "rock": {
                "nombre": "🎸 Rock emocional",
                "texto": "Directo, intenso y con carácter. No siempre buscas agradar, pero cuando conectas, conectas de verdad."
            },
            "indie": {
                "nombre": "🌙 Indie introspectivo",
                "texto": "Tienes mundo interior, detalles y una forma particular de ver lo cotidiano. No eres para todo el mundo, y eso te parece perfecto."
            },
            "latino": {
                "nombre": "🔥 Ritmo latino",
                "texto": "Social, cálido y difícil de ignorar. Levantas el ambiente y haces que incluso quien dijo que no iba a bailar termine moviéndose."
            }
        },
        "preguntas": [
            {
                "texto": "En una reunión tú...",
                "opciones": [
                    {"texto": "Conecto con casi todos", "perfil": "pop"},
                    {"texto": "Hablo claro y sin filtro", "perfil": "rock"},
                    {"texto": "Me quedo con una conversación profunda", "perfil": "indie"},
                    {"texto": "Animo el ambiente", "perfil": "latino"}
                ]
            },
            {
                "texto": "Tu forma de vestir suele ser...",
                "opciones": [
                    {"texto": "Actual y reconocible", "perfil": "pop"},
                    {"texto": "Con carácter", "perfil": "rock"},
                    {"texto": "Personal y poco obvia", "perfil": "indie"},
                    {"texto": "Viva y llamativa", "perfil": "latino"}
                ]
            },
            {
                "texto": "Cuando te enamoras...",
                "opciones": [
                    {"texto": "Lo cuento con ilusión", "perfil": "pop"},
                    {"texto": "Voy con todo", "perfil": "rock"},
                    {"texto": "Lo proceso en silencio", "perfil": "indie"},
                    {"texto": "Se me nota a kilómetros", "perfil": "latino"}
                ]
            },
            {
                "texto": "Tu defecto musical sería...",
                "opciones": [
                    {"texto": "Querer gustar demasiado", "perfil": "pop"},
                    {"texto": "Subir demasiado el volumen", "perfil": "rock"},
                    {"texto": "Complicarlo todo", "perfil": "indie"},
                    {"texto": "No saber estar quieto", "perfil": "latino"}
                ]
            },
            {
                "texto": "Tu lugar ideal para escuchar música:",
                "opciones": [
                    {"texto": "Un concierto lleno", "perfil": "pop"},
                    {"texto": "Una sala pequeña con potencia", "perfil": "rock"},
                    {"texto": "Auriculares y noche", "perfil": "indie"},
                    {"texto": "Una fiesta con gente", "perfil": "latino"}
                ]
            },
            {
                "texto": "Tu energía se resume en...",
                "opciones": [
                    {"texto": "Brillo", "perfil": "pop"},
                    {"texto": "Fuerza", "perfil": "rock"},
                    {"texto": "Profundidad", "perfil": "indie"},
                    {"texto": "Movimiento", "perfil": "latino"}
                ]
            }
        ]
    },
    {
        "id": "playlist",
        "categoria": "🎵 Música",
        "titulo": "¿Qué tipo de playlist eres?",
        "descripcion": "Tu personalidad convertida en una lista de reproducción.",
        "perfiles": {
            "fiesta": {
                "nombre": "🎉 Playlist de fiesta",
                "texto": "Tu función es levantar el ánimo. Eres energía, espontaneidad y canciones que todo el mundo termina cantando."
            },
            "nostalgia": {
                "nombre": "📼 Playlist nostálgica",
                "texto": "Guardas recuerdos en canciones. Una melodía puede devolverte a una época, una persona o una versión anterior de ti."
            },
            "concentracion": {
                "nombre": "🎧 Playlist de concentración",
                "texto": "Ordenado, constante y más profundo de lo que aparentas. Funcionas mejor cuando tienes tu espacio."
            },
            "aleatoria": {
                "nombre": "🔀 Playlist aleatoria",
                "texto": "Imprevisible y difícil de clasificar. Puedes pasar de una balada a un temazo absurdo sin dar explicaciones."
            }
        },
        "preguntas": [
            {
                "texto": "Un viaje largo necesita...",
                "opciones": [
                    {"texto": "Temazos para cantar", "perfil": "fiesta"},
                    {"texto": "Canciones de otra época", "perfil": "nostalgia"},
                    {"texto": "Música tranquila", "perfil": "concentracion"},
                    {"texto": "Todo mezclado", "perfil": "aleatoria"}
                ]
            },
            {
                "texto": "Cuando estás triste...",
                "opciones": [
                    {"texto": "Pongo algo que me levante", "perfil": "fiesta"},
                    {"texto": "Escucho canciones que me atraviesen", "perfil": "nostalgia"},
                    {"texto": "Busco calma", "perfil": "concentracion"},
                    {"texto": "Cambio de canción cada minuto", "perfil": "aleatoria"}
                ]
            },
            {
                "texto": "Tu habitación suele estar...",
                "opciones": [
                    {"texto": "Lista para recibir gente", "perfil": "fiesta"},
                    {"texto": "Llena de recuerdos", "perfil": "nostalgia"},
                    {"texto": "Ordenada para funcionar", "perfil": "concentracion"},
                    {"texto": "En un equilibrio cuestionable", "perfil": "aleatoria"}
                ]
            },
            {
                "texto": "Tus conversaciones cambian...",
                "opciones": [
                    {"texto": "Hacia la diversión", "perfil": "fiesta"},
                    {"texto": "Hacia recuerdos compartidos", "perfil": "nostalgia"},
                    {"texto": "Hacia temas concretos", "perfil": "concentracion"},
                    {"texto": "De tema sin aviso", "perfil": "aleatoria"}
                ]
            },
            {
                "texto": "La gente te describe como...",
                "opciones": [
                    {"texto": "Animado", "perfil": "fiesta"},
                    {"texto": "Sentimental", "perfil": "nostalgia"},
                    {"texto": "Centrado", "perfil": "concentracion"},
                    {"texto": "Imprevisible", "perfil": "aleatoria"}
                ]
            },
            {
                "texto": "Tu botón favorito sería...",
                "opciones": [
                    {"texto": "Subir volumen", "perfil": "fiesta"},
                    {"texto": "Repetir", "perfil": "nostalgia"},
                    {"texto": "Pausa", "perfil": "concentracion"},
                    {"texto": "Aleatorio", "perfil": "aleatoria"}
                ]
            }
        ]
    },
    {
        "id": "viajero",
        "categoria": "✈️ Viajes",
        "titulo": "¿Qué tipo de viajero eres?",
        "descripcion": "Hay quien lleva un itinerario y quien descubre el hotel al aterrizar.",
        "perfiles": {
            "organizado": {
                "nombre": "🗂️ Viajero organizado",
                "texto": "Reservas, horarios, mapas y plan B. Disfrutas más cuando sabes que todo está controlado."
            },
            "improvisado": {
                "nombre": "🎒 Viajero improvisado",
                "texto": "Decides sobre la marcha, cambias de rumbo y vuelves con historias que jamás habrían cabido en un itinerario."
            },
            "gastronomico": {
                "nombre": "🍜 Viajero gastronómico",
                "texto": "Tus recuerdos están asociados a platos, mercados y restaurantes. El monumento puede esperar; la reserva no."
            },
            "relajado": {
                "nombre": "🏖️ Viajero de descanso",
                "texto": "No viajas para agotarte. Buscas comodidad, buen clima y el noble arte de no mirar el reloj."
            }
        },
        "preguntas": [
            {
                "texto": "Antes del viaje...",
                "opciones": [
                    {"texto": "Tengo reservas y ruta", "perfil": "organizado"},
                    {"texto": "Compro el billete y ya veremos", "perfil": "improvisado"},
                    {"texto": "Investigo dónde comer", "perfil": "gastronomico"},
                    {"texto": "Miro hotel, piscina y descanso", "perfil": "relajado"}
                ]
            },
            {
                "texto": "Llegas a una ciudad nueva.",
                "opciones": [
                    {"texto": "Sigo mi itinerario", "perfil": "organizado"},
                    {"texto": "Camino sin rumbo", "perfil": "improvisado"},
                    {"texto": "Busco el mercado local", "perfil": "gastronomico"},
                    {"texto": "Dejo las cosas y descanso", "perfil": "relajado"}
                ]
            },
            {
                "texto": "Tu equipaje es...",
                "opciones": [
                    {"texto": "Completo y revisado", "perfil": "organizado"},
                    {"texto": "Lo básico y alguna cosa olvidada", "perfil": "improvisado"},
                    {"texto": "Con espacio para productos locales", "perfil": "gastronomico"},
                    {"texto": "Ligero y cómodo", "perfil": "relajado"}
                ]
            },
            {
                "texto": "Un cambio de planes...",
                "opciones": [
                    {"texto": "Me obliga a reorganizar", "perfil": "organizado"},
                    {"texto": "Me parece parte del viaje", "perfil": "improvisado"},
                    {"texto": "Mientras no afecte a la cena...", "perfil": "gastronomico"},
                    {"texto": "Si es para descansar más, perfecto", "perfil": "relajado"}
                ]
            },
            {
                "texto": "Tu foto típica es...",
                "opciones": [
                    {"texto": "Frente al lugar imprescindible", "perfil": "organizado"},
                    {"texto": "En un sitio que encontramos por casualidad", "perfil": "improvisado"},
                    {"texto": "Del plato antes de probarlo", "perfil": "gastronomico"},
                    {"texto": "Con vistas desde la tumbona", "perfil": "relajado"}
                ]
            },
            {
                "texto": "Vuelves del viaje con...",
                "opciones": [
                    {"texto": "Todo lo previsto cumplido", "perfil": "organizado"},
                    {"texto": "Una historia inesperada", "perfil": "improvisado"},
                    {"texto": "Recomendaciones de restaurantes", "perfil": "gastronomico"},
                    {"texto": "Energía recuperada", "perfil": "relajado"}
                ]
            }
        ]
    },
    {
        "id": "destino",
        "categoria": "✈️ Viajes",
        "titulo": "¿Qué destino encaja contigo?",
        "descripcion": "No es una recomendación turística: es una radiografía con maleta.",
        "perfiles": {
            "ciudad": {
                "nombre": "🏙️ Gran ciudad",
                "texto": "Necesitas movimiento, opciones y cosas pasando. Te alimentan la variedad, las conversaciones y los planes."
            },
            "naturaleza": {
                "nombre": "🌲 Naturaleza",
                "texto": "Buscas aire, espacio y silencio real. Tu batería se recarga lejos del ruido."
            },
            "costa": {
                "nombre": "🌊 Costa",
                "texto": "Eres de ritmos más suaves, luz y planes sin demasiada estructura. Cerca del mar todo parece colocarse."
            },
            "pueblo": {
                "nombre": "🏘️ Pueblo con encanto",
                "texto": "Te gustan los detalles, el trato cercano y los lugares con historia. No necesitas grandes estímulos para disfrutar."
            }
        },
        "preguntas": [
            {
                "texto": "Un día libre perfecto incluye...",
                "opciones": [
                    {"texto": "Varias cosas distintas", "perfil": "ciudad"},
                    {"texto": "Caminar al aire libre", "perfil": "naturaleza"},
                    {"texto": "Sol y agua", "perfil": "costa"},
                    {"texto": "Comer bien y pasear", "perfil": "pueblo"}
                ]
            },
            {
                "texto": "El sonido que prefieres:",
                "opciones": [
                    {"texto": "La ciudad en movimiento", "perfil": "ciudad"},
                    {"texto": "Viento y hojas", "perfil": "naturaleza"},
                    {"texto": "Olas", "perfil": "costa"},
                    {"texto": "Campanas y conversación", "perfil": "pueblo"}
                ]
            },
            {
                "texto": "Tu ritmo natural es...",
                "opciones": [
                    {"texto": "Rápido", "perfil": "ciudad"},
                    {"texto": "Constante", "perfil": "naturaleza"},
                    {"texto": "Flexible", "perfil": "costa"},
                    {"texto": "Tranquilo", "perfil": "pueblo"}
                ]
            },
            {
                "texto": "Te atrae más...",
                "opciones": [
                    {"texto": "La variedad", "perfil": "ciudad"},
                    {"texto": "La inmensidad", "perfil": "naturaleza"},
                    {"texto": "La libertad", "perfil": "costa"},
                    {"texto": "La autenticidad", "perfil": "pueblo"}
                ]
            },
            {
                "texto": "Tu alojamiento ideal:",
                "opciones": [
                    {"texto": "Hotel céntrico", "perfil": "ciudad"},
                    {"texto": "Cabaña", "perfil": "naturaleza"},
                    {"texto": "Apartamento frente al mar", "perfil": "costa"},
                    {"texto": "Casa rural", "perfil": "pueblo"}
                ]
            },
            {
                "texto": "Lo que más valoras de un lugar:",
                "opciones": [
                    {"texto": "Todo lo que ofrece", "perfil": "ciudad"},
                    {"texto": "Su paisaje", "perfil": "naturaleza"},
                    {"texto": "Su clima y luz", "perfil": "costa"},
                    {"texto": "Su gente e historia", "perfil": "pueblo"}
                ]
            }
        ]
    },
    {
        "id": "amigo",
        "categoria": "👥 Amistad",
        "titulo": "¿Qué tipo de amigo eres?",
        "descripcion": "En todo grupo hay quien escucha, quien organiza y quien aparece con una idea peligrosa.",
        "perfiles": {
            "confidente": {
                "nombre": "🤍 Confidente",
                "texto": "Escuchas sin convertirlo todo en ti. La gente sabe que puede contarte lo importante."
            },
            "organizador": {
                "nombre": "📅 Organizador",
                "texto": "Sin ti el grupo seguiría diciendo «tenemos que quedar» durante seis meses."
            },
            "animador": {
                "nombre": "🎉 Animador",
                "texto": "Detectas el bajón y haces algo al respecto. Eres energía social en forma humana."
            },
            "protector": {
                "nombre": "🛡️ Protector",
                "texto": "Estás pendiente, defiendes a los tuyos y recuerdas detalles que otros pasan por alto."
            }
        },
        "preguntas": [
            {
                "texto": "Un amigo está mal.",
                "opciones": [
                    {"texto": "Le escucho durante horas", "perfil": "confidente"},
                    {"texto": "Organizo algo para ayudar", "perfil": "organizador"},
                    {"texto": "Intento sacarle una sonrisa", "perfil": "animador"},
                    {"texto": "Me aseguro de que no esté solo", "perfil": "protector"}
                ]
            },
            {
                "texto": "El grupo lleva meses sin quedar.",
                "opciones": [
                    {"texto": "Pregunto cómo está cada uno", "perfil": "confidente"},
                    {"texto": "Pongo fecha y lugar", "perfil": "organizador"},
                    {"texto": "Mando un meme para reactivar", "perfil": "animador"},
                    {"texto": "Escribo a quien se ha aislado", "perfil": "protector"}
                ]
            },
            {
                "texto": "En una fiesta...",
                "opciones": [
                    {"texto": "Acabo en conversación profunda", "perfil": "confidente"},
                    {"texto": "Coordino al grupo", "perfil": "organizador"},
                    {"texto": "Levanto el ambiente", "perfil": "animador"},
                    {"texto": "Vigilo que todos vuelvan bien", "perfil": "protector"}
                ]
            },
            {
                "texto": "Tu móvil está lleno de...",
                "opciones": [
                    {"texto": "Audios importantes", "perfil": "confidente"},
                    {"texto": "Reservas y recordatorios", "perfil": "organizador"},
                    {"texto": "Memes", "perfil": "animador"},
                    {"texto": "Mensajes preguntando si llegaron", "perfil": "protector"}
                ]
            },
            {
                "texto": "Tu frase habitual:",
                "opciones": [
                    {"texto": "Cuéntame", "perfil": "confidente"},
                    {"texto": "He hecho una reserva", "perfil": "organizador"},
                    {"texto": "Tengo una idea", "perfil": "animador"},
                    {"texto": "Avísame cuando llegues", "perfil": "protector"}
                ]
            },
            {
                "texto": "Lo que aportas al grupo:",
                "opciones": [
                    {"texto": "Confianza", "perfil": "confidente"},
                    {"texto": "Movimiento", "perfil": "organizador"},
                    {"texto": "Alegría", "perfil": "animador"},
                    {"texto": "Seguridad", "perfil": "protector"}
                ]
            }
        ]
    },
    {
        "id": "humor",
        "categoria": "😂 Humor",
        "titulo": "¿Qué tipo de humor tienes?",
        "descripcion": "La risa también tiene personalidad.",
        "perfiles": {
            "ironico": {
                "nombre": "😏 Humor irónico",
                "texto": "No necesitas subir la voz. Una frase seca y una pausa bien colocada hacen todo el trabajo."
            },
            "absurdo": {
                "nombre": "🛸 Humor absurdo",
                "texto": "Tu cabeza conecta cosas que nadie había relacionado. A veces ni tú sabes explicar por qué hace gracia."
            },
            "negro": {
                "nombre": "🖤 Humor negro",
                "texto": "Usas la risa para atravesar situaciones incómodas. No es para todos los públicos y lo sabes."
            },
            "blanco": {
                "nombre": "😊 Humor blanco",
                "texto": "Te gusta hacer reír sin dejar a nadie debajo del autobús. Tu humor une más de lo que pincha."
            }
        },
        "preguntas": [
            {
                "texto": "Alguien dice una obviedad.",
                "opciones": [
                    {"texto": "Respondo con ironía", "perfil": "ironico"},
                    {"texto": "Invento una teoría absurda", "perfil": "absurdo"},
                    {"texto": "Hago un comentario oscuro", "perfil": "negro"},
                    {"texto": "Me río sin atacar", "perfil": "blanco"}
                ]
            },
            {
                "texto": "Tu meme favorito suele ser...",
                "opciones": [
                    {"texto": "Una captura con doble sentido", "perfil": "ironico"},
                    {"texto": "Algo completamente sin contexto", "perfil": "absurdo"},
                    {"texto": "Algo que no enseñarías en una comida familiar", "perfil": "negro"},
                    {"texto": "Algo cotidiano y reconocible", "perfil": "blanco"}
                ]
            },
            {
                "texto": "Cuando hay tensión...",
                "opciones": [
                    {"texto": "Lanzo una frase seca", "perfil": "ironico"},
                    {"texto": "Cambio la realidad con una tontería", "perfil": "absurdo"},
                    {"texto": "Voy al límite", "perfil": "negro"},
                    {"texto": "Intento aliviar sin herir", "perfil": "blanco"}
                ]
            },
            {
                "texto": "Tu mayor riesgo es...",
                "opciones": [
                    {"texto": "Que no capten la ironía", "perfil": "ironico"},
                    {"texto": "Que nadie entienda la referencia", "perfil": "absurdo"},
                    {"texto": "Pasarte tres pueblos", "perfil": "negro"},
                    {"texto": "Ser demasiado suave", "perfil": "blanco"}
                ]
            },
            {
                "texto": "Tu reacción a un mal chiste:",
                "opciones": [
                    {"texto": "Lo mejoro con una réplica", "perfil": "ironico"},
                    {"texto": "Lo llevo a un lugar aún más raro", "perfil": "absurdo"},
                    {"texto": "Lo entierro sin piedad", "perfil": "negro"},
                    {"texto": "Me río por cariño", "perfil": "blanco"}
                ]
            },
            {
                "texto": "La gente se ríe contigo porque...",
                "opciones": [
                    {"texto": "Eres rápido", "perfil": "ironico"},
                    {"texto": "Eres imprevisible", "perfil": "absurdo"},
                    {"texto": "Te atreves", "perfil": "negro"},
                    {"texto": "Haces sentir cómodo", "perfil": "blanco"}
                ]
            }
        ]
    },
    {
        "id": "fiesta",
        "categoria": "🎉 Planes",
        "titulo": "¿Qué papel tienes en una fiesta?",
        "descripcion": "La noche tiene reparto y tú siempre acabas ocupando un puesto.",
        "perfiles": {
            "anfitrion": {
                "nombre": "🏠 Anfitrión profesional",
                "texto": "Estás pendiente de la música, la comida y de que nadie se quede fuera. Te cuesta relajarte, pero sin ti el plan no existe."
            },
            "bailarin": {
                "nombre": "💃 Alma de la pista",
                "texto": "Has venido a moverte. Contagias energía y consigues que alguien que juró no bailar termine haciendo el ridículo contigo."
            },
            "conversador": {
                "nombre": "🛋️ Conversador de esquina",
                "texto": "Empiezas hablando del tiempo y terminas analizando la vida a las tres de la mañana."
            },
            "fantasma": {
                "nombre": "👻 Desaparición estratégica",
                "texto": "Llegas, saludas, disfrutas y en algún momento desapareces sin que nadie sepa exactamente cuándo."
            }
        },
        "preguntas": [
            {
                "texto": "Nada más llegar...",
                "opciones": [
                    {"texto": "Pregunto si falta algo", "perfil": "anfitrion"},
                    {"texto": "Busco la música", "perfil": "bailarin"},
                    {"texto": "Me siento con alguien interesante", "perfil": "conversador"},
                    {"texto": "Estudio cuánto tiempo debo quedarme", "perfil": "fantasma"}
                ]
            },
            {
                "texto": "Tu lugar habitual:",
                "opciones": [
                    {"texto": "Cerca de quien organiza", "perfil": "anfitrion"},
                    {"texto": "Donde se baile", "perfil": "bailarin"},
                    {"texto": "En una esquina hablando", "perfil": "conversador"},
                    {"texto": "Cerca de la salida", "perfil": "fantasma"}
                ]
            },
            {
                "texto": "A medianoche tú...",
                "opciones": [
                    {"texto": "Compruebo que todos estén bien", "perfil": "anfitrion"},
                    {"texto": "Estoy en mi mejor momento", "perfil": "bailarin"},
                    {"texto": "Tengo una conversación intensa", "perfil": "conversador"},
                    {"texto": "Ya he valorado irme", "perfil": "fantasma"}
                ]
            },
            {
                "texto": "Si baja el ambiente...",
                "opciones": [
                    {"texto": "Cambio música o saco comida", "perfil": "anfitrion"},
                    {"texto": "Arrastro gente a bailar", "perfil": "bailarin"},
                    {"texto": "Aprovecho para hablar tranquilo", "perfil": "conversador"},
                    {"texto": "Es mi señal", "perfil": "fantasma"}
                ]
            },
            {
                "texto": "Tu mensaje al día siguiente:",
                "opciones": [
                    {"texto": "¿Llegaron todos bien?", "perfil": "anfitrion"},
                    {"texto": "Tengo agujetas", "perfil": "bailarin"},
                    {"texto": "Qué conversación más interesante", "perfil": "conversador"},
                    {"texto": "Perdón, me fui sin despedirme", "perfil": "fantasma"}
                ]
            },
            {
                "texto": "Lo esencial en una fiesta:",
                "opciones": [
                    {"texto": "Que todos estén cómodos", "perfil": "anfitrion"},
                    {"texto": "La música", "perfil": "bailarin"},
                    {"texto": "La gente", "perfil": "conversador"},
                    {"texto": "Poder irme cuando quiera", "perfil": "fantasma"}
                ]
            }
        ]
    },
    {
        "id": "hogar",
        "categoria": "🏠 Vida cotidiana",
        "titulo": "¿Qué tipo de persona eres en casa?",
        "descripcion": "La verdadera personalidad aparece cuando nadie mira.",
        "perfiles": {
            "orden": {
                "nombre": "🧹 Guardián del orden",
                "texto": "Necesitas que cada cosa tenga su sitio. El caos visual te roba energía y no entiendes cómo alguien puede perder las llaves dentro de casa."
            },
            "nido": {
                "nombre": "🛋️ Constructor de nidos",
                "texto": "Tu casa es refugio: mantas, comodidad, comida y cero necesidad de salir porque sí."
            },
            "creativo": {
                "nombre": "🎨 Caos creativo",
                "texto": "Puede parecer desorden, pero tú sabes dónde está casi todo. Casi."
            },
            "funcional": {
                "nombre": "🔧 Habitante funcional",
                "texto": "No buscas perfección ni estética de revista. Quieres que la casa funcione y no dé trabajo innecesario."
            }
        },
        "preguntas": [
            {
                "texto": "Al entrar en casa...",
                "opciones": [
                    {"texto": "Coloco cada cosa", "perfil": "orden"},
                    {"texto": "Voy directo al sofá", "perfil": "nido"},
                    {"texto": "Dejo cosas donde me viene bien", "perfil": "creativo"},
                    {"texto": "Hago lo necesario y sigo", "perfil": "funcional"}
                ]
            },
            {
                "texto": "Una tarde libre en casa:",
                "opciones": [
                    {"texto": "Ordeno algo pendiente", "perfil": "orden"},
                    {"texto": "Manta, serie y comida", "perfil": "nido"},
                    {"texto": "Empiezo un proyecto", "perfil": "creativo"},
                    {"texto": "Descanso sin ceremonia", "perfil": "funcional"}
                ]
            },
            {
                "texto": "Tu cocina está...",
                "opciones": [
                    {"texto": "Organizada", "perfil": "orden"},
                    {"texto": "Preparada para picar algo", "perfil": "nido"},
                    {"texto": "Con ingredientes de ideas a medias", "perfil": "creativo"},
                    {"texto": "Con lo básico", "perfil": "funcional"}
                ]
            },
            {
                "texto": "Si viene visita inesperada...",
                "opciones": [
                    {"texto": "Repaso todo rápidamente", "perfil": "orden"},
                    {"texto": "Saco algo de comer", "perfil": "nido"},
                    {"texto": "Muevo el caos de sitio", "perfil": "creativo"},
                    {"texto": "Que entren; esto es una casa", "perfil": "funcional"}
                ]
            },
            {
                "texto": "Tu objeto imprescindible:",
                "opciones": [
                    {"texto": "Organizador o caja", "perfil": "orden"},
                    {"texto": "Sofá o cama cómoda", "perfil": "nido"},
                    {"texto": "Algo para crear", "perfil": "creativo"},
                    {"texto": "Una herramienta útil", "perfil": "funcional"}
                ]
            },
            {
                "texto": "Tu casa ideal se siente...",
                "opciones": [
                    {"texto": "En calma", "perfil": "orden"},
                    {"texto": "Acogedora", "perfil": "nido"},
                    {"texto": "Personal", "perfil": "creativo"},
                    {"texto": "Práctica", "perfil": "funcional"}
                ]
            }
        ]
    },
    {
        "id": "mascota",
        "categoria": "🐾 Mascotas",
        "titulo": "¿Qué energía de mascota tienes?",
        "descripcion": "No preguntamos qué animal prefieres, sino cuál te representa.",
        "perfiles": {
            "perro": {
                "nombre": "🐶 Energía de perro",
                "texto": "Leal, expresivo y feliz de ver a los tuyos. Se te nota cuando alguien te importa."
            },
            "gato": {
                "nombre": "🐱 Energía de gato",
                "texto": "Selectivo, independiente y cariñoso bajo tus propias condiciones. No persigues atención; decides cuándo darla."
            },
            "loro": {
                "nombre": "🦜 Energía de loro",
                "texto": "Social, curioso y con una capacidad peligrosa para repetir la frase exacta en el momento más inoportuno."
            },
            "capibara": {
                "nombre": "🦫 Energía de capibara",
                "texto": "Tranquilo, adaptable y sorprendentemente bueno conviviendo con personalidades muy distintas."
            }
        },
        "preguntas": [
            {
                "texto": "Cuando ves a alguien que quieres...",
                "opciones": [
                    {"texto": "Se me nota muchísimo", "perfil": "perro"},
                    {"texto": "Me acerco cuando me apetece", "perfil": "gato"},
                    {"texto": "Empiezo a hablar enseguida", "perfil": "loro"},
                    {"texto": "Comparto espacio tranquilamente", "perfil": "capibara"}
                ]
            },
            {
                "texto": "En un grupo nuevo...",
                "opciones": [
                    {"texto": "Busco conexión", "perfil": "perro"},
                    {"texto": "Observo primero", "perfil": "gato"},
                    {"texto": "Rompo el silencio", "perfil": "loro"},
                    {"texto": "Me adapto", "perfil": "capibara"}
                ]
            },
            {
                "texto": "Tu límite social aparece...",
                "opciones": [
                    {"texto": "Cuando me siento ignorado", "perfil": "perro"},
                    {"texto": "Cuando invaden mi espacio", "perfil": "gato"},
                    {"texto": "Cuando nadie responde", "perfil": "loro"},
                    {"texto": "Cuando hay demasiado drama", "perfil": "capibara"}
                ]
            },
            {
                "texto": "Tu talento natural:",
                "opciones": [
                    {"texto": "Dar cariño", "perfil": "perro"},
                    {"texto": "Poner límites", "perfil": "gato"},
                    {"texto": "Animar conversaciones", "perfil": "loro"},
                    {"texto": "Mantener la calma", "perfil": "capibara"}
                ]
            },
            {
                "texto": "Tu plan ideal:",
                "opciones": [
                    {"texto": "Con mi gente", "perfil": "perro"},
                    {"texto": "En mi espacio", "perfil": "gato"},
                    {"texto": "Donde haya conversación", "perfil": "loro"},
                    {"texto": "Donde no haya presión", "perfil": "capibara"}
                ]
            },
            {
                "texto": "Tu energía principal:",
                "opciones": [
                    {"texto": "Lealtad", "perfil": "perro"},
                    {"texto": "Independencia", "perfil": "gato"},
                    {"texto": "Curiosidad", "perfil": "loro"},
                    {"texto": "Serenidad", "perfil": "capibara"}
                ]
            }
        ]
    },
    {
        "id": "tecnologia",
        "categoria": "📱 Tecnología",
        "titulo": "¿Qué tipo de usuario tecnológico eres?",
        "descripcion": "Tu relación con las actualizaciones, las contraseñas y el botón de reiniciar.",
        "perfiles": {
            "early": {
                "nombre": "🚀 Explorador tecnológico",
                "texto": "Pruebas novedades antes de que sean estables y aceptas que algo pueda romperse por el camino."
            },
            "practico": {
                "nombre": "📲 Usuario práctico",
                "texto": "La tecnología debe servirte, no convertirse en una afición obligatoria. Usas lo que funciona."
            },
            "tradicional": {
                "nombre": "☎️ Resistente al cambio",
                "texto": "Si lo anterior iba bien, necesitas una razón muy convincente para cambiarlo."
            },
            "tecnico": {
                "nombre": "🛠️ Técnico improvisado",
                "texto": "Lees ajustes, buscas soluciones y terminas arreglando los dispositivos de media familia."
            }
        },
        "preguntas": [
            {
                "texto": "Sale una actualización nueva.",
                "opciones": [
                    {"texto": "La instalo enseguida", "perfil": "early"},
                    {"texto": "Espero a que sea necesaria", "perfil": "practico"},
                    {"texto": "La evito todo lo posible", "perfil": "tradicional"},
                    {"texto": "Leo primero qué cambia", "perfil": "tecnico"}
                ]
            },
            {
                "texto": "Una aplicación cambia el diseño.",
                "opciones": [
                    {"texto": "Exploro todo", "perfil": "early"},
                    {"texto": "Busco dónde está lo que uso", "perfil": "practico"},
                    {"texto": "Me enfado porque antes estaba mejor", "perfil": "tradicional"},
                    {"texto": "Reviso configuración", "perfil": "tecnico"}
                ]
            },
            {
                "texto": "Algo deja de funcionar.",
                "opciones": [
                    {"texto": "Pruebo funciones nuevas", "perfil": "early"},
                    {"texto": "Reinicio", "perfil": "practico"},
                    {"texto": "Pido ayuda", "perfil": "tradicional"},
                    {"texto": "Investigo el error", "perfil": "tecnico"}
                ]
            },
            {
                "texto": "Tu móvil tiene...",
                "opciones": [
                    {"texto": "Aplicaciones experimentales", "perfil": "early"},
                    {"texto": "Solo lo que necesito", "perfil": "practico"},
                    {"texto": "Aplicaciones de hace años", "perfil": "tradicional"},
                    {"texto": "Herramientas que nadie conoce", "perfil": "tecnico"}
                ]
            },
            {
                "texto": "La contraseña del wifi...",
                "opciones": [
                    {"texto": "La tengo en una app", "perfil": "early"},
                    {"texto": "Está apuntada", "perfil": "practico"},
                    {"texto": "No recuerdo quién la puso", "perfil": "tradicional"},
                    {"texto": "La configuré yo", "perfil": "tecnico"}
                ]
            },
            {
                "texto": "La tecnología ideal debe ser...",
                "opciones": [
                    {"texto": "Innovadora", "perfil": "early"},
                    {"texto": "Útil", "perfil": "practico"},
                    {"texto": "Familiar", "perfil": "tradicional"},
                    {"texto": "Configurable", "perfil": "tecnico"}
                ]
            }
        ]
    },
    {
        "id": "conversacion",
        "categoria": "💬 Vida social",
        "titulo": "¿Qué tipo de conversador eres?",
        "descripcion": "Hablar no es solo hablar: también es escuchar, preguntar y saber cuándo parar.",
        "perfiles": {
            "profundo": {
                "nombre": "🌌 Conversador profundo",
                "texto": "Saltas rápido de lo superficial a lo importante. Te interesan las ideas, las emociones y lo que hay detrás."
            },
            "narrador": {
                "nombre": "📚 Narrador de anécdotas",
                "texto": "Tienes historias, detalles y una forma de contarlos que convierte cualquier tarde en episodio."
            },
            "pregunton": {
                "nombre": "🔎 Preguntador curioso",
                "texto": "Quieres entender. Haces preguntas que abren temas y consigues que la gente se explique."
            },
            "ligero": {
                "nombre": "☀️ Conversador ligero",
                "texto": "Sabes mantener el ambiente cómodo. No todo tiene que convertirse en terapia o debate."
            }
        },
        "preguntas": [
            {
                "texto": "Con alguien nuevo empiezas por...",
                "opciones": [
                    {"texto": "Algo que revele cómo piensa", "perfil": "profundo"},
                    {"texto": "Una historia divertida", "perfil": "narrador"},
                    {"texto": "Preguntarle por su vida", "perfil": "pregunton"},
                    {"texto": "Un tema fácil", "perfil": "ligero"}
                ]
            },
            {
                "texto": "En un silencio incómodo...",
                "opciones": [
                    {"texto": "Lanzo una pregunta importante", "perfil": "profundo"},
                    {"texto": "Cuento algo", "perfil": "narrador"},
                    {"texto": "Pregunto por un detalle", "perfil": "pregunton"},
                    {"texto": "Hago un comentario sencillo", "perfil": "ligero"}
                ]
            },
            {
                "texto": "Lo que más valoras al hablar:",
                "opciones": [
                    {"texto": "La sinceridad", "perfil": "profundo"},
                    {"texto": "La conexión mediante historias", "perfil": "narrador"},
                    {"texto": "Descubrir cosas", "perfil": "pregunton"},
                    {"texto": "La comodidad", "perfil": "ligero"}
                ]
            },
            {
                "texto": "Tu riesgo habitual:",
                "opciones": [
                    {"texto": "Ir demasiado hondo", "perfil": "profundo"},
                    {"texto": "Alargar demasiado una historia", "perfil": "narrador"},
                    {"texto": "Parecer un interrogatorio", "perfil": "pregunton"},
                    {"texto": "Quedarte en la superficie", "perfil": "ligero"}
                ]
            },
            {
                "texto": "Una buena conversación termina con...",
                "opciones": [
                    {"texto": "Una nueva perspectiva", "perfil": "profundo"},
                    {"texto": "Una anécdota para recordar", "perfil": "narrador"},
                    {"texto": "Más curiosidad", "perfil": "pregunton"},
                    {"texto": "Buen ambiente", "perfil": "ligero"}
                ]
            },
            {
                "texto": "Tu frase más probable:",
                "opciones": [
                    {"texto": "¿Y cómo te hizo sentir?", "perfil": "profundo"},
                    {"texto": "Eso me recuerda a una vez...", "perfil": "narrador"},
                    {"texto": "¿Y por qué?", "perfil": "pregunton"},
                    {"texto": "Bueno, tampoco pasa nada", "perfil": "ligero"}
                ]
            }
        ]
    },
    {
        "id": "nostalgia",
        "categoria": "📼 Nostalgia",
        "titulo": "¿Qué tipo de nostálgico eres?",
        "descripcion": "Todos miramos atrás, pero no todos buscamos lo mismo.",
        "perfiles": {
            "musical": {
                "nombre": "🎶 Nostálgico musical",
                "texto": "Tu memoria tiene banda sonora. Una canción puede devolverte a un lugar exacto en segundos."
            },
            "objetos": {
                "nombre": "📦 Guardián de recuerdos",
                "texto": "Conservas entradas, fotos y objetos pequeños porque para ti cuentan una historia."
            },
            "epocas": {
                "nombre": "🕰️ Viajero de épocas",
                "texto": "Te fascinan estéticas, costumbres y momentos que quizá ni siquiera viviste."
            },
            "personas": {
                "nombre": "🤍 Nostálgico emocional",
                "texto": "Lo que echas de menos no son las cosas, sino cómo te sentías con ciertas personas."
            }
        },
        "preguntas": [
            {
                "texto": "Algo te transporta al pasado:",
                "opciones": [
                    {"texto": "Una canción", "perfil": "musical"},
                    {"texto": "Un objeto", "perfil": "objetos"},
                    {"texto": "Una estética antigua", "perfil": "epocas"},
                    {"texto": "Una conversación", "perfil": "personas"}
                ]
            },
            {
                "texto": "Lo que más guardas:",
                "opciones": [
                    {"texto": "Listas de canciones", "perfil": "musical"},
                    {"texto": "Entradas y recuerdos", "perfil": "objetos"},
                    {"texto": "Fotos de otras décadas", "perfil": "epocas"},
                    {"texto": "Mensajes y cartas", "perfil": "personas"}
                ]
            },
            {
                "texto": "Tu viaje al pasado ideal:",
                "opciones": [
                    {"texto": "Un concierto", "perfil": "musical"},
                    {"texto": "Una habitación de infancia", "perfil": "objetos"},
                    {"texto": "Otra década", "perfil": "epocas"},
                    {"texto": "Un día con alguien", "perfil": "personas"}
                ]
            },
            {
                "texto": "Cuando recuerdas...",
                "opciones": [
                    {"texto": "Escucho música", "perfil": "musical"},
                    {"texto": "Busco fotos u objetos", "perfil": "objetos"},
                    {"texto": "Comparo épocas", "perfil": "epocas"},
                    {"texto": "Pienso en vínculos", "perfil": "personas"}
                ]
            },
            {
                "texto": "Tu debilidad:",
                "opciones": [
                    {"texto": "Canciones antiguas", "perfil": "musical"},
                    {"texto": "Cajas que nunca tiras", "perfil": "objetos"},
                    {"texto": "Moda y cultura retro", "perfil": "epocas"},
                    {"texto": "Personas que marcaron una etapa", "perfil": "personas"}
                ]
            },
            {
                "texto": "El pasado para ti es...",
                "opciones": [
                    {"texto": "Una melodía", "perfil": "musical"},
                    {"texto": "Un archivo", "perfil": "objetos"},
                    {"texto": "Un mundo", "perfil": "epocas"},
                    {"texto": "Una emoción", "perfil": "personas"}
                ]
            }
        ]
    },
    {
        "id": "decision",
        "categoria": "🧠 Personalidad",
        "titulo": "¿Cómo tomas decisiones?",
        "descripcion": "Entre la lógica, la intuición y el impulso hay muchos caminos.",
        "perfiles": {
            "logico": {
                "nombre": "📊 Decisor lógico",
                "texto": "Comparas opciones, valoras consecuencias y necesitas que la elección tenga sentido."
            },
            "intuitivo": {
                "nombre": "🔮 Decisor intuitivo",
                "texto": "Lees sensaciones y ambientes. A veces no puedes explicar por qué, pero sabes cuándo algo no encaja."
            },
            "impulsivo": {
                "nombre": "⚡ Decisor impulsivo",
                "texto": "Actúas rápido y confías en que ya resolverás lo que venga. Tu vida rara vez se atasca por exceso de análisis."
            },
            "consultor": {
                "nombre": "💬 Decisor consultivo",
                "texto": "Necesitas hablarlo. Escuchar otras perspectivas te ayuda a ordenar lo que realmente quieres."
            }
        },
        "preguntas": [
            {
                "texto": "Te ofrecen un plan inesperado.",
                "opciones": [
                    {"texto": "Reviso si encaja", "perfil": "logico"},
                    {"texto": "Siento si me apetece", "perfil": "intuitivo"},
                    {"texto": "Digo que sí", "perfil": "impulsivo"},
                    {"texto": "Pregunto quién va", "perfil": "consultor"}
                ]
            },
            {
                "texto": "Una compra importante...",
                "opciones": [
                    {"texto": "La comparo", "perfil": "logico"},
                    {"texto": "Elijo la que me da mejor sensación", "perfil": "intuitivo"},
                    {"texto": "La compro si me entusiasma", "perfil": "impulsivo"},
                    {"texto": "Pido opiniones", "perfil": "consultor"}
                ]
            },
            {
                "texto": "Cuando dudas...",
                "opciones": [
                    {"texto": "Hago una lista", "perfil": "logico"},
                    {"texto": "Me escucho", "perfil": "intuitivo"},
                    {"texto": "Elijo y sigo", "perfil": "impulsivo"},
                    {"texto": "Lo hablo", "perfil": "consultor"}
                ]
            },
            {
                "texto": "Tu mayor problema al decidir:",
                "opciones": [
                    {"texto": "Analizar demasiado", "perfil": "logico"},
                    {"texto": "No poder justificarlo", "perfil": "intuitivo"},
                    {"texto": "Arrepentirme después", "perfil": "impulsivo"},
                    {"texto": "Recibir opiniones contradictorias", "perfil": "consultor"}
                ]
            },
            {
                "texto": "La frase que más te representa:",
                "opciones": [
                    {"texto": "Veamos pros y contras", "perfil": "logico"},
                    {"texto": "Hay algo que no me cuadra", "perfil": "intuitivo"},
                    {"texto": "Ya veremos", "perfil": "impulsivo"},
                    {"texto": "¿Tú qué harías?", "perfil": "consultor"}
                ]
            },
            {
                "texto": "Una buena decisión debe...",
                "opciones": [
                    {"texto": "Ser coherente", "perfil": "logico"},
                    {"texto": "Sentirse correcta", "perfil": "intuitivo"},
                    {"texto": "Moverte", "perfil": "impulsivo"},
                    {"texto": "Resistir varias perspectivas", "perfil": "consultor"}
                ]
            }
        ]
    },
    {
        "id": "grupo_chat",
        "categoria": "💬 Vida social",
        "titulo": "¿Qué papel tienes en un grupo de chat?",
        "descripcion": "Todo grupo tiene administradores no oficiales, lectores silenciosos y fabricantes de caos.",
        "perfiles": {
            "motor": {
                "nombre": "🚀 Motor del chat",
                "texto": "Abres temas, respondes y evitas que el grupo parezca un cementerio digital."
            },
            "observador": {
                "nombre": "👀 Observador silencioso",
                "texto": "Lees casi todo, intervienes cuando merece la pena y sabes más del grupo de lo que la gente imagina."
            },
            "meme": {
                "nombre": "😂 Proveedor de memes",
                "texto": "Tal vez no respondas con un ensayo, pero siempre tienes la imagen exacta."
            },
            "mediador": {
                "nombre": "🕊️ Mediador",
                "texto": "Detectas tensiones y sabes bajar el volumen antes de que alguien salga del grupo dramáticamente."
            }
        },
        "preguntas": [
            {
                "texto": "El grupo lleva horas en silencio.",
                "opciones": [
                    {"texto": "Abro un tema", "perfil": "motor"},
                    {"texto": "Sigo leyendo cuando hablen", "perfil": "observador"},
                    {"texto": "Mando un meme", "perfil": "meme"},
                    {"texto": "Pregunto cómo están", "perfil": "mediador"}
                ]
            },
            {
                "texto": "Aparece una discusión.",
                "opciones": [
                    {"texto": "Intento reconducir el tema", "perfil": "motor"},
                    {"texto": "Leo antes de posicionarme", "perfil": "observador"},
                    {"texto": "Tengo una reacción gráfica perfecta", "perfil": "meme"},
                    {"texto": "Calmo a las partes", "perfil": "mediador"}
                ]
            },
            {
                "texto": "Entra alguien nuevo.",
                "opciones": [
                    {"texto": "Le doy conversación", "perfil": "motor"},
                    {"texto": "Observo cómo encaja", "perfil": "observador"},
                    {"texto": "Le recibo con humor", "perfil": "meme"},
                    {"texto": "Me aseguro de que se sienta incluido", "perfil": "mediador"}
                ]
            },
            {
                "texto": "Tu tipo de mensaje habitual:",
                "opciones": [
                    {"texto": "Pregunta o propuesta", "perfil": "motor"},
                    {"texto": "Respuesta puntual", "perfil": "observador"},
                    {"texto": "Sticker o meme", "perfil": "meme"},
                    {"texto": "Mensaje conciliador", "perfil": "mediador"}
                ]
            },
            {
                "texto": "Tu mayor riesgo:",
                "opciones": [
                    {"texto": "Hablar demasiado", "perfil": "motor"},
                    {"texto": "Parecer ausente", "perfil": "observador"},
                    {"texto": "Responder a todo con memes", "perfil": "meme"},
                    {"texto": "Cargar con problemas ajenos", "perfil": "mediador"}
                ]
            },
            {
                "texto": "Lo que aportas al chat:",
                "opciones": [
                    {"texto": "Actividad", "perfil": "motor"},
                    {"texto": "Perspectiva", "perfil": "observador"},
                    {"texto": "Humor", "perfil": "meme"},
                    {"texto": "Equilibrio", "perfil": "mediador"}
                ]
            }
        ]
    }
]


def obtener_test_por_id(test_id):
    """Devuelve un test por su ID o None si no existe."""
    for test in TESTS:
        if test["id"] == test_id:
            return test
    return None


def validar_base_tests():
    """Comprueba la estructura al importar el archivo."""
    ids = set()

    for test in TESTS:
        campos = {"id", "categoria", "titulo", "descripcion", "perfiles", "preguntas"}
        faltantes = campos - set(test)

        if faltantes:
            raise ValueError(
                f"El test {test.get('id', 'sin_id')} no tiene: {sorted(faltantes)}"
            )

        if test["id"] in ids:
            raise ValueError(f"ID de test repetido: {test['id']}")

        ids.add(test["id"])

        if len(test["preguntas"]) < 4:
            raise ValueError(
                f"El test {test['id']} debe tener al menos 4 preguntas."
            )

        perfiles = set(test["perfiles"])

        for numero, pregunta in enumerate(test["preguntas"], start=1):
            if "texto" not in pregunta or "opciones" not in pregunta:
                raise ValueError(
                    f"Pregunta {numero} incompleta en {test['id']}."
                )

            if len(pregunta["opciones"]) < 2:
                raise ValueError(
                    f"Pregunta {numero} sin suficientes opciones en {test['id']}."
                )

            for opcion in pregunta["opciones"]:
                if opcion.get("perfil") not in perfiles:
                    raise ValueError(
                        f"Perfil inválido en {test['id']}, pregunta {numero}."
                    )


validar_base_tests()
