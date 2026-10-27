
import sqlite3
from pathlib import Path
from datetime import datetime

# Store the database in the main project folder.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_DIR / "fitness_history.db"


def get_connection():
    connection = sqlite3.connect(str(DATABASE_PATH))
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS workout_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                workout_date TEXT NOT NULL,
                goal TEXT NOT NULL,
                duration INTEGER NOT NULL,
                completed_exercises INTEGER NOT NULL,
                total_exercises INTEGER NOT NULL,
                calories_estimate REAL NOT NULL
            )
        """)


def save_workout(
    user_name,
    goal,
    duration,
    completed_exercises,
    total_exercises,
    calories_estimate,
):
    workout_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO workout_history (
                user_name,
                workout_date,
                goal,
                duration,
                completed_exercises,
                total_exercises,
                calories_estimate
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_name,
                workout_date,
                goal,
                duration,
                completed_exercises,
                total_exercises,
                calories_estimate,
            ),
        )


def get_workout_history(user_name):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM workout_history
            WHERE user_name = ?
            ORDER BY workout_date DESC, id DESC
            """,
            (user_name,),
        ).fetchall()

    return [dict(row) for row in rows]


# Create the database and table if they do not exist.
initialize_database()
