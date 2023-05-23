import discord
from discord.ext import commands
import database
from functions import *
from discordFunctions import *
import objects
import embeds
import views
import buttons

# -----------------------------------------------------------
class Location(discord.ui.Select):
    def __init__(self, ctx: commands.Context, db: database.Database, bot: discord.Client, fish: objects.Fishes, locations: objects.Locations):
        self.ctx: commands.Context = ctx
        self.db: database.Database = db
        self.bot: discord.Client = bot
        self.fish: objects.Fishes = fish
        self.locations: objects.Locations = locations
        options = [discord.SelectOption(label = location) for location in self.locations]
        super().__init__(placeholder = "Select location!", options = options, row = 0)

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        selected_location: str = self.values[0]
        selected_location_id: str = self.locations.Id(selected_location)
        selected_location_details: dict = self.locations.Details(selected_location)
        available_fishes: list = self.fish.AvailableFishes(selected_location_id)
        location: objects.Location = objects.Location(location_details = selected_location_details, available_fishes = available_fishes)
        caught, shiny = self.db.Caught(selected_location_id), self.db.Shiny(selected_location_id)
        if location.additional_locations:
            embed: discord.Embed = embeds.AdditionalLocations(ctx = self.ctx, bot = self.bot, location = selected_location, caught = caught, shiny = shiny).Get()
            file: discord.File = await GetFile(filename = location.badge_id, folder = "badges")
            view: discord.ui.View = views.AdditionalLocations(ctx = self.ctx, db = self.db, bot = self.bot, fish = self.fish, locations = self.locations, location = location)
            await interaction.response.edit_message(file = file, embed = embed, view = view)
        else:
            embed: discord.Embed = embeds.Location(ctx = self.ctx, bot = self.bot, location = selected_location, caught = caught, shiny = shiny)
            file: discord.File = await GetFile(filename = location.badge_id, folder = "badges")
            view: discord.ui.View = views.Fish(ctx = self.ctx, db = self.db, bot = self.bot, fish = self.fish, locations = self.locations, available_fishes = available_fishes, location = location)
            await interaction.response.edit_message(view = view)

# -----------------------------------------------------------
class AdditionalLocations(discord.ui.Select):
    def __init__(self, ctx: commands.Context, db: database.Database, bot: discord.Client, fish: objects.Fishes, locations: objects.Locations, location: objects.Location):
        self.ctx: commands.Context = ctx
        self.db: database.Database = db
        self.bot: discord.Client = bot
        self.fish: objects.Fishes = fish
        self.locations: objects.Locations = locations
        self.location: objects.Location = location
        options = [discord.SelectOption(label = location) for location in self.location.AdditionalLocations()]
        super().__init__(placeholder = "Select location!", options = options, row = 0)

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        selected_additional_location = self.values[0]
        available_fishes = self.location.AvailableFishes(additional_location_name = selected_additional_location)
        await interaction.response.edit_message(view = views.Fish(ctx = self.ctx, db = self.db, bot = self.bot, fish = self.fish, locations = self.locations, available_fishes = available_fishes, location = self.location))

# -----------------------------------------------------------
class Fish(discord.ui.Select):
    def __init__(self, ctx: commands.Context, db: database.Database, bot: discord.Client, fish_view: discord.ui.View, available_fishes: list):
        self.ctx: commands.Context = ctx
        self.db: database.Database = db
        self.bot: discord.Client = bot
        self.fish_view: discord.ui.View = fish_view
        self.fish: objects.Fishes = objects.Fishes(fishes = available_fishes)
        self.select: discord.ui.Select = self.fish_view.get_item("fish_select")
        options = [discord.SelectOption(label = available_fish["name"]) for available_fish in available_fishes]
        super().__init__(placeholder = "Select fish", options = options, custom_id="fish_select", row = 0)

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        # Remove all buttons if exists to avoid - In components.2.components.1.custom_id: Component custom id cannot be duplicated
        for button_custom_id in ["caught", "shiny"]:
            button: discord.ui.Button = self.fish_view.get_item(button_custom_id)
            self.fish_view.remove_item(button)
        # ------------------------------------------------------------------------------------------------------------------------
        selected_fish_name: str = self.values[0]
        self.fish_view.selected_fish_name = selected_fish_name
        selected_fish = self.fish.Fish(selected_fish_name)
        self.fish_view.selected_fish = selected_fish
        caught, shiny = self.db.isCaught(selected_fish_name), self.db.isShiny(selected_fish_name)
        self.fish_view.add_item(buttons.Caught(ctx = self.ctx, db = self.db, bot = self.bot, fish_view = self.fish_view, caught = caught))
        self.fish_view.add_item(buttons.Shiny(ctx = self.ctx, db = self.db, bot = self.bot, fish_view = self.fish_view, shiny = shiny))
        await interaction.response.edit_message(file = await GetFile(selected_fish, "fish"), embed = embeds.FishEmbed(ctx = self.ctx, bot = self.bot, fish = selected_fish, caught = caught, shiny = shiny).Get(), view = self.fish_view)
