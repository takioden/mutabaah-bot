import discord
from services.habitService import toggle_habit
from datetime import datetime
from zoneinfo import ZoneInfo

from services.userService import get_or_create_user

class HabitVoteView(discord.ui.View):
    def __init__(self, habits, date_str=None):
        super().__init__(timeout=None)
        self.habits = habits
        tz = ZoneInfo("Asia/Jakarta")
        self.created_date = date_str or datetime.now(tz).date().isoformat()
        self.add_buttons()

    def add_buttons(self):
        for habit in self.habits:
            btn = discord.ui.Button(
                label=habit['name'], 
                custom_id=f"habit_{habit['id']}",
                style=discord.ButtonStyle.primary
            )
            btn.callback = self.create_callback(habit['id'], habit['name'])
            self.add_item(btn)

    def create_callback(self, habit_id, habit_name):
        async def callback(interaction: discord.Interaction):
            tz = ZoneInfo("Asia/Jakarta")
            now = datetime.now(tz)
            today = now.date().isoformat()

            if today != self.created_date:
                return await interaction.response.send_message(
                    "⏰ **Deadline Terlewati!**\n"
                    "Batas pengisian untuk daftar ini adalah pukul 23:59 hari kemarin. ",
                    ephemeral=True
                )
            
            db_user_id = await get_or_create_user(interaction.user.id, interaction.user.name)

            
            action = await toggle_habit(db_user_id, habit_id)
            
            status = "✅ Selesai" if action == "checked" else "❌ Dibatalkan"
            await interaction.response.send_message(
                f"{status}: **{habit_name}** untuk hari ini.",
                ephemeral=True
            )
        return callback
