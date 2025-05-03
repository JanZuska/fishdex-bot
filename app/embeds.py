import discord
from discord.ext import commands
from functions import *

# -----------------------------------------------------------
class Locations:
    def __init__(self, ctx: commands.Context, bot: discord.Client, caught: int, shiny: int) -> None:
        self.embed = discord.Embed(
        title = "SELECT LOCATION",
        description = "",
        color = discord.Colour.blurple())
        self.author = ctx.author
        self.bot = bot.user

        self.embed.set_author(name = self.bot.name, icon_url = self.bot.avatar.url)

        self.embed.add_field(name = "Fishao username:", value = "Unknown", inline = True)
        self.embed.add_field(name = "Caught:", value = caught, inline = True)
        self.embed.add_field(name = "Shiny:", value = shiny, inline = True)
        self.embed.add_field(name = "Select location in dropdown menu.", value = "", inline = False)

        self.embed.set_image(url = "https://i.imgur.com/H2Zrn4A.png")

        if self.author.avatar:
            self.embed.set_footer(text = self.author, icon_url = self.author.avatar.url)
        else:
            self.embed.set_footer(text = self.author, icon_url = self.author.default_avatar.url)

    def Get(self):
        return self.embed

# -----------------------------------------------------------    
class Location:
    def __init__(self, ctx: commands.Context, bot: discord.Client, location: str, caught: int, shiny: int) -> None:
        self.embed = discord.Embed(
            title = location,
            description = "",
            color = discord.Colour.blurple())
        self.author = ctx.author
        self.bot = bot.user

        badge_id = Get.BadgeId(location)

        self.embed.set_author(name = self.bot.name, icon_url = self.bot.avatar.url)

        #self.embed.set_thumbnail(url = f"https://www.fishao.com/data/image/badges/badge_{badge_id}_128x128.png")

        self.embed.add_field(name = "Fishao username:", value = "Unknown", inline = True)
        self.embed.add_field(name = "Caught:", value = caught, inline = True)
        self.embed.add_field(name = "Shiny:", value = shiny, inline = True)

        self.embed.set_image(url = f"attachment://{badge_id}.png")

        if self.author.avatar:
            self.embed.set_footer(text = self.author, icon_url = self.author.avatar.url)
        else:
            self.embed.set_footer(text = self.author, icon_url = self.author.default_avatar.url)

    def Get(self):
        return self.embed

# -----------------------------------------------------------
class AdditionalLocations:
    def __init__(self, ctx: commands.Context, bot: discord.Client, location: str, caught: int, shiny: int) -> None:
        self.embed = discord.Embed(
            title = location,
            description = "",
            color = discord.Colour.blurple())
        self.author = ctx.author
        self.bot = bot.user

        badge_id = Get.BadgeId(location)

        self.embed.set_author(name = self.bot.name, icon_url = self.bot.avatar.url)

        #self.embed.set_thumbnail(url = f"https://www.fishao.com/data/image/badges/badge_{badge_id}_128x128.png")

        self.embed.add_field(name = "Fishao username:", value = "Unknown", inline = True)
        self.embed.add_field(name = "Caught:", value = caught, inline = True)
        self.embed.add_field(name = "Shiny:", value = shiny, inline = True)

        self.embed.set_image(url = f"attachment://{badge_id}.png")

        if self.author.avatar:
            self.embed.set_footer(text = self.author, icon_url = self.author.avatar.url)
        else:
            self.embed.set_footer(text = self.author, icon_url = self.author.default_avatar.url)

    def Get(self):
        return self.embed

# -----------------------------------------------------------
class FishEmbed:
    def __init__(self, ctx: commands.Context, bot: discord.Client, fish: dict, caught: bool, shiny: bool, image = None) -> None:
        self.fish_name = fish["name"]
        self.embed = discord.Embed(
            title = self.fish_name,
            description = "",
            color = discord.Colour.red())
        self.author = ctx.author
        self.bot = bot.user

        fish_id = fish["id"]
        fish_rating = ""
        for i in range(int(fish["rating"])):
            fish_rating += f"{Get.Emoji('star', 'others')} "
        fish_rarity_factor = float(fish["rarity_factor"])
        fish_catch_req = fish["catch_req"]
        fish_location = ""
        for location in fish_catch_req["location_ids"]:
            fish_location += f"{Get.LocationName(location)}\n"
        fish_baits = ""
        for bait in fish_catch_req["bait_category"]:
            fish_baits += f"{Get.Emoji(bait)} "
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
                fish_caught_date += f"{FormatDate(date)}\n"
            fish_active = "No"
            for date in caught_date:
                if TodayIsInInterval(date):
                    fish_active = "Yes"
        except:
            fish_caught_date = "Always"
            fish_active = "Yes"

        fish_price = fish["price"]
        fish_price_shiny = fish["price_shiny"]

        if caught:
            caught = Get.Emoji('true', 'others')
            self.embed.color = discord.Colour.green()
        else:
            caught = Get.Emoji('false', 'others')

        if shiny:
            shiny = Get.Emoji('true', 'others')
        else:
            shiny = Get.Emoji('false', 'others')


        self.embed.set_author(name = self.bot.name, icon_url = self.bot.avatar.url)

        self.embed.add_field(name = "Rating:", value = f"{fish_rating} ({fish_rarity_factor:.2f})", inline = False)
        self.embed.add_field(name = "Location:", value = fish_location, inline = False)
        self.embed.add_field(name = "Baits:", value = fish_baits, inline = False)

        self.embed.add_field(name = "Min length:", value = fish_min_length, inline = True)
        self.embed.add_field(name = "Avg length:", value = fish_avg_length, inline = True)
        self.embed.add_field(name = "Max length:", value = fish_max_length, inline = True)

        self.embed.add_field(name = "Caught time:", value = fish_caught_time, inline = True)
        self.embed.add_field(name = "Caught date:", value = fish_caught_date, inline = True)
        self.embed.add_field(name = "Active: <:Season:1100778583741435996>", value = fish_active, inline = True)

        self.embed.add_field(name = "Price:", value = f"{fish_price} {Get.Emoji('fishbucks', 'others')}", inline = True)
        self.embed.add_field(name = "Price shiny:", value = f"{fish_price_shiny} {Get.Emoji('fishbucks', 'others')}", inline = True)
        self.embed.add_field(name = "", value = "", inline = True)

        self.embed.add_field(name = "Caught", value = caught, inline = True)
        self.embed.add_field(name = "Shiny", value = shiny, inline = True)
        self.embed.add_field(name = "", value = "", inline = True)
        
        if image is None:
            self.embed.set_image(url = f"attachment://{fish_id}.png")
        else:
            self.embed.set_image(url = f"attachment://{image}")

        
        if self.author.avatar:
            self.embed.set_footer(text = self.author, icon_url = self.author.avatar.url)
        else:
            self.embed.set_footer(text = self.author, icon_url = self.author.default_avatar.url)
    
    def Get(self):
        return self.embed