import discord
from discord.ext import commands
import views
from discordFunctions import *
import database
import embeds
import functions
import objects

class PreviousPage(discord.ui.Button):
    def __init__(self, fishdex_view: discord.ui.View):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        super().__init__(label = "Previous page", disabled = True, custom_id = "previous", style = discord.ButtonStyle.blurple, row = 1, emoji = "⬅️")

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        self.next_button: discord.ui.Button = self.fishdex_view.get_item("next")
        self.fish_select: discord.ui.View = self.fishdex_view.get_item("fish_select")

        self.fishdex_view.page -= 1
        self.next_button.disabled = False
        if self.fishdex_view.page == 0:
            self.disabled = True

        new_options: list = [discord.SelectOption(label = available_fish["name"]) for available_fish in self.fishdex_view.available_fishes_pages[self.fishdex_view.page]]
        self.fish_select.options.clear()
        self.fish_select.options.extend(new_options)
        await interaction.response.edit_message(view = self.fishdex_view)

class NextPage(discord.ui.Button):
    def __init__(self, fishdex_view: discord.ui.View):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        super().__init__(label = "Next page", custom_id = "next", style = discord.ButtonStyle.blurple, row = 1, emoji = "➡️")

    @Authorization
    async def callback(self, interaction: discord.Interaction):

        self.previous_button: discord.ui.Button = self.fishdex_view.get_item("previous")
        self.fish_select: discord.ui.View = self.fishdex_view.get_item("fish_select")

        self.fishdex_view.page += 1

        self.previous_button.disabled = False

        if self.fishdex_view.page == (len(self.fishdex_view.available_fishes_pages) - 1):
            self.disabled = True

        new_options: list = [discord.SelectOption(label = available_fish["name"]) for available_fish in self.fishdex_view.available_fishes_pages[self.fishdex_view.page]]
        self.fish_select.options.clear()
        self.fish_select.options.extend(new_options)
        await interaction.response.edit_message(view = self.fishdex_view)
    
class BackToLocations(discord.ui.Button):
    def __init__(self, fishdex_view: discord.ui.View):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        self.db: database.Database = self.fishdex_view.db
        self.bot: discord.Client = self.fishdex_view.bot
        self.fish: objects.Fishes = self.fishdex_view.fish
        self.locations: objects.Locations = self.fishdex_view.locations
        super().__init__(label = "Back", custom_id = "back", style = discord.ButtonStyle.grey, row = 3, emoji = "↩️")

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        caught, shiny = self.db.Caught(), self.db.Shiny()

        embed: discord.Embed = embeds.Locations(ctx = self.ctx, bot = self.bot, caught = caught, shiny = shiny).Get()

        await self.fishdex_view.BackToLocations()
        
        await interaction.response.edit_message(attachments = [], embed = embed, view = self.fishdex_view)

class BackToAdditionalLocations(discord.ui.Button):
    def __init__(self, fishdex_view: discord.ui.View):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        self.db: database.Database = self.fishdex_view.db
        self.bot: discord.Client = self.fishdex_view.bot
        self.fish: objects.Fishes = self.fishdex_view.fish
        self.locations: objects.Locations = self.fishdex_view.locations
        self.selected_location: objects.Location = self.fishdex_view.selected_location
        super().__init__(label = "Back", custom_id = "back", style = discord.ButtonStyle.grey, row = 3, emoji = "↩️")

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        caught, shiny = self.db.Caught(self.selected_location.location_id), self.db.Shiny(self.selected_location.location_id)

        embed: discord.Embed = embeds.AdditionalLocations(ctx = self.ctx, bot = self.bot, location = self.selected_location.location_name, caught = caught, shiny = shiny).Get()
        file: discord.File = await functions.GetFile(filename = self.selected_location.badge_id, folder = "badges")
        
        await self.fishdex_view.BackToAdditionalLocations()

        await interaction.response.edit_message(file = file, embed = embed, view = self.fishdex_view)

class Caught(discord.ui.Button):
    def __init__(self, fishdex_view: discord.ui.View, caught: bool):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        self.db: database.Database = self.fishdex_view.db
        self.bot: discord.Client = self.fishdex_view.bot
        
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
            button: discord.ui.Button = self.fishdex_view.get_item(button_custom_id)
            self.fishdex_view.remove_item(button)
        # -----------------------------------------------------
        self.db.SetCaught(fish_name = self.fishdex_view.selected_fish_name, true = not self.caught)
        caught, shiny = self.db.isCaught(self.fishdex_view.selected_fish_name), self.db.isShiny(self.fishdex_view.selected_fish_name)

        self.fishdex_view.add_item(Caught(fishdex_view = self.fishdex_view, caught = not self.caught))
        self.fishdex_view.add_item(Shiny(fishdex_view = self.fishdex_view, shiny = shiny))

        embed: discord.Embed = embeds.FishEmbed(ctx = self.ctx, bot = self.bot, fish = self.fishdex_view.selected_fish, caught = caught, shiny = shiny).Get()
        await interaction.response.edit_message(embed = embed, view = self.fishdex_view)

class Shiny(discord.ui.Button):
    def __init__(self, fishdex_view: discord.ui.View, shiny: bool):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        self.db: database.Database = self.fishdex_view.db
        self.bot: discord.Client = self.fishdex_view.bot

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
            button: discord.ui.Button = self.fishdex_view.get_item(button_custom_id)
            self.fishdex_view.remove_item(button)
        # -----------------------------------------------------
        self.db.SetShiny(fish_name = self.fishdex_view.selected_fish_name, true = not self.shiny)
        caught, shiny = self.db.isCaught(self.fishdex_view.selected_fish_name), self.db.isShiny(self.fishdex_view.selected_fish_name)

        self.fishdex_view.add_item(Caught(fishdex_view = self.fishdex_view, caught = caught))
        self.fishdex_view.add_item(Shiny(fishdex_view = self.fishdex_view, shiny = not self.shiny))

        embed: discord.Embed = embeds.FishEmbed(ctx = self.ctx, bot = self.bot, fish = self.fishdex_view.selected_fish, caught = caught, shiny = shiny).Get()
        await interaction.response.edit_message(embed = embed, view = self.fishdex_view)