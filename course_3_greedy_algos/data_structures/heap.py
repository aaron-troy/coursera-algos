"""
Class for a min-heap data structure
"""
class MinHeap:

    def __init__(self):
        """
        Constructor. Here heap is implemented using a list. Indexed from 1 for numerical simplicity in the sifting operations
        """
        self.heap_arr = [0]
        self.val_arr = [(0, 0)]
        self.heap_size = 0

    def insert(self, key, val):
        """
        Insert an entry with (key and value) into the heap, maintain the heap structure
        Args:
            key: key for the heap entry, determines position in the heap
            val: val tied to the key

        Returns: None
        """
        # Append to the heap and value arrays
        self.heap_arr.append(key)
        self.val_arr.append(val)
        # Update the size
        self.heap_size += 1
        # Sift upwards to maintain the heap property
        self.sift_up(self.heap_size)

        return None

    def min_child(self, i):
        """
        Return the minimum child for entry at index i in the heap array, if it exists
        Args:
            i: index in heap array of the entry to find the minimum child for, if it exists

        Returns: index in heap array of minimum child
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
            i: index in heap array of the entry to find the minimum child for, if it exists

        Returns:
            pt: index of parent in heap array, None if no parent exist
        """
        pt = int(i / 2)
        if pt == 0:
            return None
        else:
            return pt
    def sift_up(self, i):
        """
        Sift upwards from index i to maintain the heap
        Args:
            i: index in the heap array to sift upwards from

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
                self.val_arr[i], self.val_arr[pt] = self.val_arr[pt], self.val_arr[i]
            # Get the new parent
            i = pt
            pt = self.parent(pt)
        return None

    def sift_down(self, i):
        """
        Sift downwards, starting from entry i to maintain the heap structure
        Args:
            i: index in the heap array to sift downwards from

        Returns:
            None
        """
        # Get the min child of the starting node
        mc = self.min_child(i)

        # If the child exists, see if it is smaller than the parent
        while mc:
            if self.heap_arr[mc] < self.heap_arr[i]:
                self.heap_arr[i], self.heap_arr[mc] = self.heap_arr[mc], self.heap_arr[i]
                self.val_arr[i], self.val_arr[mc] = self.val_arr[mc], self.val_arr[i]
            i = mc
            mc = self.min_child(i)
        return None

    def pop_root(self):
        """
        Returns the minimum key and corresponding value of the heap, dy definition the root.

        Returns: (key, value) for the root
        """
        assert self.heap_size > 0, 'Empty heap!'
        # Get the minimum val, stored at 1 index
        min_key = self.heap_arr[1]
        min_val = self.val_arr[1]

        # Move the end entry to the root of the heap
        self.heap_arr[1] = self.heap_arr[self.heap_size]
        self.val_arr[1] = self.val_arr[self.heap_size]

        *self.heap_arr, _ = self.heap_arr
        *self.val_arr, _ = self.val_arr

        # Update the heap size
        self.heap_size -= 1

        # Sift downwards to maintain the heap structure
        self.sift_down(1)

        return min_key, min_val
