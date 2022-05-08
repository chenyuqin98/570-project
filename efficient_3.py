# @Author : Yuqin Chen
# @email : yuqinche@usc.edu

import sys
# from resource import *
import time
import psutil

input_file = sys.argv[1]
output_file = sys.argv[2]
gap_penalty = 30
mismatch_penalty_val = {('A', 'A'):0, ('A', 'C'):110, ('A', 'G'):48, ('A', 'T'):94,
                        ('C', 'A'):110, ('C', 'C'):0, ('C','G'):118, ('C', 'T'):48,
                        ('G', 'A'):48, ('G', 'C'):118, ('G', 'G'):0, ('G', 'T'):110,
                        ('T', 'A'):94, ('T', 'C'):48, ('T', 'G'):110, ('T', 'T'):0}

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def time_wrapper():
    start_time = time.time()
    call_algorithm()
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    return time_taken

def insert(pos, str):
    curr_s = str
    s1_li = list(str)
    s1_li.insert(pos, curr_s)
    str = ''.join(s1_li)
    return str

def generate():
    s1 = ''
    s2 = ''
    which_s = 0
    with open(input_file) as f:
        for l in f.readlines():
            l = l.strip('\n')
            # break
            if l.isalpha():
                # print(11111)
                if which_s == 0:
                    s1 += l
                    which_s += 1
                else:
                    s2 += l
                    which_s += 1
            elif l.isdigit():
                pos = int(l) + 1
                if which_s == 1:
                    s1 = insert(pos, s1)
                elif which_s == 2:
                    s2 = insert(pos, s2)
            # print(l, len(s1), len(s2), 'show current s: ', s1, s2)
    return s1, s2

def call_algorithm(s1, s2):
    cost = dp(s1, s2)[-1]
    rlt1, rlt2 = divide_conquer(s1, s2)
    return cost, rlt1, rlt2

def split_s(s, pos = -1):
    if pos == -1: # default to split in the mid
        pos = len(s)//2
    return s[:pos], s[pos:]

def basic_dp(s1, s2):
    m, n = len(s1), len(s2)
    matrix = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        matrix[i][0] = i * gap_penalty
    for j in range(n + 1):
        matrix[0][j] = j * gap_penalty

    # bottom up
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            key = (s1[i - 1], s2[j - 1])
            mismatch_penalty = mismatch_penalty_val[key]
            matrix[i][j] = min(matrix[i][j - 1] + gap_penalty,
                               matrix[i - 1][j] + gap_penalty,
                               matrix[i - 1][j - 1] + mismatch_penalty)
    # top down
    i, j = m, n
    s1_rlt, s2_rlt = '', ''
    while i > 0 or j > 0:
        if matrix[i][j] == matrix[i][j - 1] + gap_penalty:
            s1_rlt += '_'
            s2_rlt += s2[j - 1]
            j -= 1
        elif matrix[i][j] == matrix[i - 1][j] + gap_penalty:
            s1_rlt += s1[i - 1]
            s2_rlt += '_'
            i -= 1
        else:
            s1_rlt += s1[i - 1]
            s2_rlt += s2[j - 1]
            i -= 1
            j -= 1
    s1_rlt, s2_rlt = s1_rlt[::-1], s2_rlt[::-1]
    return s1_rlt, s2_rlt

def divide_conquer(s1, s2):
    s1_1, s1_2 = split_s(s1)
    cost1 = dp(s1_1, s2)
    cost2 = dp(s1_2[::-1], s2[::-1])[::-1]
    cost = [cost1[i]+cost2[i] for i in range(len(cost1))]
    best_pos = cost.index(min(cost)) + 1
    best_pos = len(cost) - cost[::-1].index(min(cost))
    # print(cost, best_pos, '-----s1_1, s2_1: ', s1_1, s2[:best_pos], '\n')

    mincost = cost1[0] + cost2[0]
    best_pos = 0
    # print(len(cost1), len(s2))
    for i in range(1, len(s2) + 1):
        if cost1[i] + cost2[i] < mincost:
            mincost = cost1[i] + cost2[i]
            best_pos = i

    s2_1, s2_2 = split_s(s2, best_pos)

    if len(s1_1) <= 1 or len(s2_1) <= 1:
        s1_rlt_1, s2_rlt_1 = basic_dp(s1_1, s2_1)
    else:
        s1_rlt_1, s2_rlt_1 = divide_conquer(s1_1, s2_1)
    if len(s1_2) <= 1 or len(s2_2) <= 1:
        s1_rlt_2, s2_rlt_2 = basic_dp(s1_2, s2_2)
    else:
        s1_rlt_2, s2_rlt_2 = divide_conquer(s1_2, s2_2)
    return s1_rlt_1+s1_rlt_2, s2_rlt_1+s2_rlt_2

def dp(s1, s2):
    m, n = len(s1), len(s2)

    pre_row = [0] * (n + 1)
    for j in range(n + 1):
        pre_row[j] = j * gap_penalty

    for i in range(1, m + 1):
        new_row = [0] * (n + 1)
        new_row[0] = i * gap_penalty
        for j in range(1, n + 1):
            key = (s1[i - 1], s2[j - 1])
            mismatch_penalty = mismatch_penalty_val[key]
            new_row[j] = min(new_row[j - 1] + gap_penalty, pre_row[j] + gap_penalty,
                             pre_row[j - 1] + mismatch_penalty)
        pre_row = new_row
    cost = pre_row

    return cost

def compute_cost(s1, s2):
    cost = 0
    for i in range(len(s1)):
        if s1[i] == '_' or s2[i] =='_':
            cost += gap_penalty
        elif s1[i] != s2[i]:
            # print('mismatch', s1[i], s2[i])
            key = tuple(sorted([s1[i], s2[i]]))
            mismatch_penalty = mismatch_penalty_val[key]
            cost += mismatch_penalty
    return cost

if __name__=='__main__':
    s1, s2 = generate()
    rlt1, rlt2 = s1, s2
    replace_s1, replace_s2 = [], []

    final_rlt = call_algorithm(s1, s2)
    print('cost : ',  final_rlt[0])
    print('final_rlt of s1 and s2: ')
    print(final_rlt[1])
    print(final_rlt[2])
    print('test cost: ', compute_cost(final_rlt[1], final_rlt[2]))

    # debug:
    # s1_1, s1_2 = split_s(s1)
    # cost1 = dp(s1_1, s2)
    # cost2 = dp(s1_2[::-1], s2[::-1])[::-1]
    # cost = [cost1[i] + cost2[i] for i in range(len(cost1))]
    # print(cost)
    # best_pos = cost.index(min(cost)) + 1
    # print(s1_1, s2[:best_pos])