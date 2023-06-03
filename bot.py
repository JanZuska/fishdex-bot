#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
__author__ = "Jan Zuska"
__date__ = "2023/4/24"
__copyright__ = "Copyright 2023, Jan Zuska"
__credits__ = []
__license__ = "GPLv3"
__version__ = "2.1.0"
__maintainer__ = "Jan Zuska"
__email__ = "jan.zuska.04@gmail.com"
__status__ = "Production"
# ----------------------------------------------------------------------------
import discord
from discord.ext import commands
import database
import functions
import embeds
import json
import consoleLog
import views
import objects

with open("assets/json/fishao-data.json", "r") as file:
    fish: list = json.load(file)
    file.close()

with open("assets/json/config.json", "r") as file:
    config = json.load(file)
    API_KEY: str = config["API_KEY"]
    file.close()

with open("assets/json/location.json", "r") as file:
    locations: dict = json.load(file)
    file.close()

FISH = objects.Fishes(fish)
LOCATIONS = objects.Locations(locations)

WHITELIST = [705076428118556744, 602125362612404224, 979391818993131530]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.slash_command()
async def fishdex(ctx: commands.Context):
    await ctx.response.defer()
    
    db: database.Database = database.Database(user_id = ctx.author.id)
    caught, shiny = db.Caught(), db.Shiny()
    embed: discord.Embed = embeds.Locations(ctx = ctx, bot = bot, caught = caught, shiny = shiny).Get()
    
    view: discord.ui.View = views.Fishdex(ctx = ctx, db = db, bot = bot, fish = FISH, locations = LOCATIONS)
    
    message = await ctx.followup.send(embed = embed, view = view)

    consoleLog.Log(action = consoleLog.EXECUTE, guild = ctx.guild.name, channel = ctx.channel.name, user = ctx.author.name, message = message.id)

    view.message = message

@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandNotFound):
        return 
    raise error

@bot.event
async def on_ready():
    guilds = []
    for guild in bot.guilds:
        guilds.append({guild.name : guild.id})

    consoleLog.Ready(bot.user.name, guilds)

@bot.event
async def on_guild_join(guild):
    consoleLog.Join(bot.user.name, guild)
    if guild.id not in WHITELIST:
        await guild.leave()
        consoleLog.Leave(bot.user.name, guild)

bot.run(API_KEY)