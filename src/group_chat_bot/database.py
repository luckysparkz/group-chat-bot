from typing import Iterable

import aiosqlite

from .models import ChatMessage
from .schema import SCHEMA


class Database:

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection: aiosqlite.Connection | None = None

    @property
    def conn(self) -> aiosqlite.Connection:
        if self.connection is None:
            raise RuntimeError(
                "Database connection is not open. Did you forget to call .connect()?"
            )
        return self.connection

    async def _execute(self, sql: str, parameters: tuple = ()) -> None:
        async with self.conn.execute(sql, parameters):
            await self.conn.commit()

    async def _fetch_all(
        self, sql: str, parameters: tuple = ()
    ) -> Iterable[aiosqlite.Row]:
        async with self.conn.execute(sql, parameters) as cursor:
            return await cursor.fetchall()

    async def _fetch_one(
        self, sql: str, parameters: tuple = ()
    ) -> aiosqlite.Row | None:
        async with self.conn.execute(sql, parameters) as cursor:
            return await cursor.fetchone()

    async def connect(self) -> None:
        self.connection = await aiosqlite.connect(self.db_path)
        self.connection.row_factory = aiosqlite.Row
        await self._execute("PRAGMA journal_mode=WAL")
        await self._execute(SCHEMA)

    async def close(self) -> None:
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def add_message(self, message: ChatMessage) -> None:
        await self._execute(
            "INSERT INTO messages (id, user_id, user_full_name, content, sent_at) VALUES (?, ?, ?, ?, ?)",
            (
                message.id,
                message.user_id,
                message.user_full_name,
                message.content,
                message.sent_at,
            ),
        )

    async def get_recent_messages(self, limit: int) -> list[ChatMessage]:
        messages = []
        results = await self._fetch_all(
            "SELECT * FROM messages ORDER BY id DESC LIMIT ?", (limit,)
        )

        for row in results:
            new_message = ChatMessage(
                int(row["id"]),
                int(row["user_id"]),
                row["user_full_name"],
                row["content"],
                int(row["sent_at"]),
            )
            messages.append(new_message)

        messages.reverse()
        return messages
