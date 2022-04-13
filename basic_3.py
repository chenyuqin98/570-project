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

def call_algorithm():
    m, n = len(s1), len(s2)
    # matrix = [[float('inf')]*(n+1) for _ in range(m+1)]
    # for i in range(m+1):
    #     matrix[i][0] = 0
    # for j in range(n+1):
    #     matrix[0][j] = 0
    matrix = [[0] * (n + 1) for _ in range(m + 1)]
    # bottom up
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                matrix[i][j] = matrix[i-1][j-1]
            else:
                key = tuple(sorted([s1[i-1], s2[j-1]]))
                mismatch_penalty = mismatch_penalty_val[key]
                matrix[i][j] = min(matrix[i][j-1]+gap_penalty,
                                   matrix[i-1][j]+gap_penalty,
                                   matrix[i-1][j-1]+mismatch_penalty)
    # return matrix[-1] # for test
    # top down
    i, j = m, n
    common = ''
    while i>0 and j>0:
        # print(i, j)
        if s1[i-1]==s2[j-1]:
            common += s1[i-1]
            i -= 1
            j -= 1
        elif matrix[i][j] == matrix[i][j-1]+gap_penalty:
            j -= 1
        elif matrix[i][j] == matrix[i-1][j]+gap_penalty:
            i -= 1
        else:
            i -= 1
            j -= 1
    return common[::-1]


if __name__=='__main__':
    s1, s2 = generate()
    # cost = call_algorithm()
    # print(cost)
    common = call_algorithm()
    print(common, len(common))