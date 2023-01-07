import os

class Tensor:
    """Класс определяющий объект файла, как набор векторов.
    Каждый абзац - новый вектор
    
    Поля:
        .path_to_file - путь к файлу
        .head - последовательность ИО к этому файлу
        symbols - строка из всех символов в файле
        rows_list - список строк файла 
    """
    def __init__(self, path_to_file) -> None:
        self.path_to_file: str = path_to_file # путь к файлу по которому создан объект
        self.root: str = path_to_file[len(os.getcwd()):] # относительный путь к файлу
        self._symbols: str = None # все символы, которые записаны в файлк
        self._rows_list: list[str,] = None # список строк из файла

    @property
    def rows_list(self):
        "Список из строк"
        if self._rows_list is None:
            self._rows_list = self.symbols.split('\n')
        return self._rows_list

    @property
    def symbols(self):
        "Все символы в файле"
        if self._symbols is None:
            with open(self.path_to_file, encoding='utf-8') as file:
                self._symbols = file.read()
        return self._symbols

    def __repr__(self):
        return self.path_to_file[len(os.getcwd()):]
