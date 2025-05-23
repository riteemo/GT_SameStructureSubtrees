from typing import List, Set, Tuple
import networkx as nx
from networkx.algorithms import isomorphism
from utils import *


def _filter_by_structure(
        pattern_edges: List[Tuple[int, int]],
        G_main: nx.Graph,
        matches: List[List[int]],
        G_pattern: nx.Graph
) -> List[List[int]]:
    """
    Фильтрует найденные подграфы, оставляя только те, в которых структура (иерархия) совпадает с паттерном.
    :param pattern_edges: список ребер в паттерне (как parent -> child)
    :param G_main: граф основного дерева
    :param matches: найденные совпадения (каждое — список узлов из G_main)
    :param G_pattern: граф паттерна
    """
    valid_matches = []

    for match_nodes in matches:
        if len(match_nodes) != G_pattern.number_of_nodes():
            continue  # по размеру не совпадает

        # сопоставим вершины паттерна и основного дерева по индексам
        pattern_nodes = list(G_pattern.nodes())
        mapping = dict(zip(pattern_nodes, match_nodes))
        inverse_mapping = {v: k for k, v in mapping.items()}

        is_valid = True
        for parent_p, child_p in pattern_edges:
            parent_m = mapping[parent_p]
            child_m = mapping[child_p]

            # 1. Проверка существования ребра в основном графе
            if not G_main.has_edge(parent_m, child_m):
                is_valid = False
                break

            # 2. Проверка, что parent действительно ближе к корню, чем child
            # Выполним BFS от parent_m и убедимся, что мы можем дойти до child_m
            visited = set()
            queue = [parent_m]
            found = False
            while queue:
                node = queue.pop(0)
                if node == child_m:
                    found = True
                    break
                if node in visited:
                    continue
                visited.add(node)
                queue.extend([n for n in G_main.neighbors(node) if n not in visited])
            if not found:
                is_valid = False
                break

        if is_valid:
            valid_matches.append(match_nodes)

    return valid_matches

# класс для описания дерева
class NTree:
    #@timer
    def __init__(self, edges: List[Tuple[int, int]], size: int):
        self.size = size
        self.edges = edges
        self.graph = [[] for _ in range(self.size)]

        for u, v in edges:
            self.graph[u].append(v)
            self.graph[v].append(u)

    def to_networkx_graph(self):
        G = nx.Graph()
        for u in range(self.size):
            G.add_node(u)
        for u, v in self.edges:
            G.add_edge(u, v)
        return G

    @timer
    @memory_timer
    def find_subtrees_by_structure(self, pattern_edges: List[Tuple[int, int]]) -> List[List[int]]:
        """
        Ищет все поддеревья в текущем дереве, структурно совпадающие с паттерном.
        pattern_edges — ребра паттерна (маленькое дерево для поиска).
        Возвращает список списков вершин, соответствующих найденным поддеревьям.
        """
        pattern_size = len(pattern_edges) + 1
        pattern_tree = NTree(pattern_edges, pattern_size)
        G_main = self.to_networkx_graph()
        G_pattern = pattern_tree.to_networkx_graph()

        GM = isomorphism.GraphMatcher(G_main, G_pattern,
                                      node_match=lambda n1, n2: True)  # игнорируем метки узлов
        results = []
        for subgraph_mapping in GM.subgraph_isomorphisms_iter():
            # subgraph_mapping: dict {node_main: node_pattern}
            # берем только ключи — узлы главного дерева
            subtree_nodes = list(subgraph_mapping.keys())
            results.append(subtree_nodes)

        unique_results = set()
        filtered_results = []

        for subgraph_mapping in GM.subgraph_isomorphisms_iter():
            subtree_nodes = tuple(sorted(subgraph_mapping.keys()))
            if subtree_nodes not in unique_results:
                unique_results.add(subtree_nodes)
                filtered_results.append(list(subtree_nodes))

        return _filter_by_structure(pattern_edges, G_main, filtered_results, G_pattern)


