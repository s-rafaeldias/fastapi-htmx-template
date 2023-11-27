from app.models import ItemForm
from databases import Database


async def init_db(db: Database) -> None:
    await db.execute(
        """
    CREATE TABLE IF NOT EXISTS items (
        id   INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    );
    """
    )

    await db.execute_many(
        query="INSERT INTO items (name) VALUES (:name)",
        values=[{"name": "test1"}, {"name": "test2"}],
    )


async def insert(item: ItemForm, db: Database) -> None:
    await db.execute(
        query="INSERT INTO items (name) VALUES (:name)", values={"name": item.name}
    )
