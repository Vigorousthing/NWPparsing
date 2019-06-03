import threading


class Philosopher(threading.Thread):
    seat_num = 0

    def __init__(self, left, right):
        threading.Thread.__init__(self)
        self.left_fork = left
        self.right_fork = right


a = Philosopher(1,2)
b = Philosopher(1,2)