import time
import heap

class HuffmanNode:
    def __init__(self, id, weight):
        self.id = id
        self.weight = weight
        self.left_child = None
        self.right_child = None
        self.parent = None
        self.code = ''

class HuffmanTree:

    def __init__(self):
        self.nodes = {}
        self.leaves = {}
        self.codes = {}
        self.min_heap = heap.MinHeap()
        self.size = 0
        self.root = None

    def insert(self, key, weight: int, leaf: bool = False):
        if key not in self.nodes:
            self.nodes[key] = HuffmanNode(key, weight)
            self.min_heap.insert(weight, key)
            self.size += 1
            # Add to leaves if desired
            if leaf:
                self.leaves[key] = key

    def build_encoding(self):

        i = max(self.nodes.keys())
        while self.min_heap.heap_size > 1:
            i += 1
            # Get next two weights for the children
            right_weight, right_child = self.min_heap.pop_root()
            left_weight, left_child = self.min_heap.pop_root()

            # Create a new node that is parent to the two lowest weight nodes in the heap
            self.insert(i, left_weight + right_weight)
            self.nodes[i].right_child = right_child
            self.nodes[i].left_child = left_child

        self.root = i
    def generate_codes(self, root_key, code: str= ''):
        """
        Recursively work through a Huffman tree to assign codes
        """

        self.nodes[root_key].code = code
        self.codes[root_key] = code

        if (self.nodes[root_key].left_child is None) and (self.nodes[root_key].right_child is None):
            return None
        else:
            self.generate_codes(self.nodes[root_key].left_child, code=self.codes[root_key] + '0')
            self.generate_codes(self.nodes[root_key].right_child, code=self.codes[root_key] + '1')
        return None
def read_input(src : str):
    with open(src) as file:
        inp = []
        for line in file.readlines()[1:]:
            inp.append(int(line))
    return inp

def huffman_encode(weights: list):

    # Initialize Huffman tree
    HT = HuffmanTree()
    for i, w in enumerate(weights):
        HT.insert(i, w, leaf=True)

    # Build the encoding
    HT.build_encoding()

    # Generate codes
    HT.generate_codes(HT.root)

    # Return only codes for leaves
    leaf_codes = {key : HT.codes[key] for key in HT.leaves}

    return leaf_codes

def generate_huffman_coding(tree: dict, root: HuffmanNode, code: str = ''):
    """
    Recursively work through a Huffman tree to assign codes
    """
    root.code = code

    if (root.left_child is None) and (root.right_child is None):
        return None
    else:
        generate_huffman_coding(tree, tree[root.left_child], code=root.code + '0')
        generate_huffman_coding(tree, tree[root.right_child], code=root.code + '1')
    return None


if __name__ == "__main__":

    # Source file for the input symbol weights
    source = "huffman.txt"

    # Build the graph
    W = read_input(source)

    # Timing
    begin = time.time()

    # Generate Huffman tree
    codes = huffman_encode(W)

    print("Huffman coding ran in", time.time() - begin, "seconds")
    print("Max code length:", max([len(c) for c in codes.values()]))
    print("Min code length:", min([len(c) for c in codes.values()]))