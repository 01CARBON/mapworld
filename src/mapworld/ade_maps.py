from src.mapworld.maps import BaseMap
import os
import json
import numpy as np

class ADEMap(BaseMap):

    def __init__(self, m: int = 3, n: int = 3, n_rooms: int = 9):
        """
        Set up a base 2-D graph whose nodes are based on ADE20k dataset.
        
        Args:
            m: Number of rows in the graph.
            n: Number of columns in the graph
            n_rooms: Required number of rooms. Should be less than n*m

        Raises:
            ValueError: If any value is unset
            AssertionError: If `n_rooms` > `n*m`
        """
        super().__init__(m, n, n_rooms)

    
    def assign_types(self, G, json_path: str = os.path.join("src", "mapworld", "categories.json"), ambiguity: list[int] = [1]):
        """
        Assign room categories and images to the nodes in the generated graph.
        Example G.nodes[room] = {
            'base_type': 'indoor',
            'type': 'k/kitchen',
            'target': True
        }

        Args:
            G: Generated graph. (via BaseMap.create_acyclic_graph()/BaseMap.create_cyclic_graph())
            json_path: Path to a json file containing "targets", "outdoors" and "distractors" categories
            ambiguity: List of integers to control ambiguity. Example: [3,2] means - at
            least two types of potential target categories, and that
            the first will occur three times, and the second twice. Only applies to indoor rooms
        
        Raises:
            ValueError: if possible indoor rooms (rooms with more than 1 neighbor) < sum of ambiguity
        """
        
        outdoor_rooms = []
        indoor_rooms = []
        for room in G.nodes():
            if G.degree(room) == 1:
                outdoor_rooms.append(room)
            elif G.degree(room) > 1:
                indoor_rooms.append(room)
            else:
                raise ValueError(f"Check Graph Generation!! Found a node with no neighbors!")

        if len(indoor_rooms) < sum(ambiguity):
            raise ValueError(
                f"Ambiguity passed is {ambiguity}, But number of indoor rooms in the generated graph is {len(indoor_rooms)}"
                f"Try decreasing ambiguity such that sum of ambiguity is <= {len(indoor_rooms)}"
                f"If ambiguity is strictly required and possible with the initialized Map, try generating another random graph.")
        
        with open(json_path, 'r') as f:
            categories = json.load(f)

        outdoor_room_assigned = []
        for room in outdoor_rooms:
            # Keep ambiguity 1 for outdoor rooms
            # TODO : Add ambiguity for outdoor rooms as well, thinking specifically for EscapeRoom Game
            random_outdoor_room = np.random.choice(categories["outdoors"])
            while random_outdoor_room in outdoor_room_assigned:
                random_outdoor_room = np.random.choice(categories["outdoors"])

            outdoor_room_assigned.append(random_outdoor_room)

            G.nodes[room]['base_type'] = "outdoor"
            G.nodes[room]['type'] = random_outdoor_room
            G.nodes[room]['target'] = False     
    
        # TODO: Pass 'type' as argument as well, to pre set certain type of rooms
        # atleast 2 home_office and 2 bedrooms, for example
        
        indoor_rooms_assigned = []
        room_type_assigned = []
        for room_type in ambiguity:
            # TODO: Add check to see length of ambiguity <= len(categories["targets"])
            random_room_type = np.random.choice(categories["targets"])
            while random_room_type in room_type_assigned:
                random_room_type = np.random.choice(categories["targets"])
            room_type_assigned.append(random_room_type)

            for r in range(room_type):
                room = indoor_rooms[np.random.randint(len(indoor_rooms))]
                while room in indoor_rooms_assigned:
                    room = indoor_rooms[np.random.randint(len(indoor_rooms))]
                indoor_rooms_assigned.append(room)

                G.nodes[room]['base_type'] = "indoor"
                G.nodes[room]['type'] = random_room_type
                G.nodes[room]['target'] = True

        # Remaining nodes - as distractors
        distractor_rooms = list(set(indoor_rooms) - set(indoor_rooms_assigned))

        # Collect remaining room_types from targets and aa categories["distractors"] to it
        dist_categories = list(set(categories["targets"]) - set(room_type_assigned) | set(categories["distractors"]))

        distractor_assigned = []
        for room in distractor_rooms:
            random_distractor = np.random.choice(dist_categories)
            while random_distractor in distractor_assigned:
                random_distractor = np.random.choice(dist_categories)
            
            G.nodes[room]['base_type'] = "indoor"
            G.nodes[room]['type'] = random_distractor
            G.nodes[room]['target'] = False

        return G

if __name__ == '__main__':

    ademap = ADEMap(4, 4, 10)
    G = ademap.create_cyclic_graph(2)
    G = ademap.assign_types(G, ambiguity=[2,2])

    nodes = G.nodes()
    for n in nodes:
        print(G.nodes[n])





