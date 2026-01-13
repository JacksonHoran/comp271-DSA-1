from math import *
class MyFirstPriorityQueue:
    """A heap-based priority queue implementation."""

    DEFAULT_CAPACITY = 10

    def __init__(self, capacity:int = DEFAULT_CAPACITY):
        """Initialize an empty priority queue."""

        self._capacity = capacity
        self._underlying: list[int] = [None] * self._capacity
        self._size = 0

    def __bool__(self) -> bool:
        """Returns False if the queue is empty. """
        return not self.is_empty()

    def __str__(self) -> str:
        """Return a user-friendly string representaiton of the class using
        f-strings."""
        if self.is_empty():
            return "MyFirstPriorityQueue([])"
        elements = self._underlying[:self._size]
        return f"MyFirstPriorityQueue({elements})"

    def __len__(self) -> int:
        """Return a non-negative integer with the number of items stored in the
        object."""
        return self.size()

    def is_empty(self) -> bool:
        """Returns True if priority queue is empty, false otherwise

        Returns:
            bool: true if size attribute equal to 0, false otherwise
        """
        return (self._size) == 0


    def size(self) -> int:
        """Getter method for size attribute. Size is the number of elements in
        the underlying array.

        Returns:
            int: _description_
        """
        return self._size

    def add(self, value: int):
        """Adds item to the priority queue. 

        Uses sift up algorithm to move the new item to the correct location in
        the max heap.

        Args:
            value (int): The value to be added to the priority queue.

        Raises:
            Exception: If the queue is full.
        """
        if self._size >= self._capacity:
            raise Exception("Priority queue is full.")
        self._underlying[self._size] = value
        self._size += 1
        self._sift_up(self._size - 1)

    def extract(self) -> int:
        """Remove and return the most important item in the queue.

        Raises:
            Exception: If priority queue is empty.

        Returns:
            int: The most important item in the priority queue.
        """
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        most_imp = self._underlying[0]
        self._underlying[0] = self._underlying[self._size - 1]
        self._underlying[self._size - 1] = None
        self._size -= 1
        self._sift_down(0)
        return most_imp

    def peek(self) -> int:
        """Return but not remove the most important value in the maximum heap
        priority queue.

        Raises:
            IndexError: If underlying array is empty.

        Returns:
            int: Most important value in priority queue.
        """
        if self.is_empty():
            raise IndexError("Priority Queue is empty.")
        return self._underlying[0]

    def peek_next(self) -> int:
        """Return but not remove the second most important value in the maximum
        heap priority queue.

        Raises:
            IndexError: If underlying array is empty.

        Returns:
            int: Second most important value in priority queue.
        """
        if self._size < 2:
            raise IndexError("Not enough items to peek next.")
        left = self._left_child(0)
        right = self._right_child(0)
        return max(self._underlying[left], self._underlying[right])

    def _swap(self, position, with_position):
        """Swaps positions between two elements in the list.

        Args:
            position (int): index of list item you want to swap
            with_position (int): index of list item you want to swap
        """
        temp = self._underlying[position]
        self._underlying[position] = self._underlying[with_position]
        self._underlying[with_position] = temp

    def _left_child(self, parent: int) -> int:
        """Compute and return the array index of a parent's left child.

        Uses the array-based heap property that a parent at index 'i' has a 
        left child located at (2 * i + 1)

        Args:
            parent (int): index of parent node

        Returns:
            int | None: returns the array index of left child node
        """
        return 2 * parent + 1

    def _right_child(self, parent: int) -> int:
        """Compute and return the array index of a parent's right child.

        Uses the array-based heap property that a parent at index 'i' has a 
        right child located at (2 * i + 2)

        Args:
            parent (int): index of parent node

        Returns:
            int: returns the array index of right child node
        """
        return 2 * parent + 2
    
    def _parent(self, child: int) -> int:
        """Compute and return the array index of a child's parent

        Uses the array-based heap property that a child at index 'i' has a 
        parent located at (i - 1) // 2

        
        Args:
            child (int): index of a node in the array-based heap

        Raises:
            ValueError: if child argument is less than or equal to 0, since the
            root node does not have a parent

        Returns:
            int: index of a child's parent node
        """
        if child <= 0:
            parentIndex = None
        else:
            parentIndex = (child - 1) // 2
        return parentIndex

    def _sift_down(self, parent: int):
        """Move a node downward to restore the max heap property.

        This method is called when the root node is removed or is replaced with 
        the last element in the array. The method compares the value of the 
        parent with its children swapping as needed when the max-heap propert is
        violated. The method operates in O(Log(n)) time complexity. 

        Args:
            parent (int): index of the parent node to start at, typically the
            root node.
        """
        left = self._left_child(parent)
        right = self._right_child(parent)
        correct_parent = parent

        if (left < self._size and self._underlying[left] > 
            self._underlying[correct_parent]):
            correct_parent = left
        if (right < self._size and self._underlying[right] > 
            self._underlying[correct_parent]):
                correct_parent = right
        if correct_parent != parent:
            self._swap(parent, correct_parent)
            self._sift_down(correct_parent)
        
    def _sift_up(self, child: int):
        """Move a node upward to restore the max heap property.

        This method is called when an element is placed at the end of the array.
        The method compares the value of the parent with its children swapping
        as needed when the max-heap property is violated. The method operates 
        in O(log(n)) time complexity.

        Args:
            child (int): Index of the node to start at, typically the last item
            in the array.
        """
        if child == 0:
            return
        parent = self._parent(child)
        if self._underlying[parent] < self._underlying[child]:
            self._swap(child, parent)
            self._sift_up(parent)


    def pretty_print(self, width: int=None):
        """Print the queue as a pyramid to visualize the heap.
        
        Source:
            https://gist.github.com/ydm/4f0c948bc0d151631621

        Args:
            width (int, optional): Determines spacing if needed. Defaults to 
            None.
        """
        heap = [item for item in self._underlying if item is not None]
        if not heap:
            print("Heap is empty.")
            return
        first = lambda h: 2**h - 1      
        last = lambda h: first(h + 1)
        level = lambda heap, h: heap[first(h):last(h)]
        prepare = lambda e, field: str(e).center(field)
        if width is None:
            width = max(len(str(e)) for e in heap)
        height = int(log(len(heap), 2)) + 1
        gap = ' ' * width
        for h in range(height):
            below = 2 ** (height - h - 1)
            field = (2 * below - 1) * width
            print(gap.join(prepare(e, field) for e in level(heap, h)))
        print()
        print("----------------------------")
