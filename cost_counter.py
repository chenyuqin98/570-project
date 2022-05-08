# @Author : Yuqin Chen
# @email : yuqinche@usc.edu
gap_penalty = 30
mismatch_penalty_val = {('A', 'A'):0, ('A', 'C'):110, ('A', 'G'):48, ('A', 'T'):94,
                        ('C', 'A'):110, ('C', 'C'):0, ('C','G'):118, ('C', 'T'):48,
                        ('G', 'A'):48, ('G', 'C'):118, ('G', 'G'):0, ('G', 'T'):110,
                        ('T', 'A'):94, ('T', 'C'):48, ('T', 'G'):110, ('T', 'T'):0}

def compute_cost(s1, s2):
    cost = 0
    for i in range(len(s1)):
        if s1[i] == '_' or s2[i] =='_':
            cost += gap_penalty
        elif s1[i] != s2[i]:
            key = tuple(sorted([s1[i], s2[i]]))
            mismatch_penalty = mismatch_penalty_val[key]
            cost += mismatch_penalty
    return cost

def call_algorithm(s1, s2):
    m, n = len(s1), len(s2)
    matrix = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m+1):
        matrix[i][0] = i * gap_penalty
    for j in range(n+1):
        matrix[0][j] = j * gap_penalty

    # bottom up
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]: matrix[i][j] = matrix[i-1][j-1]
            else:
                key = (s1[i-1], s2[j-1])
                mismatch_penalty = mismatch_penalty_val[key]
                matrix[i][j] = min(matrix[i][j - 1] + gap_penalty,
                                   matrix[i - 1][j] + gap_penalty,
                                   matrix[i - 1][j - 1] + mismatch_penalty)
    # for ma in matrix:
    #     print(ma)
    # top down
    i, j = m, n
    s1_rlt, s2_rlt = '', ''
    while i>0 or j>0:
        # print(i, j, s1_rlt[::-1], s2_rlt[::-1], s1[i - 1], s2[j - 1])
        if matrix[i][j] == matrix[i][j-1]+gap_penalty:
            s1_rlt += '_'
            s2_rlt += s2[j - 1]
            j -= 1
        elif matrix[i][j] == matrix[i-1][j]+gap_penalty:
            s1_rlt += s1[i - 1]
            s2_rlt += '_'
            i -= 1
        else:
            s1_rlt += s1[i - 1]
            s2_rlt += s2[j - 1]
            i -= 1
            j -= 1
    # print(matrix)
    return matrix[-1][-1], s1_rlt[::-1], s2_rlt[::-1]

if __name__=='__main__':
    print(compute_cost('GGACTGACTACTGACT', 'G_AC_G_C____GA_T')+compute_cost('GGTGACTAC_TGACTG_G', '__T_A_TACGCGAC_GCG'))
    print(compute_cost('GGAC_TGACTACTGACT', 'G_ACGCGA_T__T_A_T')+compute_cost('GGTGACTACTGACTG_G', '____AC_GC_GAC_GCG'))
    print(compute_cost('_A_CA_CACT__G__A_C_TAC_TGACTG_GTGA__C_TACTGACTGGACTGACTACTGACTGGTGACTACT_GACTG_G',
                       'TATTATTA_TACGCTATTATACGCGAC_GCG_GACGCGTA_T_AC__G_CT_ATTA_T_AC__GCGAC_GC_GGAC_GCG'))