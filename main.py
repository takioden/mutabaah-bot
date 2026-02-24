import discord
from discord.ext import commands

from database.database import init_db
from config import TOKEN

from commands.userCommand import auto_leaderboard, register_user_commands, auto_habit_check
from commands.adminCommand import register_admin_commands, daily_hadits_task

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree


@bot.event
async def on_ready():
    await tree.sync()
    await init_db()
    if not auto_habit_check.is_running():
        auto_habit_check.start(bot)
    if not auto_leaderboard.is_running():
        auto_leaderboard.start(bot)
    if not daily_hadits_task.is_running():
        daily_hadits_task.start(bot)
    print(f"Logged in as {bot.user}")
    

register_user_commands(tree)
register_admin_commands(tree)


bot.run(TOKEN)
