import time


from question_service import get_question_by_id
from participant_service import get_participant_by_phone, add_score
from answer_service import save_answer

from settings_service import get_timer_seconds
from settings_service import get_correct_answer_points

current_game = {

    "active": False,

    "status": "waiting",

    "question_id": None,

    "start_time": None,

    "answers": [],

    "winner_place": None,

    "winner": None

}

# =========================
# Game Control
# =========================


def start_game(question_id):

    current_game["active"] = True

    current_game["status"] = "question"

    current_game["question_id"] = question_id

    current_game["start_time"] = time.time()

    current_game["answers"] = []




def stop_game():

    current_game["active"] = False

    current_game["status"] = "waiting"

    current_game["question_id"] = None

    current_game["start_time"] = None

    current_game["answers"] = []

    current_game["winner_place"] = None





def get_current_game():

    return current_game






def get_current_question():

    if current_game["question_id"] is None:

        return None


    return get_question_by_id(
        current_game["question_id"]
    )






def is_game_active():

    return current_game["active"]






def get_remaining_time():

    if current_game["start_time"] is None:

        return 0



    elapsed = time.time() - current_game["start_time"]


    remaining = get_timer_seconds() - int(elapsed)



    if remaining <= 0:

        return 0



    return remaining





# =========================
# Answers
# =========================


def submit_answer(phone, answer):


    # בדיקת זמן - לא לקבל תשובות אחרי 10 שניות

    if get_remaining_time() <= 0:

        return False



    if not current_game["active"]:

        return False





    participant = get_participant_by_phone(phone)


    participant_id = None

    name = None



    if participant:

        participant_id = participant["id"]

        name = participant["name"]





    question = get_current_question()



    correct = False

    score = 0





    if question:


        if str(answer) == str(question["correct_answer"]):


            correct = True

            score = get_correct_answer_points()





    if correct:


        add_score(
            phone,
            score
        )







    # שמירת תשובה במסד הנתונים

    save_answer(

        participant_id,

        current_game["question_id"],

        answer,

        1 if correct else 0

    )







    # שמירה זמנית להצגה במסך המשחק

    current_game["answers"].append(

        {

            "phone": phone,

            "name": name,

            "answer": answer,

            "correct": correct,

            "score": score,

            "time": time.time()

        }

    )



    return True







def get_answers():

    return current_game["answers"]



def get_answer_statistics():

    statistics = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0
    }


    for answer in current_game["answers"]:

        selected = str(answer["answer"])


        if selected in statistics:

            statistics[selected] += 1



    return statistics



def set_winner_place(place):

    current_game["status"] = "winner"

    current_game["winner_place"] = place