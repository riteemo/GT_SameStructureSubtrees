from typing import List, Set, Tuple
import networkx as nx
from networkx.algorithms import isomorphism
from collections import deque
from utils import *


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

        return filtered_results