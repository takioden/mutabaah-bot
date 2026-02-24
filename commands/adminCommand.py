from discord import app_commands
import discord
from datetime import time
from zoneinfo import ZoneInfo
from discord.ext import tasks
from services.habitService import store_habit, disable, get_all, enable, update, fetch_short_hadits

hadits_time = time(hour=5, minute=0, tzinfo=ZoneInfo("Asia/Jakarta"))
@tasks.loop(time=hadits_time)
async def daily_hadits_task(bot):
    channel = bot.get_channel(1463836813780320280) 
    if not channel:
        return

    result = await fetch_short_hadits()
    if result:
        data = result['data']
        info = result['info']['perawi']
        
        embed = discord.Embed(
            title=f"✨ One Day One Hadits: HR {info['name']}",
            color=0x2ecc71,
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="Teks Arab:", value=f"```ar\n{data['arab']}\n```", inline=False)
        embed.add_field(name="📖 Terjemahan:", value=f"> {data['id']}", inline=False)
        embed.set_footer(text=f"Nomor: {data['number']} | Perawi: {info['name']}")
        
        await channel.send("Assalamu'alaikum! Semangat pagi, berikut hadits untuk hari ini:", embed=embed)

def register_admin_commands(tree):

    def is_admin(interaction: discord.Interaction):
        return interaction.user.guild_permissions.administrator

    @tree.command (name = "get_all_habits", description = "Habit")
    @app_commands.default_permissions(administrator=True)
    async def get_all_habits_command(interaction: discord.Interaction):

        if not is_admin(interaction):
            return await interaction.response.send_message(
                "Kamu bukan admin.",
                ephemeral=True
            )

        habits = await get_all()

        if not habits:
            return await interaction.response.send_message(
                "Belum ada habit.",
                ephemeral=True
            )

        message = "**Daftar Habit**\n\n"

        for habit in habits:
            status = "Aktif" if habit["is_active"] else "Nonaktif"
            message += f"ID: {habit['id']} - {habit['name']} ({status})\n"

        await interaction.response.send_message(message, ephemeral=True)

    @tree.command(name="add_habit", description="Tambah habit baru")
    @app_commands.default_permissions(administrator=True)
    async def add_habit_command(interaction: discord.Interaction, name: str):

        if not is_admin(interaction):
            return await interaction.response.send_message(
                "Kamu bukan admin.",
                ephemeral=True
            )
        await interaction.response.defer(ephemeral=True)
        await store_habit(name)

        await interaction.followup.send(
            f"Habit '{name}' berhasil ditambahkan.",
            ephemeral=True
        )
        habits = await get_all()
        message = "**Daftar Habit**\n\n"

        for habit in habits:
            status = "Aktif" if habit["is_active"] else "Nonaktif"
            message += f"ID: {habit['id']} - {habit['name']} ({status})\n"

        await interaction.followup.send(message, ephemeral=True)

    @tree.command(name="disable_habit", description="Nonaktifkan habit")
    @app_commands.default_permissions(administrator=True)
    async def disable_habit_command(
        interaction: discord.Interaction,
        habit_id: int
    ):

        if not is_admin(interaction):
            return await interaction.response.send_message(
                "Kamu bukan admin.",
                ephemeral=True
            )

        await interaction.response.defer(ephemeral=True)
        await disable(habit_id)

        await interaction.followup.send(
            f"Habit ID {habit_id} dinonaktifkan.",
            ephemeral=True
        )
        habits = await get_all()
        message = "**Daftar Habit**\n\n"

        for habit in habits:
            status = "Aktif" if habit["is_active"] else "Nonaktif"
            message += f"ID: {habit['id']} - {habit['name']} ({status})\n"

        await interaction.followup.send(message, ephemeral=True)

    @tree.command(name="enable_habit", description="Aktifkan habit")
    @app_commands.default_permissions(administrator=True)
    async def enable_habit_command(
        interaction: discord.Interaction,
        habit_id: int
    ):

        if not is_admin(interaction):
            return await interaction.response.send_message(
                "Kamu bukan admin.",
                ephemeral=True
            )

        await interaction.response.defer(ephemeral=True)
        await enable(habit_id)

        await interaction.followup.send(
            f"Habit ID {habit_id} diaktifkan.",
            ephemeral=True
        )
        habits = await get_all()
        message = "**Daftar Habit**\n\n"

        for habit in habits:
            status = "Aktif" if habit["is_active"] else "Nonaktif"
            message += f"ID: {habit['id']} - {habit['name']} ({status})\n"

        await interaction.followup.send(message, ephemeral=True)


    @tree.command(name="update_habit", description="Update nama habit")
    @app_commands.default_permissions(administrator=True)
    async def update_habit_command(
        interaction: discord.Interaction,
        habit_id: int,
        new_name: str
    ):

        if not is_admin(interaction):
            return await interaction.response.send_message(
                "Kamu bukan admin.",
                ephemeral=True
            )

        await update(habit_id, new_name)

        await interaction.response.send_message(
            f"Habit ID {habit_id} diupdate menjadi '{new_name}'.",
            ephemeral=True
        )
    
    # @tree.command(name="delete_habit", description="Hapus habit")
    # @app_commands.default_permissions(administrator=True)
    # async def delete_habit_command(
    #     interaction: discord.Interaction,
    #     habit_id: int
    # ):

    #     if not is_admin(interaction):
    #         return await interaction.response.send_message(
    #             "Kamu bukan admin.",
    #             ephemeral=True
    #         )

    #     await delete(habit_id)

    #     await interaction.response.send_message(
    #         f"Habit ID {habit_id} dihapus.",
    #         ephemeral=True
    #     )