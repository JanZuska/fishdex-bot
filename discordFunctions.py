import discord

async def BlockNonAuthorInteraction(interaction: discord.Interaction) -> None:
    message = f"{interaction.user.mention} you can't do that! Please don't ruin interactions created by other users. You can create you own using `/fishex`."
    await interaction.response.send_message(message, ephemeral=True, delete_after=30)
    return

def Authorization(func):
    async def callback(self: discord.ui, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            await func(self, interaction)
        else:
            await BlockNonAuthorInteraction(interaction)
    return callback

async def Response(object, interaction, file: discord.File | None = None, embed: discord.Embed | None = None, view: discord.ui.View | None = None):
    object.fishdex_view.disable_all_items()
    await interaction.response.edit_message(content = f"Loading <a:loading:1113829058019602452>", view = object.fishdex_view)
    object.fishdex_view.enable_all_items()
    await interaction.message.edit(content = "", file = file, embed = embed, view = view)