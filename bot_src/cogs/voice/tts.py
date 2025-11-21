from typing import Dict, List, Any
import io
import re

import discord
from discord import app_commands
from discord.ext import commands
from gtts import gTTS, lang

from utils.database import TTSDBUtil
from utils.configs.tts import replacements


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

    def _message_replacement(self, user: discord.Member, text: str) -> str:
        # replace codeblock
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        text = re.sub(r"`[^`]+`", "", text)

        # replace links
        text = re.sub(r"\b[a-zA-Z][a-zA-Z0-9+.-]*://\S+", "", text)
        text = re.sub(r"(\b[a-zA-Z][a-zA-Z0-9+.-]*://\S+|www\.\S+)", "", text)

        for pattern, repl in replacements:
            text = re.sub(pattern, repl, text)

        if len(text) >= 200:
            text = f"{user.name}님이 말하셨습니다."
        return text.strip()

    @app_commands.command(
        name="tts_언어_변경", description="TTS 채널의 언어를 바꿉니다."
    )
    @app_commands.describe(
        channel="선택할 채널을 지정하십시오", channel_lang="선택할 언어를 지정하십시오."
    )
    @app_commands.choices(
        channel_lang=[
            app_commands.Choice(name="한국어", value="ko"),
            app_commands.Choice(name="영어", value="en"),
            app_commands.Choice(name="일본어", value="ja"),
            app_commands.Choice(name="중국어", value="zh"),
        ]
    )
    async def tts_language_change(
        self,
        interaction: discord.Interaction,
        channel: discord.VoiceChannel,
        channel_lang: str,
    ):
        guild = interaction.guild
        db_records = TTSDBUtil.read_tts_data(guild.id)

        target_record = next(
            (r for r in db_records if r["channel_id"] == channel.id), None
        )
        target_record["channel_lang"] = channel_lang

        TTSDBUtil.upsert_tts_channel(
            guild_id=guild.id,
            channel_id=target_record["channel_id"],
            channel_lang=target_record["channel_lang"],
        )

        await interaction.response.send_message(
            f"{channel.mention}의 TTS 언어를 `{channel_lang}`로 바꾸었습니다.",
            ephemeral=True,
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.author == self.bot.user
            or not message.guild
            or message.content.startswith(self.bot.command_prefix)
        ):
            return

        guild = message.guild
        channel = message.channel
        db_records: List[Dict[str, Any]] = TTSDBUtil.read_tts_data(guild.id)

        tts_channel_data = next(
            (record for record in db_records if record["channel_id"] == channel.id),
            None,
        )

        if tts_channel_data:
            pass
        else:
            TTSDBUtil.upsert_tts_channel(
                guild_id=guild.id, channel_id=channel.id, channel_lang="ko"
            )
            tts_channel_data = {"channel_id": channel.id, "channel_lang": "ko"}

        tts_lang = tts_channel_data.get("channel_lang", "ko")
        tts_message = self._message_replacement(message.author, message.content)

        if tts_lang not in lang.tts_langs():
            await message.channel.send(f"{tts_lang}을 지원하지 않습니다.")
            tts_lang = "ko"

        tts = gTTS(text=tts_message, lang=tts_lang)
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
