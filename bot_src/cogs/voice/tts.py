from typing import Dict, List, Any
import io

import discord
from discord import app_commands
from discord.ext import commands
from gtts import gTTS

from utils.database import TTSDBUtil


class TTSCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue: Dict[int, List[io.BytesIO]] = {}

    def _play_next_in_queue(self, guild_id, error):
        if error:
            print(error)

        guild_queue = self.queue.get(guild_id)
        
        if not guild_queue:
            return

        next_audio_fp = guild_queue.pop(0)
        voice_client = self.bot.get_guild(guild_id).voice_client

        if voice_client and not voice_client.is_playing():
            voice_client.play(
                discord.FFmpegPCMAudio(next_audio_fp, pipe=True),
                after=lambda e: self._play_next_in_queue(guild_id, e),
            )

    @app_commands.command(
        name="tts_채널_지정", description="TTS에 사용될 채널을 지정합니다."
    )
    @app_commands.describe(channel="선택할 채널을 지정하십시오.")
    @app_commands.default_permissions(administrator=True)
    async def add_tts_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        guild_id = interaction.guild.id
        channel_id = channel.id
        
        TTSDBUtil.upsert_tts_channel(guild_id, channel_id, lang="ko")

        await interaction.response.send_message(
            f"{channel.mention} 채널이 TTS용으로 지정되었습니다. (기본 언어: 한국어)", ephemeral=True
        )

    @app_commands.command(
        name="tts_채널_해제", description="TTS 채널 지정을 해제합니다."
    )
    @app_commands.describe(channel="해제할 채널을 지정하십시오.")
    @app_commands.default_permissions(administrator=True)
    async def remove_tts_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        guild_id = interaction.guild.id
        channel_id = channel.id
        
        TTSDBUtil.delete_guild_tts_channel(guild_id, channel_id)

        await interaction.response.send_message(
            f"{channel.mention} 채널의 TTS 지정이 해제되었습니다.", ephemeral=True
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or not message.guild or message.content.startswith(self.bot.command_prefix):
            return

        guild = message.guild
        channel = message.channel
        
        db_records: List[Dict[str, Any]] = TTSDBUtil.read_tts_data(guild.id)

        tts_channel_data = next(
            (record for record in db_records if record['channel_id'] == channel.id), 
            None
        )

        if tts_channel_data:
            tts_lang = tts_channel_data.get('lang', 'ko') 
            
            try:
                tts = gTTS(text=message.content, lang=tts_lang)
            except:
                tts = gTTS(text=message.content, lang="ko")
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)

            if guild.id not in self.queue:
                self.queue[guild.id] = []

            voice_client = guild.voice_client
            
            if not voice_client:
                return
            
            if voice_client.is_playing() or self.queue[guild.id]:
                self.queue[guild.id].append(fp)
            else:
                voice_client.play(
                    discord.FFmpegPCMAudio(fp, pipe=True),
                    after=lambda e: self._play_next_in_queue(guild.id, e),
                )


async def setup(bot: commands.Bot):
    await bot.add_cog(TTSCog(bot))