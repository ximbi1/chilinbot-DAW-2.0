import os
import time
import random
import paginate
import requests
from bs4 import BeautifulSoup
import nltk
import json
import config
import asyncio
import datetime
#import wordle
import SQLmanager
from discord import Embed

from minipoly import *
from datetime import date
import discord
from keep_alive import keep_alive
from discord.ext import commands
#Custom imports
from economy import add_ppl, add_coins, remove_coins, KickCoins, leaderboard, update_leaderboard
from cards import deck as deckf, add_pile, draw, pile, value

#######################prefijo para llamar al bot############
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="a ", intents=intents, case_insensitive=True)
token = os.environ["DISCORD_BOT_SECRET"]

bot.author_id = 1041801498608275556  # Change to your discord id!!!
preguntas = [
    {"pregunta": "¿Cuál es la capital de España?", "respuesta": "Madrid"},
    {"pregunta": "¿Cuál es el planeta más grande del sistema solar?", "respuesta": "Júpiter"},
    {"pregunta": "¿Quién escribió la novela 'Don Quijote de la Mancha'?", "respuesta": "Miguel de Cervantes"},
    {"pregunta": "¿Cuál es el símbolo químico del oro?", "respuesta": "Au"},
    {"pregunta": "¿Cuantos deportes diferentes se practican en un triatlon?","respuesta":"3"},
    {"pregunta": "¿Que mide la escala de Ritcher?","respuesta":"terremotos"},
    {"pregunta": "¿Quien interpreto el papel principal de Taxi Driver?","respuesta":"Robert de Niro"},
    {"pregunta": "¿Como se llama la boca de un volcan?","respuesta":"Crater"},
    {"pregunta": "¿Quien construyo las piramides?","respuesta":"Los antiguos egipcios"},
    {"pregunta": "¿En que continente esta ubicada España?","respuesta":"Europa"},
    {"pregunta": "¿Quien era pablo Picasso?","respuesta":"Un pintor"},
    {"pregunta": "¿Segun la historia de que nacionalidad era el primero hombre que piso la luna?","respuesta":"estadounidense"}
]
puntuacion = {}
#################
@bot.command(description="para aceder al mooodle")
async def moodle(ctx):
    link = ("https://gracia.sallenet.org/")
    await ctx.send("Aquí tienes el enlace para el moodle:\n"+link)         

#################
@bot.command(description="para aceder a chat gpt")
async def chatgpt(ctx):
    link = ("https://chat.openai.com/chat")
    await ctx.send("Aquí tienes el enlace para el chatgpt:\n"+link)
###########################
@bot.command(description="para aceder al github")
async def github(ctx):
    link = ("https://github.com")
    await ctx.send("Aquítienes el enlace para github:\n"+link)  
