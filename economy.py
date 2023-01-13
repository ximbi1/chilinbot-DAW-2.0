import json
import discord
import datetime

#Add ppl
def add_ppl(user, basecoins = 0):
  with open("users.json", "r") as f:
    users = json.load(f)

  if not f"{user.id}" in users:

    users[f"{user.id}"] = {}
    users[f"{user.id}"]["KickCoins"] = basecoins
    users[f"{user.id}"]["Name"] = user.name

    with open("users.json", "w") as f:
      json.dump(users, f, indent = 2)

#Add Coins
async def add_coins(user, coins):
  with open("users.json", "r") as f:
    users = json.load(f)

  if f"{user.id}" in users:
    users[f"{user.id}"]["KickCoins"] += int(coins)

    with open("users.json", "w") as f:
      json.dump(users, f, indent = 2)

  else:
    add_ppl(user, int(coins))
  

#Remove Coins
async def remove_coins(user, coins):
  with open("users.json", "r") as f:
    users = json.load(f)

  if f"{user.id}" in users:
    users[f"{user.id}"]["KickCoins"] -= int(coins)
    if users[f"{user.id}"]["KickCoins"] < 0:
      users[f"{user.id}"]["KickCoins"] = 0

    with open("users.json", "w") as f:
      json.dump(users, f, indent = 2)
  else:
    add_ppl(user)

#KickCoins
def KickCoins(user):
  with open("users.json", "r") as f:
    file = json.load(f)  
  if f"{user.id}" in file:
    return file[f"{user.id}"]["KickCoins"] 
  else:
   add_ppl(user)
   return 0

#leaderboard
def leaderboard(server):
  users = []
  for member in server.members:
    for user in users:      
      if KickCoins(member) >= KickCoins(user) and not member in users:
        users.insert(users.index(user), member)
      elif user == users[-1] and not member in users:
        users.append(member) 
    if users == []:
      users.append(member)

  return users

#UpdateLeaderboard
async def update_leaderboard(guild):
  channel = guild.get_channel(832668715799281685)
  msg = await channel.fetch_message(841419861435088956)

  embed = discord.Embed(title="LEADERBOARD",
	                      description="Se actualiza cada hora",
	                      color=0xfbff00,
	                      timestamp=datetime.datetime.utcnow())
  i = 0
  for user in leaderboard(guild):
    embed.add_field(
      name = f"{i+1}. {user.name}",
      value=f"BALANCE = {KickCoins(user)}",
      inline = False  
    )
    i += 1
    if i == 10:
      break

  await msg.edit(content= None, embed = embed)
  