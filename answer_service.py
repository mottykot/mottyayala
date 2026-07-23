import sqlite3

from config import DATABASE_NAME



def save_answer(
    participant_id,
    question_id,
    selected_answer,
    is_correct
):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO answers
        (
            participant_id,
            question_id,
            selected_answer,
            is_correct
        )

        VALUES (?, ?, ?, ?)

    """,
    (
        participant_id,
        question_id,
        selected_answer,
        is_correct
    ))


    conn.commit()

    conn.close()