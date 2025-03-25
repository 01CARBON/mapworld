from src.mapworld.maps import BaseMap

class ADEMap(BaseMap):

    def __init__(self, m: int = 3, n: int = 3, n_rooms: int = 9, target_distr: list[int] = [1]):
        """
        Set up a base 2-D graph whose nodes are based on ADE20k dataset.
        
        Args:
            m: Number of rows in the graph.
            n: Number of columns in the graph
            n_rooms: Required number of rooms. Should be less than n*m
            target_distr: List of integers to control ambiguity. Example: [3,2] means - at
            least two types of potential target categories, and that
            the first will occur three times, and the second twice.

        Raises:
            ValueError: If any value is unset
            AssertionError: If `n_rooms` > `n*m`
        """
        super().__init__(m, n, n_rooms)
        self.distribution = target_distr

    
    def assign_types(self, G):
        """
        Assign room categories and images to the nodes in the generated graph.

        Args:
            G: Generated graph. (via BaseMap.create_acyclic_graph()/BaseMap.create_cyclic_graph())
        """
        pass


if __name__ == '__main__':

    ademap = ADEMap(3, 3, 5, [1,1])
    G = ademap.create_cyclic_graph(1)
    ademap.plot_graph(G)





