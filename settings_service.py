timer_seconds = 10

correct_answer_points = 10


def get_timer_seconds():

    return timer_seconds



def set_timer_seconds(seconds):

    global timer_seconds

    timer_seconds = int(seconds)



def get_correct_answer_points():

    return correct_answer_points



def set_correct_answer_points(points):

    global correct_answer_points

    correct_answer_points = int(points)