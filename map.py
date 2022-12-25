# Открываю объект TensorFile в памяти Python
# Составляю карту ссылок
# Вывожу список количества упоминаний ИО в текстах

import os, sys
import pandas as pd

from files import Tensor # объект .md файла
from folders import Folder # объект каталогов
from intel_obj import get_all_obj # собрать объекты всех наборов символов, которые буду считать словом


def refresh_relation(path=os.getcwd()) -> list:
    """
    В каждом каталоге местонахождения скрипта ищем marckdown файлы.
    """
    # tensors.clear()
    # folders.clear()
    files_and_folders_list = os.listdir(path)

    for file_or_catalog in files_and_folders_list:
        if '.md' in file_or_catalog:
            file = file_or_catalog
            file_path = path + f'\\{file}'
            tensors.append(Tensor(file_path))
        elif '.' not in file_or_catalog:
            folder = file_or_catalog
            folder_path = path + f'\\{folder}'
            refresh_relation(folder_path)
            folders.append(Folder(folder_path))
    
    def _sort(A: list) -> None:
        """
        Сортировка объектов списка А по количеству вложений. 
        Те файлы что ближе к корню запуска скрипта первые
        Те файлы что лежат в далеких папках - последние
        """
        N = len(A)
        for bypass in range(1, N):
            for k in range(0, N-bypass):
                if len(A[k].root.split('\\')) > len(A[k+1].root.split('\\')):
                    A[k], A[k+1] = A[k+1], A[k]

    _sort(tensors)
    _sort(folders)

if __name__ == '__main__':
    tensors = [] # все объекты файлов .md
    folders = [] # все объекты обобщающих каталогов/папок
    refresh_relation()

    d = get_all_obj(tensors)
    df = pd.DataFrame(dict([ (k, pd.Series(v)) for k,v in d.items() ]))
    print(df.head(7))

    print('---')
    for variable in dir():
        if '__' != variable[:2] and '__' != variable[-2:]:
            print(f'> {variable}')
    print('---')
    