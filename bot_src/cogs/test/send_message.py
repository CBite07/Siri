import discord


async def send_message(interaction: discord.Interaction, message: str):
    try:
        await interaction.response.send_message(message)
    except:
        await interaction.followup.message(message)