#####################################################CK
#balance
@bot.command(description="para ver el dinero")
async def balance(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    embed = discord.Embed(title="COINS",
                          color=0x00ff33,
                          timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="BALANCE --------->", value=":3", inline=True)
    embed.add_field(name=KickCoins(user), value="uwu", inline=True)
    embed.set_footer(text=user)
    await ctx.send(embed=embed)


#pay
@bot.command(description="para pagrle a alguien")
async def pay(ctx, ammount, user: discord.Member):
    await add_coins(user, ammount)
    await ctx.send(f"{ammount}KC añadidos a {user.mention}")


#tax
@bot.command(description="para cobrar taxas")
async def tax(ctx, ammount, user: discord.Member):
    if ammount == "all":
        ammount = KickCoins(user)

    await remove_coins(user, ammount)
    await ctx.send(f"{ammount}KC restados a {user.mention}")
  
#####para buscar mensajes###

@bot.command()
async def buscar(ctx, word: str):
    '''para buscar contendio especifico'''
    channel = ctx.message.channel
    messages = await ctx.channel.history(limit=200).flatten()

    for msg in messages:
        if word in msg.content:
            embed = discord.Embed(title="Buscador de contenido!",
                                  description=f"Busquedas: " + msg.jump_url,
                                  color=0x00FFFF)
            await ctx.message.delete()
            await ctx.send(embed=embed)


  

#fuck
@bot.command(description="para echr a aluien por 500 CK")
async def fuck(ctx, user: discord.Member):
    if KickCoins(ctx.author) >= 500:
        try:
            await user.kick()
            await remove_coins(ctx.author, 500)
            await ctx.send(
                f"{user.name} ha sido kickeado. Se te han restado 500 KickCoins"
            )
        except discord.Forbidden:
            await add_coins(ctx.author, reward)
    else:
        await ctx.send("No tienes suficientes KickCoins. Necessitas 500")


#gamble betssssss
@bot.command(description="para apostar ")
async def gamble(ctx, ammount):
    '''Apuesta tu dinero para ganar (o perder ;) )la misma cantidad '''
    if ammount == "all":
        ammount = KickCoins(ctx.author)
    elif ammount == "half":
        ammount = int(KickCoins(ctx.author) / 2)
    else:
        ammount = int(ammount)
    if ammount <= 0:
        await ctx.send("Buen intento maquina")
        return
    if KickCoins(ctx.author) >= ammount:
        num = random.randint(1, 2)
        await ctx.send(
            f"{ctx.author.mention} Acabas de apostar {ammount} KC...")
        await asyncio.sleep(3)
        if num == 1:
            await ctx.send(
                f"¡¡¡ {ctx.author.mention} Has ganado {ammount}KC!!!")
            await add_coins(ctx.author, ammount)
        elif num == 2:
            await ctx.send(f"{ctx.author.mention}Has perdido {ammount}KC :(. F"
                           )
            await remove_coins(ctx.author, ammount)
    else:
        await ctx.send(
            f"{ctx.author.mention} No tienes tantos KC!! te faltan {ammount - KickCoins(ctx.author)}"
        )


#Transfer
@bot.command()
async def transfer(ctx, coins, user: discord.Member):
    coins = int(coins)
    if coins <= 0:
        await ctx.send("Nope")
        return

    if KickCoins(ctx.author) >= coins:
        await add_coins(user, coins)
        await remove_coins(ctx.author, coins)
        await ctx.send("Done!")
    else:
        ctx.send(
            f"No tienes KickCoins suficientes. Te faltan {coins - KickCoins(user)}"
        )


#rank
@bot.command()
async def rank(ctx, arg=None):
    embed = discord.Embed(title="LEADERBOARD",
                          description="the top 10 most mone pep",
                          color=0xfbff00,
                          timestamp=datetime.datetime.utcnow())
    if arg == "fekas":
        fekas = True
    else:
        fekas = False
    ricos = [
        810735914782818354, 823886106725711922, 815423482966835220,
        272021299772129281
    ]
    i = 0
    for user in leaderboard(ctx.guild):
        if not fekas:
            embed.add_field(name=f"{i+1}. {user.name}",
                            value=f"BALANCE = {KickCoins(user)}",
                            inline=False)
            i += 1
        else:
            if not user.id in ricos:
                embed.add_field(name=f"{i+1}. {user.name}",
                                value=f"BALANCE = {KickCoins(user)}",
                                inline=False)
                i += 1
        if i == 10:
            break

    await ctx.send(embed=embed)
#########################ruletarusa ejemplo#############################
#Ruleta
@bot.command(
    description=
    "Te avates en duelo con el usuario especificado. Que gane el mejor")
async def rrr(ctx, named: discord.User, sloter):
    '''Te avates en duelo con el usuario especificado. Que gane el mejor'''
    namer = ctx.author
    namerMen = ctx.author.mention
    namedMen = named.mention
    await ctx.send(
        f"{namerMen} ha retado a {namedMen} a un duelo! Tienes un minuto para responder. (un numero del 1 al 6, si no me rallo)"
    )

    try:
        msg = await ctx.bot.wait_for("message",
                                     timeout=60,
                                     check=lambda message: message.author ==
                                     named and message.channel == ctx.channel)
        if msg:
            bulleter = random.randint(1, 6)
            bulleted = random.randint(1, 6)
            sloted = msg.content

            if (bulleted == int(sloted)) and (bulleter == int(sloter)):
                await ctx.send(
                    "¡Increible, Ambos han disparado y se han chocado las balas en el aire! Nadie muere"
                )
            elif bulleted == int(sloted):
                await ctx.send(
                    f"{namedMen} ha disparado a {namerMen}, quien no ha tenido la misma suerte"
                )
                try:
                    await namer.kick(reason="muerto en combate")
                except discord.Forbidden:
                    add_coins(ctx.author, reward)
            elif bulleter == int(sloter):
                await ctx.send(
                    f"{namerMen} ha disparado la ranura {sloted} matando a {namedMen}, que no ha tenido la misma suerte"
                )
                try:
                    await named.kick(reason="muerto en combate")
                except discord.Forbidden:
                    add_coins(ctx.author, reward)
            else:
                await ctx.send(
                    f"Nadie ha disparado. Se comenta por el barrio que {namerMen} y {namedMen} son unos pringados."
                )

#elOceanoDeElif

    except asyncio.TimeoutError:
        await ctx.send(f"Demasiado lento {namedMen}.")

###########HOMBRE LOBO EN INFORMATICA########
# Crear una función para contar las reglas del juego del hombre lobo
              
@bot.command()
async def cartamd(ctx):
    directory = "Cartas/"
    files = os.listdir(directory)
    random_img = random.choice(files)
    img_path = directory + "/" + random_img
    for user in ctx.guild.members:
        try:
            await user.send(file=discord.File(img_path))
        except:
            continue
    await ctx.send("Las cartas han sido enviadas a todos los miembros del servidor.")
      
@bot.command()
async def cartaleatoria(ctx):
    card_folder = "Cartas/"
    card_list = os.listdir(card_folder)
    card = card_list[random.randint(0, len(card_list) - 1)]
    with open(f"{card_folder}/{card}", "rb") as f:
        await ctx.send(file=discord.File(f))

@bot.command()
async def mostrarcartas(ctx):
    card_folder = "Cartas/"
    card_list = "\n".join(os.listdir(card_folder))
    await ctx.send(f"List of cards: {card_list}")


      



#########FINS AQUI NO FUNCIONA######################
diccionario = {}


#################################
#######para suicidarseeeee##############
@bot.command()
async def morir(ctx):
    '''para suicidarse'''
    suicideembed = discord.Embed(title=f'{ctx.author} se ha suicidado',
                                 description="Probablemente este triste",
                                 color=0x000000)
    suicideembed.set_image(
        url='https://media1.giphy.com/media/c6DIpCp1922KQ/giphy.gif')
    suicideembed.set_footer(text='*No hagan esto en sus casas xd*')
    suicideembed2 = discord.Embed(title=f'{ctx.author} se ha suicidado',
                                  description="Probablemente este triste",
                                  color=0x000000)
    suicideembed2.set_image(
        url=
        'https://media1.tenor.com/images/041dddf7d24b9ba3d591e0bed2ce38c7/tenor.gif?itemid=4524247'
    )
    suicideembed2.set_footer(text='*No hagan esto en sus casas xd*')
    suicideembed3 = discord.Embed(title=f'{ctx.author} se ha suicidado',
                                  description="Probablemente este triste",
                                  color=0x000000)
    suicideembed3.set_image(
        url='https://i.makeagif.com/media/9-14-2015/vyNnjt.gif')
    suicideembed3.set_footer(text='*No hagan esto en sus casas xd*')
    suicideembed4 = discord.Embed(title=f'{ctx.author} se ha suicidado',
                                  description="Probablemente este triste",
                                  color=0x000000)
    suicideembed4.set_image(
        url='https://thumbs.gfycat.com/SnarlingTameEquine-max-1mb.gif')
    suicideembed4.set_footer(text='*No hagan esto en sus casas xd*')
    suicideembed6 = discord.Embed(title=f'{ctx.author} se ha suicidado',
                                  description="Probablemente este triste",
                                  color=0x000000)
    suicideembed6.set_image(
        url='https://tenor.com/view/epic-meme-kermit-suicide-gif-20626092')
    suicideembed6.set_footer(text='*No hagan esto en sus casas xd*')
    suicideembed5 = discord.Embed(title=f'{ctx.author} se ha suicidado',
                                  description="Probablemente este triste",
                                  color=0x000000)
    suicideembed5.set_image(
        url='https://media2.giphy.com/media/13kJc5CTOnqdQk/giphy.gif')
    suicideembed5.set_footer(text='*No hagan esto en sus casas xd*')
    suicidio = [
        suicideembed, suicideembed2, suicideembed3, suicideembed4,
        suicideembed5, suicideembed6
    ]
    await ctx.send(embed=random.choice(suicidio))


##############################################
@bot.command()
async def eliminar(ctx, amount: int):
    # Eliminar mensajes en el canal
    await ctx.channel.purge(limit=amount)
    # Enviar un mensaje de confirmación
    await ctx.send(f'{amount} mensajes eliminados.')

  
#####para tomar chupitoooosss########
@bot.command()
async def fumeteo(ctx):
    '''aver quantos calos aguantas campeeon'''
    salve = random.randint(1, 15)
    boss = [
        f'{ctx.author} se mantiene en pie despues de {salve} calos!',
        f'{ctx.author} empezo a ir ciego despues de {salve} calazos!'
    ]
    poo = random.choice(boss)
    deshqiperine = [
        'https://media.tenor.com/lWYKkXN2tasAAAAM/smoke-cigarette.gif',
        'https://media.tenor.com/zoglollWU_8AAAAM/smoke-cigarette.gif',
        'https://media.tenor.com/KCDaAubmS4YAAAAM/smoke-shrug.gif'
    ]
    if salve > 7:
        embed = discord.Embed(
            title=
            f'{ctx.author} como se nota que te gusta la hierbita eeh jajajaja!',
            description=
            f'{ctx.author.mention} sa fumao unos petas como un misil y sigue en pie!',
            color=0x000000)
        embed.add_field(name='Epico,este es immortal seguro',
                        value=poo,
                        inline=False)
        embed.set_image(url=random.choice(deshqiperine))
        embed.set_footer(text='en la real life es pegriloso xd')
    else:
        embed = discord.Embed(
            title=f'{ctx.author} te falta practica...que la palmas!',
            description=
            f'{ctx.author.mention} intento ser un pro...y el blancazo se llevo!JAJJAJA',
            color=0x000000)
        embed.add_field(
            name=f'{ctx.author} le dio blanca despues de {salve} calazos!',
            value='que lastima...',
            inline=False)
        embed.set_image(url=random.choice(deshqiperine))
        embed.set_footer(text='en la rial life es pegriloso xd')
    await ctx.send(embed=embed)


##################################################

extensions = [
    'cogs.cog_example'  # Same name as it would be if you were importing it
]
###############################################
#######para practicar operaciones de mates#######
@bot.command()
async def op(ctx):
    primero = random.randint(1, 100)
    segundo = random.randint(1, 100)
    operandacio = random.randint(1, 100)
    oper = "+"
    bonus = 1
    if operandacio < 9:
        oper = "*"
        respuestaa = str(primero * segundo)
        tiempo = 40
        bonus = 4
    elif operandacio < 40:
        oper = "-"
        respuestaa = str(primero - segundo)
        tiempo = 30
        bonus = 2
    else:
        tiempo = 20
        respuestaa = str(primero + segundo)
    timepo = int(tiempo)

    pregunta = "Cuanto es " + str(primero) + " " + oper + " " + str(
        segundo) + "?"
    embed = discord.Embed(title=pregunta,
                          description="tienes " + str(tiempo) +
                          " segundos para resolverlo y una unica oportunidad.",
                          color=discord.Colour.blue())
    await ctx.send(embed=embed)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        mensajeRespuesta = await ctx.bot.wait_for("message",
                                                  timeout=tiempo,
                                                  check=check)
        contenidoMensaje = mensajeRespuesta.content

        if contenidoMensaje == respuestaa:
            embed = discord.Embed(
                title="Tu respuesta: " + respuestaa + " es correcta!",
                description=f"Eres un celebrito te ganaste x dinero",
                color=discord.Colour.blue())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Tu respuesta no fue correcta!",
                description="deja los porros y ponte a estudiar.",
                color=discord.Colour.red())
            await ctx.send(embed=embed)

    except discord.Forbidden:
        await ctx.send("demasiado tiempo esperando..")








