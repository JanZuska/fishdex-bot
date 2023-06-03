import discord
from discord.ext import commands
import views
from discordFunctions import *
import database
import embeds
import functions
import objects
import os
from PIL import Image

class PreviousPage(discord.ui.Button):
    def __init__(self, fishdex_view: discord.ui.View):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        super().__init__(label = "Previous page", disabled = True, custom_id = "previous", style = discord.ButtonStyle.blurple, row = 1, emoji = "⬅️")

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        self.fishdex_view.disabled = True
        await interaction.response.edit_message(content = f"Loading <a:loading:1113829058019602452>", view = self.fishdex_view)

        self.next_button: discord.ui.Button = self.fishdex_view.get_item("next")
        self.fish_select: discord.ui.View = self.fishdex_view.get_item("fish_select")

        self.fishdex_view.page -= 1
        self.next_button.disabled = False
        if self.fishdex_view.page == 0:
            self.disabled = True

        new_options: list = [discord.SelectOption(label = available_fish["name"]) for available_fish in self.fishdex_view.available_fishes_pages[self.fishdex_view.page]]
        self.fish_select.options.clear()
        self.fish_select.options.extend(new_options)

        self.fishdex_view.disabled = False
        await interaction.message.edit(content = "", view = self.fishdex_view)

class NextPage(discord.ui.Button):
    def __init__(self, fishdex_view: discord.ui.View):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        super().__init__(label = "Next page", custom_id = "next", style = discord.ButtonStyle.blurple, row = 1, emoji = "➡️")

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        self.fishdex_view.disabled = True
        await interaction.response.edit_message(content = f"Loading <a:loading:1113829058019602452>", view = self.fishdex_view)

        self.previous_button: discord.ui.Button = self.fishdex_view.get_item("previous")
        self.fish_select: discord.ui.View = self.fishdex_view.get_item("fish_select")

        self.fishdex_view.page += 1

        self.previous_button.disabled = False

        if self.fishdex_view.page == (len(self.fishdex_view.available_fishes_pages) - 1):
            self.disabled = True

        new_options: list = [discord.SelectOption(label = available_fish["name"]) for available_fish in self.fishdex_view.available_fishes_pages[self.fishdex_view.page]]
        self.fish_select.options.clear()
        self.fish_select.options.extend(new_options)

        self.fishdex_view.disabled = False
        await interaction.message.edit(content = "", view = self.fishdex_view)
    
class BackToLocations(discord.ui.Button):
    def __init__(self, fishdex_view: discord.ui.View):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        self.db: database.Database = self.fishdex_view.db
        self.bot: discord.Client = self.fishdex_view.bot
        self.fish: objects.Fishes = self.fishdex_view.fish
        self.locations: objects.Locations = self.fishdex_view.locations
        super().__init__(label = "Back", custom_id = "back", style = discord.ButtonStyle.grey, row = 4, emoji = "↩️")

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        self.fishdex_view.disabled = True
        await interaction.response.edit_message(content = f"Loading <a:loading:1113829058019602452>", view = self.fishdex_view)

        caught, shiny = self.db.Caught(), self.db.Shiny()

        embed: discord.Embed = embeds.Locations(ctx = self.ctx, bot = self.bot, caught = caught, shiny = shiny).Get()

        await self.fishdex_view.BackToLocations()
        
        self.fishdex_view.disabled = False
        await interaction.message.edit(content = "", attachments = [], embed = embed, view = self.fishdex_view)

