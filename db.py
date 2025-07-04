import aiosqlite

DB_PATH = "users.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                subscription_until TEXT,
                invoice_uuid TEXT
            )
        """)
        await db.commit()


async def get_subscription(user_id: int) -> str | None:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT subscription_until FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None


async def set_subscription(user_id: int, until: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (user_id, subscription_until)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET subscription_until = excluded.subscription_until
        """, (user_id, until))
        await db.commit()


async def set_invoice_uuid(user_id: int, uuid: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (user_id, invoice_uuid)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET invoice_uuid = excluded.invoice_uuid
        """, (user_id, uuid))
        await db.commit()


async def get_invoice_uuid(user_id: int) -> str | None:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT invoice_uuid FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None
