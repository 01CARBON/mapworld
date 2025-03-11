import networkx as nx
import numpy as np


class BaseMap:

    def __init__(self, m: int = 3, n: int = 3, n_rooms: int = 9, cycle: bool = False):
        """ 
        Set up a base 2-D graph, assign cycles in the graph if required 
        
        Args:
            m: Number of rows in the graph
            n: Number of columns in the graph
            n_rooms: Required number of rooms. Should be less than n*m
            cycle: Set True if the graph should contain a cycle. Requires n_rooms >= 4
        
        Raises:
            AssertionError: If `n_rooms` > `n*m`
            AssertionError: If cycle and `n_rooms` < `4`
        
        """

        assert n_rooms <= m*n, "Number of Rooms cannot exceed grid size"
        if cycle:
            assert n_rooms >= 4, "At least 4 rooms are required to setup a cycle"

        self.m = m
        self.n = n
        self.n_rooms = n_rooms
        self.cycle = cycle
        self.dir_to_delta = {
            'n': np.array([0,1]), # x, y co-ordinate system
            's': np.array([0,-1]),
            'e': np.array([1, 0]),
            'w': np.array([-1, 0])
        }

        """ 
        Create a cycle starting from the current node, depending on the size. 
        Example for a 3x3 graph, and size of 2,


        Possible solutions - 
        1) Create grpah, check cycle, add/remove cycle
        2) Create specific cyclic and acyclic graphs?? 
        
        Going with 2) option
        """

    def create_acyclic_graph(self, current_position: np.array = [0,0], G = None ):
        """
        Create an Acyclic graph
        """
        
        visited = set()
        map_grid = np.zeros((self.m, self.n))
        
        G.add_node(current_position)
        map_grid[current_position] = 1
        visited.add(tuple(current_position))

        while map_grid.sum() < self.n_rooms:
            random_step = np.random.choice(['n', 's', 'e', 'w'])
            step_delta = self.dir_to_delta[random_step]
            next_position = tuple(current_position + step_delta)
            if min(next_position) < 0 or next_position[0] >= self.m or next_position[1] >= self.n or next_position in visited:
                continue # Out of bounds position / Illegal move / Forming a cycle
                            
            map_grid[next_position] = 1
            G.add_node(next_position)
            G.add_edge(current_position, next_position) 
            current_position = next_position

        return G

    def create_cyclic_graph(self, current_position: np.array = [0,0], G = None):
        pass

    def generate_graph(self):
        """ Return a networkx based 2-D graph, based on the initialized parameters """
        G = nx.Graph()
        
        # Select a random point in the Graph to create a room/node
        # Use this as the start_position to build the graph
        current_position = np.random.randint(0, self.m),  np.random.randint(0, self.n)

        G = self.create_acyclic_graph(current_position, G)

        return G

if __name__ == '__main__':
    map = BaseMap(3, 3, 5, False)
    G = map.generate_graph()
    print(G)
