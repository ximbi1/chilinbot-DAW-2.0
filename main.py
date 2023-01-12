import os
import random
import config
#import wordle
import SQLmanager
from minipoly import *
from datetime import date
import discord
from keep_alive import keep_alive
from discord.ext import commands

#####Zona para la classe del laberinto#####
from builder import make_maze
import random
import math

class Map:
    def rand(self):
        direction = random.randint(0, 3)
        if direction == 0:
            x = random.randint(1, len(self.map) - 2)
            y = 0
        elif direction == 1:
            x = 0
            y = random.randint(1, len(self.map[0]) - 2)
        elif direction == 2:
            x = random.randint(1, len(self.map) - 2)
            y = len(self.map[0]) - 1
        else:
            x = len(self.map) - 1
            y = random.randint(1, len(self.map[0]) - 2)

        if (x == 0 and self.map[x+1][y] != " ") or (y == 0 and self.map[x][y+1] != " ") or (x == len(self.map) - 1 and self.map[x-1][y] != " ") or (y == len(self.map[0]) - 1 and self.map[x][y-1]) :
            return self.rand()

        return [x,y]

    def __init__(self, map):
        self.map = map
        self.player = [0, 0]
        self.won = False


        x,y = self.rand()
        self.player = [x, y]
        self.map[x] = self.map[x][:y] + "🐒" + self.map[x][y+1:]

        while x == self.player[0] and y == self.player[1] or self.map[x][y] == " ":
            x, y = self.rand()

        self.map[x] = self.map[x][:y] + "🏁" + self.map[x][y+1:]


    def __str__(self):
        return "\n".join(self.map)

    def move(self,x,y):
        try:
            if self.map[x][y] != " "  and self.map[x][y] != "🏁":
                return
        except IndexError:
            return

        if self.map[x][y] == "🏁":
            self.won = True

        self.map[self.player[0]] = self.map[self.player[0]].replace("🐒", " ")
        self.player = [x, y]
        self.map[x] = self.map[x][:y] + "🐒" + self.map[x][y+1:]


games = {}
##################FINAL PRIMERA PARTE##############

#######################prefijo para llamar al bot############
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "a ", intents=intents, case_insensitive=True)
token = os.environ["DISCORD_BOT_SECRET"]

bot.author_id = 1041801498608275556  # Change to your discord id!!!


####################INICIO DE SEGUNDA PARTE PARA EL LABERINTO

def draw(game, status):
    blank = str(discord.utils.get(bot.emojis, name="v_"))
    message = ""
    for i in range(game.player[0] - 5, game.player[0] + 5):
        for j in range(game.player[1] - 5, game.player[1] + 5):
            if i < 0 or j < 0 or i >= len(game.map) or j >= len(game.map[i]):
                message += blank
                continue

            message += game.map[i][j] if game.map[i][j] != " " else blank

        message += "\n"

    return message + status

@bot.command(name = "laberinto")
async def laberinto(ctx, size = "3x3", color = "white"):
    b = "⬜" if color.lower() == "white" else "⬛"
    w,h = size.lower().split("x")
    if int(w) < 3 or int(h) < 3 or int(w) > 35 or int(h) > 35:
        await ctx.send("Tamaño no valido: rango(3x3 - 35x35)")
        return

    try:
        if games.get(ctx.author.id) is not None:
            await games[ctx.author.id][1].delete()
    except Exception:
        pass

    game = Map(make_maze(int(w),int(h)).replace("+", b).replace("-", b).replace("|", b).split("\n")[:-2])
    message = draw(game, f"\nPropietario: {ctx.author.name}\nEstado: JUGANDO")
    msg = await ctx.send(message)

    games[ctx.author.id] = (game, msg)

    await msg.add_reaction("⬅️")
    await msg.add_reaction("⬆️")
    await msg.add_reaction("⬇️")
    await msg.add_reaction("➡️")

    await msg.add_reaction("🛑")

@bot.event
async def on_reaction_add(reaction, user):
    try:
        game = games[user.id][0]
    except KeyError:
        return

    if str(reaction) == "⬅️":
        game.move(game.player[0], game.player[1] - 1)

    if str(reaction) == "⬆️":
        game.move(game.player[0] - 1, game.player[1])

    if str(reaction) == "⬇️":
        game.move(game.player[0] + 1, game.player[1])

    if str(reaction) == "➡️":
        game.move(game.player[0], game.player[1] + 1)

    await games[user.id][1].remove_reaction(str(reaction), user)
    if str(reaction) == "🛑":
        await games[user.id][1].delete()
        del games[user.id]
        return

    if game.won:
        await games[user.id][1].edit(content=draw(game, f"\nPropietario: {user.name}\nEstado: Ganaste"))
        del games[user.id]
    else:
        await games[user.id][1].edit(content=draw(game, f"\nPropietario: {user.name}\nEstado: JUGANDO"))

