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