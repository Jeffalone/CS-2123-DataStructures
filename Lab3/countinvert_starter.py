# Project 3: counting inversions with divide-and-conquer

import random
import time

# input: two sorted arrays L and R
# return: a tuple with two components (T, sc)
# T: the sorted array merging L and R
# sc: the number of split inversions between L and R 
def mergeAndCountSplitInv(L, R):
    T = [] # T is the combined list. Don't change this line
    sc = 0 # sc is the number of split inversions. Don't change this line
    ''' add your code here '''
    i = 1
    j = 1
    
    while i < len(L) and j < len(R):

        if L[i] <= R[j]:
            T.append(L[i])
            i += 1

        else:
            T.append(R[j])
            j += 1
            sc += len(L[i:])
            
    T.append(L[i:])
    T.append(R[j:])
    return T, sc # Don't change this line    

# input: an unordered array A
# return: a tuple with two components (component 1, component 2)
# component 1: the ordered array 
# component 2: the count of inversions in A
# Note: this function will be recursive and will invoke mergeAndCountSplitInv()
def sortAndCountInv(A):
    ''' add your code here '''  
    if len(A) == 0 or len(A) == 1:
        return (A, 0)
    else:
        mid = len(A)//2
        L, leftInv =  sortAndCountInv(A[:mid])
        R, rightInv = sortAndCountInv(A[mid:])
        T, splitInv = mergeAndCountSplitInv(L,R)
        return (T, leftInv + rightInv + splitInv)

# brute-force inversion counting
# Don't change this function
def bfInv(A):
    k = 0
    for i in range(0,len(A)-1):
        for j in range(i+1, len(A)):
            if A[i]>A[j]: k = k + 1
    return k

# Suppose list X provides a correct ascending order of its elements 
# find the inversion in list Y compared with list X
# Note: this function must invoke your sortAndCountInv() function
def findInv(X, Y):
    rank = 0
    songToRank = {}
    for i in X:
        songToRank[i] = rank
        rank += 1
    
    list = []
    for i in X:
        list.append(songToRank[i])
        
    for j in Y:
        list.append(songToRank[i])

    return sortAndCountInv(list)
   

if __name__ == "__main__":
    # part1: test the correctness
    Ain1 = [5,4,3,2,1]
    Aout1, tc1 = sortAndCountInv(Ain1)
    print(Aout1)
    print(tc1)
    print(bfInv(Ain1))
    
    # part2: compare the performance between divide-and-conquer and brute-force algorithms
    Ain2 = random.sample(range(50000), 10000) # create a random input list
    t1 = time.time()
    Aout2, tc2 = sortAndCountInv(Ain2) # counting inversions with the divide-and-conquer algorithm
    t2 = time.time()
    bfc2 = bfInv(Ain2) # counting inversions with the brute-force algorithm
    t3 = time.time()
    print("Number of inversions found by the divide-and-conquer algorithm:", tc2)
    print("Number of inversions found by the brute-force algorithm:", bfc2)
    print("Running time of the divide-and-conquer algorithm:", t2-t1, "seconds")
    print("Running time of the brute-force algorithm:", t3-t2, "seconds")
    
    # part3: solve a practical problem
    # suppose listX provides a correct ascending order of songs, find the number of inversions in listY
    listX = ['songA', 'songB', 'songC', 'songD', 'songE', 'songF', 'songG', 'songH' ]
    listY = ['songH', 'songC', 'songA', 'songD', 'songG', 'songF', 'songE', 'songB' ]
    nInv = findInv(listX, listY)[1]
    print("The number of inversions in list Y compared with list X is", nInv)