import aiohttp

from database.database import get_connection
import pytz
import aiosqlite
from datetime import datetime
from zoneinfo import ZoneInfo

async def get_all():
    conn = await get_connection()

    async with conn.execute(
        "SELECT id, name, is_active FROM habits ORDER BY created_at"
    ) as cursor:
        habits = await cursor.fetchall()

    await conn.close()
    return habits


async def store_habit(name):
    conn = await get_connection()
    
    tz = pytz.timezone("Asia/Jakarta")
    created_at = datetime.now(tz).isoformat()

    await conn.execute(
        "INSERT INTO habits (name, created_at) VALUES (?, ?)",
        (name, created_at)
    )
    await conn.commit()
    await conn.close()


async def disable(habit_id):
    conn = await get_connection()
    
    try:
        await conn.execute(
            "UPDATE habits SET is_active = 0 WHERE id = ?",
            (habit_id,)
        )
        await conn.commit()
    finally:
        await conn.close()

async def update(habit_id, new_name):
    conn = await get_connection()
    
    try:
        await conn.execute(
            "UPDATE habits SET name = ? WHERE id = ?",
            (new_name, habit_id)
        )
        await conn.commit()
    finally:
        await conn.close()

async def enable(habit_id):
    conn = await get_connection()
    
    try:
        await conn.execute(
            "UPDATE habits SET is_active = 1 WHERE id = ?",
            (habit_id,)
        )
        await conn.commit()
    finally:
        await conn.close()


async def get_active_habits():
    conn = await get_connection()

    async with conn.execute(
        "SELECT id, name FROM habits WHERE is_active = 1 ORDER BY created_at"
    ) as cursor:
        habits = await cursor.fetchall()

    await conn.close()
    return habits

async def toggle_habit(user_id, habit_id):
    tz = ZoneInfo("Asia/Jakarta")
    today = datetime.now(tz).date().isoformat()

    conn = await get_connection()
    conn.row_factory = aiosqlite.Row

    async with conn.execute("""
        SELECT id FROM daily_logs
        WHERE user_id = ? AND habit_id = ? AND date = ?
    """, (user_id, habit_id, today)) as cursor:
        existing = await cursor.fetchone()

    if existing:

        await conn.execute("""
            DELETE FROM daily_logs
            WHERE id = ?
        """, (existing["id"],))
        action = "unchecked"
    else:
        await conn.execute("""
            INSERT INTO daily_logs (user_id, habit_id, date)
            VALUES (?, ?, ?)
        """, (user_id, habit_id, today))
        action = "checked"

    await conn.commit()
    await conn.close()

    return action

# async def delete(habit_id):
#     conn = await get_connection()
    
#     try:
#         await conn.execute(
#             "DELETE FROM habits WHERE id = ?",
#             (habit_id,)
#         )
#         await conn.commit()
#     finally:
#         await conn.close()

async def fetch_short_hadits():
    url = "https://api.myquran.com/v2/hadits/perawi/random"
    async with aiohttp.ClientSession() as session:
        for _ in range(5): 
            async with session.get(url) as response:
                if response.status == 200:
                    resp_json = await response.json()
                    if resp_json.get('status') and 'data' in resp_json:
                        data = resp_json['data']
                        if len(data['arab']) <= 1000 and len(data['id']) <= 1000:
                            return resp_json
    return None