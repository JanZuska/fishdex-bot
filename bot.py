#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
__author__ = "Jan Zuska"
__date__ = "2023/4/24"
__copyright__ = "Copyright 2023, Jan Zuska"
__credits__ = []
__license__ = "GPLv3"
__version__ = "2.0.2beta"
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

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.slash_command()
async def fishdex(ctx: commands.Context):
    await ctx.response.defer()
    
    consoleLog.ConsoleLog(user = ctx.author.name)
    db: database.Database = database.Database(user_id = ctx.author.id)
    caught, shiny = db.Caught(), db.Shiny()
    embed: discord.Embed = embeds.Locations(ctx = ctx, bot = bot, caught = caught, shiny = shiny).Get()
    file: discord.File = await functions.GetFile(filename = "world", folder = "resources")
    view: discord.ui.View = views.Fishdex(ctx = ctx, db = db, bot = bot, fish = FISH, locations = LOCATIONS)
    
    await ctx.followup.send(file = file, embed = embed, view = view)

@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandNotFound):
        return 
    raise error

API_KEY = "NjcxMzYyNzM2ODE0NDI0MTE0.GH4Zex.6WoGUCQdLMjGDk6giKr6SsLnWvrc2GdXbNauIE"
print("Bot is running.")
bot.run(API_KEY)