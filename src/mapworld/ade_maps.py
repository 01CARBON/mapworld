from src.mapworld.maps import BaseMap

class ADEMap(BaseMap):

    def __init__(self, m: int = 3, n: int = 3, n_rooms: int = 9):
        """
        Set up a base 2-D graph, assign cycles in the graph if required 
        
        Args:
            m: Number of rows in the graph.
            n: Number of columns in the graph
            n_rooms: Required number of rooms. Should be less than n*m

        Raises:
            ValueError: If any value is unset
            AssertionError: If `n_rooms` > `n*m`
        """
        super().__init__(m, n, n_rooms)


temp = ADEMap().create_acyclic_graph()
print(temp)

