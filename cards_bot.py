import csv
from discord.ext import commands
import discord
import pandas as pd
import numpy as np
import random, math

bot = commands.Bot(command_prefix='!', description='')



common = ['Kurotsuchi', 'Ebisu', 'Kiba', 'Ino', 'Shikadai', 'Inoichi', 'Sakura', 'Konohamaru', 'Kushina', 'Karin', 'Jugo', 'Udon',
          'Moegi', 'TenTen', 'Rin', 'Temari', 'Kankuro', 'Mabui', 'Darui', 'TonTon', 'Shizune', 'Kimimaro', 'Fugaku', 'Anko',
          'Sai', 'Chiyo', 'Karui', 'Mei', 'Ao']
rare = ['A', 'Bee', 'Gamakichi', 'Gamatatsu', 'Neji', 'Hinata', 'Lee', 'Guy', 'Asuma', 'Shikamaru', 'Hidan', 'Deidara', 'Kakuzu', 'Konan', 'Yahiko', 'Kabuto',
        'Sasori', 'Yamato', 'Haku', 'Suigetsu', 'Chojuro', 'Iruka']
epic = ['Naruto', 'Sasuke', 'Kakashi', 'Gaara', 'Kisame', 'Obito', 'Danzo', 'Hiruzen', 'Tobirama', 'Zetsu', 'Zabuza', 'Gamabunta', 'Ohnoki', 'Shisui']
legendary = ['Jiraiya', 'Orochimaru', 'Tsunade', 'Madara', 'Hashirama', 'Nagato', 'Itachi', 'Hagoromo', 'Minato', 'Ichiraku']


fieldname = ['id', 'name', 'points']

@bot.event
async def on_member_join(member):
    joined = False
    with open('playerStats.csv', 'r', newline='') as w:
        reader = csv.DictReader(w, delimiter=',', fieldnames=fieldname)
        for row in reader:
            if (row['id'] == str(member)):
                joined = True
                break

    with open('playerStats.csv', 'a+', newline='') as w:
        writer = csv.DictWriter(w, fieldname, lineterminator='\n')
        if(joined == False):
            writer.writerow({'id': str(member), 'name': str(member.name), 'points': 0})


@bot.command()
async def join(ctx):
    joined = False
    with open('playerStats.csv', 'r', newline='') as w:
        reader = csv.DictReader(w, delimiter=',', fieldnames=fieldname)
        for row in reader:
            if (row['id'] == str(ctx.author)):
                joined = True
                await ctx.send("you already joined")
                break

    with open('playerStats.csv', 'a+', newline='') as w:
        writer = csv.DictWriter(w, fieldname, lineterminator='\n')
        if(joined == False):
            writer.writerow({'id': str(ctx.author), 'name': str(ctx.author.name), 'points': 0})


@bot.command()
async def playerstats(ctx, name: str):
    with open('playerStats.csv', 'r', newline='') as w:
        reader = csv.DictReader(w, delimiter=',', fieldnames=fieldname)
        for row in reader:
            playerName = str(row['name'])
            if (playerName.lower() == name.lower()):
                await ctx.send("```\n" + "Name: " + row['name'] + "\n" + "Points: " + row['points'] + "\n" + "```")
                break


@bot.command()
async def stats(ctx):
    with open('playerStats.csv', 'r', newline='') as w:
        reader = csv.DictReader(w, delimiter=',', fieldnames=fieldname)
        for row in reader:
            if row['id'] == str(ctx.author):
                await ctx.send("```\n" + "Name: " + row['name'] + "\n" + "Points: " + row['points'] + "\n" + "```")


@bot.command()
async def addpoints(ctx, name: str, amount: int):
    df = pd.read_csv('playerStats.csv')
    df.loc[df['name'] == name, 'points'] += amount
    df.to_csv('playerStats.csv', index=False)
    await ctx.send("Added " + str(amount) + " points to " + name + "'s account")


@bot.command()
async def removepoints(ctx, name: str, amount: int):
    df = pd.read_csv('playerStats.csv')
    df.loc[df['name'] == name, 'points'] -= amount
    df.to_csv('playerStats.csv', index=False)
    await ctx.send("Removed " + str(amount) + " points from " + name + "'s account")


@bot.command()
async def setpoints(ctx, name: str, amount: int):
    df = pd.read_csv('playerStats.csv')
    df.loc[df['name'] == name, 'points'] = amount
    df.to_csv('playerStats.csv', index=False)
    await ctx.send("Set " + name + "'s points" + " to " + str(amount))


@bot.command()
async def disclaimer(ctx):
    await ctx.send("Disclaimer: person placement is purely subjective based off the experiences of Ish and RZKT, don't take this too seriously")


