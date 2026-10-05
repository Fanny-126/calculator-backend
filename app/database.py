import os
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(
    os.getenv(
        "DATABASE_PATH",
        Path(__file__).resolve().parent.parent / "calculator.db",
    )
)


def get_connection():
    """Create a database connection."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    """Initialize the calculation history table."""
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS calculation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()
    finally:
        connection.close()


def add_history(expression: str, result) -> int:
    """Save a successful calculation to the database."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO calculation_history (expression, result)
            VALUES (?, ?)
            """,
            (expression, str(result)),
        )

        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()
def get_history():
    """Get all calculation history records."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT id, expression, result, created_at
            FROM calculation_history
            ORDER BY id DESC
            """
        )

        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()
def delete_history(history_id: int) -> bool:
    """Delete a calculation history record by ID."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM calculation_history
            WHERE id = ?
            """,
            (history_id,),
        )

        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()