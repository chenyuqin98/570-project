# @Author : Yuqin Chen
# @email : yuqinche@usc.edu

import sys
# from resource import *
import time
import psutil

input_file = sys.argv[1]
output_file = sys.argv[2]
gap_penalty = 30
mismatch_penalty_val = {('A','C'):110, ('A','G'):48, ('A','T'):94,
                        ('C','G'):118, ('C','T'):48,
                        ('G','T'):110}

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

def split_s(s, pos = -1):
    if pos == -1: # default to split in the mid
        pos = len(s)//2
    return s[:pos], s[pos:]

def call_algorithm(s1, s2):
    cost = dp(s1, s2)[-1]
    divide_conquer(s1, 0, s2, 0)
    return cost, rlt1, rlt2
    # return cost, s1_rlt, s2_rlt

def divide_conquer(s1, s1_start, s2, s2_start):
    # 需要处理终止条件，若len（s1）为0则将对应的s2替换为'_'，s2亦然
    if len(s1) == 0:
        print(s1, s1_start, s2, s2_start)
        global rlt2
        rlt2 = rlt2[:s2_start] + '_' * len(s2) + rlt2[s2_start + len(s2):]
        print('rlt2', rlt2)
        return
    if len(s2) == 0:
        print(s1, s1_start, s2, s2_start)
        global rlt1
        rlt1 = rlt1[:s1_start] + '_' * len(s1) + rlt1[s1_start + len(s1):]
        print('rlt1', rlt1)
        return
    if s1 == s2:
        return
    s1_1, s1_2 = split_s(s1)
    cost1 = dp(s1_1, s2)
    # cost2 = dp(s1_2[::-1], s2[::-1])[::-1]
    # cost = [cost1[i]+cost2[i] for i in range(len(cost1))] # 也可能是只用cost1？不确定是不是要加起来！
    cost = cost1
    best_pos = cost.index(min(cost)) + 1

    s2_1, s2_2 = split_s(s2, best_pos)
    divide_conquer(s1_1, s1_start, s2_1, s2_start)
    divide_conquer(s1_2, s1_start + len(s1_1), s2_2, s2_start + len(s2_1))

def dp(s1, s2):
    m, n = len(s1), len(s2)

    pre_row = [0] * (n + 1)
    for j in range(n + 1):
        pre_row[j] = j * gap_penalty

    for i in range(1, m + 1):
        new_row = [0] * (n + 1)
        new_row[0] = i * gap_penalty
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                new_row[j] = pre_row[j - 1]
            else:
                key = tuple(sorted([s1[i - 1], s2[j - 1]]))
                mismatch_penalty = mismatch_penalty_val[key]
                new_row[j] = min(new_row[j - 1] + gap_penalty, pre_row[j] + gap_penalty,
                                 pre_row[j - 1] + mismatch_penalty)
        pre_row = new_row
    cost = pre_row[1:]

    return cost

def compute_score(s1, s2):
    return 0

if __name__=='__main__':
    s1, s2 = generate()
    rlt1, rlt2 = s1, s2

    final_rlt = call_algorithm(s1, s2)
    print(final_rlt)

    # debug:
    # s1_1, s1_2 = split_s(s1)
    # cost1 = dp(s1_1, s2)
    # cost2 = dp(s1_2[::-1], s2[::-1])[::-1]
    # cost = [cost1[i] + cost2[i] for i in range(len(cost1))]
    # best_pos = cost.index(min(cost)) + 1
    # print(s1_1, s2[:best_pos])