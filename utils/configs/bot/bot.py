import discord
from ..env import EnvConfig


# Bot configuration class
# code review result: nice. Useful static method to get command count.
class BotConfig:
    TOKEN = EnvConfig.BOT_TOKEN
    COMMAND_PREFIX = EnvConfig.BOT_COMMAND_PREFIX

    @staticmethod
    def get_command_count(bot: discord.Client) -> int:
        return len(bot.tree.get_commands())
