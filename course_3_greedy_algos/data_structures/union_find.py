
class UnionFind:
    """
    Union-find data structure. Implemented with lazy union by rank and path compression
    """
    def __init__(self):
        """
        Constructor
        """
        self.parents = {}
        self.ranks = {}
        self.ids = {}

    def add_member(self, member: int):
        """
        Add member to the UF data strucutre
        Args:
            member: unique, hashable key for the member to add

        Returns: None
        """
        # Add member, given rank 0 and as its own parent
        if member not in self.ids:
            self.ids[member] = member
            self.parents[member] = member
            self.ranks[member] = 0
        return None

    def find(self, member: int):
        """
        Recursively find the root, or oldest ancestor, of a member
        Args:
            member: unique, hashable key for the member to find the root for

        Returns: key of the root, or oldest ancestor
        """
        if self.parents[member] == member:
            return self.parents[member]
        else:
            return self.find(self.parents[member])

    def union(self, member_1: int, member_2: int):
        """
        Lazy union by rank with path compression. This refers to two specific optimizations
            1. Union by rank: when combining sub-trees, the root with the greater maximum
            steps to reach a leaf becomes the root of the resulting tree
            2. Path compression: upon completing a union of two members, both members along with
            the lower rank parent, take the remaining parent as their own. I.e. paths are compressed
            directly to a single root.
        Args:
            member_1: key of member_1
            member_2: key of member_2

        Returns: None
        """
        # Get the current parents
        parent_1 = self.find(member_1)
        parent_2 = self.find(member_2)

        # Maintain the root with the larger rank
        if self.ranks[parent_1] >= self.ranks[parent_2]:
            # Path compressed union
            self.parents[member_2] = parent_1
            self.parents[parent_2] = parent_1
            # If the ranks are the same, increase the new parent's rank by 1
            if self.ranks[parent_1] == self.ranks[parent_2]:
                self.ranks[parent_1] += 1
        else:
            # Path compressed union
            self.parents[member_1] = parent_2
            self.parents[parent_1] = parent_2
        return None

