from database.database import get_connection
import pytz
from datetime import datetime

async def get_or_create_user(discord_id, username):
    conn = await get_connection()

    async with conn.execute(
        "SELECT id FROM users WHERE discord_id = ?",
        (discord_id,)
    ) as cursor:
        user = await cursor.fetchone()

    if user:
        await conn.close()
        return user["id"]

    join_date = datetime.now().date().isoformat()

    await conn.execute(
        "INSERT INTO users (discord_id, username, join_date) VALUES (?, ?, ?)",
        (discord_id, username, join_date)
    )
    await conn.commit()

    async with conn.execute(
        "SELECT id FROM users WHERE discord_id = ?",
        (discord_id,)
    ) as cursor:
        user = await cursor.fetchone()

    await conn.close()
    return user["id"]


