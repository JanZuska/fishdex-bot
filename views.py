import discord
from discord.ext import commands
import database
from discordFunctions import *
import selects
import objects
import buttons

# -----------------------------------------------------------
class Location(discord.ui.View):
    def __init__(self, ctx: commands.Context, db: database.Database, bot: discord.Client, fish: objects.Fishes, locations: objects.Locations):
        self.ctx: commands.Context = ctx
        self.db: database.Database = db
        self.bot: discord.Client = bot
        self.fish: objects.Fishes = fish
        self.locations: objects.Locations = locations
        super().__init__()
        self.add_item(selects.Location(ctx = self.ctx, db = self.db, bot = self.bot, fish = self.fish, locations = self.locations))

    async def on_timeout(self):
        await Timeout(self)
        return await super().on_timeout()

# -----------------------------------------------------------    
class AdditionalLocations(discord.ui.View):
    def __init__(self, ctx: commands.Context, db: database.Database, bot: discord.Client, fish: objects.Fishes, locations: objects.Locations, location: objects.Location):
        self.ctx: commands.Context = ctx
        self.db: database.Database = db
        self.bot: discord.Client = bot
        self.fish: objects.Fishes = fish
        self.locations: objects.Locations = locations
        self.location: objects.Location = location
        super().__init__()
        self.add_item(selects.AdditionalLocations(ctx = self.ctx, db = self.db, bot = self.bot, fish = self.fish, locations = self.locations, location = self.location))
        self.add_item(buttons.BackToLocations(ctx = self.ctx, db = self.db, bot = self.bot, fish = self.fish, locations = self.locations))

    async def on_timeout(self):
        await Timeout(self)
        return await super().on_timeout()

# -----------------------------------------------------------    
class Fish(discord.ui.View):
    def __init__(self, ctx: commands.Context, db: database.Database, bot: discord.Client, fish: objects.Fishes, locations: objects.Locations, available_fishes: list, location: objects.Location):
        self.ctx: commands.Context = ctx
        self.db: database.Database = db
        self.bot: discord.Client = bot
        self.fish: objects.Fishes = fish
        self.locations: objects.Locations = locations
        self.location: objects.Location = location
        self.selected_fish_name = None
        self.selected_fish = None
        super().__init__()

        if len(available_fishes) > 25:
            self.available_fishes: list = available_fishes[0:25]
            self.available_fishes_pages: list = self.split_list(available_fishes)
            self.page: int = 0
            self.add_item(selects.Fish(ctx = self.ctx, db = self.db, bot = self.bot, fish_view = self, available_fishes = self.available_fishes))
            self.add_item(buttons.PreviousPage(ctx = self.ctx, fish_view = self))
            self.add_item(buttons.NextPage(ctx = self.ctx, fish_view = self))
        else:
            self.available_fishes: list = available_fishes
            self.add_item(selects.Fish(ctx = self.ctx, db = self.db, bot = self.bot, fish_view = self, available_fishes = self.available_fishes))
        if not self.location.additional_locations:
            self.add_item(buttons.BackToLocations(ctx = self.ctx, db = self.db, bot = self.bot, fish = self.fish, locations = self.locations))
        elif self.location.additional_locations:
            self.add_item(buttons.BackToAdditionalLocations(ctx = self.ctx, db = self.db, bot = self.bot, fish = self.fish, locations = self.locations, location = self.location))

    async def on_timeout(self):
        await Timeout(self)
        return await super().on_timeout()
    
    @staticmethod
    def split_list(input_list: list, max_list_size: int = 25) -> list:
        output_list = []
        for i in range(0, len(input_list), max_list_size):
            output_list.append(input_list[i:i + max_list_size])
        return output_list