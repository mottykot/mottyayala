import sqlite3

DATABASE_NAME = "quiz.db"


def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # שאלות
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer1 TEXT NOT NULL,
        answer2 TEXT NOT NULL,
        answer3 TEXT NOT NULL,
        answer4 TEXT NOT NULL,
        correct_answer INTEGER NOT NULL
    )
    """)

    # משתתפים
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS participants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        score INTEGER DEFAULT 0
    )
    """)

    # תשובות
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        participant_id INTEGER,
        question_id INTEGER,
        selected_answer INTEGER,
        is_correct INTEGER,
        answer_time DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully!")