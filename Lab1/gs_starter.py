def gs(men, women, pref):
    """
    Original Gale-shapley algorithm
    Inputs: men (list of men's names)
            women (list of women's names)
            pref (dictionary of preferences mapping names to list of preferred names in sorted order)
    Output: dictionary of stable matches
    """
    # preprocessing
    ## build the rank dictionary
    rank = {}
    for w in women:
        rank[w] = {}
        i = 1
        for m in pref[w]:
            rank[w][m] = i
            i += 1
    ## create a "pointer" to the next woman to propose
    prefptr = {}
    for m in men:
        prefptr[m] = 0

    freemen = set(men)  # initially all men and women are free
    numpartners = len(men)
    S = {}  # build dictionary to store engagements

    # run the algorithm
    while freemen:
        m = freemen.pop()
        # get the highest ranked woman that has not yet been proposed to
        w = pref[m][prefptr[m]]
        prefptr[m] += 1
        if w not in S:
            S[w] = m
        else:
            mprime = S[w]
            if rank[w][m] < rank[w][mprime]:
                S[w] = m
                freemen.add(mprime)
            else:
                freemen.add(m)
    return S


def gs_block(men, women, pref, blocked):
    """
    Gale-shapley algorithm, modified to exclude unacceptable matches
    Inputs: men (list of men's names)
            women (list of women's names)
            pref (dictionary of preferences mapping names to list of preferred names in sorted order)
            blocked (list of (man,woman) tuples that are unacceptable matches)
    Output: dictionary of stable matches
    """
    # preprocessing
    ## build the rank dictionary
    rank = {}
    for w in women:
        rank[w] = {}
        i = 1
        for m in pref[w]:
            rank[w][m] = i
            i += 1

    ## create a "pointer" to the next woman to propose
    prefptr = {}
    for m in men:
        prefptr[m] = 0

    freemen = set(men)  # initially all men and women are free
    numpartners = len(men)
    S = {}  # build dictionary to store engagements

    # run the algorithm
    while freemen:
        m = freemen.pop()
        # get the highest ranked woman that has not yet been proposed to
        w = pref[m][prefptr[m]]
        prefptr[m] += 1

        if not (m, w) in blocked:  # checks if pair is blocked before recording it
            if w not in S:
                S[w] = m
            else:
                mprime = S[w]
                if rank[w][m] < rank[w][mprime]:
                    S[w] = m
                    freemen.add(mprime)
                else:
                    freemen.add(m)

        else:
            if not prefptr[m] == len(pref[m]):  # if pairing is failed because of a blocked pair this ensures
                freemen.add(m)  # that the rest of the m's pairing list is considered

    return S


def gs_tie(men, women, preftie):
    # preprocessing
    ## build the rank dictionary
    rank = {}
    for w in women:
        rank[w] = {}
        i = 1
        for sets in preftie[w]: # gives each person in same ranking set the same number ranking../
            for m in sets:
                rank[w][m] = i
            i += 1

    ## create a "pointer" to the next woman to propose
    prefptr = {}
    for m in men:
        prefptr[m] = 0

    freemen = set(men)  # initially all men and women are free
    numpartners = len(men)
    S = {}  # build dictionary to store engagements

    # run the algorithm
    while freemen:
        m = freemen.pop()
        # get the highest ranked woman that has not yet been proposed to
        pref = preftie[m][prefptr[m]]  # first set of prefs from list
        if len(pref) == 1:
            w = pref.pop()
            prefptr[m] += 1  # only updates pointer if this rank is empty
        else:
            w = pref.pop()  # doesnt update until rank is full full

        if w not in S:
            S[w] = m
        else:
            mprime = S[w]
            if rank[w][m] <= rank[w][mprime]:
                S[w] = m
                freemen.add(mprime)
            else:
                freemen.add(m)
    return S


if __name__ == "__main__":
    # input data
    menlist = ['xavier', 'yancey', 'zeus']
    womenlist = ['amy', 'bertha', 'clare']

    thepref = {'xavier': ['amy', 'bertha', 'clare'],
               'yancey': ['bertha', 'amy', 'clare'],
               'zeus': ['amy', 'bertha', 'clare'],
               'amy': ['yancey', 'xavier', 'zeus'],
               'bertha': ['xavier', 'yancey', 'zeus'],
               'clare': ['xavier', 'yancey', 'zeus']
               }
    thepreftie = {'xavier': [{'bertha'}, {'amy'}, {'clare'}],
                  'yancey': [{'amy', 'bertha'}, {'clare'}],
                  'zeus': [{'amy'}, {'bertha', 'clare'}],
                  'amy': [{'zeus', 'xavier', 'yancey'}],
                  'bertha': [{'zeus'}, {'xavier'}, {'yancey'}, ],
                  'clare': [{'xavier', 'yancey'}, {'zeus'}]
                  }

    blocked = {('xavier', 'clare'), ('zeus', 'clare'), ('zeus', 'amy')}

    # eng
    match = gs(menlist, womenlist, thepref)
    print(match)

    match_block = gs_block(menlist, womenlist, thepref, blocked)
    print(match_block)

    match_tie = gs_tie(menlist, womenlist, thepreftie)
    print(match_tie)
