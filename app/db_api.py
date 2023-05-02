import sqlite3
from contextlib import contextmanager

from . import config

@contextmanager
def db_ops(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    yield cur, conn
    conn.commit()
    conn.close()


class SQLAPI:
    def __init__(self, settings: config.Database) -> None:
        self.db_file = settings.file_path
        with db_ops(self.db_file) as (cur, _):
            cur.execute(
                "CREATE TABLE IF NOT EXISTS messages(message_id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, message TEXT, role TEXT)"
            )

    def post_message(self, session_id: str, message: str, role: str):
        with db_ops(self.db_file) as (cur, conn):
            cur.execute(
                f"INSERT INTO messages(session_id,message,role) VALUES(?,?,?)",
                (
                    session_id,
                    message,
                    role,
                ),
            )
            conn.commit()

    def get_messages(self, *, session_id=None):
        with db_ops(self.db_file) as (cur, _):
            if not session_id:
                cur.execute("SELECT * FROM messages")
            else:
                cur.execute(
                    "SELECT * FROM messages WHERE messages.session_id=?", (session_id,)
                )

            rows = cur.fetchall()

        return rows
