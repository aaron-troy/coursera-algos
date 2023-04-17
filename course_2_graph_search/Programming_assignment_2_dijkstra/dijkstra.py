import time, heap, graphs

def dijkstra(G : graphs.Graph(), start : int):

    explored = {start : True}
    G.verts[start].explored = True
    D = {start : 0}

    while explored.keys() != G.get_vertices():
        min_dgc = float('inf')
        for node in explored:
            frontier = G.verts[node].neighbors
            for n, w in frontier.items():
                if not G.verts[n].explored:
                    dgc = D[node] + w
                    if dgc < min_dgc:
                        min_dgc = dgc
                        add = n
        G.verts[add].explored = True
        explored[add] = True
        D[add] = min_dgc

    return D


if __name__ =="__main__":

    source = "dijkstraData.txt"

    graph = graphs.Graph()

    # Read in the input and construct the forward and reverse graphs
    with open(source) as file:
        for l in file.readlines():
            arr = l.split()
            start = int(l[0])
            for e in arr[1:]:
                end, weight = int(e.split(',')[0]), int(e.split(',')[1])
                graph.add_edge(start, end, weight)

    distances = dijkstra(graph, 1)

    verts_of_interest = [7,37,59,82,99,115,133,165,188,197]
    dists_of_interest = []
    for v in verts_of_interest:
        dists_of_interest.append(distances[v])
    print(dists_of_interest)
    begin = time.time()