# Project 2 DFS-based Topological Sorting
# starter code
# student name: David Jeffalone
# student id number: 1558099


# The built-in Graph
# Use this graph to test the correctness of your DFS-based topological sorting
cs143, cs321, cs322, cs142, cs370, cs341, cs326, cs378, cs401, cs421 = range(10)

G1 = {
     cs143: [cs321, cs341, cs370, cs378],
     cs321: [cs322, cs326],
     cs322: [cs401, cs421],
     cs142: [cs143],
     cs370: [],
     cs341: [cs401],
     cs326: [cs401, cs421],
     cs378: [cs401],
     cs401: [],
     cs421: []
     }

names = ['cs143', 'cs321', 'cs322', 'cs142', 'cs370', 
         'cs341', 'cs326', 'cs378', 'cs401', 'cs421']    

# This is one of the two functions for DFS-based topological sorting    
# complete this function using the algorithm DFS-Topo on page 50 of the 2nd textbook
# G as the input graph
# s as the current vertex to be explored      
def dfs_topo(G, s, explored, ordering): # You may add more input parameters if necessary
    
    explored[s] = 1
    for vertex in G[s]:
        if explored[vertex] == 0:
            label = dfs_topo(G, vertex, explored ,ordering) 
    
    ordering.append(s) # adds verticies who no longer have neighbors that are unexplored to list 
                       # this gives the topological ordering in reverse order
    
    
# This is one of the two functions for DFS-based topological sorting    
# complete this function using the algorithm TopoSort on page 50 of the 2nd textbook
# G as the input graph
# L as the Python list to record the ordering of vertices
def topo_sort(G): # you may add more input parameters if necessary
    L = [0]*len(G)
    explored = [0]*len(G)
    ordering = [] 
    for vertex in G.keys(): # kicks off topologocal sorting
        if explored[vertex] == 0:
            dfs_topo(G, vertex, explored, ordering)


    currLabel= len(G)-1 # starts at highest rank since ordering is reversed
    for vertex in ordering:# orders vertexes in to L with indexes corresponding to their rank 
        L[currLabel] = vertex
        currLabel -= 1

    return L

# This is the function for induction-based topological sorting
# It will be compmared with your DFS-based topological sorting for performance     
# don't change any part of this function
def ind_topo(G):
    count = dict((u, 0) for u in G) # count the number of incoming edges 
    for u in G:
        for v in G[u]:
            count[v] += 1
    Q = [u for u in G if count[u]==0] # stack to store source vertices
    L = [0]*len(G) # record the ordering of each vertex
    k = 1
    while Q:
        u = Q.pop() # take away a source vertex
        L[u] = k # assign an ordering number to the removed vertex
        k += 1
        for v in G[u]:
            count[v] -= 1
            # a new source vertex will be appended to Q
            if count[v] == 0: Q.append(v) 
    return L

if __name__=="__main__":
    #print(topo_sort(G1))

    # test the correctness of your topological sorting functions
    topo_order = topo_sort(G1)
    print({names[x]: topo_order[x] for x in range(10)})
    
    # load the DAG from external files
    # every line of the data file represent an edge from the DAG   
    f = open("DAG5.txt") # use DAG1.txt through DAG5.txt to compare the performance    
    # do NOT change the remaining lines
    G2 = {}
    n = 0
    while True:
        line = f.readline()
        if line:
            words = line.split()
            key = int(words[0])
            value = int(words[1])
            if value>n: n=value
            if key not in G2: G2[key]=[value]
            else: G2[key].append(value)
        else: break
    n += 1
    for i in range(n):
        if i not in G2: G2[i]=[]
    f.close()

    import time
    start = time.time()
    topo_order1 = topo_sort(G2) # measure the running time of the DFS-based version
    end = time.time()
    topo_order2 = ind_topo(G2) # measure the running time of the induction-based version
    end2 = time.time()
    print("DFS-based toposort took ", end-start, " seconds")
    print("Induction-based toposort took ", end2-end, " seconds")
    
    
    
    
    