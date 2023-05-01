#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
__author__ = "Jan Zuska"
__date__ = "2023/4/24"
__copyright__ = "Copyright 2023, Jan Zuska"
__credits__ = []
__license__ = "GPLv3"
__version__ = "1.2.0"
__maintainer__ = "Jan Zuska"
__email__ = "jan.zuska.04@gmail.com"
__status__ = "Production"
# ----------------------------------------------------------------------------
import discord
import json
from discord.ext import commands
import datetime

with open("fishao-data.json", "r") as file:
    data = json.load(file)
    file.close()

with open("config.json", "r") as file:
    config = json.load(file)
    API_KEY = config["API_KEY"]
    file.close()

def GetEmoji(key):
    for name, value in emoji.items():
        if name == key:
            return value

def GetLocationName(key):
    for id, name in locations.items():
        if int(id) == key:
            return name
        
def GetLocationId(key):
    for id, name in locations.items():
        if name == key:
            return id
        
def GetBadgeId(key):
    for name, id in badges.items():
        if name == key:
            return id

def LocationsList():
    locations_list = []
    for id, name in locations.items():
        locations_list.append(name)
    return locations_list

def TodayIsInInterval(interval: str) -> bool:
    today = datetime.date.today()
    year_now = today.year
    interval_start = interval.split("-")[0]
    interval_end = interval.split("-")[1]
    start_date = datetime.date(year_now, int(interval_start.split(".")[0]), int(interval_start.split(".")[1]))
    enf_date = datetime.date(year_now, int(interval_end.split(".")[0]), int(interval_end.split(".")[1]))
    if start_date <= today <= enf_date:
        return True
    else: 
        return False
    
def split_list(input_list: list, max_list_size: int = 25) -> list:
        output_list = []
        for i in range(0, len(input_list), max_list_size):
            output_list.append(input_list[i:i + max_list_size])
        return output_list

async def GetFish(location_id):
    fish = []
    for one_fish in data:
        try:
          locations = one_fish["catch_req"]["location_ids"]
          if int(location_id) in locations:
              fish.append(one_fish["name"])
        except Exception as e:
          print(f"Error reading the price. Error: {e}")
    return fish

async def FishDetails(fish):
    for one_fish in data:
        try:
          name = one_fish["name"]
          if str(fish) == name:
              return one_fish
        except Exception as e:
          print(f"Error reading the data. Error: {e}")

async def GetFile(name: str, folder: str):
    if folder == "fish":
        name = name["id"]
    file_name = f"{name}.png"
    file_path = f"images/{folder}/{file_name}"
    file = discord.File(file_path, filename = file_name)
    return file

async def BuildFishEmbed(ctx: commands.Context, fish):
    fish_name = fish["name"]
    fish_id = fish["id"]
    fish_rating = ""
    for i in range(int(fish["rating"])):
        fish_rating += f"{GetEmoji('star')} "
    fish_rarity_factor = fish["rarity_factor"]
    fish_catch_req = fish["catch_req"]
    fish_location = ""
    for location in fish_catch_req["location_ids"]:
        fish_location += f"{GetLocationName(location)}\n"
    fish_baits = ""
    for bait in fish_catch_req["bait_category"]:
        fish_baits += f"{GetEmoji(bait)} "
    fish_min_length = int(fish["min_length"]) + 1
    fish_avg_length = int(fish["avg_length"])
    fish_max_length = int(fish["max_length"]) - 1
    try:
        caught_time = fish_catch_req["caught_time"]
        fish_caught_time = ""
        for time in caught_time:
            fish_caught_time += f"{time}\n"
    except:
        fish_caught_time = "Always"
    try:
        caught_date = fish_catch_req["caught_date"]
        fish_caught_date = ""
        for date in caught_date:
            fish_caught_date += f"{date}\n"
        fish_active = "No"
        for date in caught_date:
            if TodayIsInInterval(date):
                fish_active = "Yes"
    except:
        fish_caught_date = "Always"
        fish_active = "Yes"

    embed = discord.Embed(
        title = fish_name,
        description = "",
        color = discord.Colour.blurple(),

    )
    embed.set_author(name = bot.user.name, icon_url = bot.user.avatar.url)

    embed.add_field(name = "Rating:", value = f"{fish_rating} ({fish_rarity_factor})", inline = False)
    embed.add_field(name = "Location:", value = fish_location, inline = False)
    embed.add_field(name = "Baits:", value = fish_baits, inline = False)

    embed.add_field(name = "Min length:", value = fish_min_length, inline = True)
    embed.add_field(name = "Avg length:", value = fish_avg_length, inline = True)
    embed.add_field(name = "Max length:", value = fish_max_length, inline = True)

    embed.add_field(name = "Caught time:", value = fish_caught_time, inline = True)
    embed.add_field(name = "Caught date:", value = fish_caught_date, inline = True)
    embed.add_field(name = "Active: <:Season:1100778583741435996>", value = fish_active, inline = True)
    embed.set_image(url = f"attachment://{fish_id}.png")

    author = ctx.author
    embed.set_footer(text = author, icon_url = author.avatar)
    return embed

