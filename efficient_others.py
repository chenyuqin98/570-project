import time
import psutil
import sys

alpha_dict = {'AA': 0, 'AC': 110, 'AG': 48, 'AT': 94,
              'CA': 110, 'CC': 0, 'CG': 118, 'CT': 48,
              'GA': 48, 'GC': 118, 'GG': 0, 'GT': 110,
              'TA': 94, 'TC': 48, 'TG': 110, 'TT': 0}
delta = 30

def main():
    outpath = './out1.txt'

    inpath = './SampleTestCases/input1.txt'
    x, y = generate_input(inpath)
    # print(x+"\n"+y+"\n")
    x_al, y_al, score, tdif,kb_used = sequenceAlignment(x, y)

    f = open(outpath,"w")
    s = str(score) + "\n" + x_al + "\n" + y_al + "\n" + tdif + "\n" + kb_used
    f.write(s)
    # print(s) # delete/comment me before submission
    f.close()


def Xtohalves(X):
    xlen = len(X)
    split = int(xlen / 2)
    if xlen % 2 == 1:
        split = split + 1

    xl = X[0:split]
    xr = X[split:xlen]
    return xl, xr, split

def getFinalColXr(xr,y):
    revxr = xr[::-1]
    revy = y[::-1]
    return getFinalColXl(revxr,revy)[::-1]


def getFinalColXl(xl,y): # final column of x & y matrix (of naive implementation)
    n = len(y)
    m = len(xl)
    c1 = [int(i*delta) for i in range(n+1)] # left col of our sliding window
    c2 = [int(0) for j in range(n+1)]       # right col of our sliding window
    c2[0] = 30

    for i in range(1,m+1): # move horizontally
        c2[0] = delta * (i)
        for j in range(1,n+1): # move up the col
            charpair = (xl[i-1]+ y[j-1]).upper()
            # opt of         align x_i and y_j            add a gap in Y over xi          add a gap in xl over Yi
            c2[j] = min(c1[j-1]+alpha_dict.get(charpair), delta + c2[j-1],              delta + c1[j])

        # slide window one over
        for j in range(n + 1):
            c1[j] = c2[j]
    return c2

def findOptSplit(xl,xr,y):
    n = len(y)
    xl_splitcost = getFinalColXl(xl,y)
    xr_splitcost = getFinalColXr(xr,y)

    mincost = xl_splitcost[0] + xr_splitcost[0]
    argmin = 0
    for i in range(1,n+1):
        if xl_splitcost[i]+xr_splitcost[i] < mincost:
            mincost = xl_splitcost[i]+xr_splitcost[i]
            argmin = i

    return argmin

def sequenceAlignment(X, Y):
    tstart = time.time()
    xl, xr, split = Xtohalves(X)
    xL_len = len(xl)
    xR_len = len(xr)
    xlen = xL_len + xR_len
    ylen = len(Y)

    topYL = findOptSplit(xl,xr,Y)
    yl = Y[:topYL]
    yr = Y[topYL:]
    yL_len = len(yl)
    yR_len = len(yr)

    x_align_left = ''
    y_align_left = ''
    x_align_right = ''
    y_align_right = ''

    score_left = 0
    score_right = 0

    if xL_len < 2 or yL_len < 2:
        x_align_left,y_align_left,score_left = naiveAlignment(xl,yl)
    else:
        x_align_left,y_align_left,score_left,tdif_dummy, kb_used_dummy = sequenceAlignment(xl,yl)

    if xR_len < 2 or yR_len < 2:
        x_align_right,y_align_right,score_right = naiveAlignment(xr,yr)
    else:
        x_align_right,y_align_right,score_right,tdif_dummy, kb_used_dummy = sequenceAlignment(xr,yr)

    x_aligned = x_align_left + x_align_right
    y_aligned = y_align_left + y_align_right
    score = score_left + score_right
    tfin = time.time();
    tdif = str(1.0 * (tfin - tstart) * 1000)

    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed= int(memory_info.rss/1024)

    return x_aligned,y_aligned,score, tdif, str(memory_consumed)

def naiveAlignment(X,Y):
    m = len(X)
    n = len(Y)
    A = [[0 for i in range(n+1)] for j in range(m+1)] # np.zeros((m + 1, n + 1)) #

    for i in range(0, m + 1):
        A[i][0] = delta * i

    for j in range(0, n + 1):
        A[0][j] = delta * j

    for j in range(1, n+1):
        for i in range(1, m+1):
            alphapair = 0
            try:
                alphapair = X[i-1] + Y[j-1]
            except:
                print("An error occurred with (i = " + str(i) + ", j = " + str(j) + ")")
            # these are just used for debugging; the next 6 lines could be deleted and everything works fine
            match_xy = alpha_dict.get(alphapair) + A[i-1][j-1]
            unmatchX = delta + A[i-1][j]
            unmatchY = delta + A[i][j-1]
            a_im1_jm1 = A[i-1][j-1]
            a_im1_j = A[i - 1][j]
            a_i_jm1 = A[i][j - 1]
            A[i][j] = min(alpha_dict.get(alphapair) + A[i - 1][j - 1], delta + A[i - 1][j], delta + A[i][j - 1])

    i = m
    j = n

    alphapair = "" # also for debugging

    x_align = ""
    y_align = ""
    while i != 0 and j != 0:
        alphapair = X[i-1] + Y[j-1]
        if A[i][j] == (A[i - 1][j - 1] + alpha_dict.get(alphapair)):
            x_align = X[i-1] + x_align
            y_align = Y[j-1] + y_align
            i = i - 1
            j = j - 1

        elif A[i][j] == (A[i][j-1] + delta):
            x_align = '_' + x_align
            y_align = Y[j-1] + y_align
            j = j - 1

        elif A[i][j] == (A[i - 1][j] + delta):
            x_align = X[i-1] + x_align
            y_align = '_' + y_align
            i = i - 1

        else:
            print("Error! at (i = " + str(i) + ", j = " + str(j) + ")")

    while i != 0: # gaps on y's
        x_align = X[i - 1] + x_align
        y_align = '_' + y_align
        i = i - 1

    while j != 0: # gaps on x's
        x_align = '_' + x_align
        y_align = Y[j - 1] + y_align
        j = j - 1

    score = A[m][n]
    return x_align, y_align, score


def generate_input(inpath):
    all_inputs = read_inputs(inpath)
    x_str = all_inputs[0]

    y_idx = 0
    idx = 0
    for i in range(1, len(all_inputs)):
        if type(all_inputs[i]) == int:
            idx = all_inputs[i] + 1
            base = x_str
            x_str = base[0:idx] + base + base[idx:]
        else:
            y_idx = i
            break

    y_str = all_inputs[y_idx]

    for i in range(y_idx + 1, len(all_inputs)):
        idx = all_inputs[i]+1
        base = y_str
        y_str = base[0:idx] + base + base[idx:]

    return x_str, y_str


def read_inputs(inpath):
    file = open(inpath, 'r')
    mixed_list = []
    while True:
        next_line = file.readline().strip()
        if not next_line:
            break
        if next_line.isnumeric():
            mixed_list.append(int(next_line))
        else:
            mixed_list.append(next_line)
    file.close()

    return mixed_list


if __name__ == '__main__':
    main()