@bot.event
async def on_ready():
    print("ready")
    await bot.change_presence(activity=discord.Game('TERMINA AITOR'))

competition = False
competitors = {}

#on sessage######################
xd = ["uwu", "f", "xd", "nice", 'a', "maricon"]
blacklist = []
levels = {}
######################
@bot.command()
async def jugamos(ctx, game_name: str, game_description: str):
    author = ctx.message.author
    embed = discord.Embed(title=f"Petición de juego: {game_name}", description=game_description, color=0x00ff00)
    embed.set_author(name=author.name, icon_url=author.avatar_url)
    await ctx.send(embed=embed)
################

  ##################mensajes motivacionales
motivational_quotes = [
    "La vida es 10% lo que te sucede y 90% cómo reaccionas a ello.",
    "La única manera de hacer un gran trabajo es amar lo que haces.",
    "El éxito no es la clave de la felicidad. La felicidad es la clave del éxito.",
    "No dejes que el miedo te detenga de hacer lo que realmente quieres.",
    "El fracaso es solo una oportunidad para comenzar de nuevo con más experiencia."
]

motivational_images = [
    "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
    "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
    "https://images.unsplash.com/photo-1497366811353-6870744d04b2?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
    "https://images.unsplash.com/photo-1513104890138-7c749659a591?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
    "https://images.unsplash.com/photo-1496128858413-b36217c2ce36?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
]

def motivational_message():
    return random.choice(motivational_quotes)

def motivational_image():
    return random.choice(motivational_images)



@bot.command()
async def motivacion(ctx):
    embed = Embed(title="Mensaje Motivacional", description=motivational_message(), color=0x00ff00)
    embed.set_image(url=motivational_image())
    await ctx.send(embed=embed)


#competit
def count_errors(text):
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    errors = 0
    words = nltk.word_tokenize(text)
    for word in words:
        if not nltk.corpus.wordnet.synsets(word):
            errors += 1
    return errors

def ranking(competitors):
    ranking = sorted(competitors.items(), key=lambda x: x[1][0])
    ranking_str = 'Ranking:\n'
    for i, competitor in enumerate(ranking):
        user = client.get_user(competitor[0])
        ranking_str += '{}. {} - Tiempo: {} segundos, Errores: {}\n'.format(i+1, user.name, competitor[1][0], competitor[1][1])
    return ranking_str

  
##########################################
@bot.event
async def on_message(message):
    global competition,competitors
    author = message.author
    content = message.content
    canal = message.channel
    aitor = 817313326161592342
    if author.id in blacklist:
        await canal.send(" calla tontika")
    elif content.lower() in xd and author.id != aitor:
        await canal.send(content)
    elif canal.id == 1047957981200924693 and author.id != aitor:
        lastmsg = await canal.history(limit=2).flatten()
        if lastmsg[1].author == author:
            await message.delete()
        elif random.randint(1, 10) == 5:
            try:
                await canal.send(f"{int(content) + 1}")
            except ValueError:
                await canal.send("xd")
    #para escribir textopop          
    if message.content.startswith('!escribir'):
        await message.channel.send('Empieza a escribir')
        start = time.time()
        user_message = await bot.wait_for('message')
        end = time.time()
        elapsed_time = end - start
        await message.channel.send('Tiempo de escritura: {} segundos'.format(elapsed_time))
