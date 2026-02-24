import aiosqlite
import os

DB_PATH = os.path.join("data", "mutabaah.db")

async def get_connection():
    conn = await aiosqlite.connect(DB_PATH)
    conn.row_factory = aiosqlite.Row
    await conn.execute("PRAGMA journal_mode=WAL;")
    return conn


async def init_db():

    conn = await get_connection()

    await conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        discord_id TEXT UNIQUE,
        username TEXT,
        join_date TEXT
    )
    """)

    await conn.execute("""
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        created_at TEXT,
        is_active INTEGER DEFAULT 1
    )
    """)

    await conn.execute("""
    CREATE TABLE IF NOT EXISTS daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        habit_id INTEGER,
        date TEXT,
        UNIQUE(user_id, habit_id, date)
    )
    """)

    await conn.execute("CREATE INDEX IF NOT EXISTS idx_user_date ON daily_logs(user_id, date)")
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_date ON daily_logs(date)")

    await conn.commit()
    await conn.close()
