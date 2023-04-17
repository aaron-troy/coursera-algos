"""
Class for a min-heap data structure
"""
class MinHeap:

    def __init__(self):
        """
        Constructor. Here heap is implemented using a list.
        """
        self.heap_arr = [0]
        self.heap_size = 0

    def insert(self, key):
        """
        Insert an entry with value key to the heap, maintain the heap structure
        """
        # Append to the heap array
        self.heap_arr.append(key)
        # Update the size
        self.heap_size += 1
        # Sift upwards to maintain the heap property
        self.sift_up(self.heap_size)

    def delete(self, i):
        """Remove entry i from the heap, maintain the heap structure"""
        # Remove the value at the specified index from the heaped array
        self.heap_arr.pop(i)
        # Update the heap size
        self.heap_size -= 1
        # Sift downwards to maintain the heap property
        self.sift_down(i)

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
            i = mc
            mc = self.min_child(mc)

    def pop_min_val(self):
        """
        Returns the minimum value of the heap, dy definition the root.
        """
        assert self.heap_size > 0, 'Empty heap!'
        # Get the minimum val, stored at 1 index
        val = self.heap_arr.pop(1)
        # Update the heap size
        self.heap_size -= 1
        #Sift downwards to maintain the heap structure
        self.sift_down(1)

        return val