#me falla como una escopeta de feria
    if message.content.startswith('!competir'):
        competition = True
        await message.channel.send('Empieza la competencia! escribir una frase')
    if competition:
        if message.author.id in competitors:
            await message.channel.send('Ya has participado')
            return
        start = time.time()
        user_message = await bot.wait_for('message', check=lambda m: m.author == message.author)
        end = time.time()
        elapsed_time = end - start
        errors = count_errors(user_message.content)
        competitors[message.author.id] = (elapsed_time, errors)
        await message.channel.send('Tiempo de escritura: {} segundos, Errores: {}'.format(elapsed_time, errors))
        if len(competitors) == len(message.guild.members):
            competition = False
            await message.channel.send(ranking(competitors))  
    # Si el mensaje comienza con "!pregunta"
    if message.content.startswith("!pregunta"):
        # Seleccionar una pregunta aleatoria de la lista
        pregunta = preguntas[random.randint(0, len(preguntas)-1)]
        # Enviar la pregunta al canal
        await message.channel.send(pregunta["pregunta"])

        # Esperar la respuesta del usuario
        respuesta = await bot.wait_for("message", check=lambda m: m.author == message.author)

        # Comprobar si la respuesta es correcta
        if respuesta.content.lower() == pregunta["respuesta"].lower():
            # Aumentar la puntuación del usuario
            if message.author in puntuacion:
                puntuacion[message.author] += 1
            else:
                puntuacion[message.author] = 1
            await message.channel.send("¡Respuesta correcta! Tu puntuación es de " + str(puntuacion[message.author]) + " puntos.")
        else:
            await message.channel.send("Respuesta incorrecta. La respuesta correcta es: " + pregunta["respuesta"])

    if message.content.startswith("!estado"):
        user = message.mentions[0]
        activity = user.activity
        if activity is None:
            await message.channel.send("El usuario no tiene una actividad actual.")
        else:
            await message.channel.send("El usuario está actualmente {} {}".format(activity.type, activity.name))
    
    if message.content.startswith("!agregar"):  #agregar al diccionario
        palabra, significado = message.content[8:].split(":")
        diccionario[palabra] = significado
        await message.channel.send(
            f"Palabra '{palabra}' agregada al diccionario con significado '{significado}'"
        )

    elif message.content.startswith("!buscar"):  #para buscar palabra
        palabra_buscada = message.content[7:]
        if palabra_buscada in diccionario:
            significado = diccionario[palabra_buscada]
            await message.channel.send(
                f"La palabra '{palabra_buscada}' tiene el significado: '{significado}'"
            )
        else:
            await message.channel.send(
                f"La palabra '{palabra_buscada}' no se encuentra en el diccionario."
            )

    if message.content.startswith("!reflejos"):  #para juego de reflejos
        await message.channel.send(
            "¡Empezando juego de reflejos! Responde listo rápido para ganar.")
        start_time = time.time()

        def check(m):
            return m.content.lower(
            ) == "listo" and m.channel == message.channel

        try:
            ready_message = await bot.wait_for("message",
                                               check=check,
                                               timeout=5.0)
            end_time = time.time()
            elapsed_time = end_time - start_time
            await message.channel.send(
                "¡Listo! Tu tiempo de reacción fue de {:.2f} segundos.".format(
                    elapsed_time))
        except asyncio.TimeoutError:
            await message.channel.send(
                "¡Tiempo fuera! No fuiste lo suficientemente rápido.")
    if message.content == "AITOR":
        await message.channel.send("TERMINATOR!")
    if message.author.bot:
        return
    if message.content.startswith('!level'):
        return
    if message.author.id not in levels:
        levels[message.author.id] = {
            "name": message.author.name,
            "level": 1,
            "messages": 1
        }
    else:
        levels[message.author.id]["messages"] += 1
        if levels[message.author.id]["messages"] % 10 == 0:
            levels[message.author.id]["level"] += 1
            await message.channel.send(
                f"Felicidades {message.author.mention}, has subido al nivel {levels[message.author.id]['level']}!"
            )
    with open('levels.json', 'w') as f:
        json.dump(levels, f)
    await bot.process_commands(message)


@bot.command()
#PARA MOSTRARR QUE NIVEL ERES
async def minivel(ctx):

    def cargar_niveles():
        try:
            with open('levels.json', 'r') as file:
                levels = json.load(file)
        except:
            levels = {}

    if ctx.author.id in levels:
        await ctx.send(
            f"{ctx.author.mention}, tu nivel actual es {levels[ctx.author.id]['level']}."
        )
    else:
        await ctx.send(f"{ctx.author.mention}, no tienes ningun nivel.")


#PARA MOSTRAR EL RANGO DE NIVELES
@bot.command()
async def rankingn(ctx):
    sorted_levels = sorted(levels.items(),
                           key=lambda x: x[1]['level'],
                           reverse=True)
    ranking = ""
    for i, (user_id, user_data) in enumerate(sorted_levels):
        ranking += f"{i+1}. {user_data['name']} - Nivel {user_data['level']}\n"
    await ctx.send(f"**Ranking de niveles:**\n{rankingn}")


#Clear#################################################
@bot.command(description="elimina el numero de mensajes especificados")
async def clear(ctx, amount=1):
    '''borra x mensajesd (defecto = 1)'''
    print(ctx.author, "ha eliminado", amount, "mensajes")
    await ctx.channel.purge(limit=amount + 1)


####################mesnaje vacio#########################
@bot.command()
async def mvacio(ctx):
    """envia mensaje vacio."""
    await ctx.send(chr(173))
    await ctx.delete_message(ctx.message)


#salta error pero hace su funcionamiento xd
#######################anunciamiento#########################
@bot.command()
async def pesca(ctx):
    fish_list = [
        "sardina", "bacalao", "atún", "salmón", "trucha", "merluza", "gamba"
    ]
    catch = random.choice(fish_list)
    await ctx.send(f'¡Has atrapado un {catch}!')


