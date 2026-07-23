display_mode = "waiting"

display_version = 0




def set_display_mode(mode):

    global display_mode
    global display_version

    display_mode = mode
    display_version += 1


def get_display_mode():
    """
    מחזיר את מצב התצוגה הנוכחי.
    """
    return display_mode

def get_display_version():
    return display_version


def show_waiting():
    set_display_mode("waiting")


def show_question():
    set_display_mode("question")


def show_answer():
    set_display_mode("answer")


def show_statistics():
    set_display_mode("statistics")


def show_winners():
    set_display_mode("winner")