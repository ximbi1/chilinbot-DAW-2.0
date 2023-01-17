
levels = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith('!level'):
        return
    if message.author.id not in levels:
        levels[message.author.id] = {"name": message.author.name, "level": 1, "messages": 1}
    else:
        levels[message.author.id]["messages"] += 1
        if levels[message.author.id]["messages"] % 10 == 0:
            levels[message.author.id]["level"] += 1
            await message.channel.send(f"Felicidades {message.author.mention}, has subido al nivel {levels[message.author.id]['level']}!")
    with open('levels.json', 'w') as f:
        json.dump(levels, f)

@bot.command()
async def level(ctx):
    if ctx.author.id in levels:
        await ctx.send(f"{ctx.author.mention}, tu nivel actual es {levels[ctx.author.id]['level']}.")
    else:
        await ctx.send(f"{ctx.author.mention}, no tienes ningun nivel.")

@bot.command()
async def ranking(ctx):
    sorted_levels = sorted(levels.items(), key=lambda x: x[1]['level'], reverse=True)
    ranking = ""
    for i, (user_id, user_data) in enumerate(sorted_levels):
        ranking += f"{i+1}. {user_data['name']} - Nivel {user_data['level']}\n"
    await ctx.send(f"**Ranking de niveles:**\n{ranking}")