async def BuildLocationsEmbed(ctx: commands.Context):
    embed = discord.Embed(
        title = "SELECT LOCATION",
        description = "",
        color = discord.Colour.blurple(),
    )
    embed.set_author(name = bot.user.name, icon_url = bot.user.avatar.url)

    embed.add_field(name = "Fishao username:", value = "Unknown", inline = True)
    embed.add_field(name = "Fish caught:", value = "0/615", inline = True)
    embed.add_field(name = "", value = "*:arrow_up: These features are coming soon!*", inline = False)
    embed.add_field(name = "Select location in dropdown menu.", value = "", inline = False)
    

    embed.set_image(url = f"attachment://world.png")

    author = ctx.author
    embed.set_footer(text = author, icon_url = author.avatar)

    return embed

async def BuildLocationEmbed(location: str, ctx: commands.Context):
    badge_id = GetBadgeId(location)
    embed = discord.Embed(
        title = location,
        description = "",
        color = discord.Colour.blurple(),
    )
    embed.set_author(name = bot.user.name, icon_url = bot.user.avatar.url)

    embed.set_image(url = f"attachment://{badge_id}.png")

    author = ctx.author
    embed.set_footer(text = author, icon_url = author.avatar)

    return embed

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

locations = {
1 : "Laketown",
2 : "Rio Tropical",
3 : "Pinheira Beach",
4 : "Cool Mountain",
5 : "Mystic Desert",
6 : "Sibiri City",
7 : "Aquayama",
8 : "Seagull Harbor",
9 : "Thombani Town",
10 : "Marshville",
11 : "Palm Island",
12 : "Lucky Raft",
101 : "Trout Farm",
104 : "Pyramid",
108 : "Lost Valley",
110 : "Little Rio",
111 : "Pirate Cave",
112 : "Club",
113 : "Factory",
201 : "Boat on Sea",
202 : "Lake Run",
203 : "Race",
204 : "Moray",
300 : "Backyard"
}
emoji = {
"hook" : "<:Hook:1099982706928005162>", 
"vegetal" : "<:Vegetal:1099982710287638619>",
"dough" : "<:Dough:1099982712099577936>",
"fish" : "<:Fish:1099982714901381132>",
"insects" : "<:Insects:1099982716159660034>", 
"meat" : "<:Meat:1099982718240030793>",
"lures" : "<:Lures:1099982720307822642>",
"shark" : "<:Shark:1099982721746468864>",
"prehistoric" : "<:Prehistoric:1099982723856216114>",
"pelican" : "<:Pelican:1099982724967694368>",
"monkfish" : "<:Monkfish:1099982727803043900>",
"star" : "<:Star:1099982729925365790>",
"tuna" : "<:Tuna:1099982732119003188>",
"marlin" : "<:Marlin:1099982830685130795>",
"barracuda" : "<:Barracuda:1099982833159778376>",
"monster" : "<:Monster:1099982737768718346>",
"star" : "<:FishaoStar:1099982901325611118>"
}
badges = {
"Laketown" : 1,
"Rio Tropical" : 2,
"Pinheira Beach" : 3,
"Cool Mountain" : 4,
"Mystic Desert" : 5,
"Sibiri City" : 6,
"Aquayama" : 7,
"Seagull Harbor" : 8,
"Thombani Town" : 9,
"Marshville" : 10,
"Palm Island" : 52,
"Lucky Raft" : 76,
"Trout Farm" : 1,
"Pyramid" : 5,
"Lost Valley" :33,
"Little Rio" : 55,
"Pirate Cave" : 56,
"Club" : 75,
"Factory" : 5,
"Boat on Sea" : 11,
"Lake Run" : 12,
"Race" : 13,
"Moray" : 54,
"Backyard" : 14
}
async def BlockNonAuthorInteraction(interaction: discord.Interaction):
    message = f"{interaction.user.mention} you can't do that! Please don't ruin interactions created by other users.You can create you own using `/fishex`."
    await interaction.response.send_message(message, ephemeral=True, delete_after=30)

