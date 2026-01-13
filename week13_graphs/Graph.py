# Jackson Horan
# COMP 271
# Simple graphs - week 13


### Enviroment contstants ###
DEFAULT_GRAPH_DIM = 4
INFINITY = float('inf')
NEG_INFINITY = float('-inf')
NO_EDGE_VALUE = 0


### Part 1 ###
    
def is_edge(matrix: list[list[int]], u: int, v: int) -> bool:
    """Returns True if an edge exists at a given index of an adjacency matrix.

    Args:
        matrix (list[list[int]]): The adjacency matrix
        u (int): row
        v (int): collumn

    Returns:
        bool: True if is the value is not equal to the no edge constant
    """
    return (matrix[u][v] != NO_EDGE_VALUE)

def describe(matrix: list[list[int]]):
    """Prints the number of vertices, edges, as well as the index and value of
    the longest and shortest edge in the adjacency matrix.

    Args:
        matrix (list[list[int]]): The adjacency matrix
    """
    short_edge_index, short_edge_length = get_short_edge(matrix)
    long_edge_index, long_edge_length = get_long_edge(matrix)
    print(f"""\ 
        Number of vertices: {len(matrix)}
        Number of edges: {count_edge(matrix)}
        Shortest Edge:
            Index: {short_edge_index}
            Length: {short_edge_length}
        Longest Edge:
            Index: {long_edge_index}
            Length: {long_edge_length}
        """)

def count_edge(matrix: list[list[int]]) -> int:
    """Return the number of edges in an adjacency matrix.

    The method only iterates through the upper triangle to eliminate instances
    of double counting. However it still operates in O(n^2).

    Args:
        matrix (list[list[int]]): The adjacency matrix.

    Returns:
        int: The number of edges in the adjacency matrix.
    """
    edge = 0
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix[i])):
            if is_edge(matrix, i, j):
                edge += 1
    return edge

def get_long_edge(matrix: list[list[int]]) -> tuple[tuple, int]:
    """Returns the index and value of the longest edge in an adjacency matrix.

    The method only iterates through the upper triangle to eliminate instances
    of double counting. However it still operates in O(n^2).

    Args:
        matrix (list[list[int]]): The adjacency matrix.

    Returns:
        tuple[tuple, int]: The index as a tuple and the value at that index.
    """
    long_value = NEG_INFINITY
    index: tuple
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if is_edge(matrix, i, j):
                length = matrix[i][j]
                if length > long_value:
                    index = (i, j)
                    long_value = length
    return index, long_value

def get_short_edge(matrix: list[list[int]]) -> tuple[tuple, int]:
    """Returns the index and value of the shortest edge in an adjacency matrix.

    The method only iterates through the upper triangle to eliminate instances
    of double counting. However it still operates in O(n^2).

    Args:
        matrix (list[list[int]]): The adjacency matrix.

    Returns:
        tuple[tuple, int]: The index as a tuple and the value at that index.
    """
    short_value = INFINITY
    index: tuple
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if is_edge(matrix, i, j):
                length = matrix[i][j]
                if length < short_value:
                    index = (i, j)
                    short_value = length
    return index, short_value
    # return the index of the vertex with the most neighbors

def find_popular(matrix: list[list[int]]) -> int:
    """Return the index of the vertex with the most neighbors.

    The method searches the entire 

    Args:
        matrix (list[list[int]]): The adjacency matrix.

    Returns:
        int: The index of the most popular vertex.
    """
    highest_degree = 0
    index: int
    for i in range(len(matrix)):
        degree = 0
        for j in range(len(matrix[i])):
            if is_edge(matrix, i, j):
                degree += 1
        if highest_degree < degree:
            highest_degree = degree
            index = i
    return index



### Part 2 ###

