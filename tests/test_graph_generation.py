from src.mapworld.world import BaseMap
from tqdm import tqdm
import logging

logging.basicConfig(
    filename="test_graph_generation.log",
    level=logging.ERROR
)

m = 99
n = 99

# Test Acyclic
for i in tqdm(range(1, m)):
    for j in range(1, n):
        n_rooms = m*n
        for k in range(1, n_rooms):
            if k <= i*j:
                try:
                    logging.info(f"Running experiment - m : {i}, n : {j}, n_rooms: {k}")
                    map = BaseMap(i, j, k)
                    map.create_acyclic_graph()
                except Exception as e:
                    logging.error(f"Acyclic graph failed for m={i}, n={j}, n_rooms={k}. Error: {repr(e)}")


# Test Cyclic
# Only fails in extreme conditions, although an exhaustive search can be amde, its quite time-consuming.
for i in range(2, m):
    for j in range(2, n):
        n_rooms = m*n
        for k in tqdm(range(4, n_rooms)):
            if k <= i*j:
                n_loops = max(1,k-3)
                for l in range(1, n_loops):
                    try:
                        logging.info(f"Running experiment - m : {i}, n : {j}, n_rooms: {k}, n_loops: {l}")
                        map = BaseMap(i, j, k)
                        map.create_cyclic_graph(n_loops=l)
                    except Exception as e:
                        logging.error(f"Cyclic graph failed for m={i}, n={j}, n_rooms={k}, n_loops: {l}. Error: {repr(e)}")