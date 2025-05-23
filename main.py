from TreeGenerator import TreeGenerator
from FileManager import FileManager
from NTree import NTree
from TreeVisualizer import TreeVisualizer


def input_edges():
    print("Input the number of edges and list of edges")
    n = int(input("Input the number of edges: "))
    edges = []
    for _ in range(n):
        u, v = map(int, input("Edge (separate nodes by a space): ").split())
        edges.append((u, v))
    return edges

# Дано н-арное дерево. Найти все поддеревья, структура которых совпадает с заданной.
def main():
    generator = TreeGenerator() # объект генерации дерева
    file_manager = FileManager() # объект для работы с файлами
    visualizer = TreeVisualizer() # объект для визуализации

    filename = "tree.txt"
    edges = None # переменная для хранения ребер
    tree = None
    n = 0 # количество вершин в дереве
    arity = 0 # арность дерева

    while True:
        print("\nMenu:")
        print("1 — Generate the tree") # генерация дерева
        print("2 — Load tree from file") # загрузка из файла
        print("3 — Show the tree") # визуализация дерева
        print("4 — Find subtrees with same structure") # найти поддеревья, исключив заданные вершины
        print("5 — Save tree to file") # сохранение в файл
        print("0 — Exit")

        try:
            choice = input("Choose: ")

            if choice == "1":
                try:
                    n = int(input("Input number of vertices: "))
                    if n <= 0:
                        raise ValueError("The number of vertices must be positive")
                    arity = int(input("Input the arity of the tree: "))
                    if arity < 1:
                        raise ValueError("The minimum arity of the tree is 1")
                    edges = generator.generate_tree(n, arity)
                    tree = NTree(edges, n)
                    print("Tree is generated.")
                except ValueError as e:
                    print(f"Invalid value: {e}")

            elif choice == "2":
                try:
                    filename = input("Enter the filename + .txt: ")
                    edges = file_manager.read_graph(filename)
                    n = len(edges) + 1
                    tree = NTree(edges, n)
                    print(f"The tree is loaded from {filename}")
                except FileNotFoundError:
                    print("File not found")
                except Exception as e:
                    print(f"Error loading: {e}")

            elif choice == "3":
                if tree:
                    print("Full tree: ")
                    visualizer.print_tree(tree.graph, list(range(n)), 0)
                else:
                    print("Firstly load or generate the tree")

            elif choice == "4":
                if tree is None:
                    print("Firstly load or generate the tree")
                    continue
                print("The pattern should be a small tree with vertices numbered from 0 to number of edges inclusive")
                print("Enter the number of edges of the pattern: ")
                try:
                    m = int(input())
                    if m < 0:
                        raise ValueError("The number of edges must be positive")

                    pattern_size = m + 1
                    print(f"Enter the edges of the pattern (each edge is two numbers from 0 to {pattern_size - 1} separated by a space):")
                    pattern_edges = []

                    for _ in range(m):
                        u, v = map(int, input().split())
                        if not (0 <= u < pattern_size) or not (0 <= v < pattern_size):
                            raise ValueError(f"The vertex {u} or {v} extends beyond the boundaries of the pattern (0..{pattern_size - 1})")

                        pattern_edges.append((u, v))
                    matches = tree.find_subtrees_by_structure(pattern_edges)

                    if not matches:
                        print("No subtrees with this structure were found")

                    else:
                        #print(f"Found {len(matches)} of subtrees with this structure:")
                        #for i, subtree_nodes in enumerate(matches, 1):
                            #print(f"{i}: vertices {sorted(subtree_nodes)}")
                        visualizer.visualize(tree.graph, matches)
                except ValueError as e:
                    print(f"Wrong input: {e}")

            elif choice == "5":
                if edges is not None:
                    try:
                        filename = input("Enter the filename + .txt: ")
                        file_manager.save_graph(edges, filename)
                        print(f"The tree is saved to {filename}")
                    except Exception as e:
                        print(f"Error saving: {e}")
                else:
                    print("Firstly load or generate the tree")

            elif choice == "0":
                print("Bye!")
                break

            else:
                print("Invalid input")

        except Exception as e:
            print(f"You've ruined everything. So what did you get in return? \nError text: {e}")

if __name__ == "__main__":
    main()