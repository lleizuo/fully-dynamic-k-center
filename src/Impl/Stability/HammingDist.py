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
    for i in range(0, len(L1)):
        interNum = list(filter(lambda p: p!=0, contingencyT[i]))
        if len(interNum) > 1:
            disagreements += findProductSum(interNum)
    for j in range(0, n):
        interNum = list(filter(lambda p: p!=0, [a[j] for a in contingencyT]))
        if len(interNum) > 1:
            disagreements += findProductSum(interNum)
    return disagreements/(N*(N-1)/2)


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