######para pescarrrr pero no me lo detectaaaaaaa
@bot.command(description="de pesca chavaless")
async def pescar(ctx):
    '''nos vamos de pesca'''
    num = random.randint(1, 100)
    special = 0
    #para poner mas dificultad peronerño en 95
    if num < 75:
        _catch = await catch()
    else:
        _catch = await special_catch()
        special = 1
    e = discord.Embed(title="A Pescar!",
                      description="Te fuiste a pescar!",
                      colour=0xf54242)
    e.set_thumbnail(url="https://i.imgur.com/3Q3VDp9.jpg")
    msg = await ctx.send(embed=e)
    await asyncio.sleep(3)
    e = discord.Embed(title="Pescando",
                      description="Algo ha picado!",
                      colour=0xd4f542)
    e.set_thumbnail(url="https://i.imgur.com/Y3mpQhm.jpg")
    await msg.edit(embed=e)
    await asyncio.sleep(3)
    e = discord.Embed(title="Pescando",
                      description=f"Has conseguido {_catch[0]}!",
                      colour=0x919191)
    e.set_thumbnail(url="https://i.imgur.com/59TKpfE.jpg")
    if special == 0:
        basePrice = _catch[2]
        minWeight = _catch[3]
        maxWeight = _catch[4]
        goldWeight = _catch[5]
        weight = round(random.uniform(minWeight, maxWeight), 3)
        # PRECIO
        price = 0
        a = ""
        if weight >= goldWeight:
            price = round(basePrice + ((basePrice / 50) * weight * 3), 2)
            a = "\nEste pez es extraordinariamente largo!"
        else:
            price = round(basePrice + ((basePrice / 100) * weight), 2)
        if _catch[0] == "Nada":
            e.add_field(name=_catch[0], value="Has perdido el tiempo!")
            e.set_thumbnail(url="https://i.imgur.com/C6rQmPZ.gif")
        else:
            e.add_field(name=_catch[0],
                        value=f"**Peso**: `{weight}kg`\n" +
                        f"**Valor**: `{price}$ `" + a)
    else:
        price = _catch[2]
        description = _catch[3]
        icon = _catch[4]
        e.set_thumbnail(
            url="https://live.staticflickr.com/22/25807800_4f776527bb_b.jpg")
        e = discord.Embed(
            title="Pescando",
            description=f"**Item Especial! Has conseguido {_catch[0]}!!!**",
            colour=0xcc00ff)
        e.add_field(name=icon + " " + _catch[0],
                    value=f"**Descripcion**: `{description}`\n" +
                    f"**Valor**: `{price}$`")

    await msg.edit(embed=e)


fishes = (
    # 0Name, 1Weight (Chance), 2Base Price, 3minWeight, 4maxWeight, 5goldWeight
    ("Nada", 30, 0, 0, 0, 1),
    ("sardina", 10, 10, 1, 22.4, 16),
    ("Pececillo", 17, 5, 0.3, 4, 25),
    ("Trucha", 10, 12, 8, 48, 35),
    ("bacalao", 10, 10, 3, 212, 180))
special = (
    # Name, Weight, Price, Description, Icon
    ("Tu gracia", 1, 6969, "Muy raro de encontrar", ":monkey:"),
    ("Bota", 4, 3, "Vieja bota usada ", ":boot:"),
    ("Prostituta", 2, 200, "Dios te escucha.", ":dancer:"),
    ("Dildo", 3, 23, "humedo y usado (por el agua xd)", ":baby_bottle:"),
    ("Skateboard", 3, 200, "Muy raro y dificil de encontrar", ":skateboard:"),
    ("Invitacion a patinar", 0.0001, 99999, "%skrt%", ":skateboard:"),
    ("Mierda de perro", 6, 1, "Huele a mierda por aqui.", ":poop:"),
    ("Tu madre", 0.005, 2, "Es gorda pero no vale la pena.", ":cap:"))


async def catch():

    pr = []
    for i in range(0, len(fishes)):
        pr.append(fishes[i][1])
    pr = round_to_100_percent(pr)
    return fishes[np.random.choice(len(fishes), p=pr)]


async def special_catch():
    pr = []
    for i in range(0, len(special)):
        pr.append(special[i][1])
    pr = round_to_100_percent(pr)
    return special[np.random.choice(len(special), p=pr)]


def round_to_100_percent(number_set, digit_after_decimal=2):
    unround_numbers = [
        x / float(sum(number_set)) * 100 * 10**digit_after_decimal
        for x in number_set
    ]
    decimal_part_with_index = sorted(
        [(index, unround_numbers[index] % 1)
         for index in range(len(unround_numbers))],
        key=lambda y: y[1],
        reverse=True)
    remainder = 100 * 10**digit_after_decimal - sum(
        [int(x) for x in unround_numbers])
    index = 0
    while remainder > 0:
        unround_numbers[decimal_part_with_index[index][0]] += 1
        remainder -= 1
        index = (index + 1) % len(number_set)
    return [(int(x) / float(10**digit_after_decimal)) / 100
            for x in unround_numbers]


########################preuab y verdas#################
@bot.command(help="prueva o verdad")
async def pv(ctx):
    '''para hacer prueva o verdad'''
    truth_items = [
        'Si pudieras ser invisible,cual es la primera cosa que harias?',
        'Si te dieran tres deseos cuales serian?',
        'Cual es el maximo de dias que has podido pasar sin ducharte?',
        'Cual es el animal que crees que te pareces mas?',
        'Dime uno de tus mayores secretos', 'Has robado alguna vez?',
        'Quien es tu crush famoso?', ''
    ]
    dare_items = [
        'Comete unos yatekomo crudos.',
        ' Baila sin musica durante 20 segundos.',
        'Deja que alguien que escojas tenga el privilegio de decidir un mensaje que deberas mandar a alaguien que el decida.',
        ' Deja que una persona te dibuje en la cara con un boli.',
        'Intenta hacer un truco de magia.',
        'Rebientate dos huevos en la cabeza.',
        'Grita por la ventana :no he sido yo ha sido el.',
        ' Dile a tu madre que necesitas mariguana para aliviar las penas.'
    ]

    embed = discord.Embed(
        title="Prueva o Verdad!",
        description="Porfavor escribe v para verdad y p para prueba",
        color=0x00FFFF)
    await ctx.message.delete()
    await ctx.send(embed=embed)

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel and message.content.lower(
        ) in ("v", "p")

    message = await ctx.bot.wait_for("message", check=check)
    choice = message.content.lower()
    if choice == "v":
        embed = discord.Embed(title="Verdad",
                              description=f"{random.choice(truth_items)}",
                              color=0x00FFFF)
    await ctx.send(embed=embed)

    if choice == "p":
        embed = discord.Embed(title="Prueba!",
                              description=f"{random.choice(dare_items)}",
                              color=0x00FFFF)
    await ctx.send(embed=embed)


