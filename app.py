from flask import jsonify

from flask import Flask, render_template, request, redirect

from question_service import (
    get_all_questions,
    get_question_by_id,
    add_question,
    update_question,
    delete_question
)

from participant_service import (
    get_all_participants,
    get_participant_by_id,
    add_participant,
    update_participant,
    delete_participant,
    get_top_participants
)

from game_service import (
    start_game,
    stop_game,
    get_current_game,
    get_current_question,
    get_remaining_time,
    get_answers,
    submit_answer,
    get_answer_statistics,
    set_winner_place
)

from display_service import (
    get_display_mode,
    get_display_version,
    show_question,
    show_waiting,
    show_answer,
    show_statistics,
    show_winners
)

from settings_service import (
    get_timer_seconds,
    set_timer_seconds,
    get_correct_answer_points,
    set_correct_answer_points
)


app = Flask(__name__)


@app.route("/start")
def start():

    show_waiting()

    return redirect("/game")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/display")
def display():

    game = get_current_game()

    current_question = None

    remaining_time = 0

    statistics = {}


    screen = get_display_mode()


    if game["question_id"] is not None:

        current_question = get_current_question()

        remaining_time = get_remaining_time()



    if screen == "statistics":

        statistics = get_answer_statistics()



    if screen == "winner":

        current_question = game



    return render_template(

        "display.html",

        current_game=current_question,

        remaining_time=remaining_time,

        status=screen,

        statistics=statistics,

    	winner_place=game.get("winner_place"),
	
	display_version=get_display_version()

    )


@app.route("/manager")
def manager():
    return render_template("manager.html")

@app.route("/settings")
def settings():

    timer = get_timer_seconds()

    points = get_correct_answer_points()

    return render_template(
        "settings.html",
        timer=timer,
        points=points
    )

@app.route("/save_settings", methods=["POST"])
def save_settings():

    timer = request.form["timer"]

    points = request.form["points"]


    set_timer_seconds(timer)

    set_correct_answer_points(points)


    return redirect("/settings")


# =========================
# Questions
# =========================

@app.route("/questions")
def questions():

    questions = get_all_questions()

    return render_template(
        "questions.html",
        questions=questions
    )


@app.route("/add_question", methods=["GET", "POST"])
def add_question_page():

    if request.method == "POST":

        add_question(
            request.form["question"],
            request.form["answer1"],
            request.form["answer2"],
            request.form["answer3"],
            request.form["answer4"],
            request.form["correct_answer"]
        )

        return redirect("/questions")

    return render_template("add_question.html")


@app.route("/edit_question/<int:question_id>", methods=["GET", "POST"])
def edit_question(question_id):

    if request.method == "POST":

        update_question(
            question_id,
            request.form["question"],
            request.form["answer1"],
            request.form["answer2"],
            request.form["answer3"],
            request.form["answer4"],
            request.form["correct_answer"]
        )

        return redirect("/questions")


    question = get_question_by_id(question_id)

    return render_template(
        "edit_question.html",
        question=question
    )


@app.route("/delete_question/<int:question_id>")
def delete_question_page(question_id):

    delete_question(question_id)

    return redirect("/questions")


# =========================
# Participants
# =========================

@app.route("/participants")
def participants():

    participants = get_all_participants()

    return render_template(
        "participants.html",
        participants=participants
    )


@app.route("/add_participant", methods=["GET", "POST"])
def add_participant_page():

    if request.method == "POST":

        add_participant(
            request.form["name"],
            request.form["phone"]
        )

        return redirect("/participants")


    return render_template("add_participant.html")


@app.route("/edit_participant/<int:participant_id>", methods=["GET", "POST"])
def edit_participant(participant_id):

    if request.method == "POST":

        update_participant(
            participant_id,
            request.form["name"],
            request.form["phone"]
        )

        return redirect("/participants")


    participant = get_participant_by_id(participant_id)

    return render_template(
        "edit_participant.html",
        participant=participant
    )


@app.route("/delete_participant/<int:participant_id>")
def delete_participant_page(participant_id):

    delete_participant(participant_id)

    return redirect("/participants")


# =========================
# Game
# =========================

@app.route("/game")
def game():

    current_game = get_current_game()

    current_question = None
    remaining_time = 0
    answers = []


    if current_game["active"]:

        remaining_time = get_remaining_time()


        if remaining_time > 0:

            current_question = get_current_question()
            answers = get_answers()



    questions = get_all_questions()


    return render_template(
        "game.html",
        questions=questions,
        current_game=current_question,
        remaining_time=remaining_time,
        answers=answers
    )



@app.route("/start_game/<int:question_id>")
def start_game_page(question_id):

    start_game(question_id)

    show_question()

    return redirect("/game")



@app.route("/stop_game")
def stop_game_page():

    stop_game()

    show_waiting()

    return redirect("/game")



@app.route("/test_answer", methods=["POST"])
def test_answer():

    phone = request.form["phone"]
    answer = request.form["answer"]


    submit_answer(
        phone,
        answer
    )


    return redirect("/game")

# =========================
# Display Control
# =========================


@app.route("/display_question")
def display_question():

    show_question()

    return redirect("/manager")



@app.route("/display_answer")
def display_answer():

    show_answer()

    return "", 204



@app.route("/display_waiting")
def display_waiting():

    show_waiting()

    return redirect("/manager")



@app.route("/display_statistics")
def display_statistics():

    show_statistics()

    return "", 204



@app.route("/display_winners")
def display_winners():

    return redirect("/winner_control")

@app.route("/winner_control")
def winner_control():

    return render_template(
        "winner_control.html"
    )

@app.route("/show_winner/<int:place>")
def show_winner(place):

    winners = get_top_participants()


    game = get_current_game()


    if len(winners) >= place:

        game["winner"] = winners[place - 1]


    set_winner_place(place)

    show_winners()


    return redirect("/winner_control")

@app.route("/display_status")
def display_status():

    return jsonify({
        "status": get_display_mode(),
        "version": get_display_version()
    })



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)