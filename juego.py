
import discord
import logging
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
import os
import random

token="<Enter Bot Token here>"

bot = commands.Bot(command_prefix="!")
bot.remove_command('help')

@bot.event
async def on_ready():
   print("Ye boi is up!")
   await bot.change_presence(activity=discord.Game(name="Type !signup to signup", type = 2))

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def logout(ctx):
    await bot.logout()

Players=[]
Roles=["K","Q","M","P","T"]
TRoles=[]
PR={}
GS =0
NOP=0
Round=0
Points={}
Thief=""
Police=""

@bot.command()
async def signup(ctx):
    global Players
    global GS
    global NOP
    global Points
    global Roles
    global PR
    if GS == 0:
        if not ctx.author in Players:
         Players.append(ctx.author)
         Points[ctx.author]=0
         PR[ctx.author]=""
         await ctx.send("Done!Signed up {} !".format(ctx.author.mention))
         NOP += 1
         print (NOP)
         if NOP >5:
             Roles.append("M")
             print(Roles)
        else:
            await ctx.send("You have already signed-up!")
    else:
        await ctx.send("A game is on-going.")

@bot.command()
async def start(ctx):
    global GS
    global NOP
    global TRoles
    global Roles
    TRoles=Roles[:]
    if NOP>4:
        GS=1
        await draw()
        await ctx.send("Roles have been choosen , The Police Please proceed to find the thief.")
    else:
        await ctx.send("More players are required.")

@bot.command()
async def slist(ctx):
    global Players
    for i in Players:
        await ctx.send(i.mention)

@bot.command()
async def s(ctx,it:discord.Member):
    global Thief
    global Police
    global Roles
    global TRoles
    global PR
    global Points
    if GS==1:
        if ctx.author==Police:
            if it==Thief:
                await ctx.send("The thief is found!")
                Points[ctx.author]+=1000
                Police=""
                Thief=""
                Roles=TRoles[:]
                PR={}
            else:
                await ctx.send("The thief escaped.")
                Points[Thief]+=500
                print(Points[Thief])
                Police=""
                Thief=""
                Roles=Troles[:]
                PR={}
        else:
            await ctx.send("You are not the police.")

        

@bot.command()
async def nxtround(ctx):
    global GS
    if GS ==1:
        await draw()
        await ctx.send("Roles have been choosen , The Police Please proceed to find the thief.")

@bot.command()
async def points(ctx):
    global Points
    for i in Points:
        await ctx.send("{} ,Your points are , {}".format(i.mention,Points[i]))

@bot.command()
async def end(ctx):
    global Players
    global Roles
    global PR
    global GS 
    global NOP
    global Round
    global Points
    global Thief
    global Police
    global TRoles
    for i in Points:
        await ctx.send("{} ,Your points are , {}".format(i.mention,Points[i]))
    Players=[]
    Roles=["K","Q","M","P","T"]
    TRoles=[]
    PR={}
    GS =0
    NOP=0
    Round=0
    Points={}
    Thief=""
    Police=""

async def draw():
    global Roles
    global PR
    global Points
    global Police
    global Thief
    global Round
    global TRoles
    for i in Players:
        a= random.choice(Roles)
        Roles.remove(a)
        await i.send(a)
        PR[i]=a
        print(PR[i])
        if a=="K":
            Points[i]+= 10000
            await i.send("Points Awarded.Total points:- {}".format(Points[i]))
        elif a=="Q":
            Points[i]+= 5000
            await i.send("Points Awarded.Total points:- {}".format(Points[i]))
        elif a=="M":
            Points[i]+= 3000
            await i.send("Points Awarded.Total points:- {}".format(Points[i]))
        elif a=="P":
            await i.send("Use !s <user> to confirm your target.")
            Police = i
        elif a=="T":
            Thief = i
    Round+=1
    Roles=[]
    print(Round)

@bot.command()
async def help(ctx):
    help=discord.Embed(colour=discord.Colour.red())
    help.set_author(name="HELP")
    help.add_field(name="Help",value="Displays this message",inline="false")
    help.add_field(name="Ping",value="Returns pong",inline="false")
    help.add_field(name="Logout",value="Turns off the bot",inline="false")
    help.add_field(name="Signup",value="Signs you up.",inline="false")
    help.add_field(name="Start",value="Starts the game .Will only work if more than 4 people have signed up.",inline="false")
    help.add_field(name="slist",value="Shows the people who have signed up.",inline="false")
    help.add_field(name="nxtround",value="Starts the next round.",inline="false")
    help.add_field(name="Points",value="Shows the points of every person.",inline="false")
    help.add_field(name="How to play?",value="To start people need to type !signup to join.After more than 4 people have joined, type !start to start the game.After you typed that , each person will get a message mentioning your role",inline="false")
    help.add_field(name="Roles",value="K -King - +10000 points. \nQ -Queen - +5000 points. \n M -Minister - +3000 points. \nP -Police - IF he finds the thief , +1000 points. \nT- Thief - +500 points if the police doesn't find you",inline="false")
    help.add_field(name="How to end the game?",value="The game will end as soon as the police attempts to find the thief.Type !start or !nxtround to start the next round. Typing !end will end the whole game and post all the points.",inline="false")
    await ctx.send(embed=help)
