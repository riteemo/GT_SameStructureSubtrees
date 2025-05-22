import random
from typing import List, Tuple
from utils import timer


# класс для генерации деревьев
class TreeGenerator:
    #@timer
    def generate_tree(self, size: int, max_children : int) -> List[Tuple[int, int]]:
        edges: List[Tuple[int, int]] = []
        children_counter = {0: 0}
        candidates = [0]  # возможные родители

        for i in range(1, size):
            parent = random.choice(candidates)
            edges.append((parent, i))

            children_counter[parent] += 1
            if children_counter[parent] == max_children:
                candidates.remove(parent)  # больше не может быть родителем

            children_counter[i] = 0
            candidates.append(i)  # новый узел может быть родителем

        return edges
