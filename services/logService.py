from database.database import get_connection
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


async def get_weekly_leaderboard():
    tz = ZoneInfo("Asia/Jakarta")
    now = datetime.now(tz)
    today = now.date()
    
    weekday = (today.weekday() + 1) % 7
    week_start = today - timedelta(days=weekday)
    days_passed = (today - week_start).days + 1

    conn = await get_connection()
    leaderboard = [] 

    try:
        async with conn.execute("SELECT COUNT(*) as count FROM habits WHERE is_active = 1") as cursor:
            row = await cursor.fetchone()
            habit_count = row["count"] if row else 0

        if habit_count == 0:
            return []

        total_possible = habit_count * days_passed

        async with conn.execute("""
            SELECT 
                u.username,
                COUNT(dl.id) as total_completed
            FROM users u
            LEFT JOIN daily_logs dl
                ON u.id = dl.user_id
                AND dl.date BETWEEN ? AND ?
            GROUP BY u.id
            ORDER BY total_completed DESC
        """, (week_start.isoformat(), today.isoformat())) as cursor:
            results = await cursor.fetchall()

        for row in results:
            total_completed = row["total_completed"]
            percentage = round((total_completed / total_possible) * 100, 2) if total_possible > 0 else 0
            
            leaderboard.append({
                "username": row["username"],
                "total_completed": total_completed,
                "percentage": percentage
            })

    finally:
        await conn.close()

    return leaderboard
