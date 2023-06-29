"""
Class for a min-heap data structure.

This implementation maintains a min-heap with a single entry, a (weight, ident) pair for each ident. ident is a unique
identifier. Also maintained is dictionary with the current weight for each ident for constant time look-up.
"""


class MinHeap:
    """
    Mininmum heap class
    """
    def __init__(self):
        """
        Constructor. Here heap is implemented using a list.

        self.heap_arr -- array with the heap itself. Index 1 is the root, the minimum weight element
        self.ident_arr -- array with identifiers for each entry. Value at index i has weight at index i in the heap
        self.weight_dict -- dict with identifiers weighted to the corresponding weight in the heap. Useful for fast lookup
        self.heap_size -- int, heap size
        """
        self.heap_arr = [0]
        self.ident_arr = [-1]
        self.weight_dict = {}
        self.heap_size = 0

    def insert(self, weight, ident):
        """
         Insert an element into the heap. Sift up to maintain the min heap property

        Args:
            weight: weight to insert into heap
            ident: unique, hashable identifier for element to insert

        Returns:
            None
        """

        # Only add a weight, ident to the heap if the new weight is smaller or it's not in the heap already.
        if weight < self.weight_dict.get(ident, float("inf")):

            # Append to the heap and identue arrays
            self.heap_arr.append(weight)
            self.ident_arr.append(ident)
            # Update the min-weight dict
            self.weight_dict[ident] = weight
            # Update the size
            self.heap_size += 1
            # Sift upwards to maintain the heap property
            self.sift_up(self.heap_size)
        return None

    def min_child(self, i: int):
        """
        Return minimum weight child for heap entry at index i.

        Args:
            i: int, index of parent in heap array

        Returns:
            int, index of the minimum child in the heap array
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

        Args:
            i: index of the child element in the heap array

        Returns:
            int, index of the parent element in the heap array
        """
        pt = int(i / 2)
        if pt == 0:
            return None
        else:
            return pt

    def sift_up(self, i):
        """
        Sift an element upwards until the heap property is restored

        Args:
            i: index of the element to sift upwards

        Returns:
            None
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
        return None

    def sift_down(self, i):
        """
        Sift an element downwards until the heap property is restored
        Args:
            i: index of the element to sift downwards

        Returns:
            None
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
        return None

    def pop_root(self):
        """
        Returns the minimum weight and corresponding identifier of the heap, by definition the root.

        Returns:
            (min_weight, min_ident) - min_weight - the weight of the entry at the root of the heap;
                 min_ident: hashable identifier for the root element
        """

        assert self.heap_size > 0, 'Empty heap!'
        # Get the minimum ident, stored at 1 index
        min_weight = self.heap_arr[1]
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

        # Remove the entry from the min-weight dict
        self.weight_dict.pop(min_ident)

        return min_weight, min_ident
