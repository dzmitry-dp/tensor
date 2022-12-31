import re, sys
from threading import Thread

from exception_words import exception_words_list


class IntelligentObject:
    """
    Объект набора символов в котором:

    .root - в каком файле этот набор символов
    .symbols - символы по которым создается объект
    .row_number - в какой строке встречается
    .word_number_in_row - какое по счету слово
    """
    def __init__(self, root: str, symbols: str, row_number: int, word_number_in_row: int) -> None:
        self.root = root # где встретился
        self.symbols = symbols # символы по которым собирается объект
        self.row_number = row_number # в какой строке
        self.word_number_in_row = word_number_in_row # порядковый номер в строке
        
        if '|' not in symbols: # прямая черта это символ ссылки и псевдонима в obsidian
            self._symbols = re.sub("[^А-Яа-я]", "", symbols).upper()
        else:
            # [[объект|псевдоним]]
            self._symbols = re.sub("[^А-Яа-я]", "", symbols.split('|')[0]).upper()

        if self._symbols in exception_words_list:
            sys.exit()

        if self._symbols == '': # если небыло ни одного русского символа
            sys.exit()

    def __repr__(self) -> str:
        return self._symbols

def get_all_obj(tensors: list) -> dict[str, list[IntelligentObject]]:
    """
    Возвращает множество интеллектуальных объектов из всех текстов.
    Соответствие 'набор_символов': [список_из_объектов]
    Внутри каждого объекта хранится информация о местах, где этот ИО находится и в каких текстах
    """

    objects_of_words: dict[str, list[IntelligentObject]] = {} # все объекты которые созданы для набора из русских символов
    
    def watch_all_rows(rows_list: list, root: str):
        "К каждой строке применяем алгоритм check_symbols_in_the_row()"

        def check_symbols_in_the_row(row: str, row_number: int):
            "Выделяем объект из символов, ограниченных' 'пробелами' '"

            def create_IO(word, row_number, word_number_in_row):
                "Превращаю слово в интеллектуальный объект"
                if len(word) <= 1: # мне не нужны предлоги
                    sys.exit()

                # остальные наборы символов можно как-то интерпретировать
                io = IntelligentObject(root, word, row_number, word_number_in_row)
                
                if io.symbols in objects_of_words.keys():
                    objects_of_words[io.symbols].append(io)
                else:
                    objects_of_words[io.symbols] = [io]
            
            # разбиваем строку на список слов
            words_list = row.split(' ')
            # для всех слов в строке
            thread_list = []
            for word_number_in_row, word in enumerate(words_list):
                match word:
                    case '' | '___': # не несет никакой информации
                        sys.exit()
                    case '#' | '##' | '###' | '####' | '#####' | '######': # обозначегте заголовка
                        sys.exit()
                    case _:
                        thread = Thread(target=create_IO, args=[word, row_number, word_number_in_row], name=f'thread_for_word-{word_number_in_row}')
                        thread.start()
                        thread_list.append(thread)

            for t in thread_list:
                t.join()

        # для каждой строки в файле
        thread_list = []
        for row_number, row in enumerate(rows_list):
            thread = Thread(target=check_symbols_in_the_row, args=[row, row_number], name=f'thread_for_row-{row_number}')
            thread.start()
            thread_list.append(thread)

        for t in thread_list:
            t.join()
    
    # для каждого объекта в списке tensors_list
    thread_list = []
    for idx, tensor in enumerate(tensors):
        thread = Thread(target=watch_all_rows, args=[tensor.rows_list, tensor.root], name=f'thread_for_tensor-{idx}')
        thread.start()
        thread_list.append(thread)

    for t in thread_list:
        t.join()
        
    return objects_of_words