@bot.command()
async def commons(ctx):
    global common
    commonStr = ""
    for person in common:
        commonStr += person + "\n"
    await ctx.send("```\n" + "50% Chance to be opened. \n" + commonStr + "```")


@bot.command()
async def rares(ctx):
    global rare
    rareStr = ""
    for person in rare:
        rareStr += person + "\n"
    await ctx.send("```\n" + "30% Chance to be opened. \n" + rareStr + "```")


@bot.command()
async def epics(ctx):
    global epic
    epicStr = ""
    for person in epic:
        epicStr += person + "\n"
    await ctx.send("```\n" + "14% Chance to open opened. \n" + epicStr + "```")


@bot.command()
async def legendaries(ctx):
    global legendary
    legStr = ""
    for person in legendary:
        legStr += person + "\n"
    await ctx.send("```\n" + "1% Chance to be opened. \n" + legStr + "```")


@bot.command()
async def roll(ctx):
    df = pd.read_csv('playerStats.csv')
    x = random.randrange(0,100)
    playerPoints = 0
    player = ""
    rarity = ""
    with open('playerStats.csv', 'r+', newline='') as w:
        reader = csv.DictReader(w, delimiter=',', fieldnames=fieldname)
        writer = csv.DictWriter(w, fieldname)
        for row in reader:
            if (row['name'] == ctx.author.name):
                playerPoints = int(row['points'])

    if (playerPoints >= 100):
        if (x==99):
            player = legendary[random.randrange(0,len(legendary))]
            rarity = 'Legendary'
            await ctx.send("Congrats! You opened a legendary " + player + "!")
        if(x>=90 and x<99):
            player = epic[random.randrange(0,len(epic))]
            rarity = 'Epic'
            await ctx.send("You opened an epic " + player + "!")
        if(x>=50 and x<90):
            player = rare[random.randrange(0,len(rare))]
            rarity = 'Rare'
            await ctx.send("You opened a rare " + player + ".")
        if(x<50):
            player = common[random.randrange(0,len(common))]
            rarity = 'Common'
            await ctx.send("You opened a common " + player + ".")

        df.loc[df['name'] == ctx.author.name, 'points'] -= 100
        df.to_csv('playerStats.csv', index=False)

        with open('playerCards.csv', 'a', newline='') as w:
            writer2 = csv.DictWriter(w, ['name', 'id', 'card','rarity'], lineterminator='\n')
            writer2.writerow({'name': ctx.author.name, 'id': ctx.author, 'card': player, 'rarity': rarity})

    else:
        await ctx.send("You do not have enough points to roll!")

@bot.command()
async def collection(ctx, page: int):
    cardStr = []
    pageNum = 0
    with open('playerCards.csv', 'r', newline='') as w:
        reader = csv.DictReader(w, delimiter=',', fieldnames=['name', 'id', 'card','rarity'])
        for row in reader:
            if (row['id'] == str(ctx.author)):
                cardStr.append('Your Collection: ''\n')
                cardStr[int(pageNum/10)] += (row['card'] + ":" + row['rarity'] + "\n")
                pageNum += 1
    await ctx.send("```\n" + cardStr[page-1] + 'Page ' + str(page) + ' of ' + str(int(math.ceil(pageNum/10))) + "\n" + "```")


@bot.command()
async def playercollection(ctx, name: str, page: int):
    cardStr = []
    pageNum = 0
    with open('playerCards.csv', 'r', newline='') as w:
        reader = csv.DictReader(w, delimiter=',', fieldnames=['name', 'id', 'card','rarity'])
        for row in reader:
            playerName = str(row['name'])
            if (playerName.lower() == name.lower()):
                cardStr.append(playerName + '\'s Collection: ''\n')
                cardStr[int(pageNum/10)] += (row['card'] + ":" + row['rarity'] + "\n")
                pageNum += 1
    print(str(pageNum/10))
    await ctx.send("```\n" + cardStr[page-1] + 'Page ' + str(page) + ' of ' + str(int(math.ceil(pageNum/10))) + "\n" + "```")


@bot.command()
async def rarity(ctx, rarity: str):
    cardStr = ""

    numRarity = 0
    numTotal = 0

    if (rarity.lower() == 'epic'):
        numTotal = len(epic)
    if (rarity.lower() == 'legendary'):
        numTotal = len(legendary)
    if (rarity.lower() == 'common'):
        numTotal = len(common)
    if (rarity.lower() == 'rare'):
        numTotal = len(rare)

    with open('playerCards.csv', 'r', newline='') as w:
        reader = csv.DictReader(w, delimiter=',', fieldnames=['name', 'id', 'card','rarity'])
        cardStr += ('Your ' + rarity + ' collection: ' + '\n')
        for row in reader:
            if (row['id'] == str(ctx.author) and str(row['rarity']).lower() == rarity.lower() and (cardStr.find(str(row['card'])) == -1)):
                cardStr += (row['card'] + ":" + row['rarity'] + "\n")
                numRarity += 1
        cardStr += ('You have ' + str(numRarity) + '/' + str(numTotal) + " " +rarity + 's')
    await ctx.send("```\n" + cardStr + "\n" + "```")


