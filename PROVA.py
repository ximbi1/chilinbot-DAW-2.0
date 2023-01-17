import discord
from discord.ext import commands
import random
import time

bot = commands.Bot(command_prefix='!')

words = ["palabra1", "palabra2", "palabra3", "palabra4", "palabra5"]

players = {}

def search_word(word, letter):
    if letter in word:
        return True
    else:
        return False

@bot.command()
async def play(ctx):
    await ctx.send("El juego ha comenzado. Escriba una palabra que contenga la letra 'x'.")
    chosen_word = random.choice(words)
    start_time = time.time()
    def check(message):
        return message.author != bot.user and search_word(message.content, "x")
    try:
        guess = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Se acabó el tiempo. La palabra correcta era: " + chosen_word)
    else:
        end_time = time.time()
        elapsed_time = end_time - start_time
        if guess.content == chosen_word:
            await ctx.send("¡Correcto! La palabra era " + chosen_word + " y lo has adivinado en " + str(elapsed_time) + " segundos.")
            if ctx.message.author.name in players:
                players[ctx.message.author.name]["score"] += 1
                players[ctx.message.author.name]["time"] += elapsed_time
            else:
                players[ctx.message.author.name] = {"score":1, "time":elapsed_time}
        else:
            await ctx.send("Lo siento, la palabra correcta era " + chosen_word + ".")

@bot.command()
async def top(ctx):
    if len(players) == 0:
        await ctx.send("No hay jugadores aún.")
    else:
        sorted_players = sorted(players.items(), key=lambda x: x[1]["score"], reverse=True)
        top_players = sorted_players[:3]
        top_message = "Top 3 jugadores:\n"
        for player in top_players:
            top_message += player[0] + ": " + str(player[1]["score"]) + " aciertos en " + str(player[1]["time"]) + " segundos.\n"
        await ctx.send(top_message)

bot.run('Your_Token_Here')
