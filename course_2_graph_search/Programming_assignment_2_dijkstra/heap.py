
class MinHeap:
    """
    Class for a min-heap data structure
    """
    def __init__(self):
        """
        Constructor. Here heap is implemented using a list. Arrays start from index 1, for numerical
        simplicity in the sifting operations
        """
        self.heap_arr = [0]
        self.val_arr = [0]
        self.heap_size = 0

    def insert(self, key, val):
        """
        Insert an entry with value key to the heap, maintain the heap structure
        :param key: unique, hashable key for positioning the heap
        :param val: value associated with the key in the heap
        :return: None
        """
        # Append to the heap and value arrays
        self.heap_arr.append(key)
        self.val_arr.append(val)
        # Update the size
        self.heap_size += 1
        # Sift upwards to maintain the heap property
        self.sift_up(self.heap_size)

        return None

    def delete(self, key):
        """
        Delete an entry with arbitrary position from the heap
        :param key: key of heap entry to delete
        :return: None
        """
        # Move replace the entry to delete with the last entry of the heap
        if key == self.heap_size:
            return
        self.heap_arr[key] = self.heap_arr[self.heap_size]
        self.val_arr[key] = self.val_arr[self.heap_size]
        *self.heap_arr, _ = self.heap_arr
        *self.val_arr, _ = self.val_arr

        # Update the heap size
        self.heap_size -= 1

        # If the replacing element is less than the parent, sift up. Otherwise sift down
        if self.parent(key):
            if self.parent(key) > self.heap_arr[key]:
                self.sift_up(key)
            else:
                self.sift_down(key)
        return None


    def min_child(self, i: int):
        """
        Return the minimum child for entry i, if it exists
        :param i: Heap array index of entry to find the min child for
        :return: Heap array index of the minimum child of the entry at i
        """
        # Check if there are children
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

    def parent(self, i: int):
        """
        Get the parent of the entry at index i in the heap array, if it exists.
        :param i: index of the entry in the heap array to find the parent for
        :return: index of the parent in the heap array, if it exists.
        """
        pt = int(i / 2)
        if pt == 0:
            return None
        else:
            return pt
    def sift_up(self, i: int):
        """
        Sift upwards starting at index i in the heap array to maintain the heap
        :param i: index in the heap array to sift upwards from
        :return: None
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

    def sift_down(self, i: int):
        """
        Sift downwards, starting from index i in the heap array to maintain the heap structure
        :param i: index in the heap array to sift downwards from
        :return: None
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
        Returns the minimum key and corresponding value of the heap, by definition the root.
        :return: key and value for the entry at the heap root
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
