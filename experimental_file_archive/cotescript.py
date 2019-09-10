
def solution(key, lock):
    num_key_1 = sum([sum(i) for i in key])
    num_lock_0 = 9 - sum([sum(i) for i in lock])
    if num_lock_0 > num_key_1:
        return False

    def add_pad(array):
        new_list = []
        for i in range(3):
            new_list.append([0 for i in 3*len(array)])
        for i in array:
            for j in range(len(array)):
                i.insert(0, 0)
                i.append(0)
            new_list.append(i)
        for i in range(3):
            new_list.append([0 for i in 3*len(array)])
        return new_list

    def right_rotation(key):
        new_list = []
        for i in range(len(key)):
            new_list.append([])
            for j in range(len(key)):
                new_list[i].append(key[len(key) - j][i])
        return new_list

    # def left_rotation(key):
    #     new_list = []
    #     for i in range(3):
    #         new_list.append([])
    #         for j in range(3):
    #             new_list[i].append(key[j][2 - i])
    #     print(new_list)

    def right_move(key):
        new_list = []
        for i, con_key in enumerate(key):
            new_list.append([])
            for j, con in enumerate(con_key):
                if j == 0:
                    new_list[i].append(0)
                else:
                    new_list[i].append(con_key[j - 1])
        return new_list

    def left_move(key):
        new_list = []
        for i, con_key in enumerate(key):
            new_list.append([])
            for j, con in enumerate(con_key):
                if j == len(con_key) - 1:
                    new_list[i].append(0)
                    break
                else:
                    new_list[i].append(con_key[j+1])
        return new_list

    def up_move(key):
        new_list = []
        for i, lst in enumerate(key):
            if i == len(key)-1:
                new_list.append([0 for i in lst])
                break
            new_list.append(key[i + 1])
        return new_list

    def down_move(key):
        new_list = []
        for i, lst in enumerate(key):
            if i == 0:
                new_list.append([0 for i in lst])
                continue
            new_list.append(key[i - 1])
        return new_list

    def success(key, lock):
        success = True
        for i in range(3, 6):
            for j in range(3, 6):
                if key[i][j] + lock[i][j] != 1:
                    success = False
            if success == False:
                return False
        return True

    key = add_pad(key)
    lock = add_pad(lock)

    outcome = False
    if not success(key, lock):
        n_key1 = key
        for i in range(4):
            n_key1 = right_rotation(n_key1)
            if not success(n_key1, lock):
                n_key2 = n_key1
                for i in range(3):
                    n_key2 = up_move(n_key2)
                    if not success(n_key2, lock):
                        n_key3 = n_key2
                        for i in range(3):
                            n_key3 = right_move(n_key3)
                            if not success(n_key3, lock):
                                n_key4 = n_key3
                                for i in range(5):
                                    n_key4 = down_move(n_key4)
                                    if not success(n_key4, lock):
                                        n_key5 = n_key4
                                        for i in range(5):
                                            n_key5 = left_move(n_key5)
                                            if not success(n_key5, lock):
                                                continue
                                            else:
                                                outcome = True
                                    else:
                                        outcome = True
                            else:
                                outcome = True
                    else:
                        outcome = True
            else:
                outcome = True
    else:
        outcome = True

    return outcome


key = [[0, 0, 0], [1, 0, 0], [0, 1, 1]]
lock = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
# lock = [[1, 1, 1], [1, 1, 1], [1, 1, 0]]

# key = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
# lock = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


print(solution(key, lock))




# # 6/28
def solution(text):
    text += " "
    pre_idx = 0
    length = len(text)
    length_dic = {}
    now_chr = ""
    pre_chr = " "

    for k in range(int(length/2 + 1)):
        length_dic[k] = length
        pre_idx = 0
        state_of_new_abbrev = True

        for i, ele in enumerate(text):
            if i == pre_idx + k:
                now_chr = text[pre_idx: i]
                if now_chr == pre_chr:
                    print(now_chr)
                    if state_of_new_abbrev == True:
                        length_dic[k] -= k - 1
                        state_of_new_abbrev = False
                    else:
                        length_dic[k] -= k
                else:
                    state_of_new_abbrev = True
                pre_idx = i
                pre_chr = now_chr

    smallest = 1000
    for i in length_dic:
        if length_dic[i] < smallest:
            smallest = length_dic[i]

    print(length_dic)

    output = smallest - 1
    return output

t1 = "aabbaccc"
t2 = "ababcdcdababcdcd"
t3= "abcabcdede"
t4 = "abcabcabcabcdededededede"
t5 = "xababcdcdababcdcd"
# length : 8/16/10/24/17
# 7/9/8/14/17
print(solution(t5))