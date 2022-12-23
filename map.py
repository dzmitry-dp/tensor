# Открываю объект TensorFile в памяти Python
# Составляю карту ссылок
# Вывожу список количества упоминаний ИО в текстах
import os
from threading import Thread

class Controller:
    """Класс контроллеза за конечными данными"""
    def buble_sort(A: list) -> None:
        """
        Функция сортирует массив, который в нее отправлен
        """
        N = len(A)
        for bypass in range(1, N):
            for k in range(0, N-bypass):
                if len(A[k].head.split('\\')) > len(A[k+1].head.split('\\')):
                    A[k], A[k+1] = A[k+1], A[k]

class TensorFile:
    """Класс определяющий объект файла, как набор векторов. Каждый абзац - новый вектор"""
    def __init__(self, path_to_file):
        self.path_to_file: str = path_to_file # путь к файлу по которому создан объект
        self.head: str = self.path_to_file[len(os.getcwd()):] # относительный путь к файлу
        self._symbols: str = None # все символы, которые записаны в файлк
        self._rows_list: list[str,] = None # список, где элементом списка являетсяя строка

    @property
    def rows_list(self):
        if self._rows_list is None:
            self._rows_list = self.symbols.split('\n')
        return self._rows_list

    @property
    def symbols(self):
        if self._symbols is None:
            with open(self.path_to_file, encoding='utf-8') as file:
                self._symbols = file.read()
        return self._symbols

    def __repr__(self):
        return self.path_to_file[len(os.getcwd()):]

def refresh_files_in_tensors_list(path=os.getcwd()) -> list:
    files_and_folders_list = os.listdir(path)

    for file_or_catalog in files_and_folders_list:
        if '.md' in file_or_catalog:
            file = file_or_catalog
            file_path = path + f'\\{file}'
            tensor_obj = TensorFile(file_path)
            tensors_list.append(tensor_obj)
        elif '.' not in file_or_catalog:
            folder = file_or_catalog
            folder_path = path + f'\\{folder}'
            tensor_obj = refresh_files_in_tensors_list(folder_path)
    return tensors_list

def draw_map() -> list:
    """Устанавливает наличие слов в текстах и возвращает список интеллектуальных объектов из всех текстов"""
    word_objects_list = [] # список всех объектов которые созданы для слов
    
    def func(obj):
        print(obj.head)
    
    thread_list = []
    for idx in range(len(tensors_list)):
        thread = Thread(target=func, args=[tensors_list[idx]], name=idx)
        thread.start()
        thread_list.append(thread)

    for t in thread_list:
        t.join()

    return word_objects_list

if __name__ == '__main__':
    tensors_list = []
    refresh_files_in_tensors_list()
    Controller.buble_sort(tensors_list)
    draw_map()

    print('---')
    for variable in dir():
        if '__' != variable[:2] and '__' != variable[-2:]:
            print(f'> {variable}')
    print('---')
    