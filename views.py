import discord
from discord.ext import commands
import database
from discordFunctions import *
import selects
import objects
import buttons
    
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

        self.selected_fish: dict | None = None
        self.selected_fish_name: str | None = None

        super().__init__(disable_on_timeout = True)
        self.add_item(selects.Location(fishdex_view = self))

    async def on_timeout(self):
        await Timeout(self)
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

    
    @staticmethod
    def split_list(input_list: list, max_list_size: int = 25) -> list:
        output_list = []
        for i in range(0, len(input_list), max_list_size):
            output_list.append(input_list[i:i + max_list_size])
        return output_list