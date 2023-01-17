#linea 420
@bot.command(name='coleccion', help='Muestra la coleccion de cartas')
async def mostrar_coleccion(ctx):
    if not collection:
      await ctx.send("Tu coleccion esta vacia.")
      return
    
    else: # Calcular el número de páginas
      pages = (len(collection) - 1) // 1 + 1

    # Verificar que la página es válida
    if page < 1 or page > pages:
        await ctx.send(f"numero de pagina invalido. porfavor pon un numero del 1 al {pages}.")
        return

    # Mostrar las cartas de la página
    start = (page - 1)
    end = start + 1
    message = f"Tu coleccion (page {page} of {pages}):\n"
    for i, card in enumerate(collection[start:end], start=start+1):
        message += f"{i}. {card['name']}\n"
        message += f"{card['image_uris']['large']}\n"
    await ctx.send(message)

    # Agregar las reacciones para cambiar de página
    if pages > 1:
      msg = await ctx.send("reacciona con ⬅️ para ir a la pagina anterior, ➡️ para ir a la siguiente, o 🔴 para parar.")
      await msg.add_reaction("⬅️")
      await msg.add_reaction("➡️")
      await msg.add_reaction("🔴")
      def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️", "🔴"]

      while True:
        try:
          reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
          
        except asyncio.TimeoutError:
          await ctx.send("Tiempo agotado.")
          return

      if str(reaction.emoji) == "⬅️":
        page -= 1
        if page < 1:
          page = pages
          await msg.delete()
          await show_collection(ctx, page)
          return
      elif str(reaction.emoji) == "➡️":
        page += 1
        if page > pages:
          page = 1
          await msg.delete()
          await show_collection(ctx, page)
          return
      elif str(reaction.emoji) == "🔴":
        return
