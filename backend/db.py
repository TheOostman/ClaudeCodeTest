import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'app.db')

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return aiosqlite.connect(DB_PATH)

async def init_db():
    async with get_db() as db:
        await db.executescript('''
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                agent       TEXT NOT NULL,
                type        TEXT NOT NULL,
                payload     TEXT,
                status      TEXT DEFAULT 'pending',
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS events (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                agent     TEXT,
                message   TEXT NOT NULL,
                ts        DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS products (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT,
                etsy_id     TEXT,
                printify_id TEXT,
                mockup_url  TEXT,
                price       REAL,
                sales       INTEGER DEFAULT 0,
                views       INTEGER DEFAULT 0,
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS orders (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                etsy_order_id TEXT,
                product_id    INTEGER,
                amount        REAL,
                profit        REAL,
                status        TEXT DEFAULT 'pending',
                created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        await db.commit()

async def log_event(agent: str, message: str):
    async with get_db() as db:
        await db.execute(
            'INSERT INTO events (agent, message) VALUES (?, ?)',
            (agent, message)
        )
        await db.commit()

async def get_recent_events(limit: int = 50):
    async with get_db() as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            'SELECT agent, message, ts FROM events ORDER BY ts DESC LIMIT ?', (limit,)
        ) as cur:
            rows = await cur.fetchall()
    return [{'agent': r['agent'], 'message': r['message'], 'ts': r['ts']} for r in rows]

async def upsert_product(data: dict):
    async with get_db() as db:
        await db.execute('''
            INSERT INTO products (title, etsy_id, printify_id, mockup_url, price)
            VALUES (:title, :etsy_id, :printify_id, :mockup_url, :price)
            ON CONFLICT(etsy_id) DO UPDATE SET
                title=excluded.title, mockup_url=excluded.mockup_url,
                price=excluded.price, sales=excluded.sales
        ''', data)
        await db.commit()

async def get_all_products():
    async with get_db() as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM products ORDER BY created_at DESC') as cur:
            rows = await cur.fetchall()
    return [dict(r) for r in rows]
