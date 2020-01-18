import discord
import asyncio
import datetime
import json
import yaml
import sys
import os
import errno
import base64
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix="$")
bot.remove_command("help")

configFilename = None

configFilename = sys.argv[1]

if configFilename is None:
    print("You did not specifiy a configuration file")
    sys.exit(1)
    
with open(configFilename, 'r') as yamlConfig:
    cfg = yaml.load(yamlConfig)

admins = []
for i in cfg['admin']:
    admins.append(i)

API_KEY = cfg['api-key']
print("The P&W API Key is: {}".format(API_KEY))        

@bot.event
async def on_ready():
    print("Bot {} has successfully logged in. Servicing {} guilds".format(bot.user.name, len(bot.guilds)))
    await bot.change_presence(activity=discord.Game("With itsself..."))

@bot.command(pass_context=True)
async def nationhelp(ctx, *args):
    url = "http://politicsandwar.com/api/nation/id={}&key={}".format(137331, API_KEY)
    fetchedData = requests.get(url)
    fetchedData = fetchedData.json()
    msg = "Keys Availible:\n"
    for key in fetchedData:
        msg = msg + key + ', '
    try:
        await ctx.channel.send(msg)
    except:
        await ctx.channel.send("Message too long")    
    
@bot.command(pass_context=True)
async def getNation(ctx, *args):
    url = "http://politicsandwar.com/api/nation/id={}&key={}".format(args[0], API_KEY)
    print(url)
    fetchedData = requests.get(url)
    fetchedData = fetchedData.json()
    msg = ""
    for key in fetchedData:
        if key not in ['cityids', 'socialpolicy', 'government', 'founded','allianceposition ','allianceid', 'title', 'econpolicy', 'approval', 'latitude', 'longitude', 'population', 'gdp', 'nukeslaunched', 'nukeseaten', 'infsesttot', 'infralost', 'moneylooted','soldiercasualties', 'tankcasualties', 'aircraftcasualties' ]:
            msg = msg + key + ' : ' + str(fetchedData[key]) + '\n'
    #msg = str(fetchedData)[0:1999]
    try:
        await ctx.channel.send(msg)
    except:
        await ctx.channel.send("Message too long")
        
@bot.command(pass_context=True)
async def getNationKey(ctx, *args):
    url = "http://politicsandwar.com/api/nation/id={}&key={}".format(args[0], API_KEY)
    print(url)
    if len(args) != 2:
        await ctx.channel.send("$getNationKey <nationid> <key>")
    else:
        fetchedData = requests.get(url)
        fetchedData = fetchedData.json()    
        keyFound = False
        for key in fetchedData:
            #print(key)
            #print(args[1])
            if key == args[1]:
                msg = 'Nation ' + str(fetchedData['name']) + ' : ' + key + ' : ' + str(fetchedData[args[1]])
                keyFound = True
                break
        if keyFound is False:
            msg = "Could not find Key"
        try:
            await ctx.channel.send(msg)
        except:
            await ctx.channel.send("Message too long")

@bot.command(pass_context=True)
async def getAlliance(ctx, *args):
    if len(args) != 1:
        await ctx.channel.send("No alliance ID provided")
    else:
        url = "http://politicsandwar.com/api/alliance/id={}&key={}".format(args[0], API_KEY)
        print(url)
        fetchedData = requests.get(url)
        fetchedData = fetchedData.json()    
        msg = ""
        for key in fetchedData:
            msg = msg + key + ' : ' + str(fetchedData[key]) + '\n'
        try:
            await ctx.channel.send(msg)
        except:
            await ctx.channel.send("Message too long")
            
@bot.command(pass_context=True)
async def getLastTrades(ctx, *args):
    url = "http://politicsandwar.com/api/trade-history/key={}".format(API_KEY)
    print(url)
    count = 0
    fetchedData = requests.get(url)
    fetchedData = fetchedData.json()    
    msg = ""
    if fetchedData['success'] == True:
        for trade in fetchedData['trades']:    
            if(count < 10):
                for key in trade:
                    print(key)
                    if key in ['trade_id','offerer_nation_id','accepter_nation_id','resource','offer_type','quantity','price']:
                        msg = msg + key + ' : ' + trade[key] + ','
                print(trade)
                msg = msg + '\n'
                count += 1
            else:
                break
        print(msg)
        print(len(msg))
        try:
            await ctx.channel.send(msg)
        except:
            await ctx.channel.send("Message too long")
            
@bot.command(pass_context=True)
async def getAllianceBank(ctx, *args):
    if len(args) != 1:
        await ctx.channel.send("No alliance ID provided")
    else:
        url = "http://politicsandwar.com/api/alliance-bank/?allianceid={}&key={}".format(args[0], API_KEY)
        print(url)
        fetchedData = requests.get(url)
        fetchedData = fetchedData.json()    
        msg = ""
        for key in fetchedData['alliance_bank_contents']:
            print(key)
            for k in key:
                msg = msg + k + ' : ' + str(key[k]) + '\n'
        try:
            await ctx.channel.send(msg)
        except:
            await ctx.channel.send("Message too long")
            
@bot.command(pass_context=True)
async def help(ctx, *args):
    msg = "**Help**\n"
    msg = msg + "```\n"
    msg = msg + "8==========D~~~~~~~~\n"
    msg = msg + "```\n"
    await ctx.channel.send(msg)


@bot.event
async def on_message(msg):
    if msg.channel.name is None:
        print("No channel name: {}".format(msg))
    else:
        await bot.process_commands(msg)
    return None

Token=cfg['discord-token']

bot.run(Token)
