from src.mapworld.maps import BaseMap
import os
import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast

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

        # TODO: Fix ambiguity = None case
        if not ambiguity:
            ambiguity = [1]
        
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
    
    def assign_images(self, G, json_path: str = os.path.join("src", "mapworld", "images.json")):
        """
        Assign Images from ADE20k dataset to a graph whose nodes have already been assigned a specific room type

        Args:
            G: networkx type graph containing node info - {type, base_type, target}
            json_path: Path to a jsonn file containing mappping of room_types to various images

        Return:
            G: updated networkx graph with randomly assigned image of a specific room_type
        """

        with open(json_path, 'r') as f:
            json_data = json.load(f)

        images_assigned = []
        for node in G.nodes():
            room_type = G.nodes[node]['type']
            random_image = np.random.choice(json_data[room_type])
            while random_image in images_assigned:
                random_image = np.random.choice(json_data[room_type])
            
            G.nodes[node]['image'] = random_image

        #TODO: ADE20k categories are well-defined. Can make MapWorld with real-world constraints
        # Maybe add constraints like "h/hallway" should be in between nodes of "indoor/targets" etc..
        # Or "s/street" should be strictly between "g/garage" and a category from "sports_and_leisure" or "transportation" etc..

        return G
    

    def print_mapping(self, G):
        """
        Print a mapping of node: room_type - image_url for all nodes in the graph
        """
        for this_node in G.nodes():
            print('{}: {} - {:>50}'.format(this_node,
                                         G.nodes[this_node]['type'],
                                         G.nodes[this_node]['image']))
            
    def plot_graph(self, G):
        node_labels = {node: G.nodes[node]['type'] for node in G.nodes()}
        pos = {n: n for n in G.nodes()}

        nx.draw_networkx_nodes(G, pos, node_shape='s', node_color='blue')
        nx.draw_networkx_edges(G, pos)
        
        # Adjust label positions slightly
        label_pos = {k: (v[0], v[1] + 0.2) for k, v in pos.items()}
        nx.draw_networkx_labels(G, label_pos, labels=node_labels, font_size=10)

        plt.axis('off')
        plt.show()
        
    def plot_agent_graph(self, G, agent_pos, target_pos):
        """
        BUG - Fails when no outdoor room is present in the graph...

        Plot a graph showing locations of agent position and target room

        Args:
            G: networkx type graph
            agent_pos = Current positon of Agent - [x,y]/node
            target_pos = Position of Target room - [x,y]/node
        """
        node_labels = {node: G.nodes[node]['type'] for node in G.nodes()}
        pos = {n: n for n in G.nodes()}

        nx.draw_networkx_nodes(G, pos, node_shape='s', node_color='lightblue')
        nx.draw_networkx_edges(G, pos)

        label_pos = {k: (v[0], v[1] + 0.2) for k, v in pos.items()}
        nx.draw_networkx_labels(G, label_pos, labels=node_labels, font_size=10)

        # Draw custom agent and target nodes over main graph
        nx.draw_networkx_nodes(G, pos, nodelist=[agent_pos], node_color='blue', node_shape='o', node_size=300)
        nx.draw_networkx_nodes(G, pos, nodelist=[target_pos], node_color='black', node_shape='s', node_size=600)

        custom_labels = {
            agent_pos: "agent",
            target_pos: "target"
        }
        custom_label_pos = {k: (v[0], v[1] - 0.2) for k, v in pos.items() if k in custom_labels}
        nx.draw_networkx_labels(G, custom_label_pos, labels=custom_labels, font_size=9, font_color='black')

        plt.axis('off')
        plt.show()

    def to_fsa_def(self, G):
        """
        Finite State Automata I guess, with transitions and states(nodes?)...
        returns transitions, states, initialpos, initial_room_type
        """

        transitions = []
        graph_nodes = []

        for source in G.nodes():
            for dest in G.nodes():
                if (source[0]+1, source[1]) == dest:
                    transitions.append(
                        {
                            'source': str(source),
                            'dest': str(dest),
                            'trigger': 'e'
                        }
                    )
                elif (source[0]-1, source[1]) == dest:
                    transitions.append(
                        {
                            'source': str(source),
                            'dest': str(dest),
                            'trigger': 'w'
                        }
                    )
                elif (source[0], source[1]+1) == dest:
                    transitions.append(
                        {
                            'source': str(source),
                            'dest': str(dest),
                            'trigger': 'n'
                        }
                    )
                elif (source[0], source[1]-1) == dest:
                    transitions.append(
                        {
                            'source': str(source),
                            'dest': str(dest),
                            'trigger': 's'
                        }
                    )
            G.nodes[source]['id'] = source
            graph_nodes.append(G.nodes[source])

        initial_node = np.random.choice([str(n) for n in G.nodes()])
        initial_type = G.nodes[ast.literal_eval(initial_node)]['type']
        
        return {'transitions': transitions, 'nodes': graph_nodes,
                'initial': str(ast.literal_eval(initial_node)), 'initial_type': initial_type} # 'initial' in str format and not np.str...ref - https://github.com/clp-research/sempix/blob/master/03_Tasks/MapWorld/maps.py

    def metadata(self, G):
        """
        Get metadata related to the Grpah (specifically for textmapworld rightnow...)
        """

        pass
    
if __name__ == '__main__':

    ademap = ADEMap(4, 4, 10)
    G = ademap.create_acyclic_graph()
    G = ademap.assign_types(G, ambiguity=[2,2])
    G = ademap.assign_images(G)
    # ademap.plot_graph(G)
    # ademap.plot_agent_graph(G)

    tr = ademap.to_fsa_def(G)
    print(tr)



