# Открываю объект Tensor в памяти Python
# Составляю карту ссылок
# Вывожу список количества упоминаний ИО в текстах

import os

from files import Tensor # объект .md файла
from folders import Folder # объект каталогов
from analysis import FramesData # объект таблиц


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

def refresh_relation(path=os.getcwd()):
    """
    В каждом каталоге от местонахождения скрипта ищем marckdown файлы
    Наполняю списки tensors и folders объектами
    """
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

if __name__ == '__main__':
    tensors: list[Tensor] = [] # все объекты файлов .md
    folders: list[Folder] = [] # все объекты обобщающих каталогов/папок
    refresh_relation() # обновляю списки tensors, folders

    _sort(tensors)
    _sort(folders)

    words = FramesData(tensors) # таблица данных

    print('---')
    print("""
    tensors: list - список объектов, созданных по файлам .md
    folders: list - список объектов, созданных по каталогам
    words: FramesData - объект для анализа полученных объектов
        .df: pd.DataFrame - таблица соответвия набору символов и его объекту
    """)
    print('---')
    