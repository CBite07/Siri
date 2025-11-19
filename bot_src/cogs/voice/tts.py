import discord
from discord import app_commands
from discord.ext import commands
from utils.database import TTSDBUtil
from gtts import gTTS
import io


class TTSCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue = {}

    def play_next_in_queue(self, guild_id, error):
        if error:
            print(error)

        guild_queue = self.queue.get(guild_id)
        if guild_queue and guild_queue:
            next_audio_fp = guild_queue.pop(0)
            voice_client = self.bot.get_guild(guild_id).voice_client

            if voice_client:
                voice_client.play(
                    discord.FFmpegPCMAudio(next_audio_fp, pipe=True),
                    after=lambda e: self.play_next_in_queue(guild_id, e),
                )

    @app_commands.command(
        name="tts_채널_지정", description="TTS에 사용될 채널을 지정합니다."
    )
    @app_commands.describe(channel="선택할 채널을 지정하십시오.")
    async def add_tts_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        if not isinstance(channel, discord.TextChannel):
            return await interaction.response.send_message(
                "텍스트 채널을 선택하십시오.", ephemeral=True
            )

        guild_id = interaction.guild.id
        channel_id = channel.id
        await interaction.response.send_message(
            f"{channel.mention} 채널이 TTS용으로 지정되었습니다.", ephemeral=True
        )
        TTSDBUtil.create_guild_tts_channel(guild_id, channel_id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        guild = message.guild
        channel = message.channel
        db_channels = TTSDBUtil.read_guild_tts_channel(guild.id)

        if any(db_channel == channel.id for (db_channel,) in db_channels):
            tts = gTTS(text=message.content, lang="ko")
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)

            if guild.id not in self.queue:
                self.queue[guild.id] = []

            voice_client = guild.voice_client
            if voice_client.is_playing() or self.queue[guild.id]:
                self.queue[guild.id].append(fp)
            else:
                voice_client.play(
                    discord.FFmpegPCMAudio(fp, pipe=True),
                    after=lambda e: self.play_next_in_queue(guild.id, e),
                )


async def setup(bot: commands.Bot):
    await bot.add_cog(TTSCog(bot))