class BackToAdditionalLocations(discord.ui.Button):
    def __init__(self, fishdex_view: discord.ui.View):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        self.db: database.Database = self.fishdex_view.db
        self.bot: discord.Client = self.fishdex_view.bot
        self.fish: objects.Fishes = self.fishdex_view.fish
        self.locations: objects.Locations = self.fishdex_view.locations
        self.selected_location: objects.Location = self.fishdex_view.selected_location
        super().__init__(label = "Back", custom_id = "back", style = discord.ButtonStyle.grey, row = 4, emoji = "↩️")

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        self.fishdex_view.disabled = True
        await interaction.response.edit_message(content = f"Loading <a:loading:1113829058019602452>", view = self.fishdex_view)

        caught, shiny = self.db.Caught(self.selected_location.location_id), self.db.Shiny(self.selected_location.location_id)

        embed: discord.Embed = embeds.AdditionalLocations(ctx = self.ctx, bot = self.bot, location = self.selected_location.location_name, caught = caught, shiny = shiny).Get()
        file: discord.File = await functions.GetFile(filename = self.selected_location.badge_id, folder = "badges")
        
        await self.fishdex_view.BackToAdditionalLocations()

        self.fishdex_view.disabled = False
        await interaction.message.edit(content = "", file = file, embed = embed, view = self.fishdex_view)

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
        super().__init__(label = "Caught", custom_id = "caught", style = style, row = 3, emoji = emoji)

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        self.fishdex_view.disabled = True
        await interaction.response.edit_message(content = f"Loading <a:loading:1113829058019602452>", view = self.fishdex_view)

        # Remove Caught and Shiny buttons to avoid mixing order
        for button_custom_id in ["caught", "shiny"]:
            button: discord.ui.Button = self.fishdex_view.get_item(button_custom_id)
            self.fishdex_view.remove_item(button)
        # -----------------------------------------------------
        self.db.SetCaught(fish_name = self.fishdex_view.selected_fish_name, true = not self.caught)
        caught, shiny = self.db.isCaught(self.fishdex_view.selected_fish_name), self.db.isShiny(self.fishdex_view.selected_fish_name)

        self.fishdex_view.add_item(Caught(fishdex_view = self.fishdex_view, caught = not self.caught))
        self.fishdex_view.add_item(Shiny(fishdex_view = self.fishdex_view, shiny = shiny))

        embed: discord.Embed = interaction.message.embeds[0]

        if caught:
            value = functions.Get.Emoji('true', 'others')
            embed.color = discord.Colour.green()
        else:
            value = functions.Get.Emoji('false', 'others')
            embed.color = discord.Colour.red()
        embed.set_field_at(index = 12, name = "Caught", value = value)
        
        self.fishdex_view.disabled = False
        await interaction.message.edit(content = "", attachments = [], embed = embed, view = self.fishdex_view)

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
        super().__init__(label = "Shiny", custom_id = "shiny", style = style, row = 3, emoji = emoji)

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        self.fishdex_view.disabled = True
        await interaction.response.edit_message(content = f"Loading <a:loading:1113829058019602452>", view = self.fishdex_view)

        # Remove Caught and Shiny buttons to avoid mixing order
        for button_custom_id in ["caught", "shiny"]:
            button: discord.ui.Button = self.fishdex_view.get_item(button_custom_id)
            self.fishdex_view.remove_item(button)
        # -----------------------------------------------------
        self.db.SetShiny(fish_name = self.fishdex_view.selected_fish_name, true = not self.shiny)
        caught, shiny = self.db.isCaught(self.fishdex_view.selected_fish_name), self.db.isShiny(self.fishdex_view.selected_fish_name)

        self.fishdex_view.add_item(Caught(fishdex_view = self.fishdex_view, caught = caught))
        self.fishdex_view.add_item(Shiny(fishdex_view = self.fishdex_view, shiny = not self.shiny))

        embed: discord.Embed = interaction.message.embeds[0]

        if shiny:
            value = functions.Get.Emoji('true', 'others')
        else:
            value = functions.Get.Emoji('false', 'others')
        embed.set_field_at(index = 13, name = "Shiny", value = value)
        
        self.fishdex_view.disabled = False
        await interaction.message.edit(content = "", attachments = [], embed = embed, view = self.fishdex_view)

class PreviousFish(discord.ui.Button):
    def __init__(self, fishdex_view: discord.ui.View):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        self.bot: discord.Client = self.fishdex_view.bot
        self.db: database.Database = self.fishdex_view.db
        super().__init__(label = "Previous fish", disabled = True, custom_id = "previous_fish", style = discord.ButtonStyle.blurple, row = 2, emoji = "⬅️")

    @Authorization
    async def callback(self, interaction: discord.Interaction):
        self.fishdex_view.disabled = True
        await interaction.response.edit_message(content = f"Loading <a:loading:1113829058019602452>", view = self.fishdex_view)

        self.next_fish_button: discord.ui.Button = self.fishdex_view.get_item("next_fish")
        self.fishdex_view.index -= 1
        if self.fishdex_view.index == 0:
            self.disabled = True
        self.next_fish_button.disabled = False

        selected_fish = self.fishdex_view.available_fishes[self.fishdex_view.index]
        selected_fish_name = selected_fish["name"]
        caught, shiny = self.db.isCaught(selected_fish_name), self.db.isShiny(selected_fish_name)

        await self.fishdex_view.FishSelect(selected_fish_name = selected_fish_name, selected_fish = selected_fish, caught = caught, shiny = shiny)

        embed = embeds.FishEmbed(ctx = self.ctx, bot = self.bot, fish = selected_fish, caught = caught, shiny = shiny).Get()
        file: discord.File = await functions.GetFile(selected_fish, "fish")
        
        self.fishdex_view.disabled = False
        await interaction.message.edit(content = "", file = file, embed = embed, view = self.fishdex_view)

