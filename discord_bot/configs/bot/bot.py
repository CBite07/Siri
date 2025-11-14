import discord
from configs.env import (
    BOT_TOKEN,
    BOT_COMMAND_PREFIX
)

class BotConfig:
    @staticmethod
    def get_bot_token():
        return (BOT_TOKEN)

    @staticmethod
    def get_command_prefix():
        return BOT_COMMAND_PREFIX

    @staticmethod
    def get_command_count(bot: discord.Intents):
        return len(list(bot.tree.walk_commands()))