@bot.command()
async def playerrarity(ctx, name: str ,rarity: str):
    cardStr = ""
    numRarity = 0
    numTotal = 0

    if(rarity.lower() == 'epic'):
        numTotal = len(epic)
    if (rarity.lower() == 'legendary'):
        numTotal = len(legendary)
    if (rarity.lower() == 'common'):
        numTotal = len(common)
    if (rarity.lower() == 'rare'):
        numTotal = len(rare)

    with open('playerCards.csv', 'r', newline='') as w:
        reader = csv.DictReader(w, delimiter=',', fieldnames=['name', 'id', 'card','rarity'])
        cardStr += (name + '\'s ' + rarity + ' collection: ' + '\n')
        for row in reader:
            playerName = str(row['name'])
            if (playerName.lower() == name.lower() and str(row['rarity']).lower() == rarity.lower() and (cardStr.find(str(row['card'])) == -1)):
                cardStr += (row['card'] + ":" + row['rarity'] + "\n")
                numRarity += 1
        cardStr += (name + ' has ' + str(numRarity) + '/' + str(numTotal) + ' ' +rarity + 's')
    await ctx.send("```\n" + cardStr + "\n" + "```")


@bot.command()
async def discard(ctx, cardName: str):
    dupeCount = 0
    someCount = 0
    with open('playerCards.csv', 'r', newline='') as r, open('playerCards_edit.csv', 'w', newline='') as w:
        writer = csv.DictWriter(w, fieldnames=['name', 'id', 'card','rarity'])
        reader = csv.DictReader(r, delimiter=',')
        writer.writeheader()
        for row in reader:
            if (row['card'] != cardName or row['name'] != ctx.author.name):
                writer.writerow(row)
            if (row['card'] == cardName and row['name'] == ctx.author.name):
                if (dupeCount == 0):
                    await ctx.send("Discarded your " + row['card'] + ".")
                    dupeCount += 1
                else:
                    writer.writerow(row)
            else:
                someCount += 1
                if (someCount > 0 and someCount < 2 and row['card'] == cardName):
                    await ctx.send("You do not have a " + row['card'] + ".")

    with open('playerCards_edit.csv', 'r', newline='') as r, open('playerCards.csv', 'w', newline='') as w:
        writer = csv.DictWriter(w, fieldnames=['name', 'id', 'card','rarity'])
        reader = csv.DictReader(r, delimiter=',')
        writer.writeheader()
        for row in reader:
            writer.writerow(row)


@bot.command()
async def discardduplicates(ctx):
    df = pd.read_csv('playerCards.csv')
    df.drop_duplicates(inplace=True, keep='first')
    df.to_csv('playerCards.csv', index=False)
    await ctx.send("Discarded all duplicate cards.")

@bot.command()
async def discardall(ctx):
    df = pd.read_csv('playerCards.csv')
    df.loc[df['name'] == str(ctx.author.name), 'rarity'] = ''
    df.loc[df['name'] == str(ctx.author.name), 'card'] = ''
    df.loc[df['name'] == str(ctx.author.name), 'id'] = ''
    df.loc[(df['name'] == ctx.author.name), 'name'] = ''
    df['name'].replace('', np.nan, inplace=True)
    df.dropna(subset=['name'], inplace=True)
    #print(df)
    df.to_csv('playerCards.csv', index=False)
    await ctx.send('Discarded all cards in your collection.')

otherPlayerId = ''
otherPlayerName = ''


@bot.command()
async def trade(ctx, name: str, card1: str, card2: str):

    global otherPlayerId
    global otherPlayerName

    traderHasCard = False
    otherHasCard = False
    df = pd.read_csv('playerCards.csv')

    with open('playerCards.csv', 'r', newline='') as r:
        reader = csv.DictReader(r, delimiter=',')
        for row in reader:
            if(row['name'] == ctx.author.name and row['card'] == card1):
                traderHasCard = True
            if(row['name'] == name and row['card'] == card2):
                otherHasCard = True

    if (traderHasCard == True):
        if(otherHasCard == True):
            otherPlayerId = df.loc[(df['name'] == name) & (df['card'] == card2), 'id'].values[0]
            otherPlayerName = df.loc[(df['id'] == otherPlayerId) & (df['card'] == card2), 'name'].values[0]
            await ctx.send("Trade sent, waiting for " + otherPlayerId + " to confirm.")
            await ctx.send("To confirm, " + otherPlayerId + " must type !tradeaccept " + ctx.author.name + " " + card2 +" " + card1 + ".")
        else:
            await ctx.send("The other person does not have the card required for the trade.")
    else:
        await ctx.send("You do not have the card required for the trade.")

