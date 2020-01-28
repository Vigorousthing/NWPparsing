
import sklearn




given_number = int(input())
test_list = []

for i in range(given_number):
    test_list.append(int(input()))

output_list = [0] * given_number
output_list[0] = 0
output_list[1] = 1
output_list[2] = 2
output_list[3] = 4


def solution(given_number):
    for num in range(4, given_number):
        a = output_list[num-3]
        b = output_list[num-2]
        c = output_list[num-1]
        output_list[num] = a + b + c
    return output_list