#######apiiiiii del tiemmpo###########
@bot.command()
async def tiempo(ctx, location):
    '''sirve para mostrar el tiempo de la ciudad'''
    mykey = 'a2fad8b8ac4387388969c71bb664d785'  #get your api key from https://openweathermap.org/
    link = 'https://api.openweathermap.org/data/2.5/weather?q=' + location + '&appid=' + mykey
    api_link = requests.get(link)
    api_data = api_link.json()

    #crear variables para almacenar y mostrar datos
    temp_city = ((api_data['main']['temp']) - 273.15)  #para que sean grados
    feelslike_temp = ((api_data['main']['feels_like']) - 273.15)
    weather_desc = api_data['weather'][0]['description']
    hmdt = api_data['main']['humidity']
    wind_spd = api_data['wind']['speed']
    visibility = api_data['visibility']
    #date_time = datetime.date().strftime("%d %b %Y | %I:%M:%S %p") {round(client.latency * 1000)}

    title = f'⛅ El tiempo para {location}.'

    description = f'🌡️ Temperatura: {round(temp_city * 1)}°C \n \n 🔥 Sensacion Termica: {round(feelslike_temp * 1)}°C \n \n☁️ Tipo: {weather_desc}. \n \n 🥵 Humedad: {hmdt}% \n \n 💨 Velocidad del viento: {wind_spd} km/h \n \n 👀 Visibilidad: {visibility} Metros'
    embed = discord.Embed(title=title,
                          description=description,
                          color=discord.Colour.orange())
    await ctx.send(embed=embed)


########################################
@bot.command()
async def atencion(ctx, *, announce=None):
    if not ctx.guild:
        await ctx.send('Este comando no se puede usar en privado.')
    else:
        await ctx.message.delete()
        embed = discord.Embed(title="✅ Atension plis un mensaje importante",
                              description="Toda la informacion aqui debajo",
                              color=0xd01818)
        embed.add_field(name="Aviso echo por", value=ctx.author.mention)
        embed.add_field(name="Aviso ", value=announce)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


#Giveaway


@bot.command()
async def givaway(ctx, ammount, mins):
    message = await ctx.send(
        f"Quieres pasta? Aqui tienes pasta! Reacciona para ganar {ammount}KC. Tienes {mins} minutos!"
    )
    emoji = '💰'
    await message.add_reaction(emoji)
    await asyncio.sleep(int(mins) * 60)
    message = await ctx.channel.fetch_message(message.id)
    participantes = [None]
    for reaction in message.reactions:
        if reaction.emoji == emoji:
            async for user in reaction.users():
                if user.bot == False:
                    participantes.append(user)
                    print(user)
    await ctx.send("¡¡¡TIEMPO!!! Felicidades a quien haya podido participar.")


#Lottery
@bot.command()
async def lottery(ctx, ammount, mins, cost=10):
    message = await ctx.send(
        f"Se ha creado una loteria! Reacciona para ganar {ammount}KC. Tienes {mins} minutos! Unirse cuesta {cost}KC pero si ganas no se te restan del premio"
    )
    emoji = '💰'
    await message.add_reaction(emoji)
    await asyncio.sleep(int(mins) * 60)
    message = await ctx.channel.fetch_message(message.id)
    participantes = [None]
    for reaction in message.reactions:
        if reaction.emoji == emoji:
            async for user in reaction.users():
                if (user.bot == False) and (KickCoins(user) >= int(cost)):
                    participantes.append(user)
                    await remove_coins(user, cost)
                    print(user)

    winner = random.choice(participantes)
    await ctx.send("¡¡¡TIEMPO!!! EL GANADOR ÉS...")
    await asyncio.sleep(3)
    if winner != None:
        await ctx.send(f"¡¡¡{winner.mention}!!! Se lleva {ammount}KC")
        await add_coins(winner, int(ammount) + int(cost))
    else:
        locations = [
            "las bahamas", "mordor", "madrid", "un sotano oscuro...",
            "el Palau de la Generalitat", "su puta casa", "tonto quien lo lea",
            "tu cama", "Vietnam", "el discord personal de tu ex",
            "Club Penguin", "Habbo Hotel"
        ]
        await ctx.send(
            f"Mala suerte gente, le ha tocado a un desconocido en {random.choice(locations)}"
        )


##############################CARTASSSS####
collection = []


# Comando para solicitar una carta aleatoria
@bot.command(name='carta', help='Agafa una carta de la api')
async def carta(ctx):
    # Hacer una petición a la API para obtener una carta aleatoria
    url = f"https://api.scryfall.com/cards/random"
    response = requests.get(url)
    card = json.loads(response.text)

    # Verificar si la carta ya está en la colección de algún otro usuario
    #opcional nose si lo pondre aun

    # Enviar la carta al usuario
    await ctx.send(card['name'])  #opcional
    await ctx.send(card['image_uris']['large'])

    # Esperar la reacción del usuario para agregar la carta a su colección
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '💰'

    reaction, user = await bot.wait_for('reaction_add', check=check)

    # Agregar la carta a la colección del usuario
    collection.append(card)
    await ctx.send(f"{user.name} ha añadido {card['name']} En su coleccion!")


#####FUNCIONAA EL DE ABAIX
# Comando para ver las cartas de la colección
@bot.command(name='coleccion', help='Muestra la coleccion de cartas')
async def mostrar_coleccion(ctx):
    if not collection:
        await ctx.send("Tu coleccion esta vacia.")
        return

    else:

        message = "Tu coleccion:\n"
        for card in collection:
            message += f"- {card['name']}\n"  #['name']
            await ctx.send(card['image_uris']['large'])
        await ctx.send(message)


# Nuevo comando para intercambiar cartas con otro usuario


# Cargar las colecciones guardadas en un archivo JSON al iniciar el bot
def load_collections():
    try:
        with open('collections.json', 'r') as file:
            collections = json.load(file)
    except:
        collections = {}
    for user_id, user_collection in collections.items():
        user = bot.get_user(user_id)
        user.collection = user_collection


# Guardar las colecciones en un archivo JSON al finalizar la ejecución del bot
def save_collections():
    collections = {}
    for user in bot.users:
        collections[user.id] = user.collection
    with open('collections.json', 'w') as file:
        json.dump(collections, file)


