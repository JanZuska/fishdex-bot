import discord
from discord.ext import commands
import views
from discordFunctions import *
import database
import embeds
import functions
import objects


class PreviousPage(discord.ui.Button):
    def __init__(self, ctx: commands.Context, fish_view:discord.ui.View):
        self.ctx: commands.Context = ctx
        self.fish_view: discord.ui.View = fish_view
        super().__init__(label = "Previous page", disabled = True, custom_id = "previous", style = discord.ButtonStyle.blurple, row = 1, emoji = "⬅️")

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        self.next_button: discord.ui.Button = self.fish_view.get_item("next")
        self.fish_select: discord.ui.View = self.fish_view.get_item("fish_select")
        self.fish_view.page -= 1
        self.next_button.disabled = False
        if self.fish_view.page == 0:
            self.disabled = True
        new_options: list = [discord.SelectOption(label = available_fish["name"]) for available_fish in self.fish_view.available_fishes_pages[self.fish_view.page]]
        self.fish_select.options.clear()
        self.fish_select.options.extend(new_options)
        await interaction.response.edit_message(view = self.fish_view)

class NextPage(discord.ui.Button):
    def __init__(self, ctx: commands.Context, fish_view: discord.ui.View):
        self.ctx: commands.Context = ctx
        self.fish_view: discord.ui.View = fish_view
        super().__init__(label = "Next page", custom_id = "next", style = discord.ButtonStyle.blurple, row = 1, emoji = "➡️")

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        self.previous_button: discord.ui.Button = self.fish_view.get_item("previous")
        self.fish_select: discord.ui.View = self.fish_view.get_item("fish_select")
        self.fish_view.page += 1
        self.previous_button.disabled = False
        if self.fish_view.page == (len(self.fish_view.available_fishes_pages) - 1):
            self.disabled = True
        new_options: list = [discord.SelectOption(label = available_fish["name"]) for available_fish in self.fish_view.available_fishes_pages[self.fish_view.page]]
        self.fish_select.options.clear()
        self.fish_select.options.extend(new_options)
        await interaction.response.edit_message(view = self.fish_view)

class Caught(discord.ui.Button):
    def __init__(self, ctx: commands.Context, db: database.Database, bot: discord.Client, fish_view: discord.ui.View, caught: bool):
        self.ctx: commands.Context = ctx
        self.db: database.Database = db
        self.bot: discord.Client = bot
        self.fish_view: discord.ui.View = fish_view
        self.caught = caught
        if self.caught:
            style = discord.ButtonStyle.green
            emoji = "✅"
        else:
            style = discord.ButtonStyle.red
            emoji = "❌"
        super().__init__(label = "Caught", custom_id = "caught", style = style, row = 2, emoji = emoji)

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        # Remove Caught and Shiny buttons to avoid mixing order
        for button_custom_id in ["caught", "shiny"]:
            button: discord.ui.Button = self.fish_view.get_item(button_custom_id)
            self.fish_view.remove_item(button)
        # -----------------------------------------------------
        self.db.SetCaught(fish_name = self.fish_view.selected_fish_name, true = not self.caught)
        caught, shiny = self.db.isCaught(self.fish_view.selected_fish_name), self.db.isShiny(self.fish_view.selected_fish_name)
        self.fish_view.add_item(Caught(ctx = self.ctx, db = self.db, bot = self.bot, fish_view = self.fish_view, caught = not self.caught))
        self.fish_view.add_item(Shiny(ctx = self.ctx, db = self.db, bot = self.bot, fish_view = self.fish_view, shiny = shiny))
        embed: discord.Embed = embeds.FishEmbed(ctx = self.ctx, bot = self.bot, fish = self.fish_view.selected_fish, caught = caught, shiny = shiny).Get()
        await interaction.response.edit_message(embed = embed, view = self.fish_view)

class Shiny(discord.ui.Button):
    def __init__(self, ctx: commands.Context, db: database.Database, bot: discord.Client, fish_view: discord.ui.View, shiny: bool):
        self.ctx: commands.Context = ctx
        self.db: database.Database = db
        self.bot: discord.Client = bot
        self.fish_view: discord.ui.View = fish_view
        self.shiny = shiny
        if self.shiny:
            style = discord.ButtonStyle.green
            emoji = "✅"
        else:
            style = discord.ButtonStyle.red
            emoji = "❌"
        super().__init__(label = "Shiny", custom_id = "shiny", style = style, row = 2, emoji = emoji)

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        # Remove Caught and Shiny buttons to avoid mixing order
        for button_custom_id in ["caught", "shiny"]:
            button: discord.ui.Button = self.fish_view.get_item(button_custom_id)
            self.fish_view.remove_item(button)
        # -----------------------------------------------------
        self.db.SetShiny(fish_name = self.fish_view.selected_fish_name, true = not self.shiny)
        caught, shiny = self.db.isCaught(self.fish_view.selected_fish_name), self.db.isShiny(self.fish_view.selected_fish_name)
        self.fish_view.add_item(Caught(ctx = self.ctx, db = self.db, bot = self.bot, fish_view = self.fish_view, caught = caught))
        self.fish_view.add_item(Shiny(ctx = self.ctx, db = self.db, bot = self.bot, fish_view = self.fish_view, shiny = not self.shiny))
        embed: discord.Embed = embeds.FishEmbed(ctx = self.ctx, bot = self.bot, fish = self.fish_view.selected_fish, caught = caught, shiny = shiny).Get()
        await interaction.response.edit_message(embed = embed, view = self.fish_view)
    
class BackToLocations(discord.ui.Button):
    def __init__(self, ctx: commands.Context, db: database.Database, bot: discord.Client, fish: objects.Fishes, locations: objects.Locations):
        self.ctx: commands.Context = ctx
        self.db: database.Database = db
        self.bot: discord.Client = bot
        self.fish: objects.Fishes = fish
        self.locations: objects.Locations = locations
        super().__init__(label = "Back", custom_id = "back", style = discord.ButtonStyle.grey, row = 3, emoji = "↩️")

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        caught, shiny = self.db.Caught(), self.db.Shiny()
        embed: discord.Embed = embeds.Locations(ctx = self.ctx, bot = self.bot, caught = caught, shiny = shiny).Get()
        file: discord.File = await functions.GetFile(filename = "world", folder = "resources")
        view: discord.ui.View = views.Location(ctx = self.ctx, db = self.db, bot = self.bot, fish = self.fish, locations = self.locations)
        await interaction.response.edit_message(file = file, embed = embed, view = view)

class BackToAdditionalLocations(discord.ui.Button):
    def __init__(self, ctx: commands.Context, db: database.Database, bot: discord.Client, fish: objects.Fishes, locations: objects.Locations, location: objects.Location):
        self.ctx: commands.Context = ctx
        self.db: database.Database = db
        self.bot: discord.Client = bot
        self.fish: objects.Fishes = fish
        self.locations: objects.Locations = locations
        self.location: objects.Location = location
        super().__init__(label = "Back", custom_id = "back", style = discord.ButtonStyle.grey, row = 3, emoji = "↩️")

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        caught, shiny = self.db.Caught(), self.db.Shiny()
        embed: discord.Embed = embeds.AdditionalLocations(ctx = self.ctx, bot = self.bot, location = self.location.location_name, caught = caught, shiny = shiny).Get()
        file: discord.File = await functions.GetFile(filename = self.location.badge_id, folder = "badges")
        view: discord.ui.View = views.AdditionalLocations(ctx = self.ctx, db = self.db, bot = self.bot, fish = self.fish, locations = self.locations, location = self.location)
        await interaction.response.edit_message(file = file, embed = embed, view = view)