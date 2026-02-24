import aiohttp

from discord import app_commands
import discord
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from discord.ext import tasks

from services.userService import get_or_create_user
from services.habitService import get_active_habits
from services.logService import get_weekly_leaderboard
from ui.components import HabitVoteView

target_time = time(hour=20, minute=50, tzinfo=ZoneInfo("Asia/Jakarta"))
@tasks.loop(time=target_time)
async def auto_habit_check(bot):
    channel_id = 1463836813780320280
    channel = bot.get_channel(channel_id)
    if channel:
        habits = await get_active_habits()
        if habits:
            tz = ZoneInfo("Asia/Jakarta")
            today_str = datetime.now(tz).date().isoformat()
            view = HabitVoteView(habits, date_str=today_str)
            await channel.send("🌿 Checklist Habit Hari Ini:", view=view)

leaderboard_time = time(hour=21, minute=0, tzinfo=ZoneInfo("Asia/Jakarta"))
@tasks.loop(time=leaderboard_time)
async def auto_leaderboard(bot):
    tz = ZoneInfo("Asia/Jakarta")
    now = datetime.now(tz)
    today = now.date()
    
    weekday_idx = (today.weekday() + 1) % 7
    week_start = today - timedelta(days=weekday_idx)

    channel = bot.get_channel(1463836813780320280)
    if not channel: return

    data = await get_weekly_leaderboard()
    if not data: return

    is_sunday = (today.weekday() == 6) 
    
    if is_sunday:
        title_text = "🏆 Leaderboard Final Pekan Ini"
        color_theme = discord.Color.gold()
        footer_text = "Pekan ini telah berakhir. Mari mulai semangat baru besok!"
    else:
        title_text = "📊 Klasemen Sementara"
        color_theme = discord.Color.blue()
        footer_text = "Data dihitung secara akumulasi sejak hari Ahad."

    embed = discord.Embed(
        title=title_text,
        description=f"Periode: **{week_start}** s/d **{today}**",
        color=color_theme
    )

    value = ""
    for i, user in enumerate(data[:10], start=1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"**{i}.** "
        value += f"{medal} {user['username']} — {user['percentage']}%\n"
    
    embed.add_field(name="Peringkat 10 Besar", value=value or "Belum ada data.")
    embed.set_footer(text=footer_text)
    
    await channel.send(embed=embed)

def register_user_commands(tree):

    @tree.command(name="check", description="Checklist habit hari ini")
    async def check_command(interaction: discord.Interaction):
        habits = await get_active_habits()
        tz = ZoneInfo("Asia/Jakarta")
        today_str = datetime.now(tz).date().isoformat()
        
        view = HabitVoteView(habits, date_str=today_str)
        await interaction.response.send_message("🌿 Checklist Habit Hari Ini:", view=view, ephemeral=True)

    @tree.command(name="leaderboard", description="Leaderboard minggu ini")
    async def leaderboard(interaction: discord.Interaction):

        data = await get_weekly_leaderboard()

        if not data:
            return await interaction.response.send_message(
                "Belum ada data minggu ini.",
                ephemeral=True
            )

        message = "**🏆 Leaderboard Minggu Ini**\n\n"

        for i, user in enumerate(data[:10], start=1):
            message += (
                f"{i}. {user['username']} - "
                f"{user['total_completed']} "
                f"({user['percentage']}%)\n"
            )

        await interaction.response.send_message(message, ephemeral=True)

    