# Cargar las colecciones al iniciar el bot


#############################3
#Blackjack
@bot.command()
async def blackjack(ctx, bet):
    channel = ctx.channel
    if bet == "all":
        bet = KickCoins(ctx.author)
    elif bet == "half":
        bet = int(KickCoins(ctx.author) / 2)
    if KickCoins(ctx.author) < int(bet):
        await ctx.send("No tens tants KC")
        return
    if int(bet) <= 0:
        await ctx.send("Bon intent maquina")
        return
    await ctx.send(f"{ctx.author.mention} ha apostat {bet}KC")
    deck = deckf()
    player = "player"
    dealer = "dealer"
    stopped = False
    add_pile(deck, player, draw(deck, 2))
    add_pile(deck, dealer, draw(deck, 1))
    await remove_coins(ctx.author, bet)

    if value(deck, player) == 21:
        await channel.send(f"Les teves cartes son: {pile(deck, player)}")
        add_pile(deck, dealer, draw(deck, 1))
        await channel.send(
            f"Blackjack! Has guanyat {int(int(bet)*1.5)}KC!! (el dealer tenia {pile(deck, dealer)})"
        )
        await add_coins(ctx.author, int(int(bet) * 2.5))
        return
    while not stopped:
        if value(deck, player) == 21:
            await channel.send(
                f"Les teves cartes son: { pile(deck, player) }, ({ value(deck, player) })"
            )
            stopped = True
        elif value(deck, player) > 21:
            await channel.send(
                f"Les teves cartes son: { pile(deck, player) } ({ value(deck, player) })"
            )
            await channel.send("T'has passat! Git gud noob")
            add_pile(deck, dealer, draw(deck, 1))
            await channel.send(
                f"El dealer tenia {pile(deck, dealer)} ({ value(deck, dealer) })"
            )
            return
        else:
            await channel.send(
                f"Les teves cartes son: { pile(deck, player) } ({ value(deck, player) })"
            )
            await channel.send(
                f"Les cartes del dealer son: { pile(deck, dealer) }, ?  ({ value(deck, dealer) })"
            )
            await channel.send("Vols una altra carta?")
            try:
                msg = await ctx.bot.wait_for(
                    "message",
                    timeout=60,
                    check=lambda message: message.author == ctx.author and
                    message.channel == ctx.channel)

                if msg:
                    if msg.content.lower() == "si":
                        add_pile(deck, player, draw(deck, 1))
                    elif msg.content.lower() == "no":
                        stopped = True
                    else:
                        await channel.send("Posa si o no, brètol")
            except asyncio.TimeoutError:
                await channel.send(f"Molt lent {ctx.author.mention}.")
                return

    add_pile(deck, dealer, draw(deck, 1))
    await channel.send(
        f"Les cartes del dealer son: {pile(deck, dealer)} ({ value(deck, dealer) })"
    )
    stopped = False
    if value(deck, dealer) == 21:
        await channel.send("El dealer té blackjack! Has perdut")
        return
    elif value(deck, dealer) < 17:
        await channel.send("El dealer agafarà cartes fins a arribar a 17")
        while not stopped:
            if value(deck, dealer) > 21:
                await channel.send(
                    f"El dealer s'ha passat! {pile(deck, dealer) } ({value(deck, dealer)})"
                )
                await channel.send(f"Has guanyat {bet}KC!")
                await add_coins(ctx.author, int(bet) * 2)
                return
            elif value(deck, dealer) < 17:
                add_pile(deck, dealer, draw(deck, 1))
            else:
                stopped = True

    await channel.send(
        f"El dealer té {pile(deck, dealer)} ({value(deck, dealer)})")

    if value(deck, dealer) < value(deck, player):
        await channel.send(f"Has guanyat {bet}KC!")
        await add_coins(ctx.author, int(bet) * 2)
    elif value(deck, dealer) > value(deck, player):
        await channel.send("Has perdut!")
    else:
        await channel.send("Empat :/")
        await add_coins(ctx.author, int(bet))


###########sugerencia#########
@bot.command()
async def sugerencia(ctx, *, sugerencia=None):
    if not sugerencia:
        await ctx.send('Tienes que dar una sugerencian')
        return

    channel = ctx.bot.get_channel(config.channels['sugerencias'])

    em = discord.Embed(title=f'Sugerencia',
                       description=f'*{sugerencia}*',
                       color=discord.Color.blurple())
    em.set_author(name=f'Sugerencia de {ctx.author}',
                  icon_url=ctx.author.avatar_url)
    suggestMsg = await channel.send(embed=em)
    await suggestMsg.add_reaction('👍')
    await suggestMsg.add_reaction('👎')

    em = discord.Embed(
        description=f'Sugerencia mandada con exito en <#{channel.id}>',
        color=discord.Color.green())
    await ctx.send(embed=em)
    return


#########APALABRADOS#####################esta dando fallos por so lo comento
#game = wordle.Word()
#    if message.author == author and content == '🟩🟩🟩🟩🟩':
#        await canal.send('Has ganado!')

# don't respond to ourselves
#    if author == author:
#        return

#    if content == 'ping':
#        await canal.send('pong')

#    if content == '!nuevousuario':
#        await canal.send(SQLmanager.db.NewUser(author))

#    if content == '!leaderboard':
#        await canal.send(SQLmanager.db.ShowLeaderboard())

#    if content == '!wordle':
#        game.generate()
#        print(game.keyword)
#        await canal.send('⬜⬜⬜⬜⬜')

#    if len(content) == 5 and game.complete == False:
#        await canal.send(game.guess(content.lower()))
#        if game.complete:
#            SQLmanager.db.AddWin(message.author)

#    if content == '!letras':
#        await canal.send(''.join(game.invalid_letters))

#######################MINIPOLY##########################################
game = RealEstateGame()
rents = [
    50,
    50,
    50,
    75,
    75,
    75,
    100,
    100,
    100,
    150,
    150,
    150,
    200,
    200,
    200,
    250,
    250,
    250,
    300,
    300,
    300,
    350,
    350,
    350,
]


@bot.command(
    help="Empieza el juego del minipoly con 24 casillas ,empiezas en la salida. "
    "compras "
    "precios alrededor de $50-$350.",
    brief="Empieza el juego del Minipoly",
    name="empezar",
    # optional shorter command call, prefix w/ $ in chat to execute
)
async def jugar_minipoly(ctx):
    """Crea una partida al minipoly."""
    author = ctx.message.author
    user_name = author.name
    game.create_spaces(50, rents)
    await ctx.channel.send(f"{user_name} ha empezado el juego del Minipoly!")