########FINAL DEL LABERINTO########################

@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


extensions = [
	'cogs.cog_example'  # Same name as it would be if you were importing it
]
@bot.event
async def on_ready():
  print("ready")
  await bot.change_presence(activity=discord.Game('TERMINA AITOR'))
#on sessage######################
xd = ["uwu", "f", "xd", "nice", 'a', "maricon"]
blacklist = []
@bot.event
async def on_message(message):
  author = message.author
  content = message.content
  canal = message.channel
  aitor = 817313326161592342
  if author.id in blacklist:
    await canal.send(" calla tontika")
  elif content.lower() in xd and author.id  != aitor:
    await canal.send(content)
  elif canal.id == 1047957981200924693 and author.id != aitor:
    lastmsg = await canal.history(limit=2).flatten()
    if lastmsg[1].author == author:
      await message.delete()
    elif random.randint(1,10) == 5:
      try:
        await canal.send(f"{int(content) + 1}")
      except ValueError:
        await canal.send("xd")
  
  if message.content == "AITOR":
    await message.channel.send("TERMINATOR!")



  await bot.process_commands(message)

  #Clear#################################################
@bot.command(
    description="elimina el numero de mensajes especificados")
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
async def atencion(ctx, *, announce=None):
	if not ctx.guild:
		await ctx.send('Este comando no se puede usar en privado.')
	else:
		await ctx.message.delete()
		embed = discord.Embed(title="✅ Atension plis un mensaje importante", description="Toda la informacion aqui debajo", color=0xd01818)
		embed.add_field(name="Aviso echo por", value=ctx.author.mention)
		embed.add_field(name="Aviso ", value=announce)
		embed.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(embed=embed)

###########sugerencia#########
@bot.command()
async def sugerencia(ctx, *, sugerencia=None):
    if not sugerencia:
        await ctx.send('Tienes que dar una sugerencian')
        return

    channel = ctx.bot.get_channel(config.channels['sugerencias'])

    em = discord.Embed(
        title=f'Sugerencia',
        description=f'*{sugerencia}*',
        color=discord.Color.blurple()
    )
    em.set_author(
        name=f'Sugerencia de {ctx.author}', icon_url=ctx.author.avatar_url)
    suggestMsg = await channel.send(embed=em)
    await suggestMsg.add_reaction('👍')
    await suggestMsg.add_reaction('👎')

    em = discord.Embed(
        description=f'Sugerencia mandada con exito en <#{channel.id}>',
        color=discord.Color.green()
    )
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
    help="Primero tira el dado para tu movimiento. Despues se mueve las casillas correspondientes "
    "Para ti. "
    "Movimiento automatico que comprueva si la casilla donde estas tiene dueño, "
    "y entonces tienes "
    "que pagarle. Tu nuevo espacio se muestra, "
    "al igual que las notificaciones de renta si eso "
    "pasa. Finalmente "
    "se comprueva el estado del juego, y se declara un ganador si es que hay uno.",
    brief="Tiras los dados y te mueves, paga o compra renta en la propiedad si es necessario.",
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
    await ctx.channel.send(
        f"Posicion: {position}\n"
        f"Propietario: {owner}\n"
        f"Precio_renta: ${rent_val}\n"
        f"Precio_compra: ${buy_val}"
    )
    player = game.get_players()[user_name]
    player_space = player.get_current_space()
    player_space_owner = player_space.get_owner()
    if player_space_owner is not None:
        await ctx.channel.send(
            f"{user_name} ha pagado ${rent_val} en la renta de {owner}!"
        )
    if money_after_move == 0:
        await ctx.channel.send(f"ups. {user_name} te has quedado sin dinero.. :(\nGGWP {user_name}")
    winner = game.check_game_over()
    if winner != "":
        await ctx.channel.send(
            f"Ahi te visto! el pana {winner} es un bisnes man :D"
        )


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
    await ctx.channel.send(
        f"Posicion: {position}\n"
        f"Propietario: {owner}\n"
        f"Precio_renta: ${rent_val}\n"
        f"Precio_compra: ${buy_val}"
    )


@bot.command(
    help="Muestra tu informacion: posicion y saldo actual " ,
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
    await ctx.channel.send(f"{user_name}\nPosicion: {position}\nDinero: ${money}")


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
        f"{user_name} ha commprado una parte del vecindario!\nNuevo saldo disponible: $" f"{money}"
    )




if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
 
bot.run(token)  # Starts the bot