class NextFish(discord.ui.Button):
    def __init__(self, fishdex_view: discord.ui.View):
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        self.bot: discord.Client = self.fishdex_view.bot
        self.db: database.Database = self.fishdex_view.db
        super().__init__(label = "Next fish", custom_id = "next_fish", style = discord.ButtonStyle.blurple, row = 2, emoji = "➡️")
    
    @Authorization
    async def callback(self, interaction: discord.Interaction):
        self.fishdex_view.disabled = True
        await interaction.response.edit_message(content = f"Loading <a:loading:1113829058019602452>", view = self.fishdex_view)

        self.previous_fish_button: discord.ui.Button = self.fishdex_view.get_item("previous_fish")
        self.fishdex_view.index += 1
        if self.fishdex_view.index == (len(self.fishdex_view.available_fishes) - 1):
            self.disabled = True
        if not self.fishdex_view.index == 0:
            self.previous_fish_button.disabled = False

        selected_fish = self.fishdex_view.available_fishes[self.fishdex_view.index]
        selected_fish_name = selected_fish["name"]
        caught, shiny = self.db.isCaught(selected_fish_name), self.db.isShiny(selected_fish_name)

        await self.fishdex_view.FishSelect(selected_fish_name = selected_fish_name, selected_fish = selected_fish, caught = caught, shiny = shiny)
        
        embed = embeds.FishEmbed(ctx = self.ctx, bot = self.bot, fish = selected_fish, caught = caught, shiny = shiny).Get()
        file: discord.File = await functions.GetFile(selected_fish, "fish")
        
        self.fishdex_view.disabled = False
        await interaction.message.edit(content = "", file = file, embed = embed, view = self.fishdex_view)

class DisplayShiny(discord.ui.Button):
    def __init__(self, fishdex_view: discord.ui.View):
        super().__init__(label="Display shiny", custom_id="display_shiny", style = discord.ButtonStyle.blurple, row = 2)
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        self.db: database.Database = self.fishdex_view.db
        self.bot: discord.Client = self.fishdex_view.bot

    @Authorization
    async def callback(self, interaction):
        self.fishdex_view.disabled = True
        await interaction.response.edit_message(content = f"Loading <a:loading:1113829058019602452>", view = self.fishdex_view)

        self.fishdex_view.remove_item(self)
        self.fishdex_view.add_item(DisplayDefault(fishdex_view = self.fishdex_view))

        selected_fish_name = self.fishdex_view.selected_fish_name
        caught = self.db.isCaught(selected_fish_name)
        shiny = self.db.isShiny(selected_fish_name)

        selected_fish_id = self.fishdex_view.selected_fish["id"]
        selected_fish_hue = int(self.fishdex_view.selected_fish["hue_shift_of_shiny"])
        image_name = f"temp_image_{await functions.FileCoding()}.png"
        image = await functions.change_hue(Image.open(f"images/fish/{selected_fish_id}.png"), selected_fish_hue)
        await functions.SaveImage(image, image_name)

        file = discord.File(f"images/{image_name}")
        embed = embeds.FishEmbed(ctx = self.ctx, bot = self.bot, fish = self.fishdex_view.selected_fish, caught = caught, shiny = shiny, image = image_name).Get()
        
        self.fishdex_view.disabled = False
        await interaction.message.edit(content = "", file = file, embed = embed, view = self.fishdex_view)
        os.remove(f"images/{image_name}")

class DisplayDefault(discord.ui.Button):
    def __init__(self, fishdex_view: discord.ui.View):
        super().__init__(label="Display default", custom_id="display_default", style = discord.ButtonStyle.blurple, row = 2)
        self.fishdex_view: discord.ui.View = fishdex_view
        self.ctx: commands.Context = self.fishdex_view.ctx
        self.db: database.Database = self.fishdex_view.db
        self.bot: discord.Client = self.fishdex_view.bot

    @Authorization
    async def callback(self, interaction):
        self.fishdex_view.disabled = True
        await interaction.response.edit_message(content = f"Loading <a:loading:1113829058019602452>", view = self.fishdex_view)

        self.fishdex_view.remove_item(self)
        self.fishdex_view.add_item(DisplayShiny(fishdex_view = self.fishdex_view))

        selected_fish_name = self.fishdex_view.selected_fish_name
        caught = self.db.isCaught(selected_fish_name)
        shiny = self.db.isShiny(selected_fish_name)

        file = await functions.GetFile(self.fishdex_view.selected_fish, "fish")
        embed = embeds.FishEmbed(ctx = self.ctx, bot = self.bot, fish = self.fishdex_view.selected_fish, caught = caught, shiny = shiny).Get()

        self.fishdex_view.disabled = False
        await interaction.message.edit(content = "", file = file, embed = embed, view = self.fishdex_view)