@bot.command()
async def tradeaccept(ctx, name: str, card1: str, card2: str):
    global otherplayerId
    global otherPlayerName

    df = pd.read_csv('playerCards.csv')
    if (otherPlayerName == ctx.author.name):
        otherPlayerId = df.loc[(df['name'] == name) & (df['card'] == card2), 'id'].values[0]
        df.loc[(df['name'] == name) & (df['card'] == card2), 'id'] = ctx.author
        df.loc[(df['id'] == ctx.author) & (df['card'] == card2), 'name'] = ctx.author.name
        df.loc[(df['name'] == str(ctx.author.name)) & (df['card'] == card1), 'id'] = otherPlayerId
        df.loc[(df['id'] == otherPlayerId) & (df['card'] == card1), 'name'] = name
        df.to_csv('playerCards.csv', index=False)
        await ctx.send("Trade confirmed.")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    with open('playerStats.csv', 'r+', newline='') as w:
        fieldnames = fieldname
        writer = csv.DictWriter(w, fieldnames)
        writer.writeheader()
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!rolling for Itachi"))


@bot.command()
async def roulette(ctx, amount: int, bet: str):
    x = random.randint(0,36)
    colorInt = random.randint(0,1)
    color = ""
    if (colorInt == 0):
        color = 'black'
    else:
        color = 'red'

    playerPoints = 0
    with open('playerStats.csv', 'r', newline='') as w:
        reader = csv.DictReader(w, delimiter=',', fieldnames=fieldname)
        for row in reader:
            if row['id'] == str(ctx.author):
                playerPoints = int(row['points'])

    df = pd.read_csv('playerStats.csv')
    if (playerPoints >= amount):
        await ctx.send("The ball landed on " + str(x) + " and the color was " + color + ".")
        df.loc[df['name'] == ctx.author.name, 'points'] -= amount
        df.to_csv('playerStats.csv', index=False)
        if (bet.lower() == 'even' and x%2 == 0):
            df.loc[df['name'] == ctx.author.name, 'points'] += (2*amount)
            df.to_csv('playerStats.csv', index=False)
        if (bet.lower() == 'odd' and x%2 == 1):
            print("ra")
            df.loc[df['name'] == ctx.author.name, 'points'] += (2*amount)
            df.to_csv('playerStats.csv', index=False)
        if (bet.lower() == 'low' and x < 19):
            df.loc[df['name'] == ctx.author.name, 'points'] += (2*amount)
            df.to_csv('playerStats.csv', index=False)
        if (bet.lower() == 'high' and x > 18 and x < 36):
            df.loc[df['name'] == ctx.author.name, 'points'] += (2*amount)
            df.to_csv('playerStats.csv', index=False)
        if (bet == '36' and x == 36):
            df.loc[df['name'] == ctx.author.name, 'points'] += (36 * amount)
            df.to_csv('playerStats.csv', index=False)
        if (bet.lower() == 'red' and color == 'red'):
            df.loc[df['name'] == ctx.author.name, 'points'] += (2 * amount)
            df.to_csv('playerStats.csv', index=False)
        if (bet.lower() == 'black' and color == 'black'):
            df.loc[df['name'] == ctx.author.name, 'points'] += (2 * amount)
            df.to_csv('playerStats.csv', index=False)
    else:
        await ctx.send("You do not have enough points.")
        df.loc[df['name'] == ctx.author.name, 'points'] += amount
        df.to_csv('playerStats.csv', index=False)


@bot.command()
async def commands(ctx):
    await ctx.send("```\nCommands:\n!join, Required before starting anything using points." \
                  "\n!stats, Display your stats. \n!playerstats <Name>, display the stats of another user.\n" \
                  "!roll, Roll to get yourself a fancy new card.\n!roulette <amount of points> <bet>, bet money for a chance to get more."
                   "\n\tBet can be: even, odd, red, black, low(1-18), high (19-35), 36(returns points times 36) \n"
                   "!collection <Page Number>, Display your collection.\n!playercollection <Name> <Page Number>, Display another player's collection.\n"
                   "!discard <card>, discards a single piece from your collection.\n!discardduplicates, discards all duplicate pieces from your collection.\n"
                   "!trade <Name> <Your Card> <Their Card>, asks a user to trade for a card in their collection.\n"
                   "!commons, Display all common cards.\n!rares, Display all rare cares.\n!epics, Display all epic cards.\n"
                   "!legendaries, Display all legendary cards.""\n```") 