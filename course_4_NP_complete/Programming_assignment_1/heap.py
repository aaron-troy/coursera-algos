"""
Class for a min-heap data structure.

This implementation maintains a min-heap with a single entry, a (key, ident) pair for each ident. ident is a unique
identifier. Also maintained is dictionary with the current key for each ident for constant time look-up.

"""


class MinHeap:

    def __init__(self):
        """
        Constructor. Here heap is implemented using a list.
        """
        self.heap_arr = [0]
        self.ident_arr = [-1]
        self.min_key_dict = {}
        self.heap_size = 0

    def insert(self, key, ident):
        """
        Insert an entry with identue key to the heap, maintain the heap structure
        """

        # Only add a key, ident to the heap if the new key is smaller or it's not in the heap already.
        if key < self.min_key_dict.get(ident, float("inf")):

            # Append to the heap and identue arrays
            self.heap_arr.append(key)
            self.ident_arr.append(ident)
            # Update the min-key dict
            self.min_key_dict[ident] = key
            # Update the size
            self.heap_size += 1
            # Sift upwards to maintain the heap property
            self.sift_up(self.heap_size)

    def min_child(self, i):
        """
        Return the minimum child for entry i, if it exists
        """
        # Check there are children
        if 2 * i > self.heap_size:
            return None
        # Check if there is more than one
        elif 2 * i + 1 > self.heap_size:
            return 2 * i
        # Take the smaller of the two
        else:
            if self.heap_arr[2 * i] < self.heap_arr[2 * i + 1]:
                return 2 * i
            else:
                return 2 * i + 1


    def parent(self, i):
        """
        Get the parent for heap entry i, if it exists
        """
        pt = int(i / 2)
        if pt == 0:
            return None
        else:
            return pt

    def sift_up(self, i):
        """
        Sift upwards starting at entry i to maintain the heap
        """
        # Get the initial parent
        pt = self.parent(i)

        # If the parent exists, check if the children are smaller
        while pt:
            # Swap if necessary
            if self.heap_arr[i] < self.heap_arr[pt]:
                self.heap_arr[i], self.heap_arr[pt] = self.heap_arr[pt], self.heap_arr[i]
                self.ident_arr[i], self.ident_arr[pt] = self.ident_arr[pt], self.ident_arr[i]
            # Get the new parent
            i = pt
            pt = self.parent(pt)

    def sift_down(self, i):
        """
        Sift downwards, starting from entry i to maintain the heap structure
        """
        # Get the min child of the starting node
        mc = self.min_child(i)

        # If the child exists, see if it is smaller than the parent
        while mc:
            if self.heap_arr[mc] < self.heap_arr[i]:
                self.heap_arr[i], self.heap_arr[mc] = self.heap_arr[mc], self.heap_arr[i]
                self.ident_arr[i], self.ident_arr[mc] = self.ident_arr[mc], self.ident_arr[i]
            i = mc
            mc = self.min_child(i)

    def pop_root(self):
        """
        Returns the minimum key and corresponding identue of the heap, dy definition the root.
        """
        assert self.heap_size > 0, 'Empty heap!'
        # Get the minimum ident, stored at 1 index
        min_key = self.heap_arr[1]
        min_ident = self.ident_arr[1]

        # Move the end entry to the root of the heap
        self.heap_arr[1] = self.heap_arr[self.heap_size]
        self.ident_arr[1] = self.ident_arr[self.heap_size]

        *self.heap_arr, _ = self.heap_arr
        *self.ident_arr, _ = self.ident_arr

        # Update the heap size
        self.heap_size -= 1

        # Sift downwards to maintain the heap structure
        self.sift_down(1)

        # Remove the entry from the min-key dict
        self.min_key_dict.pop(min_ident)

        return min_key, min_ident
