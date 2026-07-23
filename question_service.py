import sqlite3

from config import DATABASE_NAME



def get_all_questions():

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM questions
        ORDER BY id DESC
    """)

    questions = cursor.fetchall()

    conn.close()

    return questions



def get_question_by_id(question_id):

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM questions WHERE id = ?",
        (question_id,)
    )

    question = cursor.fetchone()

    conn.close()

    return question



def add_question(
        question,
        answer1,
        answer2,
        answer3,
        answer4,
        correct_answer
):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO questions
        (question, answer1, answer2, answer3, answer4, correct_answer)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        question,
        answer1,
        answer2,
        answer3,
        answer4,
        correct_answer
    ))

    conn.commit()
    conn.close()



def update_question(
        question_id,
        question,
        answer1,
        answer2,
        answer3,
        answer4,
        correct_answer
):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE questions
        SET question = ?,
            answer1 = ?,
            answer2 = ?,
            answer3 = ?,
            answer4 = ?,
            correct_answer = ?
        WHERE id = ?
    """, (
        question,
        answer1,
        answer2,
        answer3,
        answer4,
        correct_answer,
        question_id
    ))

    conn.commit()
    conn.close()



def delete_question(question_id):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM questions WHERE id = ?",
        (question_id,)
    )

    conn.commit()
    conn.close()