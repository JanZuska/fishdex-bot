import discord
from discord.ext import commands
import database
from functions import *
from discordFunctions import *
import objects
import embeds
import views
import buttons
import asyncio

# -----------------------------------------------------------
class Location(discord.ui.Select):
    def __init__(self, fishdex_view: discord.ui.View):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        self.db: database.Database = self.fishdex_view.db
        self.bot: discord.Client = self.fishdex_view.bot
        self.fish: objects.Fishes = self.fishdex_view.fish
        self.locations: objects.Locations = self.fishdex_view.locations
        options = [discord.SelectOption(label = location) for location in self.locations]
        super().__init__(placeholder = "Select location!", options = options, custom_id ="location_select", row = 0)

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        self.fishdex_view.disabled = True
        await interaction.response.edit_message(content = f"Loading <a:loading:1113829058019602452>", view = self.fishdex_view)

        selected_location: str = self.values[0]
        selected_location_id: str = self.locations.Id(selected_location)
        selected_location_details: dict = self.locations.Details(selected_location)
        available_fishes: list = self.fish.AvailableFishes(selected_location_id)
        location: objects.Location = objects.Location(location_details = selected_location_details, available_fishes = available_fishes)
        caught, shiny = self.db.Caught(selected_location_id), self.db.Shiny(selected_location_id)

        await self.fishdex_view.SelectLocation(available_fishes = available_fishes, location = location)
        
        if location.additional_locations:
            embed: discord.Embed = embeds.AdditionalLocations(ctx = self.ctx, bot = self.bot, location = selected_location, caught = caught, shiny = shiny).Get()
            file: discord.File = await GetFile(filename = location.badge_id, folder = "badges")
    
        else:
            embed: discord.Embed = embeds.Location(ctx = self.ctx, bot = self.bot, location = selected_location, caught = caught, shiny = shiny).Get()
            file: discord.File = await GetFile(filename = location.badge_id, folder = "badges")

        self.fishdex_view.disabled = False
        await interaction.message.edit(content = "", file = file, embed = embed, view = self.fishdex_view)

class AdditionalLocations(discord.ui.Select):
    def __init__(self, fishdex_view: discord.ui.View):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        self.db: database.Database = self.fishdex_view.db
        self.bot: discord.Client = self.fishdex_view.bot
        self.fish: objects.Fishes = self.fishdex_view.fish
        self.locations: objects.Locations = self.fishdex_view.locations

        self.location: objects.Location = self.fishdex_view.selected_location

        options = [discord.SelectOption(label = location) for location in self.location.AdditionalLocations()]
        super().__init__(placeholder = "Select location!", options = options, custom_id ="additional_location_select", row = 0)

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        self.fishdex_view.disabled = True
        await interaction.response.edit_message(content = f"Loading <a:loading:1113829058019602452>", view = self.fishdex_view)

        selected_additional_location = self.values[0]
        available_fishes = self.location.AvailableFishes(additional_location_name = selected_additional_location)

        await self.fishdex_view.SelectAdditionalLocation(available_fishes = available_fishes)

        self.fishdex_view.disabled = False
        await interaction.message.edit(content = "", view = self.fishdex_view)

class Fish(discord.ui.Select):
    def __init__(self, fishdex_view: discord.ui.View):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        self.db: database.Database = self.fishdex_view.db
        self.bot: discord.Client = self.fishdex_view.bot
        self.fish: objects.Fishes = self.fishdex_view.fish
        self.locations: objects.Locations = self.fishdex_view.locations

        self.fishdex_view.all_available_fishes: list = self.fishdex_view.available_fishes
        self.available_fishes: objects.Fishes = objects.Fishes(fishes = self.fishdex_view.available_fishes)
        self.all_available_fishes: objects.Fishes = objects.Fishes(fishes = self.fishdex_view.all_available_fishes)

        if len(self.fishdex_view.available_fishes) <= 25:
            options = [discord.SelectOption(label = available_fish["name"]) for available_fish in self.fishdex_view.available_fishes]
        else:
            self.fishdex_view.available_fishes_pages: list = views.Fishdex.split_list(self.fishdex_view.available_fishes)
            self.fishdex_view.page: int = 0
            options = [discord.SelectOption(label = available_fish["name"]) for available_fish in self.fishdex_view.available_fishes_pages[self.fishdex_view.page]]

            self.fishdex_view.add_item(buttons.PreviousPage(fishdex_view = self.fishdex_view))
            self.fishdex_view.add_item(buttons.NextPage(fishdex_view = self.fishdex_view))

        self.fishdex_view.index = -1
        self.fishdex_view.add_item(buttons.PreviousFish(fishdex_view = self.fishdex_view))
        self.fishdex_view.add_item(buttons.NextFish(fishdex_view = self.fishdex_view))

        super().__init__(placeholder = "Select fish", options = options, custom_id="fish_select", row = 0)

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        self.fishdex_view.disabled = True
        await interaction.response.edit_message(content = f"Loading <a:loading:1113829058019602452>", view = self.fishdex_view)

        selected_fish_name: str = self.values[0]
        selected_fish = self.all_available_fishes.Fish(selected_fish_name)
        caught, shiny = self.db.isCaught(selected_fish_name), self.db.isShiny(selected_fish_name)

        self.fishdex_view.index = find_index_by_name(self.fishdex_view.available_fishes, selected_fish_name)
        
        next_fish_button = self.fishdex_view.get_item("next_fish")
        if self.fishdex_view.index == len(self.fishdex_view.available_fishes) - 1:
            next_fish_button.disabled = True
        else:
            next_fish_button.disabled = False
        
        previous_fish_button = self.fishdex_view.get_item("previous_fish")
        if self.fishdex_view.index > 0:
            previous_fish_button.disabled = False
        else:
            previous_fish_button.disabled = True
        

        await self.fishdex_view.FishSelect(selected_fish_name = selected_fish_name, selected_fish = selected_fish, caught = caught, shiny = shiny)

        embed: discord.Embed = embeds.FishEmbed(ctx = self.ctx, bot = self.bot, fish = selected_fish, caught = caught, shiny = shiny).Get()
        file: discord.File = await GetFile(selected_fish, "fish")

        self.fishdex_view.disabled = False
        await interaction.message.edit(content = "", file = file, embed = embed, view = self.fishdex_view)