class LocationSelect(discord.ui.Select):
    def __init__(self, ctx):
        options = [discord.SelectOption(label=location,description="") for location in LocationsList()]
        super().__init__(placeholder = "Select a location!", options = options, min_values = 1, max_values = 1)
        self.ctx = ctx

    async def callback(self, interaction): 
        fish = await GetFish(GetLocationId(self.values[0]))
        if interaction.user.id == self.ctx.author.id:
            # External emoji bug interaction.response.edit_message()
            await interaction.message.delete()
            await interaction.channel.send(file = await GetFile(GetBadgeId(self.values[0]), "badges"), embed = await BuildLocationEmbed(self.values[0], self.ctx), view=Fish(fish, self.ctx)) 
        else:
            await BlockNonAuthorInteraction(interaction)

class Location(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.add_item(LocationSelect(ctx))

class FishSelect(discord.ui.Select):
    def __init__(self, view , fish, ctx):
        self.ctx = ctx
        self.View = view
        self.select = self.View.get_item("fish_select")
        options = [discord.SelectOption(label=one_fish,description="") for one_fish in fish]
        super().__init__(placeholder = "Select a fish", options = options, min_values = 1, max_values = 1, custom_id="fish_select")

    async def callback(self, interaction):
        if interaction.user.id == self.ctx.author.id:
            fish = await FishDetails(self.values[0])
            await interaction.response.edit_message(file = await GetFile(fish, "fish"), embed = await BuildFishEmbed(ctx = self.ctx, fish = fish), view = self.View)
        else:
            await BlockNonAuthorInteraction(interaction)

class PreviousButton(discord.ui.Button):
    def __init__(self, fish_view: discord.ui.View, ctx):
        self.fish_view = fish_view
        self.ctx = ctx
        super().__init__(label="Previous page", disabled=True, custom_id="previous")

    
    async def callback(self, interaction):
        if interaction.user.id == self.ctx.author.id:
            self.fish_view.page -= 1
            if self.fish_view.page == 0:
                self.disabled = True
            self.fish_view.get_item("next").disabled = False
            new_options = [
                discord.SelectOption(label=fish, description="")
                for fish in self.fish_view.pages[self.fish_view.page]
            ]
            self.fish_view.get_item("fish_select").options.clear()
            self.fish_view.get_item("fish_select").options.extend(new_options)
            await interaction.response.edit_message(view=self.fish_view)
        else:
            await BlockNonAuthorInteraction(interaction)

class NextButton(discord.ui.Button):
    def __init__(self, fish_view: discord.ui.View, ctx):
        super().__init__(label="Next page", custom_id="next")
        self.fish_view = fish_view
        self.ctx = ctx
    
    async def callback(self, interaction):
        if interaction.user.id == self.ctx.author.id:
            self.fish_view.page += 1
            if self.fish_view.page == (len(self.fish_view.pages) - 1):
                self.disabled = True
            self.fish_view.get_item("previous").disabled = False
            new_options = [
                discord.SelectOption(label=fish, description="")
                for fish in self.fish_view.pages[self.fish_view.page]
            ]
            self.fish_view.get_item("fish_select").options.clear()
            self.fish_view.get_item("fish_select").options.extend(new_options)
            await interaction.response.edit_message(view=self.fish_view)
        else:
            await BlockNonAuthorInteraction(interaction)

class BackButton(discord.ui.Button):
    def __init__(self, ctx):
        super().__init__(label="Back", custom_id="back")
        self.ctx = ctx
    
    async def callback(self, interaction):
        if interaction.user.id == self.ctx.author.id:
            await interaction.response.edit_message(file = await GetFile("world", "resources"), embed = await BuildLocationsEmbed(self.ctx), view = Location(self.ctx))
        else:
            await BlockNonAuthorInteraction(interaction)

class Fish(discord.ui.View):
    def __init__(self, fish, ctx):
        super().__init__()
        fish_list = sorted(fish)
        if len(fish_list) > 25:
            self.fish = fish_list[0:24]
            self.pages = split_list(fish_list)
            self.page = 0
            self.add_item(FishSelect(self, self.fish, ctx))
            self.add_item(PreviousButton(self, ctx))
            self.add_item(NextButton(self, ctx))
        else:
            self.fish = fish_list
            self.add_item(FishSelect(self, self.fish, ctx))
        self.add_item(BackButton(ctx))

@bot.slash_command()
async def fishdex(ctx: commands.Context):
    current_date_time = datetime.datetime.now()
    formated_date_time = current_date_time.strftime("%d.%m.%Y | %H:%M:%S")
    user = ctx.author.name
    print(f"{formated_date_time} | {user} used command fishdex")
    await ctx.response.defer()
    await ctx.followup.send(file = await GetFile("world", "resources"), embed = await BuildLocationsEmbed(ctx), view=Location(ctx))

bot.run(API_KEY)