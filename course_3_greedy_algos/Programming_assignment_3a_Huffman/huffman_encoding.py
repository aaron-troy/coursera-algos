"""
Huffman encoding implemented using min heap.

Completed for programming assignment 3 of course 3 of the Coursera algorithms
specialization by Tim Roughgarden
"""

import time
from data_structures import huffman as hf


def read_input(src : str):
    """
    Helper function to read input txt file. First line the number of entries.
    Subsequent lines are the symbol weights
    Args:
        src: str, file path for the input

    Returns: list of symbol weights

    """
    with open(src) as file:
        inp = []
        for line in file.readlines()[1:]:
            inp.append(int(line))
    return inp

def huffman_encode(weights: list, use_queue: bool = False):
    """
    Generate Huffman codes for symbols best on an input list of weights
    Args:
        weights: list, entry i is the weight / frequency of symbol i

    Returns: dict of codes, key i has value of the code for symbol i
    """

    # Initialize Huffman tree
    HT = hf.HuffmanTree(queue = use_queue)
    for i, w in enumerate(weights):
        HT.add_node(i, w, is_leaf=True)

    # Build the encoding
    HT.build_encoding()

    # Generate codes
    HT.generate_codes(HT.root)

    # Return only codes for leaves, corresponding to symbols in passed list.
    # Non-leaf nodes correspond to parents created from merging nodes when building the tree.
    leaf_codes = {key : HT.codes[key] for key in HT.leaves}

    return leaf_codes

if __name__ == "__main__":

    # Source file for the input symbol weights
    source = "huffman.txt"

    # Build the graph
    W = read_input(source)

    # Timing
    begin = time.time()

    # Generate Huffman tree, first using min heap
    codes = huffman_encode(W)

    print("Huffman coding ran in", time.time() - begin, "seconds using min heap")
    print("Max code length:", max([len(c) for c in codes.values()]))
    print("Min code length:", min([len(c) for c in codes.values()]))

    # Timing
    begin = time.time()

    # Again, using queues
    codes = huffman_encode(W, use_queue=True)

    print("Huffman coding ran in", time.time() - begin, "seconds using regular queues")
    print("Max code length:", max([len(c) for c in codes.values()]))
    print("Min code length:", min([len(c) for c in codes.values()]))