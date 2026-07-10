```python
preguntas_trivial = [
    {
        "categoria": "Geografía",
        "dificultad": 1,
        "pregunta": "¿Cuál es la capital de Australia?",
        "opciones": ["Sídney", "Melbourne", "Canberra", "Perth"],
        "correcta": "Canberra",
        "explicacion": "Canberra fue elegida como capital para evitar la rivalidad entre Sídney y Melbourne."
    },
    {
        "categoria": "Ciencia",
        "dificultad": 1,
        "pregunta": "¿Qué planeta es conocido como el planeta rojo?",
        "opciones": ["Venus", "Marte", "Júpiter", "Mercurio"],
        "correcta": "Marte",
        "explicacion": "Marte tiene un aspecto rojizo por el óxido de hierro presente en su superficie."
    },
    {
        "categoria": "Arte",
        "dificultad": 1,
        "pregunta": "¿Quién pintó La Gioconda?",
        "opciones": ["Miguel Ángel", "Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh"],
        "correcta": "Leonardo da Vinci",
        "explicacion": "La Gioconda, también conocida como Mona Lisa, fue pintada por Leonardo da Vinci."
    },
    {
        "categoria": "Geometría",
        "dificultad": 1,
        "pregunta": "¿Cuántos lados tiene un hexágono?",
        "opciones": ["Cinco", "Seis", "Siete", "Ocho"],
        "correcta": "Seis",
        "explicacion": "El prefijo griego hexa significa seis."
    },
    {
        "categoria": "Geografía",
        "dificultad": 1,
        "pregunta": "¿En qué país se encuentra la Torre Eiffel?",
        "opciones": ["Francia", "Italia", "Bélgica", "Suiza"],
        "correcta": "Francia",
        "explicacion": "La Torre Eiffel está situada en París, capital de Francia."
    },
    {
        "categoria": "Geografía",
        "dificultad": 1,
        "pregunta": "¿Cuál es el océano más grande del mundo?",
        "opciones": ["Atlántico", "Pacífico", "Índico", "Ártico"],
        "correcta": "Pacífico",
        "explicacion": "El océano Pacífico ocupa aproximadamente un tercio de la superficie terrestre."
    },
    {
        "categoria": "Deportes",
        "dificultad": 1,
        "pregunta": "¿Qué deporte se disputa en Wimbledon?",
        "opciones": ["Golf", "Tenis", "Rugby", "Críquet"],
        "correcta": "Tenis",
        "explicacion": "Wimbledon es uno de los cuatro torneos de Grand Slam de tenis."
    },
    {
        "categoria": "Ciencia",
        "dificultad": 2,
        "pregunta": "¿Cuál es el gas más abundante de la atmósfera terrestre?",
        "opciones": ["Oxígeno", "Nitrógeno", "Dióxido de carbono", "Hidrógeno"],
        "correcta": "Nitrógeno",
        "explicacion": "El nitrógeno representa aproximadamente el 78 % de la atmósfera terrestre."
    },
    {
        "categoria": "Geografía",
        "dificultad": 1,
        "pregunta": "¿En qué continente está Egipto?",
        "opciones": ["Europa", "África", "América", "Oceanía"],
        "correcta": "África",
        "explicacion": "La mayor parte de Egipto se encuentra en África, aunque la península del Sinaí está en Asia."
    },
    {
        "categoria": "Cultura general",
        "dificultad": 1,
        "pregunta": "¿Cuántos minutos tiene una hora?",
        "opciones": ["50", "60", "70", "100"],
        "correcta": "60",
        "explicacion": "Una hora se divide en 60 minutos."
    },
    {
        "categoria": "Idiomas",
        "dificultad": 2,
        "pregunta": "¿Cuál es el idioma con más hablantes nativos del mundo?",
        "opciones": ["Inglés", "Español", "Chino mandarín", "Árabe"],
        "correcta": "Chino mandarín",
        "explicacion": "El chino mandarín es la lengua materna de más personas que cualquier otro idioma."
    },
    {
        "categoria": "Ciencia",
        "dificultad": 2,
        "pregunta": "¿Qué metal es líquido a temperatura ambiente?",
        "opciones": ["Mercurio", "Aluminio", "Cobre", "Plata"],
        "correcta": "Mercurio",
        "explicacion": "El mercurio permanece líquido a temperatura ambiente."
    },
    {
        "categoria": "Música",
        "dificultad": 1,
        "pregunta": "¿Qué instrumento suele tener teclas blancas y negras?",
        "opciones": ["Violín", "Piano", "Trompeta", "Flauta"],
        "correcta": "Piano",
        "explicacion": "El teclado del piano combina teclas blancas y negras."
    },
    {
        "categoria": "Cultura general",
        "dificultad": 1,
        "pregunta": "¿Cuántos colores se atribuyen tradicionalmente al arcoíris?",
        "opciones": ["Cinco", "Seis", "Siete", "Nueve"],
        "correcta": "Siete",
        "explicacion": "Tradicionalmente se distinguen siete colores: rojo, naranja, amarillo, verde, azul, añil y violeta."
    },
    {
        "categoria": "Animales",
        "dificultad": 1,
        "pregunta": "¿Qué animal es conocido popularmente como el rey de la selva?",
        "opciones": ["León", "Tigre", "Elefante", "Gorila"],
        "correcta": "León",
        "explicacion": "El león recibe popularmente ese apodo, aunque normalmente habita en sabanas."
    },
    {
        "categoria": "Historia",
        "dificultad": 1,
        "pregunta": "¿En qué año llegó Cristóbal Colón a América?",
        "opciones": ["1492", "1500", "1453", "1512"],
        "correcta": "1492",
        "explicacion": "La expedición de Colón llegó a América el 12 de octubre de 1492."
    },
    {
        "categoria": "Cine",
        "dificultad": 1,
        "pregunta": "¿Quién dirigió Titanic?",
        "opciones": ["Steven Spielberg", "James Cameron", "Ridley Scott", "Peter Jackson"],
        "correcta": "James Cameron",
        "explicacion": "James Cameron escribió y dirigió Titanic, estrenada en 1997."
    },
    {
        "categoria": "Literatura",
        "dificultad": 1,
        "pregunta": "¿Quién escribió Don Quijote de la Mancha?",
        "opciones": ["Miguel de Cervantes", "Federico García Lorca", "Francisco de Quevedo", "Lope de Vega"],
        "correcta": "Miguel de Cervantes",
        "explicacion": "Miguel de Cervantes publicó la primera parte del Quijote en 1605."
    },
    {
        "categoria": "Geografía",
        "dificultad": 1,
        "pregunta": "¿Cuál es la capital de Japón?",
        "opciones": ["Osaka", "Tokio", "Kioto", "Nagoya"],
        "correcta": "Tokio",
        "explicacion": "Tokio es la capital y la ciudad más poblada de Japón."
    },
    {
        "categoria": "Ciencia",
        "dificultad": 1,
        "pregunta": "¿Cuál es la fórmula química del agua?",
        "opciones": ["CO2", "H2O", "O2", "NaCl"],
        "correcta": "H2O",
        "explicacion": "Cada molécula de agua contiene dos átomos de hidrógeno y uno de oxígeno."
    },
    {
        "categoria": "Historia",
        "dificultad": 2,
        "pregunta": "¿En qué año cayó el Muro de Berlín?",
        "opciones": ["1975", "1989", "1991", "1968"],
        "correcta": "1989",
        "explicacion": "El Muro de Berlín comenzó a abrirse el 9 de noviembre de 1989."
    },
    {
        "categoria": "Videojuegos",
        "dificultad": 1,
        "pregunta": "¿Qué personaje de Nintendo es un fontanero italiano?",
        "opciones": ["Sonic", "Mario", "Link", "Kirby"],
        "correcta": "Mario",
        "explicacion": "Mario es el protagonista de la saga Super Mario de Nintendo."
    },
    {
        "categoria": "Música",
        "dificultad": 1,
        "pregunta": "¿Qué grupo interpretó Bohemian Rhapsody?",
        "opciones": ["Queen", "The Beatles", "U2", "ABBA"],
        "correcta": "Queen",
        "explicacion": "Bohemian Rhapsody fue publicada por Queen en 1975."
    },
    {
        "categoria": "Geografía",
        "dificultad": 1,
        "pregunta": "¿Cuál es la capital de Argentina?",
        "opciones": ["Córdoba", "Buenos Aires", "Rosario", "Mendoza"],
        "correcta": "Buenos Aires",
        "explicacion": "Buenos Aires es la capital y la ciudad más poblada de Argentina."
    },
    {
        "categoria": "Animales",
        "dificultad": 2,
        "pregunta": "¿Cuál es el mamífero más grande del mundo?",
        "opciones": ["Elefante africano", "Ballena azul", "Jirafa", "Cachalote"],
        "correcta": "Ballena azul",
        "explicacion": "La ballena azul puede superar los 25 metros de longitud."
    },
    {
        "categoria": "Tecnología",
        "dificultad": 2,
        "pregunta": "¿Qué significan las siglas WWW?",
        "opciones": ["World Wide Web", "Wide World Wireless", "Web World Work", "World Web Window"],
        "correcta": "World Wide Web",
        "explicacion": "World Wide Web es el sistema de páginas y recursos enlazados que utilizamos en Internet."
    },
    {
        "categoria": "Gastronomía",
        "dificultad": 1,
        "pregunta": "¿De qué país es originaria la pizza moderna?",
        "opciones": ["Italia", "Francia", "Grecia", "España"],
        "correcta": "Italia",
        "explicacion": "La pizza moderna se desarrolló especialmente en Nápoles, Italia."
    },
    {
        "categoria": "Deportes",
        "dificultad": 1,
        "pregunta": "¿Cuántos jugadores tiene un equipo de fútbol en el campo al comenzar un partido?",
        "opciones": ["Nueve", "Diez", "Once", "Doce"],
        "correcta": "Once",
        "explicacion": "Cada equipo comienza normalmente con once jugadores, incluido el portero."
    },
    {
        "categoria": "Espacio",
        "dificultad": 1,
        "pregunta": "¿Cuál es el satélite natural de la Tierra?",
        "opciones": ["La Luna", "Fobos", "Europa", "Titán"],
        "correcta": "La Luna",
        "explicacion": "La Luna es el único satélite natural permanente de la Tierra."
    },
    {
        "categoria": "Historia",
        "dificultad": 1,
        "pregunta": "¿Qué civilización construyó las pirámides de Guiza?",
        "opciones": ["Romanos", "Egipcios", "Mayas", "Griegos"],
        "correcta": "Egipcios",
        "explicacion": "Las pirámides de Guiza fueron construidas en el Antiguo Egipto como complejos funerarios."
    },
    {
        "categoria": "Series",
        "dificultad": 1,
        "pregunta": "¿En qué serie aparece el personaje de Walter White?",
        "opciones": ["Breaking Bad", "Lost", "Dexter", "The Walking Dead"],
        "correcta": "Breaking Bad",
        "explicacion": "Walter White es el protagonista de Breaking Bad."
    },
    {
        "categoria": "Cine",
        "dificultad": 1,
        "pregunta": "¿Cómo se llama el ogro verde protagonista de una famosa saga de animación?",
        "opciones": ["Shrek", "Fiona", "Sulley", "Hulk"],
        "correcta": "Shrek",
        "explicacion": "Shrek protagoniza la saga de animación producida por DreamWorks."
    },
    {
        "categoria": "Ciencia",
        "dificultad": 2,
        "pregunta": "¿Cuál es el órgano más grande del cuerpo humano?",
        "opciones": ["Hígado", "Piel", "Pulmón", "Intestino"],
        "correcta": "Piel",
        "explicacion": "La piel es el órgano más extenso del cuerpo humano."
    },
    {
        "categoria": "Geografía",
        "dificultad": 1,
        "pregunta": "¿Cuál es la capital de México?",
        "opciones": ["Guadalajara", "Monterrey", "Ciudad de México", "Puebla"],
        "correcta": "Ciudad de México",
        "explicacion": "Ciudad de México es la capital del país."
    },
    {
        "categoria": "Literatura",
        "dificultad": 1,
        "pregunta": "¿Quién escribió Romeo y Julieta?",
        "opciones": ["William Shakespeare", "Charles Dickens", "Oscar Wilde", "Dante Alighieri"],
        "correcta": "William Shakespeare",
        "explicacion": "Romeo y Julieta es una tragedia escrita por William Shakespeare."
    },
    {
        "categoria": "Animales",
        "dificultad": 2,
        "pregunta": "¿Qué animal terrestre es el más rápido?",
        "opciones": ["León", "Guepardo", "Antílope", "Tigre"],
        "correcta": "Guepardo",
        "explicacion": "El guepardo puede superar los 90 kilómetros por hora en carreras cortas."
    },
    {
        "categoria": "Cultura general",
        "dificultad": 1,
        "pregunta": "¿Cuántos días tiene un año bisiesto?",
        "opciones": ["365", "366", "364", "367"],
        "correcta": "366",
        "explicacion": "Los años bisiestos tienen un día adicional en febrero."
    },
    {
        "categoria": "Cine",
        "dificultad": 1,
        "pregunta": "¿Qué actor interpretó a Jack en Titanic?",
        "opciones": ["Brad Pitt", "Leonardo DiCaprio", "Tom Cruise", "Matt Damon"],
        "correcta": "Leonardo DiCaprio",
        "explicacion": "Leonardo DiCaprio interpretó a Jack Dawson en Titanic."
    },
    {
        "categoria": "Geografía",
        "dificultad": 1,
        "pregunta": "¿Cuál es la capital de Colombia?",
        "opciones": ["Medellín", "Bogotá", "Cali", "Cartagena"],
        "correcta": "Bogotá",
        "explicacion": "Bogotá es la capital y la ciudad más poblada de Colombia."
    },
    {
        "categoria": "Ciencia",
        "dificultad": 2,
        "pregunta": "¿Qué partícula tiene carga eléctrica negativa?",
        "opciones": ["Protón", "Neutrón", "Electrón", "Fotón"],
        "correcta": "Electrón",
        "explicacion": "El electrón posee carga eléctrica negativa."
    },
    {
        "categoria": "Música",
        "dificultad": 1,
        "pregunta": "¿Qué cantante era conocido como el Rey del Pop?",
        "opciones": ["Elvis Presley", "Michael Jackson", "Freddie Mercury", "David Bowie"],
        "correcta": "Michael Jackson",
        "explicacion": "Michael Jackson recibió popularmente el título de Rey del Pop."
    },
    {
        "categoria": "Historia",
        "dificultad": 2,
        "pregunta": "¿Quién fue el primer emperador romano?",
        "opciones": ["Julio César", "Augusto", "Nerón", "Trajano"],
        "correcta": "Augusto",
        "explicacion": "Octavio Augusto fue el primer emperador romano."
    },
    {
        "categoria": "Gastronomía",
        "dificultad": 1,
        "pregunta": "¿Cuál es el ingrediente principal del guacamole?",
        "opciones": ["Tomate", "Aguacate", "Pepino", "Pimiento"],
        "correcta": "Aguacate",
        "explicacion": "El guacamole se prepara principalmente con aguacate."
    },
    {
        "categoria": "Geografía",
        "dificultad": 2,
        "pregunta": "¿Cuál es el río más largo de Sudamérica?",
        "opciones": ["Amazonas", "Orinoco", "Paraná", "Uruguay"],
        "correcta": "Amazonas",
        "explicacion": "El Amazonas es el río más caudaloso del planeta y el más largo de Sudamérica."
    },
    {
        "categoria": "Deportes",
        "dificultad": 1,
        "pregunta": "¿En qué deporte se utiliza una canasta?",
        "opciones": ["Baloncesto", "Tenis", "Béisbol", "Hockey"],
        "correcta": "Baloncesto",
        "explicacion": "En baloncesto, los equipos intentan introducir el balón en la canasta rival."
    },
    {
        "categoria": "Cultura general",
        "dificultad": 1,
        "pregunta": "¿Cuál es la moneda oficial de Estados Unidos?",
        "opciones": ["Euro", "Dólar", "Peso", "Libra"],
        "correcta": "Dólar",
        "explicacion": "La moneda oficial de Estados Unidos es el dólar estadounidense."
    },
    {
        "categoria": "Ciencia",
        "dificultad": 2,
        "pregunta": "¿Qué vitamina produce el cuerpo principalmente al exponerse al sol?",
        "opciones": ["Vitamina A", "Vitamina C", "Vitamina D", "Vitamina K"],
        "correcta": "Vitamina D",
        "explicacion": "La exposición solar permite que la piel sintetice vitamina D."
    },
    {
        "categoria": "Videojuegos",
        "dificultad": 1,
        "pregunta": "¿Cuál es el nombre del protagonista de The Legend of Zelda?",
        "opciones": ["Zelda", "Link", "Ganondorf", "Mario"],
        "correcta": "Link",
        "explicacion": "Link es el héroe protagonista; Zelda es la princesa."
    },
    {
        "categoria": "Cine",
        "dificultad": 1,
        "pregunta": "¿Qué superhéroe es conocido como el Caballero Oscuro?",
        "opciones": ["Superman", "Batman", "Iron Man", "Thor"],
        "correcta": "Batman",
        "explicacion": "Batman recibe habitualmente el sobrenombre de Caballero Oscuro."
    },
    {
        "categoria": "Historia",
        "dificultad": 2,
        "pregunta": "¿En qué país comenzó la Revolución Industrial?",
        "opciones": ["Francia", "Reino Unido", "Alemania", "Estados Unidos"],
        "correcta": "Reino Unido",
        "explicacion": "La Revolución Industrial comenzó en Gran Bretaña durante el siglo XVIII."
    },
    {
        "categoria": "Geografía",
        "dificultad": 1,
        "pregunta": "¿Cuál es la capital de Perú?",
        "opciones": ["Lima", "Cusco", "Arequipa", "Trujillo"],
        "correcta": "Lima",
        "explicacion": "Lima es la capital y la ciudad más poblada de Perú."
    },
    {
        "categoria": "Animales",
        "dificultad": 1,
        "pregunta": "¿Qué animal pone los huevos más grandes?",
        "opciones": ["Águila", "Avestruz", "Pingüino", "Cisne"],
        "correcta": "Avestruz",
        "explicacion": "El avestruz pone los huevos más grandes entre los animales vivos."
    },
    {
        "categoria": "Tecnología",
        "dificultad": 1,
        "pregunta": "¿Qué empresa creó el sistema operativo Windows?",
        "opciones": ["Apple", "Microsoft", "Google", "IBM"],
        "correcta": "Microsoft",
        "explicacion": "Windows fue desarrollado y comercializado por Microsoft."
    },
    {
        "categoria": "Música",
        "dificultad": 1,
        "pregunta": "¿Cuántas cuerdas tiene normalmente una guitarra clásica?",
        "opciones": ["Cuatro", "Cinco", "Seis", "Ocho"],
        "correcta": "Seis",
        "explicacion": "La guitarra clásica estándar tiene seis cuerdas."
    },
    {
        "categoria": "Ciencia",
        "dificultad": 2,
        "pregunta": "¿Cuál es el planeta más grande del sistema solar?",
        "opciones": ["Saturno", "Júpiter", "Neptuno", "Tierra"],
        "correcta": "Júpiter",
        "explicacion": "Júpiter es el planeta de mayor tamaño del sistema solar."
    },
    {
        "categoria": "Literatura",
        "dificultad": 2,
        "pregunta": "¿Quién escribió Cien años de soledad?",
        "opciones": ["Mario Vargas Llosa", "Gabriel García Márquez", "Jorge Luis Borges", "Pablo Neruda"],
        "correcta": "Gabriel García Márquez",
        "explicacion": "Cien años de soledad fue escrita por el colombiano Gabriel García Márquez."
    },
    {
        "categoria": "Geografía",
        "dificultad": 1,
        "pregunta": "¿Cuál es la capital de Chile?",
        "opciones": ["Valparaíso", "Santiago", "Concepción", "Antofagasta"],
        "correcta": "Santiago",
        "explicacion": "Santiago es la capital de Chile."
    },
    {
        "categoria": "Series",
        "dificultad": 1,
        "pregunta": "¿Cómo se llama el continente principal de Juego de Tronos?",
        "opciones": ["Poniente", "Narnia", "Mordor", "Avalon"],
        "correcta": "Poniente",
        "explicacion": "Gran parte de la historia de Juego de Tronos se desarrolla en Poniente."
    },
    {
        "categoria": "Historia",
        "dificultad": 2,
        "pregunta": "¿Quién fue conocido como el Libertador de varios países sudamericanos?",
        "opciones": ["Simón Bolívar", "José Martí", "Emiliano Zapata", "Pancho Villa"],
        "correcta": "Simón Bolívar",
        "explicacion": "Simón Bolívar fue una figura clave en la independencia de varios países de Sudamérica."
    },
    {
        "categoria": "Gastronomía",
        "dificultad": 1,
        "pregunta": "¿Qué legumbre es la base tradicional del hummus?",
        "opciones": ["Lenteja", "Garbanzos", "Frijoles", "Soja"],
        "correcta": "Garbanzos",
        "explicacion": "El hummus tradicional se prepara principalmente con garbanzos y tahini."
    },
    {
        "categoria": "Cultura general",
        "dificultad": 1,
        "pregunta": "¿Cuántos meses tiene un año?",
        "opciones": ["Diez", "Once", "Doce", "Trece"],
        "correcta": "Doce",
        "explicacion": "El calendario gregoriano divide el año en doce meses."
    },
    {
        "categoria": "Espacio",
        "dificultad": 2,
        "pregunta": "¿Cuál es el planeta más cercano al Sol?",
        "opciones": ["Venus", "Mercurio", "Marte", "Tierra"],
        "correcta": "Mercurio",
        "explicacion": "Mercurio es el planeta más cercano al Sol."
    },
    {
        "categoria": "Cine",
        "dificultad": 1,
        "pregunta": "¿Qué película protagoniza un joven mago llamado Harry Potter?",
        "opciones": ["Harry Potter y la piedra filosofal", "El señor de los anillos", "Las crónicas de Narnia", "Percy Jackson"],
        "correcta": "Harry Potter y la piedra filosofal",
        "explicacion": "Harry Potter y la piedra filosofal es la primera película de la saga."
    },
    {
        "categoria": "Animales",
        "dificultad": 2,
        "pregunta": "¿Qué mamífero es capaz de volar de forma sostenida?",
        "opciones": ["Murciélago", "Ardilla voladora", "Pingüino", "Lémur"],
        "correcta": "Murciélago",
        "explicacion": "Los murciélagos son los únicos mamíferos capaces de realizar vuelo activo sostenido."
    },
    {
        "categoria": "Geografía",
        "dificultad": 2,
        "pregunta": "¿Cuál es el país más grande del mundo por superficie?",
        "opciones": ["Canadá", "China", "Rusia", "Estados Unidos"],
        "correcta": "Rusia",
        "explicacion": "Rusia es el país más extenso del planeta."
    },
    {
        "categoria": "Ciencia",
        "dificultad": 1,
        "pregunta": "¿Qué órgano bombea la sangre por el cuerpo?",
        "opciones": ["Cerebro", "Corazón", "Hígado", "Pulmón"],
        "correcta": "Corazón",
        "explicacion": "El corazón impulsa la sangre a través del sistema circulatorio."
    },
    {
        "categoria": "Deportes",
        "dificultad": 1,
        "pregunta": "¿Cuántos aros aparecen en el símbolo olímpico?",
        "opciones": ["Cuatro", "Cinco", "Seis", "Siete"],
        "correcta": "Cinco",
        "explicacion": "El símbolo olímpico está formado por cinco aros entrelazados."
    },
    {
        "categoria": "Música",
        "dificultad": 1,
        "pregunta": "¿Qué cantante interpretó Rolling in the Deep?",
        "opciones": ["Adele", "Beyoncé", "Rihanna", "Lady Gaga"],
        "correcta": "Adele",
        "explicacion": "Rolling in the Deep fue uno de los mayores éxitos de Adele."
    },
    {
        "categoria": "Historia",
        "dificultad": 2,
        "pregunta": "¿Qué ciudad quedó sepultada tras la erupción del Vesubio en el año 79?",
        "opciones": ["Pompeya", "Atenas", "Cartago", "Esparta"],
        "correcta": "Pompeya",
        "explicacion": "Pompeya quedó sepultada por cenizas y materiales volcánicos del Vesubio."
    },
    {
        "categoria": "Cultura general",
        "dificultad": 1,
        "pregunta": "¿Qué color se obtiene al mezclar azul y amarillo?",
        "opciones": ["Verde", "Naranja", "Violeta", "Rojo"],
        "correcta": "Verde",
        "explicacion": "En la mezcla tradicional de pigmentos, azul y amarillo producen verde."
    },
    {
        "categoria": "Tecnología",
        "dificultad": 2,
        "pregunta": "¿Qué significan las siglas GPS?",
        "opciones": ["Global Positioning System", "General Position Service", "Geographic Public Signal", "Global Personal Satellite"],
        "correcta": "Global Positioning System",
        "explicacion": "GPS significa Sistema de Posicionamiento Global."
    },
    {
        "categoria": "Geografía",
        "dificultad": 1,
        "pregunta": "¿Cuál es la capital de Venezuela?",
        "opciones": ["Caracas", "Maracaibo", "Valencia", "Barquisimeto"],
        "correcta": "Caracas",
        "explicacion": "Caracas es la capital de Venezuela."
    },
    {
        "categoria": "Literatura",
        "dificultad": 1,
        "pregunta": "¿Cómo se llama el detective creado por Arthur Conan Doyle?",
        "opciones": ["Hércules Poirot", "Sherlock Holmes", "Philip Marlowe", "Auguste Dupin"],
        "correcta": "Sherlock Holmes",
        "explicacion": "Sherlock Holmes fue creado por el escritor Arthur Conan Doyle."
    },
    {
        "categoria": "Cine",
        "dificultad": 1,
        "pregunta": "¿Cómo se llama el muñeco vaquero de Toy Story?",
        "opciones": ["Woody", "Buzz", "Andy", "Rex"],
        "correcta": "Woody",
        "explicacion": "Woody es el vaquero protagonista de Toy Story."
    },
    {
        "categoria": "Ciencia",
        "dificultad": 2,
        "pregunta": "¿Cuál es el hueso más largo del cuerpo humano?",
        "opciones": ["Fémur", "Tibia", "Húmero", "Radio"],
        "correcta": "Fémur",
        "explicacion": "El fémur, situado en el muslo, es el hueso más largo del cuerpo."
    },
    {
        "categoria": "Animales",
        "dificultad": 1,
        "pregunta": "¿Qué animal es famoso por cambiar de color?",
        "opciones": ["Camaleón", "Cebra", "Rinoceronte", "Canguro"],
        "correcta": "Camaleón",
        "explicacion": "Los camaleones pueden modificar su coloración por comunicación, temperatura y estado fisiológico."
    },
    {
        "categoria": "Geografía",
        "dificultad": 2,
        "pregunta": "¿Cuál es la montaña más alta de África?",
        "opciones": ["Kilimanjaro", "Atlas", "Monte Kenia", "Everest"],
        "correcta": "Kilimanjaro",
        "explicacion": "El Kilimanjaro, en Tanzania, es la montaña más alta de África."
    },
    {
        "categoria": "Historia",
        "dificultad": 1,
        "pregunta": "¿Qué pueblo construyó Machu Picchu?",
        "opciones": ["Incas", "Mayas", "Aztecas", "Olmecas"],
        "correcta": "Incas",
        "explicacion": "Machu Picchu fue construida por la civilización inca."
    },
    {
        "categoria": "Videojuegos",
        "dificultad": 1,
        "pregunta": "¿Qué criatura amarilla es la mascota más conocida de Pokémon?",
        "opciones": ["Pikachu", "Charmander", "Bulbasaur", "Squirtle"],
        "correcta": "Pikachu",
        "explicacion": "Pikachu es el Pokémon más asociado a la franquicia."
    },
    {
        "categoria": "Gastronomía",
        "dificultad": 2,
        "pregunta": "¿Qué país es tradicionalmente asociado con el sushi?",
        "opciones": ["Japón", "China", "Tailandia", "Vietnam"],
        "correcta": "Japón",
        "explicacion": "El sushi es uno de los platos más conocidos de la gastronomía japonesa."
    },
    {
        "categoria": "Espacio",
        "dificultad": 2,
        "pregunta": "¿Cómo se llama nuestra galaxia?",
        "opciones": ["Vía Láctea", "Andrómeda", "Triángulo", "Sombrero"],
        "correcta": "Vía Láctea",
        "explicacion": "El sistema solar se encuentra dentro de la galaxia Vía Láctea."
    },
    {
        "categoria": "Cultura general",
        "dificultad": 1,
        "pregunta": "¿Cuántas horas tiene un día?",
        "opciones": ["20", "22", "24", "26"],
        "correcta": "24",
        "explicacion": "Un día civil se divide en 24 horas."
    },
    {
        "categoria": "Series",
        "dificultad": 1,
        "pregunta": "¿En qué serie aparecen los personajes Ross, Rachel, Monica y Chandler?",
        "opciones": ["Friends", "Cómo conocí a vuestra madre", "The Big Bang Theory", "Modern Family"],
        "correcta": "Friends",
        "explicacion": "Ross, Rachel, Monica y Chandler forman parte del grupo protagonista de Friends."
    },
    {
        "categoria": "Ciencia",
        "dificultad": 2,
        "pregunta": "¿Qué científico formuló la teoría de la relatividad?",
        "opciones": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Nikola Tesla"],
        "correcta": "Albert Einstein",
        "explicacion": "Albert Einstein desarrolló las teorías de la relatividad especial y general."
    },
    {
        "categoria": "Geografía",
        "dificultad": 1,
        "pregunta": "¿Cuál es la capital de Ecuador?",
        "opciones": ["Guayaquil", "Quito", "Cuenca", "Loja"],
        "correcta": "Quito",
        "explicacion": "Quito es la capital de Ecuador."
    },
    {
        "categoria": "Cine",
        "dificultad": 2,
        "pregunta": "¿Quién dirigió El señor de los anillos?",
        "opciones": ["Peter Jackson", "George Lucas", "James Cameron", "Tim Burton"],
        "correcta": "Peter Jackson",
        "explicacion": "Peter Jackson dirigió la trilogía cinematográfica de El señor de los anillos."
    },
    {
        "categoria": "Deportes",
        "dificultad": 1,
        "pregunta": "¿Qué deporte practicaba Michael Jordan?",
        "opciones": ["Baloncesto", "Fútbol", "Tenis", "Boxeo"],
        "correcta": "Baloncesto",
        "explicacion": "Michael Jordan es considerado uno de los mejores jugadores de baloncesto de la historia."
    },
    {
        "categoria": "Historia",
        "dificultad": 2,
        "pregunta": "¿Qué imperio tuvo su capital en Constantinopla?",
        "opciones": ["Imperio bizantino", "Imperio azteca", "Imperio inca", "Imperio carolingio"],
        "correcta": "Imperio bizantino",
        "explicacion": "Constantinopla fue la capital del Imperio bizantino durante más de mil años."
    },
    {
        "categoria": "Música",
        "dificultad": 2,
        "pregunta": "¿Qué banda británica publicó el álbum Abbey Road?",
        "opciones": ["The Beatles", "Queen", "Pink Floyd", "The Rolling Stones"],
        "correcta": "The Beatles",
        "explicacion": "Abbey Road fue publicado por The Beatles en 1969."
    },
    {
        "categoria": "Tecnología",
        "dificultad": 1,
        "pregunta": "¿Qué dispositivo se utiliza normalmente para mover el cursor de un ordenador?",
        "opciones": ["Ratón", "Router", "Altavoz", "Escáner"],
        "correcta": "Ratón",
        "explicacion": "El ratón permite controlar el puntero y seleccionar elementos en pantalla."
    },
    {
        "categoria": "Animales",
        "dificultad": 2,
        "pregunta": "¿Cuántos corazones tiene un pulpo?",
        "opciones": ["Uno", "Dos", "Tres", "Cuatro"],
        "correcta": "Tres",
        "explicacion": "Los pulpos tienen tres corazones: dos branquiales y uno sistémico."
    },
    {
        "categoria": "Geografía",
        "dificultad": 2,
        "pregunta": "¿Cuál es la capital de Canadá?",
        "opciones": ["Toronto", "Vancouver", "Ottawa", "Montreal"],
        "correcta": "Ottawa",
        "explicacion": "Ottawa es la capital federal de Canadá."
    },
    {
        "categoria": "Cultura general",
        "dificultad": 1,
        "pregunta": "¿Qué estación del año viene después del verano?",
        "opciones": ["Primavera", "Otoño", "Invierno", "Verano"],
        "correcta": "Otoño",
        "explicacion": "En el ciclo anual de estaciones, el otoño sigue al verano."
    },
    {
        "categoria": "Ciencia",
        "dificultad": 2,
        "pregunta": "¿Cuál es el símbolo químico del oro?",
        "opciones": ["Ag", "Au", "Fe", "O"],
        "correcta": "Au",
        "explicacion": "Au procede del término latino aurum."
    },
    {
        "categoria": "Literatura",
        "dificultad": 2,
        "pregunta": "¿Quién escribió El principito?",
        "opciones": ["Antoine de Saint-Exupéry", "Julio Verne", "Victor Hugo", "Albert Camus"],
        "correcta": "Antoine de Saint-Exupéry",
        "explicacion": "El principito fue escrito por Antoine de Saint-Exupéry y publicado en 1943."
    },
    {
        "categoria": "Geografía",
        "dificultad": 1,
        "pregunta": "¿Cuál es la capital de Uruguay?",
        "opciones": ["Montevideo", "Salto", "Punta del Este", "Colonia"],
        "correcta": "Montevideo",
        "explicacion": "Montevideo es la capital y ciudad más poblada de Uruguay."
    },
    {
        "categoria": "Cine",
        "dificultad": 1,
        "pregunta": "¿Qué personaje pronuncia la frase Yo soy tu padre en Star Wars?",
        "opciones": ["Darth Vader", "Yoda", "Obi-Wan Kenobi", "Han Solo"],
        "correcta": "Darth Vader",
        "explicacion": "Darth Vader revela su vínculo con Luke Skywalker en El Imperio contraataca."
    },
    {
        "categoria": "Deportes",
        "dificultad": 2,
        "pregunta": "¿Cuántos puntos vale un triple en baloncesto?",
        "opciones": ["Uno", "Dos", "Tres", "Cuatro"],
        "correcta": "Tres",
        "explicacion": "Un lanzamiento anotado desde fuera de la línea de triple vale tres puntos."
    },
    {
        "categoria": "Historia",
        "dificultad": 2,
        "pregunta": "¿Qué país regaló la Estatua de la Libertad a Estados Unidos?",
        "opciones": ["Francia", "Reino Unido", "Italia", "España"],
        "correcta": "Francia",
        "explicacion": "Francia regaló la Estatua de la Libertad a Estados Unidos en el siglo XIX."
    },
    {
        "categoria": "Música",
        "dificultad": 1,
        "pregunta": "¿Qué cantante interpretó Like a Virgin?",
        "opciones": ["Madonna", "Cher", "Cyndi Lauper", "Whitney Houston"],
        "correcta": "Madonna",
        "explicacion": "Like a Virgin fue uno de los grandes éxitos de Madonna en los años ochenta."
    },
    {
        "categoria": "Animales",
        "dificultad": 1,
        "pregunta": "¿Qué animal tiene una larga trompa?",
        "opciones": ["Elefante", "Hipopótamo", "Rinoceronte", "Jirafa"],
        "correcta": "Elefante",
        "explicacion": "La trompa del elefante sirve para respirar, manipular objetos, beber y comunicarse."
    },
    {
        "categoria": "Ciencia",
        "dificultad": 3,
        "pregunta": "¿Cuál es el elemento químico más abundante del universo?",
        "opciones": ["Oxígeno", "Hidrógeno", "Carbono", "Helio"],
        "correcta": "Hidrógeno",
        "explicacion": "El hidrógeno constituye la mayor parte de la materia ordinaria del universo."
    },
    {
        "categoria": "Tecnología",
        "dificultad": 2,
        "pregunta": "¿Qué significan las siglas CPU?",
        "opciones": ["Central Processing Unit", "Computer Personal User", "Control Program Utility", "Central Power Usage"],
        "correcta": "Central Processing Unit",
        "explicacion": "La CPU es la unidad central de procesamiento de un ordenador."
    },
    {
        "categoria": "Geografía",
        "dificultad": 2,
        "pregunta": "¿Cuál es el desierto cálido más grande del mundo?",
        "opciones": ["Sáhara", "Gobi", "Atacama", "Kalahari"],
        "correcta": "Sáhara",
        "explicacion": "El Sáhara es el desierto cálido más extenso del planeta."
    },
    {
        "categoria": "Cultura general",
        "dificultad": 1,
        "pregunta": "¿Qué número romano representa la letra X?",
        "opciones": ["Cinco", "Diez", "Cincuenta", "Cien"],
        "correcta": "Diez",
        "explicacion": "En numeración romana, X representa el número diez."
    },
    {
        "categoria": "Series",
        "dificultad": 2,
        "pregunta": "¿Cómo se llama el pueblo en el que transcurre Stranger Things?",
        "opciones": ["Hawkins", "Riverdale", "Springfield", "Sunnydale"],
        "correcta": "Hawkins",
        "explicacion": "Stranger Things se desarrolla principalmente en la localidad ficticia de Hawkins."
    },
    {
        "categoria": "Gastronomía",
        "dificultad": 2,
        "pregunta": "¿Cuál es el ingrediente principal de una tortilla española?",
        "opciones": ["Patata", "Arroz", "Pasta", "Pan"],
        "correcta": "Patata",
        "explicacion": "La tortilla española se prepara principalmente con huevo y patata."
    },
    {
        "categoria": "Espacio",
        "dificultad": 2,
        "pregunta": "¿Qué planeta tiene los anillos más visibles?",
        "opciones": ["Saturno", "Marte", "Venus", "Mercurio"],
        "correcta": "Saturno",
        "explicacion": "Saturno posee el sistema de anillos más espectacular y visible del sistema solar."
    },
    {
        "categoria": "Historia",
        "dificultad": 3,
        "pregunta": "¿Qué reina egipcia estuvo vinculada sentimentalmente con Julio César y Marco Antonio?",
        "opciones": ["Cleopatra VII", "Nefertiti", "Hatshepsut", "Nefertari"],
        "correcta": "Cleopatra VII",
        "explicacion": "Cleopatra VII mantuvo alianzas políticas y relaciones con Julio César y Marco Antonio."
    },
    {
        "categoria": "Cine",
        "dificultad": 2,
        "pregunta": "¿Qué película cuenta la historia de un parque habitado por dinosaurios clonados?",
        "opciones": ["Jurassic Park", "Godzilla", "King Kong", "Avatar"],
        "correcta": "Jurassic Park",
        "explicacion": "Jurassic Park presenta un parque temático con dinosaurios creados mediante ingeniería genética."
    }
]
```
