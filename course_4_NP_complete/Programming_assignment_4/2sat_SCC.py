import time, glob
from data_structures import graphs

def read_2sat_input(src: str):
    """
    Helper function to read txt file input for the 2-sat problem. Input first line contains the number of clauses.
    Following lines have identifiers for the booleans, negative indicates not.
    Args:
        src: str, file path for the input

    Returns: inp, array of the input constraints
    """
    with open(src) as file:
        inp = []
        for line in file.readlines()[1:]:
            inp.append([int(i) for i in line.split()])
    return inp


def build_implication_graphs(edg_list: list, reverse=False):
    """
    Build an implication graph from a list of input constraints for 2sat problem. For each constraint, two edges are
    added. One for A' -> B, another for B' -> A

    Args:
        edg_list: list of lists. Each entry is a list with the two boolean values for the constraint
        reverse: Boolean flag for produce a graph with reversed edges. Optional, default False

    Returns:
        graph_out: graphs.Graph object constructed from the input
    """
    graph_out = graphs.Graph()

    if reverse:
        for e in edg_list:
            graph_out.add_edge(e[1], -e[0])
            graph_out.add_edge(e[0], -e[1])
    else:
        for e in edg_list:
            graph_out.add_edge(-e[0], e[1])
            graph_out.add_edge(-e[1], e[0])
    return graph_out


def kosaraju(g_fw: graphs.Graph, g_rev: graphs.Graph):
    """
    Run Kosaraju's algorithm to compute the strongly connected components in a direct graph.

    First run a DFS on the reversed graph, retaining the finishing order for each vertex. Then complete a second
    DFS on the forward graph using the reversed finishing order (i.e. vertices that finished last start). During
    the second DFS, keep track of the DFS source, assigning this as the leader to each node explored. Vertices in a
    SCC will have the same leader

    Args:
        g_fw: Graph object, forward edges
        g_rev: Graph object, reverse edges

    Returns:
        None
    """
    # Run the DFS loop over the graph
    print('DFS reverse graph')
    dfs_loop(g_rev)

    # Get the finishing order from the first DFS pass. Use this in descending
    # order as the search order for the second DFS pass
    search_order = [-1] * g_rev.num_verts
    for n in g_rev.verts:
        search_order[g_rev.verts[n].order] = n
    search_order.reverse()

    # Run DFS again on the forward graph, using the finishing time as the start vertex order
    print('DFS forward graph')
    dfs_loop(g_fw, order=search_order)

    return None


def dfs_loop(g_in: graphs.Graph, order: list = []):
    """
     DFS loop to intiate DFS from every node, to ensure full exploration

    Args:
        g_in: graphs.Graph object to perform DFS on
        order: list, order in which to initiate the DFS. Optional

    Returns:
        None
    """
    # Global variables for the explored vertices count and the current source vertex
    global exp_cnt, source

    # Explored count. Used to define the search order for the second DFS pass
    exp_cnt = 0

    # Current source vertex from which the DFS was initiated. Useful only during the second DFS pass
    source = None

    # If no search order was passed, just get the vertices
    if not order:
        order = g_in.get_vertices()

    # Try DFS from all vertices to ensure everything gets explored
    for n in order:
        # If a vertex is not explored, begin DFS
        if not g_in.verts[n].explored:

            source = n
            # DFS
            _ = dfs(g_in.verts[n])
    return None

def dfs(start: graphs.Vertex):
    """
    Perform DFS on directed graph from a starting Vertex object. Implemented using stack.

    Args:
        start:  Vertex object to start the DFS from

    Returns:
        None
    """
    # Global variables for the explored vertices count and the current source vertex
    global exp_cnt, source

    # Initialize the stack with only the start vertex
    stack = [start]

    while stack:
        # Get the home vertex
        home = stack[-1]

        # Explore the vertex we are starting from
        if not home.explored:
            home.explore()

        # Set the leader for this vertex as the current source
        home.set_leader(source)

        # Check all neighbors. If they are unexplored add them to the stack
        for n in home.get_connections():

            # If not explored, add to the stack
            if not n.explored:
                stack.append(n)

        # If there are no neighbours to explore, we're done with this node.
        # Remove from the stack and assign a finishing order.
        if home == stack[-1]:
            if home.order == None:
                home.order = exp_cnt
                exp_cnt += 1
            stack.pop()
    return None

def check_2sat(g_in: graphs.Graph):
    """
    Check whether a 2 sat instance represented as an implication graph is satisfiable. A graph is unsatisfiable, iff
    X and X` are contained in the same strongly connected component of the implication graph.

    Args:
        g_in: Graph object, implication graph of 2 sat instance. Must have leaders identified for each vertex.

    Returns:
        None
    """
    leaders = g_in.get_leaders()
    vert_list = list(g_in.verts.keys())

    if None in leaders.values():
        print('Missing leaders in graph! SCCs undefined.')
        return None

    while vert_list:
        x = vert_list.pop()
        if leaders[x] == leaders[-x]:
            print('Unsatisfiable!')
            print('\n')
            return None
    print('Satisfiable')
    print('\n')
    return None


if __name__ == "__main__":

    for file in glob.glob("*.txt"):

        print("Checking", file)

        two_sat_in = read_2sat_input(file)

        begin = time.time()
        print("Construct implication graphs")
        im_graph = build_implication_graphs(two_sat_in)
        im_graph_rev = build_implication_graphs(two_sat_in, reverse=True)
        print("Graph construction ran in", time.time() - begin, "seconds")

        begin = time.time()
        kosaraju(im_graph, im_graph_rev)
        print("Kosaraju ran in", time.time() - begin, "seconds")

        check_2sat(im_graph)





