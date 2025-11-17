# import discord modules
import discord
from discord.ext import commands
from discord import app_commands

# import DB util module
from utils.database.db_utils import DBUtils


# Cog for database testing commands
class DBTestCog(commands.Cog):
    # initialize cog
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # define slash commands
    # delete user command
    @app_commands.command(
        name="delete_user", description="Delete a user from the database"
    )
    @app_commands.describe(member="The Discord member to delete")
    async def delete_user(
        self, interaction: discord.Interaction, member: discord.Member
    ):
        member_id = member.id
        user = DBUtils.delete_user(member_id)
        if user:
            await interaction.response.send_message(
                f"User `{member.display_name}` deleted from the database."
            )
        else:
            await interaction.response.send_message(
                f"User `{member.display_name}` not found in the database."
            )

    # add user command
    @app_commands.command(name="update_user", description="Add a user to the database")
    @app_commands.describe(member="The Discord member to add")
    async def update_user(
        self, interaction: discord.Interaction, member: discord.Member
    ):
        member_id = member.id
        user = DBUtils.get_user(member_id)
        if user:
            await interaction.response.send_message(
                f"User {member.display_name} already exists in the database."
            )
        else:
            new_user = DBUtils.add_user(member_id)
            await interaction.response.send_message(
                f"User {member.display_name} added to the database with ID {new_user.discord_id}."
            )

    # update user points command
    @app_commands.command(name="add_points", description="Add points to a user")
    @app_commands.describe(
        member="The Discord ID of the user",
        exp="Experience points to add",
        level="Level to set",
    )
    async def add_points(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        exp: int,
        level: int,
    ):
        member_id = member.id
        user = DBUtils.get_user(member_id)
        if not user:
            user = DBUtils.add_user(member_id)

        updated_user = DBUtils.update_user_points(member_id, exp, level)
        await interaction.response.send_message(
            f"User {member} updated: EXP={updated_user.exp}, Level={updated_user.level}"
        )

    # get user info command
    @app_commands.command(
        name="get_user_info", description="Get user info from the database"
    )
    @app_commands.describe(member="The Discord member to query")
    async def get_user_info(
        self, interaction: discord.Interaction, member: discord.Member
    ):
        member_id = member.id
        user = DBUtils.get_user(member_id)
        if user:
            await interaction.response.send_message(
                f"User {member.display_name}: EXP={user.exp}, Level={user.level}, Joined At={user.created_at}"
            )
        else:
            await interaction.response.send_message(
                f"User {member.display_name} not found in the database."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(DBTestCog(bot))
