import re, sys

from exceptions import exception_words_list


class CleanSymbols:
    "Очищаем базовый набор символов"
    def __init__(self, symbols) -> None:
        match symbols:
            case '' | '___': # не несет никакой информации
                sys.exit()
            case '#' | '##' | '###' | '####' | '#####' | '######': # обозначегте заголовка
                sys.exit()

        # case r'\w+\|\w+'
        if '|' in symbols: # прямая черта это символ ссылки и псевдонима в obsidian
            # [[объект|псевдоним]]
            self._symbols = re.sub("[^А-Яа-я]", "", symbols.split('|')[0]).upper()
        else:
            self._symbols = re.sub("[^А-Яа-я]", "", symbols).upper()

        if len(self._symbols) <= 1: # мне не нужны предлоги
            sys.exit()

        if self._symbols in exception_words_list:
            sys.exit()

        if self._symbols == '': # если небыло ни одного русского символа
            sys.exit()
        # --- 

class IntelligentObject(CleanSymbols):
    """
    Объект набора символов в котором:

    .root_path - в каком файле этот набор символов
    .symbols - символы по которым создается объект
    .row_number - в какой строке встречается
    .number_in_row - какое по счету слово
    """
    def __init__(self, root_path: str, symbols_set: str, row_number: int, number_in_row: int) -> None:        
        # --- Проверка и очистка символов
        super().__init__(symbols_set)
        self.root_path = root_path # где встретился
        self.symbols = symbols_set # исходные символы для объекта
        self.row_number = row_number # в какой строке
        self.number_in_row = number_in_row # порядковый номер в строке

    def __repr__(self) -> str:
        return self._symbols
