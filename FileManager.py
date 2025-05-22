from typing import List, Tuple


# класс для работы с файлом
class FileManager:
    # сохранение в файл
    def save_graph(self, edges : List[Tuple[int, int]], filename : str) -> None:
        with open(filename, 'w') as file:
            for row in edges:
                file.write(' '.join(map(str, row)) + '\n')

    # чтение из файла
    def read_graph(self, filename : str) -> List[Tuple[int, int]]:
        with open(filename, 'r') as file:
            return [tuple(map(int, line.strip().split())) for line in file]