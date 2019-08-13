import threading
import time
import random


class Philosopher(threading.Thread):
    seat_num = 0

    def __init__(self, name):
        super(Philosopher, self).__init__()
        print("our philosopher has sat down at the table")
        # threading.Thread.__init__(self)
        self.name = name
        # super(Philosopher, self).__init__()
        Philosopher.seat_num += 1
        self.left_fork = None
        self.right_fork = None
        self.player_num = Philosopher.seat_num

    def run(self):
        while True:
            print("philosopher: {} has started thinking".format(self.name))
            time.sleep(random.randint(1, 5))
            print("philosopher {} has finished thinking".format(self.name))
            while True:
                self.left_fork.acquire(self.name)
                if self.left_fork.belong_to == self.name:
                    while True:
                        self.right_fork.acquire(self.name)
                        if self.right_fork.belong_to == self.name:
                            print("philosopher {} has attained both forks, currently eating".format(self.name))
                            time.sleep(random.randint(3, 5))
                            self.right_fork.release(self.name)
                            print("philosopher {} has released the right fork".format(self.name))
                            break
                        else:
                            continue
                    self.left_fork.release(self.name)
                    print("philosopher {} has released the left fork".format(self.name))
                    break
                else:
                    continue

            # try:
            #     self.left_fork.acquire(self.name)
            #     print("philosopher {} has acquired the left fork".format(self.name))
            #     try:
            #         self.right_fork.acquire(self.name)
            #         print("philosopher {} has attained both forks, currently eating".format(self.name))
            #     finally:
            #         self.right_fork.release(self.name)
            #         print("philosopher {} has released the right fork".format(self.name))
            # finally:
            #     self.left_fork.release(self.name)
            #     print("philosopher {} has released the left fork".format(self.name))

    def set_fork(self, fork_list):
        self.right_fork = fork_list[self.player_num-1]
        self.left_fork = fork_list[self.player_num % len(fork_list)]
    # def whats_your_name(self, a):
    #     while True:
    #         print(threading.current_thread().getName())
    #         print(a)


class Fork:
    def __init__(self, fork_name):
        self.fork_name = fork_name
        self.belong_to = None

    def acquire(self, name):
        if self.belong_to is None:
            self.belong_to = name
        else:
            # print("it's someone else's")
            pass

    def release(self, name):
        if self.belong_to == name:
            self.belong_to = None
        else:
            # print("it's not your fork")
            pass

name_list = ["Plato", "Aristotle", "Descartes", "Kant", "Heidegger"]
player_list = []
for name in name_list:
    player_list.append(Philosopher(name))

fork_list = []
for i in range(Philosopher.seat_num):
    fork_list.append(Fork(i+1))

for i in range(len(name_list)):
    player_list[i].set_fork(fork_list)

# run
for player in player_list:
    player.start()

