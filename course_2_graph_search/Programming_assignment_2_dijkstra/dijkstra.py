"""
Application of Dijkstra's algorithm to compute shortest path lengths from a single
starting vertex on an undirected weighted graph. Both naive and heap-based implementations
are included here, with the latter running considerably faster (Nlog(N) vs M*N)

The heap-based implementation uses a heap data structure, implemented as its own class.
"""

import time, heap, graphs
def heap_dijkstra(G : graphs.Graph(), start : int):
    """
    Heap based implementation of Dijkstra for an undirected graph. Runs in O(nlog(n))
    :param G: Graph object, undirected weighted graph
    :param start: int, start vertex
    :return: dict, vertex:shortest path length from start
    """
    explored = set()
    explored.add(start)
    D = {start:0}
    vert_set = set(G.get_vertices())

    # Initial heap populated with DGC and vert numbers stemming from the start node
    H = heap.MinHeap()
    for n, w in G.verts[start].neighbors.items():
        H.insert(w, n)

    while explored != vert_set:

        # Get the root from the heap and add it to the explored set
        min_dgc, add = H.pop_root()
        if add not in explored:
            D[add] = min_dgc
            explored.add(add)

        # Add new frontier DGCs to the heap
        for n, w in G.verts[add].neighbors.items():
            # If we've already explored here, move on
            if n in explored:
                continue
            elif n in H.val_arr:
                if H.heap_arr[H.val_arr.index(n)] < min_dgc + w:
                    continue
            # Insert the new path length
            H.insert(min_dgc + w, n)
    return D

def naive_dijkstra(G : graphs.Graph(), start : int):
    """
    Naive implementation of Dijkstra's algorithm, without using a heap. Runs in O(m * n) time.
    :param G: input graph, Graph object
    :param start: int, key for start vertex
    :return: dict, vertex : shortest path length from start
    """
    explored = set()
    explored.add(start)
    G.verts[start].explored = True
    D = {start:0}

    # Loop until we've explored all nodes
    while explored != set(G.get_vertices()):
        # Initial value for minimum Dijkstra's  greedy criterion (DGC)
        min_dgc = float('inf')
        # Check all edges from explored to unexplored nodes
        for node in explored:
            frontier = G.verts[node].neighbors
            for n, w in frontier.items():
                # Compute DGC. Update if it's smaller
                if not G.verts[n].explored:
                    dgc = D[node] + w
                    if dgc < min_dgc:
                        min_dgc = dgc
                        add = n
        # Expand the explored set and shortest distances
        G.verts[add].explored = True
        explored.add(add)
        D[add] = min_dgc

    return D

def build_graph(source : str):
    """
    Build an undirected weighted graph. Input is a text file. Single digits represent source
    vertices, while tuple represent neighbors and the edge weight. E.g. "1  2,10    3,20" is
    a three node graph with an edge of length 10 between 1 and 2, and an edge of length 20 between
    1 and 3.
    :param source: string to the input file path
    :return: Graph class object
    """
    graph = graphs.Graph()

    with open(source) as file:
        start = None
        # Read line-by-line
        for l in file.readlines():
            arr = l.split('\t')
            arr.remove('\n')
            # Check if the line indicates a new start node
            if len(arr[0].split(',')) == 1:
                start = int(arr[0])
                shift = 1
            else:
                shift = 0
            # Add the connections
            for e in arr[shift:]:
                end, weight = int(e.split(',')[0]), int(e.split(',')[1])
                graph.add_edge(start, end, weight)
    return graph

if __name__ =="__main__":
    # Timing
    begin = time.time()

    # Source file for the input graph
    source = "dijkstraData.txt"
    # Build the graph
    G = build_graph(source)
    print('Graph constructed in', time.time() - begin, "seconds.")

    # Timing
    begin = time.time()

    # Compute shortest path lengths using naive Dijkstra implementation
    distances_naive = naive_dijkstra(G, 1)
    print("Naive Dijkstra ran in", time.time() - begin, "seconds")

    # Vertices of interest, for the course assignment
    verts_of_interest = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    dists_of_interest = []
    for v in verts_of_interest:
        dists_of_interest.append(distances_naive[v])
    print(dists_of_interest)

    # Timing
    begin = time.time()

    # Compute shortest path lengths using heap Dijkstra implementation
    distances_heap = heap_dijkstra(G, 1)
    print("Heap Dijkstra ran in", time.time() - begin, "seconds")
    dists_of_interest = []
    # Vertices of interest, for the course assignment
    for v in verts_of_interest:
        dists_of_interest.append(distances_heap[v])
    print(dists_of_interest)

    print(distances_heap == distances_naive)

