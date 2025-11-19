import discord
from discord import app_commands
from discord.ext import commands


class TTSCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="음성방_입장", description="사용자가 있는 음성 채널에 봇이 입장합니다."
    )
    async def join_voice(self, interaction: discord.Interaction):
        author = interaction.user
        if not author.voice or not author.voice.channel:
            return await interaction.response.send_message(
                "먼저 음성 채널에 입장하십시오", ephemeral=True
            )
        voice_channel = author.voice.channel
        voice_client = interaction.guild.voice_client
        if voice_client is None:
            await voice_channel.connect()
            return await interaction.response.send_message(
                f"**<#{voice_channel.id}>**에 입장하였습니다.", ephemeral=True
            )
        if voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel)
            return await interaction.response.send_message(
                f"🚶 **<#{voice_channel.id}>** 로 이동하였습니다.", ephemeral=True
            )
        await interaction.response.send_message("이미 같은 음성 채널에 있습니다.")

    @app_commands.command(
        name="음성방_퇴장", description="사용자가 있는 음성 채널에서 봇이 퇴장합니다."
    )
    async def left_voice(self, interaction: discord.Interaction):
        author = interaction.user
        if not author.voice or not author.voice.channel:
            return await interaction.response.send_message(
                "먼저 음성 채널에 입장하십시오", ephemeral=True
            )
        voice_channel = author.voice.channel
        voice_client = interaction.guild.voice_client
        if voice_client is None:
            return await interaction.response.send_message(
                f"**<#{voice_channel.id}>** 사용자가 접속한 음성 채널이 없습니다.",
                ephemeral=True,
            )
        if voice_client.channel != voice_channel:
            return await interaction.response.send_message(
                f"**<#{voice_channel.id}>** 에 접속하십시오.", ephemeral=True
            )
        await voice_client.disconnect()
        return await interaction.response.send_message(
            f"<#{voice_channel.id}>에서 성공적으로 퇴장했습니다.", ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(TTSCog(bot))
