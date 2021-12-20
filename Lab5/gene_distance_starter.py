# Project 5: starter code
# Edit distance between gene sequences

# Please read this function comments to correctly define your gene_edit function's output 
# Don't change this function
def display_results(dist, steps):
    '''
    Display the results after computing the edit distance.
    Inputs:
        dist: the edit distance
        steps: a list of tuples. Each tuple represents a step to turn the source
        gene into the target gene. Each tuple is formatted as:
        ((source_base_letter, target_base_letter), operation)
        , where possible values for the source_base_letter and target_base_letter
        are 'A', 'C', 'G' and 'T', possible values for the operation field is 
        0 (keeping), 1 (substitution), 2 (insertion) and 3 (deletion)
    Printout:
        The edit distance between the two gene sequences
        The number of steps to convert the source into the target gene
        The steps.
    '''
    print("The edit distance is ", dist)
    print("The number of steps to turn the source into the target gene:", len(steps))
    for item in steps:
        if item[1]==0: #match, keeping operation
            print("Keep "+str(item[0][0])+" unchanged")
        elif item[1]==1: #no match, substitute
            print("Substitute "+str(item[0][1])+" for "+str(item[0][0]))
        elif item[1]==2: #insertion
            print("Insert "+str(item[0][1]))
        elif item[1]==3: #deletion
            print("Delete "+str(item[0][0]))    

# Please complete this function
def gene_edit(s, t):
    '''
    Compute the edit distance between two gene sequences (source s and target t)
    using the iterative approach from dynamic programming.
    Inputs:
      s: source gene sequence - a list of DNA base letters from (A, C, G, T)
      t: target gene sequence - a list of DNA base letters from (A, C, G, T)
    Output:
      dist: the edit distance between the source and the target sequences
      steps: the steps to convert the source into the target sequence
      (note: refer to display_results function's comments for the format of steps)

       ((source_base_letter, target_base_letter), operation)
        0 (keeping), 1 (substitution), 2 (insertion) and 3 (deletion)
    '''
    # replace the following three lines with your own code
    dist = 0
    steps = []


    s = [" "] + s
    t = [" "] + t
    cost = [[None for x in range(len(s))] for y in range(len(t))] # initialize 2d array with None values
    
    for j in range(len(t)):# Fill first row with ascending insertions 
        cost[0][j] = (2, j)
    for i in range(1,len(s)): # Fill first column with ascending deletions
        cost[i][0] = (3, i)
    
    #edit distance algorithm start 
    for i in range(1,len(s)):
        for j in range(1,len(t)):
            keeping = True
            if s[i] == t[j]: c_match = cost[i-1][j-1][1]
            else:  
                c_match = cost[i-1][j-1][1] + 1
                keeping = False #var to check if we are keeping this letter 
            
            c_ins = cost[i][j-1][1] + 1
            c_del = cost[i-1][j][1] + 1
            c_min = min(c_match, c_ins, c_del)
            # determine which operation was most optimal

            if c_min == c_match: # Check which operation was taken in the steps above. 
                if keeping: cost[i][j] = (0, c_min)
                else: cost[i][j] = (1, c_min)
            elif c_min == c_ins:
                cost[i][j] = (2, c_min)
            else:
                cost[i][j] = (3, c_min) #end of edit distance. 
    
    dist = cost[i][j][1] #grab final distance 
    #trace back to determine steps
    while (i,j) != (0,0): # will always return to the origin 
        curr = cost[i][j]
        step = curr[0] # grab step for comparison 
        steps.append(((s[i],t[j]),step))
        if step == 0 or step == 1: # check step and alter i,j indexes appropiately 
            i = i-1
            j = j-1
        elif step == 2:
            j = j-1
        elif step == 3:
            i = i-1 #end trace back. 
    
    return dist, steps

# Please complete this function
def closest_genes(geneList):
    '''
    Find two genes in the geneLists with the minimum edit distance.
    Inputs:
        A list of gene sequences
    Outputs:
        A tuple consisting three elements (e1, e2, e3)
            e1 - the minimum edit distance among all the pairs of genes
            e2 and e3 - the index of the two genes with the minimum edit distance
    Hint:
        Call your gene_edit function here 
    '''
    distances = []
    for i in range(len(geneList)):
        for j in range(1,len(geneList)):
            if i >= j: continue #prevents duplicate pairs 
            distances.append(((i,j), gene_edit(geneList[i], geneList[j])[0])) # stores distances as ((index of gene1, index of gene2), distance value )

    minVal = distances[0] #initializes minimum with first item in list
    for i in range(1,len(distances)):
        if minVal[1] > distances[i][1]: #compares each consecutive gene distance to determine minimum 
            minVal = distances[i]
    
    e1 = minVal[1]
    e2 = minVal[0][0]
    e3 = minVal[0][1]

    return e1, e2, e3

# Follow each part in the main script to test your functions
# Don't change any statements in the main script! 
if __name__ == "__main__":
    # part 1.0: verify the correctness
    # workout the edit distance and edits between seq1 and seq2, and between seq3
    # and seq4 manually, then verify if your code is able to find the same results
    seq1 = ['A', 'G', 'T', 'C']
    seq2 = ['G', 'C', 'C', 'A'] 
    seq3 = ['A', 'G', 'C', 'T', 'A', 'T', 'T', 'C']
    seq4 = ['G', 'T', 'T', 'C', 'A', 'A', 'C', 'G']
    _dist12, _steps12 = gene_edit(seq1, seq2)
    display_results(_dist12, _steps12)
    _dist34, _steps34 = gene_edit(seq3, seq4)
    display_results(_dist34, _steps34)

    # part 1.5: switch the source and target, observe the resulting edit distance
    # and edits.
    # Notice any similarities/differences compared with part 1.0? What are they? 
    _dist21, _steps21 = gene_edit(seq2, seq1)
    display_results(_dist21, _steps21)
    _dist43, _steps43 = gene_edit(seq4, seq3)
    display_results(_dist43, _steps43)

    

    # part 2.0: given ten random gene sequences, identify two sequences that are 
    # closest to each other in terms of edit distance
    # Note: the comparison between part 1.0 and 1.5 will help reduce the number
    # of source-target pairs that need to be examined
    tenGenes = []
    import random
    for i in range(10): tenGenes.append(random.choices(['A','C','G','T'], k=50))
    minDist, id1, id2 = closest_genes(tenGenes)
    print("The minimum edit distance is", minDist)
    print("The two genes with the minimum edit distance are gene %d and gene %d" %(id1, id2))