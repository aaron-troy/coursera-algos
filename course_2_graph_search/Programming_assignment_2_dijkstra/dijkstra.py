"""
Application of Dijkstra's algorithm to compute shortest path lengths from a single
starting vertex on an undirected weighted graph. Both naive and heap-based implementations
are included here, with the latter running considerably faster (Nlog(N) vs M*N)

The heap-based implementation uses a heap data structure, implemented as its own class.
"""

import time, heap, graphs
def heap_dijkstra(g: graphs.Graph(), start: int):
    """
    Min-heap based implementation of Dijkstra. Runs in O(nlog(n)) time

    Args:
        g: Graph object, undirected weighted graph
        start: int, start vertex identifier
    Returns:
        d: dict, vertex ID keyed to shortest path length from start
    """
    explored = set()
    explored.add(start)
    d = {start: 0}
    vert_set = set(g.get_vertices())

    # Initial heap populated with DGC and vert numbers stemming from the start node
    h = heap.MinHeap()
    for n, w in g.verts[start].neighbors.items():
        h.insert(w, n)

    while explored != vert_set:

        # Get the root value and key from the heap and add it to the explored set
        min_dgc, add_key = h.pop_root()
        if add_key not in explored:
            d[add_key] = min_dgc
            explored.add(add_key)

        # Add new frontier DGCs to the heap
        for n, w in g.verts[add_key].neighbors.items():
            # If we've already explored here, move on
            if n in explored:
                continue
            elif n in h.val_arr:
                # If the new path is longer or equal to than an existing one, don't add it
                if min_dgc + w >= h.heap_arr[h.val_arr.index(n)]:
                    continue
                else:
                    h.delete(h.val_arr.index(n))
            # Insert the new path length
            h.insert(min_dgc + w, n)
    return d

def naive_dijkstra(g: graphs.Graph(), start: int):
    """
    Naive implementation of Dijkstra's algorithm, without using a heap. Runs in O(m * n) time.

    Args:
        g: input graph, Graph object
        start: int, start vertex identifier

    Returns:
        d: dict, vertex ID keyed to shortest path length from start
    """
    explored = set()
    explored.add(start)
    g.verts[start].explored = True
    d = {start: 0}
    add_key = start

    # Loop until we've explored all nodes
    while explored != set(g.get_vertices()):
        # Initial value for minimum Dijkstra's  greedy criterion (DGC)
        min_dgc = float('inf')
        # Check all edges from explored to unexplored nodes
        for node in explored:
            frontier = g.verts[node].neighbors
            for n, w in frontier.items():
                # Compute DGC. Update if it's smaller
                if not g.verts[n].explored:
                    dgc = d[node] + w
                    if dgc < min_dgc:
                        min_dgc = dgc
                        add_key = n
        # Expand the explored set and shortest distances
        g.verts[add_key].explored = True
        explored.add(add_key)
        d[add_key] = min_dgc

    return d

def build_graph(src: str):
    """
    Build an undirected weighted graph. Input is a text file. Single digits represent source
    vertices, while tuple represent neighbors and the edge weight. E.g. "1  2,10    3,20" is
    a three node graph with an edge of length 10 between 1 and 2, and an edge of length 20 between
    1 and 3.

    Args:
        source: string to the input file path

    Returns:
        graph_out: graphs.Graph class object constructed from the input file
    """
    graph = graphs.Graph()

    with open(src) as file:
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
                graph.add_edge(start, end, weight=weight)
    return graph


if __name__ == "__main__":
    # Timing
    begin = time.time()

    # Source file for the input graph
    source = "dijkstraData.txt"
    # Build the graph
    input_graph = build_graph(source)
    print('Graph constructed in', time.time() - begin, "seconds.")

    # Timing
    begin = time.time()

    # Compute shortest path lengths using naive Dijkstra implementation
    distances_naive = naive_dijkstra(input_graph, 1)
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
    distances_from_heap = heap_dijkstra(input_graph, 1)
    print("Heap Dijkstra ran in", time.time() - begin, "seconds")
    dists_of_interest = []
    # Vertices of interest, for the course assignment
    for v in verts_of_interest:
        dists_of_interest.append(distances_from_heap[v])
    print(dists_of_interest)