@bot.command(
    help="Te añade como jugador. Empiezas en la casilla GO con $1000.",
    brief="Te añade como jugador. Empiezas en la casilla GO con $1000.",
    name="Jugar",
    # optional shorter command call, prefix w/ $ in chat to execute
)
async def añadir_jugador(ctx):
    """el que lo escribe se une a la partida como jugador."""
    author = ctx.message.author
    user_name = author.name
    game.create_player(f"{user_name}", 1000)
    await ctx.channel.send(f"Bienvendio al Minipoly, {user_name}")


@bot.command(
    help=
    "Primero tira el dado para tu movimiento. Despues se mueve las casillas correspondientes "
    "Para ti. "
    "Movimiento automatico que comprueva si la casilla donde estas tiene dueño, "
    "y entonces tienes "
    "que pagarle. Tu nuevo espacio se muestra, "
    "al igual que las notificaciones de renta si eso "
    "pasa. Finalmente "
    "se comprueva el estado del juego, y se declara un ganador si es que hay uno.",
    brief=
    "Tiras los dados y te mueves, paga o compra renta en la propiedad si es necessario.",
    name="tirar",
    # optional shorter command call, prefix w/ $ in chat to execute
)
async def tirar(ctx):
    """Tira los dados para mover tu personaje, paga las rentas en las casillas que caigas
    ,
    despues muestra la informacion del espacio ocupado por el usuario."""
    author = ctx.message.author
    user_name = author.name
    die_roll = random.randint(1, 6)
    # money_before_move = game.get_player_account_balance(user_name)
    game.move_player(user_name, die_roll)
    money_after_move = game.get_player_account_balance(user_name)
    info = game.space_info(user_name)
    position = info["position"]
    owner = info["owner"]
    rent_val = info["rent_value"]
    buy_val = info["buy_value"]
    await ctx.channel.send(f"{user_name} ha tirado un {die_roll}!")
    await ctx.channel.send(f"Posicion: {position}\n"
                           f"Propietario: {owner}\n"
                           f"Precio_renta: ${rent_val}\n"
                           f"Precio_compra: ${buy_val}")
    player = game.get_players()[user_name]
    player_space = player.get_current_space()
    player_space_owner = player_space.get_owner()
    if player_space_owner is not None:
        await ctx.channel.send(
            f"{user_name} ha pagado ${rent_val} en la renta de {owner}!")
    if money_after_move == 0:
        await ctx.channel.send(
            f"ups. {user_name} te has quedado sin dinero.. :(\nGGWP {user_name}"
        )
    winner = game.check_game_over()
    if winner != "":
        await ctx.channel.send(
            f"Ahi te visto! el pana {winner} es un bisnes man :D")


@bot.command(
    help="comprueva tu posicion y muestra la informacion: tabla "
    "posicion, "
    "propietario, precio_renta, precio_compra.",
    brief="Muestra la info de tu ubicacion actual.",
    name="info_parcela",  # optional shorter command call, prefix w/ $ in chat to
    # execute
)
async def info_parcela(ctx):
    """muestra la informacion del lugar actual."""
    author = ctx.message.author
    user_name = author.name
    info = game.space_info(user_name)
    position = info["position"]
    owner = info["owner"]
    rent_val = info["rent_value"]
    buy_val = info["buy_value"]
    await ctx.channel.send(f"Posicion: {position}\n"
                           f"Propietario: {owner}\n"
                           f"Precio_renta: ${rent_val}\n"
                           f"Precio_compra: ${buy_val}")


@bot.command(
    help="Muestra tu informacion: posicion y saldo actual ",
    brief="Muestra tu informacion: posicion y saldo actual ",
    name="info_p",
    # optional shorter command call, prefix w/ $ in chat to execute
)
async def info_p(ctx):
    """muestra ubicacion jugador y saldo actual"""
    author = ctx.message.author
    user_name = author.name
    position = game.get_player_current_position(user_name)
    money = game.get_player_account_balance(user_name)
    await ctx.channel.send(
        f"{user_name}\nPosicion: {position}\nDinero: ${money}")


@bot.command(
    help="Compras la propiedad y pasa a ser tuya, eso en"
    "el caso ded tener suficiente dinero.",
    brief="Compra la propiedad actual.",
    name="comprar",
    # optional shorter command call, prefix w/ $ in chat to execute
)
async def comprar(ctx):
    """Compra la posiciona actual."""
    # NEED TO ADD handling for invalid purchases (not enough money, already
    # owned, etc.)
    author = ctx.message.author
    user_name = author.name
    game.buy_space(user_name)
    money = game.get_player_account_balance(user_name)
    await ctx.channel.send(
        f"{user_name} ha commprado una parte del vecindario!\nNuevo saldo disponible: $"
        f"{money}")


@bot.command()
async def candy(self, ctx):
    """Pilla el caramelo antes que nadie!"""

    embed = discord.Embed(
        description="🍬 | El primero que la coja se lo queda!", colour=0x0EF7E2)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🍬")

    def check(reaction, user):
        return user != self.bot.user and str(
            reaction.emoji) == '🍬' and reaction.message.id == msg.id

    msg0 = await self.bot.wait_for("reaction_add", check=check)

    embed.description = f"🍬 | {msg0[1].mention} ha ganado y se lo ha comido!"

    await msg.edit(embed=embed)

    with open("candylb.json", "r") as f:

        l = json.load(f)

    try:

        l[str(msg0[1].id)] += 1

    except KeyError:

        l[str(msg0[1].id)] = 1

    with open("candylb.json", "w") as f:

        json.dump(l, f, indent=4)


@bot.command(aliases=["lb", "top"])
async def candyboard(self, ctx):
    """El ranking de top candelers!"""

    with open("candylb.json", "r") as f:

        l = json.load(f)

    lb = sorted(l, key=lambda x: l[x], reverse=True)
    print(lb)
    res = ""

    counter = 0

    for a in lb:

        counter += 1

        if counter > 10:

            pass

        else:

            u = self.bot.get_user(int(a))
            res += f"\n**{counter}.** `{u}` - **{l[str(a)]} 🍬**"

    embed = discord.Embed(description=res, colour=0x0EF7E2)
    await ctx.send(embed=embed)


if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.

bot.run(token)  # Starts the bot
