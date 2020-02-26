from typing import List
def hammingDist(L1:List[set], L2:List[set]):    # clustering1, clustering2, number of points
    m = len(L1)
    n = len(L2)
    N = sum(len(s) for s in L1)
    contingencyT : List[list] = []
    for i in range(0, m):
        r : List[int] = []
        for j in range(0, n):
            r.append(len(L1[i].intersection(L2[j])))
        contingencyT.append(r)
    disagreements = 0
    for i in range(0, m):
        interNum = list(filter(lambda p: p!=0, contingencyT[i]))
        if len(interNum) > 1:
            disagreements += findProductSum(interNum)
    for j in range(0, n):
        interNum = list(filter(lambda p: p!=0, [a[j] for a in contingencyT]))
        if len(interNum) > 1:
            disagreements += findProductSum(interNum)
    return disagreements/(N*(N-1)/2)

def ari(L1:List[set], L2:List[set]):
    m = len(L1)
    n = len(L2)
    N = sum(len(s) for s in L1)
    contingencyT : List[list] = []
    for i in range(0, m):
        r : List[int] = []
        for j in range(0,n):
            r.append(len(L1[i].intersection(L2[j])))
        contingencyT.append(r)
    N00 = 0     # in different cluster in both U and V
    N01 = 0     # in different cluster in U, same cluster in V
    N10 = 0     # in same cluster in U, different cluster in V
    N11 = 0     # in same cluster in both U and V
    for i in range(0, m):
        interNum = list(filter(lambda p: p!=0, contingencyT[i]))
        if len(interNum) > 1:
            N10 += findProductSum(interNum)
    for j in range(0, n):
        interNum = list(filter(lambda p: p!=0, [r[j] for r in contingencyT]))
        if len(interNum) > 1:
            N01 += findProductSum(interNum)
    for i in range(0,m):
        for j in range(0,n):
            N11 += contingencyT[i][j]*(contingencyT[i][j]-1)/2
    N00 = N*(N-1)/2 - N01 - N10 - N11
    # return (N00, N11, N10, N01)
    
    return 2*(N00*N11-N01*N10)/((N00+N01)*(N01+N11) + (N00+N10)*(N10+N11))

def findProductSum(A):
    n = len(A)
    array_sum = 0
    for i in range(0, n): 
        array_sum = array_sum + A[i] 
    array_sum_square = array_sum * array_sum 
    individual_square_sum = 0
    for i in range(0, n, 1): 
        individual_square_sum += A[i] * A[i] 
    return (array_sum_square - individual_square_sum) / 2