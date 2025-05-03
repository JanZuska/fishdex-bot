import discord
from discord.ext import commands
import db as database
from discordFunctions import *
import selects as selects
import objects as objects
import buttons as buttons
import consoleLog as consoleLog
    
class Fishdex(discord.ui.View):
    def __init__(self, ctx: commands.Context, db: database.Database, bot: discord.Client, fish: objects.Fishes, locations: objects.Locations):
        self.ctx: commands.Context = ctx
        self.db: database.Database = db
        self.bot: discord.Client = bot
        self.fish: objects.Fishes = fish
        self.locations: objects.Locations = locations
        self.selected_location: objects.Location | None = None

        self.available_fishes: list | None = None
        self.all_available_fishes: list | None = None

        self.available_fishes_pages: list | None = None
        self.page: int | None = None

        self.selected_fish_index: int | None = None
        self.index: int | None = None

        self.selected_fish: dict | None = None
        self.selected_fish_name: str | None = None

        self.message = None

        super().__init__()
        self.add_item(selects.Location(fishdex_view = self))

    async def on_timeout(self):
        consoleLog.Log(action = "TIMEOUT", guild = self.ctx.guild.name, channel = self.ctx.channel.name, user = self.ctx.author.name, message = self.message.id)
        await self.message.edit(view=None)
        return await super().on_timeout()
    
    async def BackToLocations(self):
        self.selected_location: objects.Location | None = None
        self.available_fishes: list | None = None
        self.all_available_fishes: list | None = None
        self.available_fishes_pages: list | None = None
        self.page: int | None = None
        self.selected_fish: dict | None = None
        self.selected_fish_name: str | None = None
        self.clear_items()
        self.add_item(selects.Location(fishdex_view = self))

    async def BackToAdditionalLocations(self):
        self.available_fishes: list | None = None
        self.clear_items()
        self.add_item(selects.AdditionalLocations(fishdex_view = self))
        self.add_item(buttons.BackToLocations(fishdex_view = self))

    async def SelectLocation(self, available_fishes:list, location: objects.Location):
        self.available_fishes = available_fishes
        self.selected_location = location

        location_select = self.get_item("location_select")
        self.remove_item(location_select)
        self.add_item(buttons.BackToLocations(fishdex_view = self))

        if location.additional_locations:
            self.add_item(selects.AdditionalLocations(fishdex_view = self))
        else:
            self.add_item(selects.Fish(fishdex_view = self))

    async def SelectAdditionalLocation(self, available_fishes):
        self.available_fishes = available_fishes

        additional_location_select = self.get_item("additional_location_select")
        self.remove_item(additional_location_select)
        self.add_item(selects.Fish(fishdex_view = self))
        back_button = self.get_item("back")
        self.remove_item(back_button)
        self.add_item(buttons.BackToAdditionalLocations(fishdex_view = self))

    async def FishSelect(self, selected_fish_name, selected_fish, caught, shiny):
        self.selected_fish_name = selected_fish_name
        self.selected_fish = selected_fish
        # Remove Caught and Shiny buttons to avoid break
        for button_custom_id in ["caught", "shiny", "display_shiny", "display_default"]:
            button: discord.ui.Button = self.get_item(button_custom_id)
            self.remove_item(button)
        # -----------------------------------------------------
        self.add_item(buttons.Caught(fishdex_view = self, caught = caught))
        self.add_item(buttons.Shiny(fishdex_view = self, shiny = shiny))
        self.add_item(buttons.DisplayShiny(fishdex_view = self))
    
    @staticmethod
    def split_list(input_list: list, max_list_size: int = 25) -> list:
        output_list = []
        for i in range(0, len(input_list), max_list_size):
            output_list.append(input_list[i:i + max_list_size])
        return output_list