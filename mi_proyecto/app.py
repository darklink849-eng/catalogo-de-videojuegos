import sqlite3
import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Esto asegura que juegos.db siempre se cree dentro de la misma carpeta de tu proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "juegos.db")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Borra la tabla vieja si existía para cargar los 150 juegos nuevos
    cursor.execute("DROP TABLE IF EXISTS videojuegos")
    
    # Crea la tabla limpia
    cursor.execute('''
        CREATE TABLE videojuegos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            consola TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            precio INTEGER NOT NULL,
            precio_promo INTEGER,
            disponible INTEGER NOT NULL,
            imagen TEXT NOT NULL
        )
    ''')

    juegos_tienda_masiva = [
        # ==========================================
        # PLAYSTATION 2 (50 JUEGOS CLÁSICOS E ICONICOS)
        # ==========================================
        ("God of War II", "PS2", "[MUY BUENO] Kratos viaja al fin de la tierra para derrotar a las Hermanas del Destino. Una obra maestra absoluta de la acción hack and slash con gráficos al límite de la PS2 y jefes colosales.", 49, 44, 1, "https://placehold.co/300x400/111/00ffcc?text=God+of+War+II"),
        ("Grand Theft Auto: San Andreas", "PS2", "[RECOMENDADO] Regresa a Los Santos con CJ en el sandbox definitivo. Mundos abiertos gigantescos, personalización total y una banda sonora legendaria.", 50, 42, 1, "https://placehold.co/300x400/111/00ffcc?text=GTA+San+Andreas"),
        ("Resident Evil 4", "PS2", "[MUY BUENO] Leon S. Kennedy debe rescatar a la hija del presidente en un pueblo europeo maldito. El juego que revolucionó la acción y el terror en tercera persona.", 50, 44, 1, "https://placehold.co/300x400/111/00ffcc?text=Resident+Evil+4"),
        ("Shadow of the Colossus", "PS2", "[NUEVO] Una experiencia artística única. Explora un valle prohibido montado a caballo para derrotar a 16 gigantes majestuosos y revivir a una joven.", 48, 40, 1, "https://placehold.co/300x400/111/00ffcc?text=Shadow+of+Colossus"),
        ("Dragon Ball Z: Budokai Tenkaichi 3", "PS2", "[MUY BUENO] El simulador de combates de anime definitivo. Más de 160 personajes, transformaciones en tiempo real y batallas aéreas frenéticas.", 55, 48, 1, "https://placehold.co/300x400/111/00ffcc?text=DBZ+Tenkaichi+3"),
        ("Metal Gear Solid 3: Snake Eater", "PS2", "[MUY BUENO] Infiltración y supervivencia extrema en la selva soviética durante la Guerra Fría. Una joya maestra dirigida por Hideo Kojima.", 50, 44, 1, "https://placehold.co/300x400/111/00ffcc?text=MGS+3"),
        ("Silent Hill 2", "PS2", "[RECOMENDADO] Obra cumbre del terror psicológico. James Sunderland busca a su esposa fallecida en un pueblo cubierto de niebla y culpa.", 55, 48, 0, "https://placehold.co/300x400/111/00ffcc?text=Silent+Hill+2"),
        ("Final Fantasy X", "PS2", "[RECOMENDADO] Acompaña a Tidus y Yuna en un viaje emotivo por Spira. Sistema de combate estratégico por turnos y una historia de amor inolvidable.", 48, 40, 1, "https://placehold.co/300x400/111/00ffcc?text=Final+Fantasy+X"),
        ("Bully", "PS2", "[NUEVO] Vive las travesuras y jerarquías sociales de la academia Bullworth con Jimmy Hopkins en un sandbox escolar único y divertidísimo.", 45, 35, 1, "https://placehold.co/300x400/111/00ffcc?text=Bully"),
        ("Need for Speed: Most Wanted", "PS2", "[MUY BUENO] Conviértete en el corredor más buscado en intensas persecuciones policiales. Modifica deportivos y asciende en la Blacklist.", 50, 43, 1, "https://placehold.co/300x400/111/00ffcc?text=NFS+Most+Wanted"),
        ("Gran Turismo 4", "PS2", "[RECOMENDADO] El simulador de conducción definitivo con más de 700 vehículos y pistas hiperrealistas para los amantes del motor.", 45, 39, 1, "https://placehold.co/300x400/111/00ffcc?text=Gran+Turismo+4"),
        ("God of War", "PS2", "[MUY BUENO] El inicio de la brutal venganza de Kratos contra el dios Ares en la Grecia mitológica.", 45, 39, 1, "https://placehold.co/300x400/111/00ffcc?text=God+of+War+1"),
        ("Devil May Cry 3", "PS2", "[MUY BUENO] Dante se enfrenta a su hermano Vergil con un sistema de combate vertiginoso lleno de estilo y armas alucinantes.", 45, 38, 1, "https://placehold.co/300x400/111/00ffcc?text=Devil+May+Cry+3"),
        ("Kingdom Hearts II", "PS2", "[RECOMENDADO] Sora, Donald y Goofy viajan por mundos de Disney combatiendo a la Organización XIII en un JRPG mágico.", 50, 42, 1, "https://placehold.co/300x400/111/00ffcc?text=Kingdom+Hearts+II"),
        ("Burnout 3: Takedown", "PS2", "[MUY BUENO] Carreras arcade frenéticas donde destruir a tus rivales mediante espectaculares choques es la clave para ganar.", 40, 35, 1, "https://placehold.co/300x400/111/00ffcc?text=Burnout+3"),
        ("Resident Evil Code: Veronica X", "PS2", "[RECOMENDADO] Claire Redfield busca a su hermano en una isla militar infestada de zombis y horrores biológicos.", 48, 40, 1, "https://placehold.co/300x400/111/00ffcc?text=RE+Code+Veronica"),
        ("Tekken 5", "PS2", "[MUY BUENO] El torneo del Puño de Hierro con gráficos soberbios, modos divertidísimos y una jugabilidad de lucha impecable.", 45, 38, 1, "https://placehold.co/300x400/111/00ffcc?text=Tekken+5"),
        ("Mortal Kombat: Shaolin Monks", "PS2", "[RECOMENDADO] Aventura épica de acción y artes marciales cooperativa protagonizada por Liu Kang y Kung Lao.", 50, 45, 1, "https://placehold.co/300x400/111/00ffcc?text=MK+Shaolin+Monks"),
        ("Prince of Persia: The Sands of Time", "PS2", "[NUEVO] Controla las arenas del tiempo para resolver puzles, caminar por paredes y evitar trampas letales en Persia.", 42, 36, 1, "https://placehold.co/300x400/111/00ffcc?text=Prince+of+Persia"),
        ("Okami", "PS2", "[NUEVO] Conviértete en la loba celestial Amaterasu y devuelve el color y la vida a Japón usando un pincel mágico.", 45, 39, 1, "https://placehold.co/300x400/111/00ffcc?text=Okami"),
        ("Ratchet & Clank: Up Your Arsenal", "PS2", "[RECOMENDADO] Acción, plataformas y un arsenal de armas descabelladas para salvar la galaxia junto a un carismático lombax.", 42, 36, 1, "https://placehold.co/300x400/111/00ffcc?text=Ratchet+and+Clank"),
        ("Jak and Daxter: The Precursor Legacy", "PS2", "[NUEVO] Explora un colorido mundo abierto lleno de secretos, plataformas fluidas y misterios antiguos.", 40, 34, 1, "https://placehold.co/300x400/111/00ffcc?text=Jak+and+Daxter"),
        ("Grand Theft Auto: Vice City", "PS2", "[MUY BUENO] Sumérgete en los años 80, los neones y la mafia de Miami con Tommy Vercetti y una banda sonora inolvidable.", 48, 40, 1, "https://placehold.co/300x400/111/00ffcc?text=GTA+Vice+City"),
        ("Black", "PS2", "[MUY BUENO] Un shooter en primera persona con destrucción de escenarios brutal y un diseño de armas sumamente realista.", 45, 39, 1, "https://placehold.co/300x400/111/00ffcc?text=Black+PS2"),
        ("Tony Hawk's Pro Skater 4", "PS2", "[RECOMENDADO] Realiza trucos imposibles, cadenas de puntos y explora niveles abiertos con los mejores skaters del mundo.", 40, 35, 1, "https://placehold.co/300x400/111/00ffcc?text=Tony+Hawk+4"),
        ("Guitar Hero II", "PS2", "[RECOMENDADO] Conecta tu guitarra de juguete y toca los mejores riffs del rock clásico frente a multitudes enfervorizadas.", 45, 38, 1, "https://placehold.co/300x400/111/00ffcc?text=Guitar+Hero+II"),
        ("Def Jam: Fight for NY", "PS2", "[MUY BUENO] Combates callejeros brutales en clubs clandestinos junto a leyendas del hip hop y personalización extrema.", 50, 44, 1, "https://placehold.co/300x400/111/00ffcc?text=Def+Jam+FFNY"),
        ("Persona 4", "PS2", "[MUY BUENO] Investiga misteriosos asesinatos en un pueblo rural japonés alternando tu vida escolar con mazmorras llenas de sombras.", 50, 44, 1, "https://placehold.co/300x400/111/00ffcc?text=Persona+4"),
        ("Final Fantasy XII", "PS2", "[RECOMENDADO] Una aventura política y fantástica colosal en el mundo de Ivalice con un sistema de gambitos automatizados.", 48, 40, 1, "https://placehold.co/300x400/111/00ffcc?text=Final+Fantasy+XII"),
        ("Silent Hill 3", "PS2", "[RECOMENDADO] Heather Mason se adentra en pesadillas grotescas relacionadas con su misterioso pasado y cultos oscuros.", 50, 44, 1, "https://placehold.co/300x400/111/00ffcc?text=Silent+Hill+3"),
        ("Zone of the Enders: The 2nd Runner", "PS2", "[NUEVO] Combates espaciales de robots gigantes ultra rápidos con una dirección artística y fluidez visual impresionante.", 45, 38, 1, "https://placehold.co/300x400/111/00ffcc?text=ZOE+2"),
        ("Onimusha 3: Demon Siege", "PS2", "[MUY BUENO] Samuráis contra demonios en el Japón feudal y en pleno París actual con Jean Reno como protagonista.", 45, 39, 1, "https://placehold.co/300x400/111/00ffcc?text=Onimusha+3"),
        ("Bully: Scholarship Edition", "PS2", "[NUEVO] Versión extendida con nuevas clases y misiones en la academia más alocada de los videojuegos.", 45, 38, 1, "https://placehold.co/300x400/111/00ffcc?text=Bully+SE"),
        ("Kingdom Hearts", "PS2", "[RECOMENDADO] El inicio del cruce mágico entre los mundos de Final Fantasy y Disney contra los sincorazón.", 45, 38, 1, "https://placehold.co/300x400/111/00ffcc?text=Kingdom+Hearts+1"),
        ("Baldur's Gate: Dark Alliance", "PS2", "[NUEVO] Acción y rol clásico de mazmorras con vista isométrica lleno de tesoros, hechizos y monstruos.", 42, 36, 1, "https://placehold.co/300x400/111/00ffcc?text=Baldurs+Gate"),
        ("Champions of Norrath", "PS2", "[RECOMENDADO] Hack and slash cooperativo profundo ambientado en el universo fantástico de EverQuest.", 45, 39, 1, "https://placehold.co/300x400/111/00ffcc?text=Champions+of+Norrath"),
        ("Star Wars: Battlefront II (2005)", "PS2", "[MUY BUENO] Participa en las batallas galácticas más emblemáticas de la saga tanto a pie como pilotando cazas espaciales.", 48, 42, 1, "https://placehold.co/300x400/111/00ffcc?text=SW+Battlefront+II"),
        ("Medal of Honor: Frontline", "PS2", "[RECOMENDADO] Vive el desembarco de Normandía y misiones bélicas históricas con una atmósfera cinematográfica única.", 40, 35, 1, "https://placehold.co/300x400/111/00ffcc?text=MOH+Frontline"),
        ("Gran Turismo 3: A-Spec", "PS2", "[RECOMENDADO] El título que definió el automovilismo virtual en la consola con físicas y gráficos rompedores en su día.", 40, 34, 1, "https://placehold.co/300x400/111/00ffcc?text=Gran+Turismo+3"),
        ("WWE SmackDown! Here Comes the Pain", "PS2", "[MUY BUENO] El simulador de Lucha Libre más divertido, frenético y completo de toda la era dorada de la WWE.", 45, 39, 1, "https://placehold.co/300x400/111/00ffcc?text=WWE+SmackDown"),
        ("Ace Combat 5: The Unsung War", "PS2", "[NUEVO] Combates aéreos tácticos y una historia militar intensa a los mandos de los mejores cazas de combate.", 42, 36, 1, "https://placehold.co/300x400/111/00ffcc?text=Ace+Combat+5"),
        ("Metal Gear Solid 2: Sons of Liberty", "PS2", "[MUY BUENO] Infiltración en una planta petrolífera marítima con giros argumentales alucinantes y gráficos revolucionarios.", 45, 39, 1, "https://placehold.co/300x400/111/00ffcc?text=MGS+2"),
        ("Rayman 3: Hoodlum Havoc", "PS2", "[NUEVO] Plataformas colorido, divertido y lleno de humor con el héroe sin extremidades.", 38, 32, 1, "https://placehold.co/300x400/111/00ffcc?text=Rayman+3"),
        ("Soulcalibur II", "PS2", "[RECOMENDADO] El juego de armas y espadas definitivo con un combate técnico extraordinario.", 42, 36, 1, "https://placehold.co/300x400/111/00ffcc?text=Soulcalibur+II"),
        ("Viewtiful Joe", "PS2", "[NUEVO] Acción beat 'em up en 2.5D con estética de cómic y superpoderes de cine como cámara lenta y aceleración.", 40, 34, 1, "https://placehold.co/300x400/111/00ffcc?text=Viewtiful+Joe"),
        ("SSX 3", "PS2", "[RECOMENDADO] Desciende por enormes montañas nevadas haciendo trucos extremos de snowboard con música electrónica brutal.", 42, 36, 1, "https://placehold.co/300x400/111/00ffcc?text=SSX+3"),
        ("Makai Kingdom", "PS2", "[NUEVO] Estrategia táctica RPG con opciones de personalización absurdas y sentido del humor desternillante.", 45, 38, 1, "https://placehold.co/300x400/111/00ffcc?text=Makai+Kingdom"),
        ("Disgaea: Hour of Darkness", "PS2", "[RECOMENDADO] El clásico RPG táctico donde puedes subir niveles hasta el 9999 y desatar ataques masivos devastadores.", 45, 39, 1, "https://placehold.co/300x400/111/00ffcc?text=Disgaea"),
        ("X-Men Legends II: Rise of Apocalypse", "PS2", "[NUEVO] Rol y acción cooperativa manejando a los mutantes más poderosos de Marvel contra Apocalipsis.", 42, 36, 1, "https://placehold.co/300x400/111/00ffcc?text=X-Men+Legends+II"),
        ("Castlevania: Curse of Darkness", "PS2", "[RECOMENDADO] Hector busca venganza invocando demonios fieles en un castillo gótico lleno de misterios y acción.", 45, 39, 1, "https://placehold.co/300x400/111/00ffcc?text=Castlevania+COD"),

        # ==========================================
        # PLAYSTATION 3 (50 JUEGOS DE LA ERA HD)
        # ==========================================
        ("The Last of Us", "PS3", "[MUY BUENO] Joel y Ellie cruzan un EE.UU. devastado por una pandemia. Narrativa cinematográfica insuperable y tensión absoluta.", 80, 65, 1, "https://placehold.co/300x400/111/00ffcc?text=The+Last+of+Us"),
        ("Grand Theft Auto V", "PS3", "[MUY BUENO] Tres criminales con vidas entrelazadas planean grandes atracos en el mundo abierto de Los Santos.", 75, 60, 1, "https://placehold.co/300x400/111/00ffcc?text=GTA+V+PS3"),
        ("God of War III", "PS3", "[MUY BUENO] El ajuste de cuentas definitivo de Kratos contra los dioses del Olimpo con escala titánica y gráficos increíbles.", 75, 60, 1, "https://placehold.co/300x400/111/00ffcc?text=God+of+War+III"),
        ("Red Dead Redemption", "PS3", "[RECOMENDADO] Vive el ocaso del salvaje oeste con John Marston obligado a cazar a los miembros de su antigua banda.", 75, 62, 1, "https://placehold.co/300x400/111/00ffcc?text=Red+Dead+Redemption"),
        ("Uncharted 2: Among Thieves", "PS3", "[MUY BUENO] Nathan Drake persigue la piedra Cintamani por el Himalaya en una aventura cinematográfica imparable.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Uncharted+2"),
        ("Batman: Arkham City", "PS3", "[RECOMENDADO] El Caballero de la Noche patrulla una prisión repleta de criminales dementes en Gotham.", 70, 55, 1, "https://placehold.co/300x400/111/00ffcc?text=Batman+Arkham+City"),
        ("Dark Souls", "PS3", "[MUY BUENO] RPG de acción de fantasía oscura legendario. Prepárate para morir y aprender en un mundo interconectado.", 75, 62, 1, "https://placehold.co/300x400/111/00ffcc?text=Dark+Souls"),
        ("BioShock Infinite", "PS3", "[RECOMENDADO] Rescata a Elizabeth en la ciudad flotante en el cielo de Columbia en una trama espaciotemporal alucinante.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=BioShock+Infinite"),
        ("Call of Duty: Black Ops II", "PS3", "[MUY BUENO] Acción bélica entre el pasado y el futuro ciberespacial con el modo zombis más adictivo.", 80, 65, 1, "https://placehold.co/300x400/111/00ffcc?text=COD+Black+Ops+II"),
        ("The Elder Scrolls V: Skyrim", "PS3", "[RECOMENDADO] Conviértete en el Sangre de Dragón y explora con total libertad un vasto mundo abierto medieval nevado.", 70, 55, 1, "https://placehold.co/300x400/111/00ffcc?text=Skyrim"),
        ("Uncharted 3: La traición de Drake", "PS3", "[RECOMENDADO] Nathan busca la legendaria 'Atlántida de las Arenas' en desiertos y escenarios dinámicos espectaculares.", 70, 55, 1, "https://placehold.co/300x400/111/00ffcc?text=Uncharted+3"),
        ("Uncharted: El tesoro de Drake", "PS3", "[NUEVO] El inicio de la legendaria saga de cazatesoros en una isla tropical llena de piratas y misterios.", 60, 48, 1, "https://placehold.co/300x400/111/00ffcc?text=Uncharted+1"),
        ("Metal Gear Solid 4: Guns of the Patriots", "PS3", "[MUY BUENO] La misión final de Solid Snake en un campo de batalla futurista lleno de emociones y cinemáticas épicas.", 70, 58, 1, "https://placehold.co/300x400/111/00ffcc?text=MGS+4"),
        ("Demon's Souls", "PS3", "[RECOMENDADO] El oscuro y desafiante precursor de los juegos tipo Souls ambientado en el reino maldito de Boletaria.", 70, 58, 1, "https://placehold.co/300x400/111/00ffcc?text=Demons+Souls"),
        ("Mass Effect 2", "PS3", "[MUY BUENO] Reúne a la mejor tripulación de la galaxia para una misión suicida contra los Segadores en este RPG espacial.", 70, 55, 1, "https://placehold.co/300x400/111/00ffcc?text=Mass+Effect+2"),
        ("Bioshock", "PS3", "[MUY BUENO] Explora la ciudad submarina distópica de Rapture en un shooter narrativo lleno de giros inolvidables.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Bioshock+1"),
        ("Borderlands 2", "PS3", "[RECOMENDADO] Shooter looter cooperativo frenético con millones de armas y el carismático villano Handsome Jack en Pandora.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Borderlands+2"),
        ("Portal 2", "PS3", "[MUY BUENO] Puzles alucinantes basados en portales espaciales y un humor negro desternillante junto a GLaDOS.", 65, 52, 1, "https://placehold.co/300x400/111/00ffcc?text=Portal+2"),
        ("Far Cry 3", "PS3", "[MUY BUENO] Sobrevive en una isla tropical dominada por piratas desquiciados y el inolvidable villano Vaas Montenegro.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Far+Cry+3"),
        ("Assassin's Creed II", "PS3", "[RECOMENDADO] Conviértete en Ezio Auditore y venga a su familia recorriendo el Renacimiento italiano en Florencia y Venecia.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=AC+II"),
        ("Assassin's Creed IV: Black Flag", "PS3", "[MUY BUENO] Navega por el Caribe como pirata y asesino junto a Edward Kenway en barcos y batallas navales.", 70, 55, 1, "https://placehold.co/300x400/111/00ffcc?text=AC+Black+Flag+PS3"),
        ("Heavy Rain", "PS3", "[RECOMENDADO] Thriller interactivo donde cada decisión puede salvar o condenar la vida de los personajes ante el Asesino del Origami.", 60, 48, 1, "https://placehold.co/300x400/111/00ffcc?text=Heavy+Rain"),
        ("Gran Turismo 5", "PS3", "[RECOMENDADO] Simulación de automovilismo masiva con miles de coches y licencias oficiales de competición.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Gran+Turismo+5"),
        ("Dead Space", "PS3", "[MUY BUENO] Terror espacial claustrofóbico a bordo de la nave minera USG Ishimura frente a necromorfos horribles.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Dead+Space"),
        ("Fallout 3", "PS3", "[RECOMENDADO] Explora el yermo nuclear de Washington D.C. tras el apocalipsis en un RPG de mundo abierto colosal.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Fallout+3"),
        ("Batman: Arkham Asylum", "PS3", "[MUY BUENO] El Joker toma el control del asilo Arkham y Batman debe restablecer el orden usando sigilo y fuerza.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Arkham+Asylum"),
        ("LittleBigPlanet", "PS3", "[NUEVO] Juega, crea y comparte niveles de plataformas con el tierno muñeco de trapo Sackboy.", 55, 45, 1, "https://placehold.co/300x400/111/00ffcc?text=LittleBigPlanet"),
        ("Infamous", "PS3", "[NUEVO] Adquiere poderes eléctricos tras una explosión y decide si ser el héroe o el villano de Empire City.", 60, 48, 1, "https://placehold.co/300x400/111/00ffcc?text=Infamous"),
        ("Infamous 2", "PS3", "[RECOMENDADO] Cole MacGrath viaja a New Marais para enfrentar a una nueva y colosal amenaza mutante con nuevos poderes.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Infamous+2"),
        ("Killzone 2", "PS3", "[MUY BUENO] Intenso shooter bélico futurista contra el imperio hostil Helghast en su planeta natal.", 60, 45, 1, "https://placehold.co/300x400/111/00ffcc?text=Killzone+2"),
        ("Resistance: Fall of Man", "PS3", "[NUEVO] Una invasión alienígena quimera arrasa la Tierra alternativa de los años 50 en un juego de disparos frenético.", 55, 42, 1, "https://placehold.co/300x400/111/00ffcc?text=Resistance"),
        ("Dragon Age: Origins", "PS3", "[RECOMENDADO] RPG de fantasía medieval épico con decisiones profundas y combates tácticos en equipo.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Dragon+Age"),
        ("Max Payne 3", "PS3", "[MUY BUENO] Acción balística en tercera persona ambientada en las favelas de São Paulo con el sistema de físicas Bullet Time.", 70, 55, 1, "https://placehold.co/300x400/111/00ffcc?text=Max+Payne+3"),
        ("L.A. Noire", "PS3", "[RECOMENDADO] Investiga crímenes e interrogatorios analizando expresiones faciales en el Hollywood de los años 40.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=LA+Noire"),
        ("Skate 3", "PS3", "[NUEVO] Realiza trucos de patineta divertidísimos y caídas físicas hilarantes en la ciudad abierta de Port Carverton.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Skate+3"),
        ("Castlevania: Lords of Shadow", "PS3", "[RECOMENDADO] Gabriel Belmont se enfrenta a las fuerzas de la oscuridad con su cruz de combate en una aventura gótica.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Castlevania+LOS"),
        ("Mafia II", "PS3", "[RECOMENDADO] Vive el ascenso y caída de un gánster en una recreación perfecta de los años 40 y 50 en Estados Unidos.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Mafia+II"),
        ("Ninja Gaiden Sigma", "PS3", "[NUEVO] Acción samurái ultrarrápida y de alta exigencia técnica protagonizada por Ryu Hayabusa.", 60, 48, 1, "https://placehold.co/300x400/111/00ffcc?text=Ninja+Gaiden+Sigma"),
        ("Dark Souls II", "PS3", "[RECOMENDADO] Continúa la desafiante saga de rol en el reino maldito de Drangleic buscando una cura para la maldición.", 75, 60, 1, "https://placehold.co/300x400/111/00ffcc?text=Dark+Souls+II"),
        ("Mirror's Edge", "PS3", "[NUEVO] Parkour en primera persona en una ciudad futurista minimalista donde correr es tu única arma para sobrevivir.", 55, 42, 1, "https://placehold.co/300x400/111/00ffcc?text=Mirrors+Edge"),
        ("Dead Space 2", "PS3", "[MUY BUENO] Isaac Clarke despierta en una estación espacial infestada de necromorfos con terror psicológico mejorado.", 65, 52, 1, "https://placehold.co/300x400/111/00ffcc?text=Dead+Space+2"),
        ("Grand Theft Auto IV", "PS3", "[MUY BUENO] Niko Bellic llega a Liberty City persiguiendo el sueño americano junto a su primo Roman en un clásico maduro.", 70, 55, 1, "https://placehold.co/300x400/111/00ffcc?text=GTA+IV"),
        ("Metal Gear Rising: Revengeance", "PS3", "[MUY BUENO] Raiden desata cortes de alta frecuencia con su espada láser en un hack and slash frenético y musicalmente brutal.", 65, 52, 1, "https://placehold.co/300x400/111/00ffcc?text=MGR+Revengeance"),
        ("Batman: Arkham Origins", "PS3", "[RECOMENDADO] Ocho asesinos intentan cazar a un joven Batman en Gotham durante la noche de Navidad.", 65, 52, 1, "https://placehold.co/300x400/111/00ffcc?text=Arkham+Origins"),
        ("Soulcalibur IV", "PS3", "[NUEVO] Batallas de armas épicas con invitados estelares como Darth Vader en el bando de PlayStation.", 60, 48, 1, "https://placehold.co/300x400/111/00ffcc?text=Soulcalibur+IV"),
        ("WWE '13", "PS3", "[NUEVO] Revive la legendaria 'Attitude Era' de la lucha libre con las superestrellas más emblemáticas de la historia.", 60, 48, 1, "https://placehold.co/300x400/111/00ffcc?text=WWE+13"),
        ("Silent Hill: Downpour", "PS3", "[NUEVO] Murphy Pendleton naufraga y llega al pueblo maldito enfrentándose a sus miedos y secretos más oscuros.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Silent+Hill+Downpour"),
        ("PES 2013", "PS3", "[RECOMENDADO] Uno de los juegos de fútbol más queridos y recordados por su jugabilidad clásica y divertida.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=PES+2013"),
        ("FIFA 18", "PS3", "[NUEVO] Fútbol de la clásica era deportiva con plantillas actualizadas y modos de torneo imperdibles.", 60, 45, 1, "https://placehold.co/300x400/111/00ffcc?text=FIFA+18"),
        ("Spec Ops: The Line", "PS3", "[MUY BUENO] Un shooter bélico en Dubái sepultado por la arena con una narrativa psicológica profunda sobre la guerra.", 65, 50, 1, "https://placehold.co/300x400/111/00ffcc?text=Spec+Ops+The+Line"),

        # ==========================================
        # PLAYSTATION 4 (50 JUEGOS DE ÚLTIMA GENERACIÓN)
        # ==========================================
        ("God of War (2018)", "PS4", "[MUY BUENO] Kratos cuida de su hijo Atreus en los brutales bosques nórdicos. Combate visceral con hacha y plano secuencia único.", 120, 99, 1, "https://placehold.co/300x400/111/00ffcc?text=God+of+War+2018"),
        ("Marvel's Spider-Man", "PS4", "[MUY BUENO] Balancéate con total fluidez por una Manhattan vibrante como Peter Parker enfrentando a villanos clásicos.", 130, 105, 1, "https://placehold.co/300x400/111/00ffcc?text=Spider-Man+PS4"),
        ("Red Dead Redemption 2", "PS4", "[MUY BUENO] Obra maestra hiperrealista. Acompaña a Arthur Morgan y la banda de Dutch huyendo de la ley en el viejo oeste.", 145, 119, 1, "https://placehold.co/300x400/111/00ffcc?text=RDR+2"),
        ("The Witcher 3: Wild Hunt", "PS4", "[MUY BUENO] El brujo Geralt de Rivia busca a su hija adoptiva en un mundo abierto masivo repleto de monstruos y magia.", 115, 90, 1, "https://placehold.co/300x400/111/00ffcc?text=The+Witcher+3"),
        ("Bloodborne", "PS4", "[MUY BUENO] Adéntrate en la maldita y tétrica ciudad gótica de Yharnam con un sistema de combate agresivo y terrorífico.", 110, 90, 1, "https://placehold.co/300x400/111/00ffcc?text=Bloodborne"),
        ("Elden Ring", "PS4", "[MUY BUENO] Explora las inmensas Tierras Intermedias a caballo en la cumbre de los mundos abiertos de acción junto a George R.R. Martin.", 180, 155, 1, "https://placehold.co/300x400/111/00ffcc?text=Elden+Ring"),
        ("Ghost of Tsushima", "PS4", "[RECOMENDADO] Conviértete en el Fantasma y libera la isla de Tsushima de la invasión mongola usando honor o astucia.", 150, 125, 1, "https://placehold.co/300x400/111/00ffcc?text=Ghost+of+Tsushima"),
        ("Horizon Zero Dawn", "PS4", "[RECOMENDADO] Aloy caza criaturas robóticas colosales descubriendo los secretos de un mundo postapocalíptico fascinante.", 100, 80, 1, "https://placehold.co/300x400/111/00ffcc?text=Horizon+Zero+Dawn"),
        ("Uncharted 4: A Thief's End", "PS4", "[MUY BUENO] La emotiva y espectacular conclusión a las aventuras de Nathan Drake en busca de un gran tesoro pirata.", 105, 85, 1, "https://placehold.co/300x400/111/00ffcc?text=Uncharted+4"),
        ("Persona 5 Royal", "PS4", "[MUY BUENO] Lidera a los Ladrones Fantasma en Tokio en un JRPG estilizado con jazz inigualable y 100 horas de contenido.", 140, 115, 1, "https://placehold.co/300x400/111/00ffcc?text=Persona+5+Royal"),
        ("The Last of Us Part II", "PS4", "[MUY BUENO] Una secuela desgarradora e intensa sobre las consecuencias de la venganza protagonizada por Ellie.", 135, 110, 1, "https://placehold.co/300x400/111/00ffcc?text=The+Last+of+Us+II"),
        ("Sekiro: Shadows Die Twice", "PS4", "[MUY BUENO] Domina el parpadeo de la katana en el Japón feudal sengoku en un juego de acción de máxima exigencia.", 140, 120, 1, "https://placehold.co/300x400/111/00ffcc?text=Sekiro"),
        ("Resident Evil 2 Remake", "PS4", "[RECOMENDADO] Regresa a Raccoon City en una reimaginación terrorífica y fotorrealista con Leon y Claire.", 110, 89, 1, "https://placehold.co/300x400/111/00ffcc?text=RE2+Remake"),
        ("Monster Hunter: World", "PS4", "[RECOMENDADO] Caza bestias gigantescas en ecosistemas vivos colaborando con amigos y creando armas formidables.", 100, 80, 1, "https://placehold.co/300x400/111/00ffcc?text=Monster+Hunter+World"),
        ("Detroit: Become Human", "PS4", "[RECOMENDADO] Tus decisiones definen el destino y la humanidad de tres androides en el futuro de Detroit.", 105, 85, 1, "https://placehold.co/300x400/111/00ffcc?text=Detroit+Become+Human"),
        ("Dark Souls III", "PS4", "[MUY BUENO] El cierre épico de la saga Souls con combates intensos contra señores de la ceniza y jefes legendarios.", 120, 99, 1, "https://placehold.co/300x400/111/00ffcc?text=Dark+Souls+III"),
        ("Grand Theft Auto V", "PS4", "[MUY BUENO] Versión mejorada de Los Santos con gráficos en alta definición y modo en primera persona completo.", 110, 89, 1, "https://placehold.co/300x400/111/00ffcc?text=GTA+V+PS4"),
        ("Resident Evil 7: Biohazard", "PS4", "[RECOMENDADO] Terror en primera persona en una mansión pantanosa de Luisiana frente a la perturbadora familia Baker.", 100, 80, 1, "https://placehold.co/300x400/111/00ffcc?text=RE7+Biohazard"),
        ("Marvel's Spider-Man: Miles Morales", "PS4", "[NUEVO] Miles Morales descubre nuevos poderes eléctricos y protege Harlem como el nuevo Spider-Man.", 110, 90, 1, "https://placehold.co/300x400/111/00ffcc?text=Miles+Morales"),
        ("Crash Bandicoot N. Sane Trilogy", "PS4", "[RECOMENDADO] Los tres clásicos de plataformas remasterizados con un diseño visual colorido y desafiante.", 115, 95, 1, "https://placehold.co/300x400/111/00ffcc?text=Crash+Trilogy"),
        ("Yakuza 0", "PS4", "[RECOMENDADO] Acción criminal y drama mafioso en los coloridos distritos de Tokio y Osaka en los años 80.", 95, 79, 1, "https://placehold.co/300x400/111/00ffcc?text=Yakuza+0"),
        ("Days Gone", "PS4", "[RECOMENDADO] Sobrevive en una motocicleta a hordas masivas de infectados en un mundo postapocalíptico de Oregón.", 110, 89, 1, "https://placehold.co/300x400/111/00ffcc?text=Days+Gone"),
        ("Nioh", "PS4", "[NUEVO] Acción samurái desafiante con elementos de rol y yokais mitológicos en el Japón del periodo Sengoku.", 100, 80, 1, "https://placehold.co/300x400/111/00ffcc?text=Nioh"),
        ("NieR: Automata", "PS4", "[MUY BUENO] Androides luchando contra máquinas alienígenas en una historia filosófica inolvidable protagonizada por 2B.", 115, 95, 1, "https://placehold.co/300x400/111/00ffcc?text=Nier+Automata"),
        ("Control", "PS4", "[NUEVO] Usa poderes telequinéticos y armas cambiantes en la Agencia Federal de Control paranormal.", 105, 85, 1, "https://placehold.co/300x400/111/00ffcc?text=Control"),
        ("Death Stranding", "PS4", "[RECOMENDADO] Conecta un mundo fragmentado entregando paquetes a través de paisajes desoladores bajo la dirección de Hideo Kojima.", 110, 89, 1, "https://placehold.co/300x400/111/00ffcc?text=Death+Stranding"),
        ("Final Fantasy VII Remake", "PS4", "[MUY BUENO] Reimaginación espectacular de Midgar con combates en tiempo real y personajes entrañables.", 120, 99, 1, "https://placehold.co/300x400/111/00ffcc?text=FFVII+Remake"),
        ("Dragon Ball FighterZ", "PS4", "[RECOMENDADO] Combates en 2.5D espectaculares y fieles al anime creados por Arc System Works.", 115, 90, 1, "https://placehold.co/300x400/111/00ffcc?text=DB+FighterZ"),
        ("Mortal Kombat 11", "PS4", "[MUY BUENO] Peleas brutales con fatalities increíbles y personalización profunda de luchadores.", 110, 88, 1, "https://placehold.co/300x400/111/00ffcc?text=Mortal+Kombat+11"),
        ("Star Wars Jedi: Fallen Order", "PS4", "[RECOMENDADO] Un padawan Jedi sobrevive a la purga imperial usando su espada láser y la fuerza en planetas lejanos.", 110, 89, 1, "https://placehold.co/300x400/111/00ffcc?text=Jedi+Fallen+Order"),
        ("Borderlands 3", "PS4", "[NUEVO] Dispara y saquea con millones de armas en una alocada aventura espacial interplanetaria.", 105, 85, 1, "https://placehold.co/300x400/111/00ffcc?text=Borderlands+3"),
        ("Fallout 4", "PS4", "[RECOMENDADO] Construye refugios y sobrevive en el yermo postnuclear de Boston buscando a tu hijo.", 95, 75, 1, "https://placehold.co/300x400/111/00ffcc?text=Fallout+4"),
        ("Far Cry 5", "PS4", "[NUEVO] Libera un condado de Montana dominado por un culto fanático religioso armado hasta los dientes.", 105, 85, 1, "https://placehold.co/300x400/111/00ffcc?text=Far+Cry+5"),
        ("Assassin's Creed Odyssey", "PS4", "[RECOMENDADO] Escribe tu propia epopeya griega como mercenario espartano o ateniense en el mar Egeo.", 110, 89, 1, "https://placehold.co/300x400/111/00ffcc?text=AC+Odyssey"),
        ("Assassin's Creed Valhalla", "PS4", "[NUEVO] Conquista tierras inglesas liderando a tu clan vikingo junto a Eivor en incursiones brutales.", 120, 99, 1, "https://placehold.co/300x400/111/00ffcc?text=AC+Valhalla"),
        ("Resident Evil 3 Remake", "PS4", "[NUEVO] Jill Valentine escapa de Raccoon City huyendo del implacable monstruo Némesis.", 105, 85, 1, "https://placehold.co/300x400/111/00ffcc?text=RE3+Remake"),
        ("LittleBigPlanet 3", "PS4", "[NUEVO] Nuevos personajes jugables con habilidades únicas en niveles de plataformas creativos.", 90, 75, 1, "https://placehold.co/300x400/111/00ffcc?text=LBP+3"),
        ("Ratchet & Clank (2016)", "PS4", "[RECOMENDADO] La reinvención cinematográfica de la gran aventura espacial de plataformas y disparos.", 95, 79, 1, "https://placehold.co/300x400/111/00ffcc?text=Ratchet+and+Clank+PS4"),
        ("Infamous Second Son", "PS4", "[RECOMENDADO] Delsin Rowe absorbe nuevos poderes de neón y humo para combatir a la represión en Seattle.", 95, 75, 1, "https://placehold.co/300x400/111/00ffcc?text=Infamous+Second+Son"),
        ("Kingdom Hearts III", "PS4", "[RECOMENDADO] Sora concluye su viaje contra la oscuridad visitando mundos de Pixar y Disney con magia deslumbrante.", 110, 89, 1, "https://placehold.co/300x400/111/00ffcc?text=Kingdom+Hearts+III"),
        ("Batman: Arkham Knight", "PS4", "[MUY BUENO] Conduce el Batimóvil y defiende Gotham del Espantapájaros y el misterioso Caballero de Arkham.", 100, 80, 1, "https://placehold.co/300x400/111/00ffcc?text=Arkham+Knight"),
        ("Uncharted: The Nathan Drake Collection", "PS4", "[RECOMENDADO] Las tres primeras entregas de PS3 remasterizadas a 1080p y 60fps para PS4.", 100, 80, 1, "https://placehold.co/300x400/111/00ffcc?text=Nathan+Drake+Collection"),
        ("Metro Exodus", "PS4", "[NUEVO] Explora la Rusia postnuclear a bordo de un tren blindado huyendo de mutantes y peligros de la superficie.", 110, 89, 1, "https://placehold.co/300x400/111/00ffcc?text=Metro+Exodus"),
        ("BioShock: The Collection", "PS4", "[RECOMENDADO] Las tres obras maestras de Rapture y Columbia remasterizadas con todos sus contenidos descargables.", 100, 80, 1, "https://placehold.co/300x400/111/00ffcc?text=Bioshock+Collection"),
        ("Need for Speed Heat", "PS4", "[NUEVO] Compite de día en carreras legales y huye de la policía corrupta en carreras callejeras ilegales de noche.", 105, 85, 1, "https://placehold.co/300x400/111/00ffcc?text=NFS+Heat"),
        ("Gran Turismo Sport", "PS4", "[RECOMENDADO] Competiciones de automovilismo en línea con licencias oficiales de la FIA y realismo puro.", 90, 70, 1, "https://placehold.co/300x400/111/00ffcc?text=GT+Sport"),
        ("The Last Guardian", "PS4", "[NUEVO] Un niño y una criatura gigante similar a un grifo forjan un vínculo inseparable para escapar de ruinas místicas.", 100, 80, 1, "https://placehold.co/300x400/111/00ffcc?text=The+Last+Guardian"),
        ("Street Fighter V", "PS4", "[NUEVO] Torneos de lucha competitiva mundial con los personajes clásicos y mecánicas de V-Trigger.", 95, 75, 1, "https://placehold.co/300x400/111/00ffcc?text=Street+Fighter+V"),
        ("Plants vs. Zombies: Garden Warfare 2", "PS4", "[NUEVO] Divertido shooter multijugador cooperativo con plantas y zombis de alocadas habilidades.", 85, 65, 1, "https://placehold.co/300x400/111/00ffcc?text=PvZ+Garden+Warfare+2"),
        ("Minecraft: PlayStation 4 Edition", "PS4", "[MUY BUENO] Construye mundos infinitos y sobrevive a la noche en la edición definitiva del juego más famoso del mundo.", 100, 85, 1, "https://placehold.co/300x400/111/00ffcc?text=Minecraft+PS4")
    ]
    
    cursor.executemany('''
        INSERT INTO videojuegos (titulo, consola, descripcion, precio, precio_promo, disponible, imagen)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', juegos_tienda_masiva)
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/catalogo")
def catalogo():
    busqueda = request.args.get("q", "").strip()
    letra = request.args.get("letra", "").strip()
    consola = request.args.get("consola", "").strip()

    conn = get_db_connection()
    query = "SELECT * FROM videojuegos WHERE 1=1"
    params = []

    if busqueda:
        query += " AND titulo LIKE ?"
        params.append(f"%{busqueda}%")
    if letra:
        query += " AND titulo LIKE ?"
        params.append(f"{letra}%")
    if consola:
        query += " AND consola = ?"
        params.append(consola)

    query += " ORDER BY titulo ASC"
    juegos = conn.execute(query, params).fetchall()
    conn.close()

    abecedario = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return render_template("catalogo.html", juegos=juegos, abecedario=abecedario, busqueda=busqueda, letra_activa=letra, consola_activa=consola)

@app.route("/juego/<int:juego_id>")
def detalle(juego_id):
    conn = get_db_connection()
    juego = conn.execute("SELECT * FROM videojuegos WHERE id = ?", (juego_id,)).fetchone()
    conn.close()
    return render_template("detalle.html", juego=juego)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)