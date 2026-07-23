import sqlite3

from config import DATABASE_NAME



def get_all_participants():

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM participants
        ORDER BY id DESC
    """)

    participants = cursor.fetchall()

    conn.close()

    return participants



def get_participant_by_id(participant_id):

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM participants WHERE id = ?",
        (participant_id,)
    )

    participant = cursor.fetchone()

    conn.close()

    return participant



def get_participant_by_phone(phone):

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM participants WHERE phone = ?",
        (phone,)
    )

    participant = cursor.fetchone()

    conn.close()

    return participant



def add_participant(name, phone):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO participants
        (name, phone)
        VALUES (?, ?)
    """, (
        name,
        phone
    ))

    conn.commit()
    conn.close()



def update_participant(participant_id, name, phone):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE participants
        SET name = ?,
            phone = ?
        WHERE id = ?
    """, (
        name,
        phone,
        participant_id
    ))

    conn.commit()
    conn.close()



def add_score(phone, score):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE participants
        SET score = score + ?
        WHERE phone = ?
    """, (
        score,
        phone
    ))

    conn.commit()
    conn.close()



def delete_participant(participant_id):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM participants WHERE id = ?",
        (participant_id,)
    )

    conn.commit()
    conn.close()

def get_top_participants():

    conn = sqlite3.connect(DATABASE_NAME)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()


    cursor.execute("""
        SELECT *
        FROM participants
        ORDER BY score DESC
        LIMIT 3
    """)


    participants = cursor.fetchall()


    conn.close()


    return participants