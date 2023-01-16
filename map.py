# Открываю объект Tensor в памяти Python
# Составляю карту ссылок
# Вывожу список количества упоминаний ИО в текстах

import os

from app.obj.files import File # объект .md файла
from app.obj.folders import Folder # объект каталогов
from app.analysis import Frames # объект таблиц


def _sort(A: list) -> None:
    """
    Сортировка объектов списка А по количеству вложений. 
    Те файлы что ближе к корню запуска скрипта первые
    Те файлы что лежат в далеких папках - последние
    """
    N = len(A)
    for bypass in range(1, N):
        for k in range(0, N - bypass):
            if len(A[k].root.split('\\')) > len(A[k+1].root.split('\\')):
                A[k], A[k+1] = A[k+1], A[k]

def get_snapshot_files_and_folders(path=os.getcwd()):
    """
    В каждом каталоге от местонахождения скрипта ищем marckdown файлы
    Наполняю списки tensors и folders объектами
    """
    files_and_folders_list = os.listdir(path)

    for file_or_catalog in files_and_folders_list:
        if '.md' in file_or_catalog:
            file = file_or_catalog
            file_path = path + f'\\{file}'
            _files.append(File(file_path))
        elif '.' not in file_or_catalog:
            folder = file_or_catalog
            folder_path = path + f'\\{folder}'
            _folders.append(Folder(folder_path))
            get_snapshot_files_and_folders(folder_path)

if __name__ == '__main__':
    _files: list[File] = [] # все объекты файлов .md
    _folders: list[Folder] = [] # все объекты обобщающих каталогов/папок
    get_snapshot_files_and_folders() # обновляю списки tensors, folders

    _sort(_files)
    _sort(_folders)

    words = Frames(_files) # таблица данных

    print('---')
    print("""
    _files: list - список объектов, созданных по файлам .md
    _folders: list - список объектов, созданных по каталогам
    words: Frames - объект для анализа слов в текстовых сообщениях
        .df: pd.DataFrame - таблица соответвия набору символов и python объектов
        .essences: pd.DataFrame - таблица связанных объектов pyhton
    """)
    print('---')
    