class Graph:
    def __init__(self,
                n: int = DEFAULT_GRAPH_DIM,
                no_edge: int | None = NO_EDGE_VALUE
                ) -> None:
        """Adjacency Matrix representation of a graph.

        Args:
            n (int, optional): The sqaure dimension of the graph. Defaults to 
            DEFAULT_GRAPH_DIM.
            no_edge (constant, optional): Constant for enviroment wide no edge
            value . Defaults to NO_EDGE_VALUE.
        """
        self._edges = 0
        self._n = n
        self._no_edge = no_edge
        self._short_edge = [None, None]
        self._long_edge = [None, None]
        self._graph = [[self._no_edge for _ in range(self._n)] 
                       for _ in range(self._n)]

    def __str__(self) -> str:
        """Text representation of the graph.

        Returns:
            str: number of vertices, edges, the longest edge index and value, 
            and the shortest edge index and value.
        """
        return (f"""\ 
        Number of vertices: {len(self._graph)}
        Number of edges: {self._edges}
        Shortest Edge:
            Index: {self._short_edge}
            Length: {self._graph[self._short_edge[0]][self._short_edge[1]]}
        Longest Edge:
            Index: {self._long_edge}
            Length: {self._graph[self._long_edge[0]][self._long_edge[1]]}
        """)

    def get_weight(self, u: int, v: int) -> int:
        """Returns the weight of a given edge in the adjacency matrix.

        Args:
            u (int): The row index in the adjacency matrix
            v (int): The collumn index in the adjacency matrix

        Returns:
            int: The weight of given edge.
        """
        return self._graph[u][v]

    def add_edge(self, u: int, v: int, weight: int):
        """Adds the edge between vertices u and v to the adjacency matrix.

        Args:
            u (int): The index of a vertex.
            v (int): The index of a vertex.
            weight (int): The weight of the new edge between vertices u and v.

        Raises:
            IndexError: If the vertex paramerters are out of range or the weight
            is negative.
        """
        if self._check_args(u, v, weight):
            self._graph[u][v] = weight
            self._graph[v][u] = weight
            self._check_length(u,v)
            self._edges += 1
        else: 
            raise IndexError("Given arguments are not valid indecies or weight")

    def adjust_edge(self, u: int, v: int, weight: int):
        """Modifies the weight of the edge between vertices u and v.

        Args:
            u (int): A vertex in the adjacency matrix
            v (int): A vertex in the adjacency matrix.
            weight (int): the new weight value.

        Raises:
            ValueError: If the edge does not already exist in the adjacency 
            matrix.
            IndexError: If the vertex arguments are out of range or the weight
            is negative.
        """
        if not self._check_args(u, v, weight):
            raise IndexError("Given arguments are not valid indecies or weight")
        if not self.edge_exists(u, v):
            raise ValueError("Given arguments do not correspond to a viable\
                              edge.")
        if self.get_weight(u, v) != weight:
            self._graph[u][v] = weight
            self._graph[v][u] = weight
            self._check_length(u, v)

    def remove_edge(self, u: int, v: int):
        """Removes the edge between vertices u and v.

        Args:
            u (int): A vertex in the adjacency matrix.
            v (int): A vertex in the adjacency matrix.

        Raises:
            ValueError: If the edge does not already exist in the adjacency 
            matrix.
            IndexError: If the vertex arguments are out of range or the weight
            is negative.
        """
        if self._check_args(u, v):
            if self.edge_exists(u, v,):
                self._graph[u][v] = self._no_edge
                self._graph[v][u] = self._no_edge
                self._check_length(u,v)
                self._edges -= 1
            else:
                raise ValueError("Given arguments do not correspond to a\
                                  viable edge.")
        else: 
            raise IndexError("Given arguments are not valid indecies or weight")

    def edge_exists(self, u: int, v: int) -> bool:
        """Returns true is the edge between vertices u and v exists.

        Args:
            u (int): A vertex in the adjacency matrix.
            v (int): A vertex in the adjacency matrix.

        Returns:
            bool: True if the edge is found in the adjacency matrix.
        """
        return self._graph[u][v] != self._no_edge

    def _check_args(self, u: int, v: int, weight = None) -> bool:
        """Returns True if vertex values are in range and weight is positive.

        Args:
            u (int): A vertex in the adjacency matrix.
            v (int): A vertex in the adjacency matrix.
            weight (int, optional): The weight of an edge. Defaults to None.

        Returns:
            bool: True if arguments are valid.
        """
        status: bool = True
        if u >= self._n or v >= self._n or u < 0 or v < 0:
            status = False
        elif weight is not None and weight < 0:
            status = False
        return status
    
    def _check_length(self, u: int, v: int):
        """Recompute the shortest and longest edge in the adjacency matrix.
        
        This method is called every time a new edge is added, a current edge is 
        modified or deleted. The method searches the upper triangle of the 
        matrix in O(n^2)

        Args:
            u (int): A vertex in the adjacency matrix.
            v (int): A vertex in the adjacency matrix.
        """
        short_val = INFINITY
        long_val = NEG_INFINITY
        short_idx = [None, None]
        long_idx = [None, None]
        for i in range(self._n):
            for j in range(i + 1, self._n):
                w = self._graph[i][j]
                if w != self._no_edge:
                    if w < short_val:
                        short_val = w
                        short_idx = [i, j]
                    if w > long_val:
                        long_val = w
                        long_idx = [i, j]
        self._short_edge = short_idx
        self._long_edge = long_idx


if __name__ == "__main__":
    x = [
        [0,0,1,0,3,55],
        [0,0,12,0,0,7],
        [1,12,0,8,2,0],
        [0,0,8,0,14,9],
        [3,0,2,14,0,1],
        [55,7,0,9,11,0]
    ]

    print(describe(x))
    print(find_popular(x))

