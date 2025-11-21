import discord
from discord import app_commands
from discord.ext import commands

from utils.log import logger
from utils.UI.embeds import StatusEmbed


class VoiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="음성방_입장", description="사용자가 있는 음성 채널에 봇이 입장합니다."
    )
    @app_commands.guild_only()
    async def join_voice(self, interaction: discord.Interaction):
        try:
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
                    f"**{voice_channel.mention}**에 입장하였습니다.", ephemeral=True
                )

            if voice_client.channel != voice_channel:
                await voice_client.move_to(voice_channel)
                return await interaction.response.send_message(
                    f"**{voice_channel.mention}** 로 이동하였습니다.", ephemeral=True
                )
            await interaction.response.send_message("이미 같은 음성 채널에 있습니다.")
        except Exception as e:
            logger.error(e)
            embed = StatusEmbed.create_error()
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="음성방_퇴장", description="사용자가 있는 음성 채널에서 봇이 퇴장합니다."
    )
    @app_commands.guild_only()
    async def left_voice(self, interaction: discord.Interaction):
        try:
            author = interaction.user
            if not author.voice or not author.voice.channel:
                return await interaction.response.send_message(
                    "먼저 음성 채널에 입장하십시오", ephemeral=True
                )
            voice_channel = author.voice.channel
            voice_client = interaction.guild.voice_client
            if voice_client is None:
                return await interaction.response.send_message(
                    "봇이 현재 어떤 음성 채널에도 연결되어 있지 않습니다.", 
                    ephemeral=True,
                )
            if voice_client.channel != voice_channel:
                return await interaction.response.send_message(
                    f"**{voice_channel.mention}** 에 접속하십시오.", ephemeral=True
                )
            await voice_client.disconnect()
            return await interaction.response.send_message(
                f"**{voice_channel.mention}**에서 성공적으로 퇴장했습니다.", ephemeral=True
            )
        except Exception as e:
            logger.error(e)
            embed = StatusEmbed.create_error()
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, user: discord.Member, before, after):
        try:
            for vc in self.bot.voice_clients:
                channel = vc.channel
                members = [m for m in channel.members if not m.bot]
                if len(members) == 0:
                    await vc.disconnect()
        except Exception as e:
            logger.error(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceCog(bot))
