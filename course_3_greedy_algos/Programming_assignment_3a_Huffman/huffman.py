"""
Module for Huffman encoding. Includes class for nodes with useful attributes for the
encoding procedure, and a separate class for maintaining a binary tree of these nodes.
The tree also maintains a min-heap for acceleating the encoding procedure.
"""

import heap

class HuffmanNode:
    """
    Node class with useful attributes for use in Huffman encoding
    Attributes:
        id: unique hashable identifier for the symbol
        weight: symbol frequency / weight
        left_child: left child of the node in a binary tree
        right_child: right child of the node in a binary tree
        parent: parent of the node in a binary tree
        code: code for the symbol produced via Huffman coding
    """
    def __init__(self, id, weight):
        """
        Constructor
        Args:
            id: unique hashable identifier for symbol
            weight: symbol frequency / weight
        """
        self.id = id
        self.weight = weight
        self.left_child = None
        self.right_child = None
        self.parent = None
        self.code = ''

class HuffmanTree:
    """
    Huffman binary tree class.
    Attributes:
        node: dictionary of unique symbol identifiers with HuffmanNodes as values
        leaves: dictionary of leaf nodes in the tree
        code: dictionary of codes produced by encoding
        min_heap: heap.MinHeap, useful for accelerating encoding by maintaining the minimum
        weight sub-tree
        size: int, number of nodes in the tree
        root: identifier for the root of the tree
    """
    def __init__(self, queue: bool = False):
        """
        Constructor
        """
        self.nodes = {}
        self.leaves = {}
        self.codes = {}
        self.size = 0
        self.root = None

        # Use queues if desired. Default implementation uses a min-heap.
        if queue:
            self.Q1 = []
            self.Q2 = []
        else:
            self.min_heap = heap.MinHeap()
        self.use_queue = queue

    def add_node(self, key, weight: int, is_leaf: bool = False):
        """
        Add a node for Huffman encoding. build_encoding must be called to form into tree
        Args:
            key: unique hashable identifier
            weight: weight / frequency of the entry
            leaf: bool, set True in the entry should be leaf node in the tree

        Returns: None
        """
        if key not in self.nodes:

            self.nodes[key] = HuffmanNode(key, weight)
            self.size += 1
            # Add to leaves if desired
            if is_leaf:
                self.leaves[key] = key
            # Add entry to either the queue or min-heap, depending on how the tree was initialized.
                if self.use_queue:
                    self.Q1.append((weight, key))
                    self.Q1.sort(key= lambda x: x[0])
            if not self.use_queue:
                self.min_heap.insert(weight, key)

    def build_encoding(self):
        """
        Build the Huffman binary tree after adding all nodes.

        Using a min_heap to maintain the minimum weight node, merge the two smallest weight nodes
        by producing a parent that has both as children. Insert the parent into the tree. Continue
        until all nodes / sub-trees are merged.

        Returns: None
        """

        # Increment integers as identifiers
        i = max(self.nodes.keys())

        if self.use_queue:
            sel_queue = 2
            while len(self.Q1) + len(self.Q2) > 1:
                i += 1

                if min(self.Q1, key= lambda x: x[0], default=(float("inf"), float("inf")))[0] < min(self.Q2,key= lambda x: x[0], default=(float("inf"),float("inf")))[0]:
                    right_weight, right_child = self.Q1.pop(0)
                else:
                    right_weight, right_child = self.Q2.pop(0)
                if min(self.Q1, key= lambda x: x[0], default=(float("inf"), float("inf")))[0] < min(self.Q2,key= lambda x: x[0], default=(float("inf"),float("inf")))[0]:
                    left_weight, left_child = self.Q1.pop(0)
                else:
                    left_weight, left_child = self.Q2.pop(0)

                self.add_node(i, left_weight + right_weight)
                self.nodes[i].right_child = right_child
                self.nodes[i].left_child = left_child

                if sel_queue == 2:
                    self.Q2.append(((left_weight + right_weight),i))
                    if not self.Q1:
                        sel_queue = 1
                else:
                    self.Q1.append(((left_weight + right_weight), i))
                    if not self.Q1:
                        sel_queue = 2
        else:
            while self.min_heap.heap_size > 1:
                i += 1
                # Get next two weights for the children
                right_weight, right_child = self.min_heap.pop_root()
                left_weight, left_child = self.min_heap.pop_root()

                # Create a new node that is parent to the two lowest weight nodes in the heap
                self.add_node(i, left_weight + right_weight)
                self.nodes[i].right_child = right_child
                self.nodes[i].left_child = left_child

        self.root = i

    def generate_codes(self, root_key, code: str= ''):
        """
        Generate Huffman codes from the binary Huffman tree. Recursive implementation that works
        down the tree, keeping track of the code as it goes.
        Args:
            root_key: unique identifier for the tree root, where to start
            code: str for tracking the code through levels of recursion.

        Returns: None
        """
        # Set the code for the root to whatever was passed
        self.nodes[root_key].code = code
        self.codes[root_key] = code

        # If we are at a leaf, we're done (base case)
        if root_key in self.leaves:
            return None
        else:
            # If not, recurse on the left and right children, altering the code as need
            self.generate_codes(self.nodes[root_key].left_child, code=self.codes[root_key] + '0')
            self.generate_codes(self.nodes[root_key].right_child, code=self.codes[root_key] + '1')
        return None