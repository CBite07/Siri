import discord
from ..env import BOT_TOKEN, BOT_COMMAND_PREFIX


class BotConfig:
    @staticmethod
    def get_bot_token():
        return BOT_TOKEN

    @staticmethod
    def get_command_prefix():
        return BOT_COMMAND_PREFIX

    @staticmethod
    async def get_command_count(bot: discord.Client):
        commands = await bot.tree.fetch_commands()
        return len(commands)
