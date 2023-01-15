import pandas as pd
from itertools import chain

from config import PERCENTAGE_FOR_SYMBOLS_IN_WORD
from app.obj import get_all_obj # собрать объекты всех наборов символов, которые буду считать словом
from app.obj.intelligent import IntelligentObject # объект собраный по набору символов
from app.obj.files import File # объект .md файла

class Frames:
    """ Таблицы данных
    """
    def __init__(self, files_objects: list[File]) -> None:
        self.all_obj: dict[str, list] = get_all_obj(files_objects)
        self._df: pd.DataFrame = None # таблица соответствия символов и интеллектуальному объекту который был создан по этим символам
        self._essences: pd.DataFrame = None # таблица в которой учтены формы слова о объеденены в одну колонку

    @property
    def df(self) -> pd.DataFrame:
        if self._df is None:
            print("""
            .df - таблица где строки - это набор символов str и соответствующий этому набору символов python объект. 
            B каждой строке объекты из конкретного файла. 
            Столбцы отражают количество появлений этого набора символов в различных файлах
            """)
            self._df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in self.all_obj.items()])).fillna(0).T
        return self._df
    
    @property
    def essences(self) -> pd.DataFrame:
        if self._essences is None:
            print("""
            .essences - таблица, где в каждой строке сущность
            """)
            self._essences = self._keep_the_same_io_in_column(
                self._get_same_symbols_in_words(self.df)
                )
        return self._essences
    
    def _get_same_symbols_in_words(self, df):
        """Отслеживаю формы одного и того же слова. Если совпадает 80% символов, то ститаю что это одна сущность.
        Возвращаю pd.DataFrame где строки - это набор символов, а столбцы уникальные объекты.
        """
        def _save_one_of_two_obj():
            "Сохраняю в словарь всю строку таблицы df без 0"
            essensce_pseudonym = ''.join(e for e in essence_2.symbols if e.isalnum())
            if essensce_pseudonym not in d.keys():
                # если раньше не сохранял
                d[essensce_pseudonym] = df.iloc[j][df.iloc[j] != 0]

        def _save_objects():
            title_es_1: str = essence_1.__str__()  # символы приведенные к верхнему регистру
            title_es_2: str = essence_2.__str__() # символы в объекте с которым сравниваем
            # разные символы
            l1 = list(title_es_1) # для удобства сравнения переводим строку в список букв
            l2 = list(title_es_2) # для удобства сравнения переводим строку в список букв
            a = int(len(l1) * PERCENTAGE_FOR_SYMBOLS_IN_WORD) # % совпадений списков
            b = int(len(l2) * PERCENTAGE_FOR_SYMBOLS_IN_WORD) # % совпадений списков
            c = int((a + b)/2)
            
            pseudonym = ''.join(e for e in essence_2.symbols if e.isalnum())
            if l1[:c] == l2[:c] and len(l1[:c]) > 1 and len(l2[:c]) >1: # если совпадает 80% букв
                gluing = pd.concat([df.iloc[j][df.iloc[j] != 0], df.iloc[i][df.iloc[i] != 0]], ignore_index=True)
                if pseudonym not in d.keys():
                    # если еще не сохранялись общие строки, то соединяем и сохраняем в словаре
                    d[pseudonym] = gluing
                else:
                    # pseudonym in d.keys()
                    for _ in gluing.values:
                        if _ not in d[pseudonym].values:
                            d[pseudonym] = pd.concat([d.pop(pseudonym), pd.Series([_])], ignore_index=True)
                    
        i = 0 # фиксируем номер строки для списка всех объектов
        d = {} # создаем словарь для нового df
        # значения первой колонки в типе данных list (т.к. она всегда будет максимально заполнена данными)
        values_from_first_column: list = df[0].values.tolist() # строка в таблице df существует потому, что есть значение в этой ячейке
        while len(values_from_first_column) != 0:
            # пока список со всеми уникальными объектами не пустой
            essence_1: IntelligentObject = values_from_first_column.pop(0)  # берем всегда первый элемент из списка
            for j, essence_2 in enumerate(df[0].values):
                j: int # нумерация строк для серии табличных данных
                essence_2: IntelligentObject
                # symbols - набор символов для которого был создан объект IntelligentObject
                if essence_1 == essence_2: 
                    # если одинаковые IntelligentObject
                    _save_one_of_two_obj()
                else: 
                    # если объекты разные
                    _save_objects()
            i += 1
        return pd.DataFrame(d).fillna(0).T

    def _keep_the_same_io_in_column(self, df):
        '''
        Проверяю колонки на наличие повторяющихся в них объектах
        '''
        def _clearing_duplicates_objects_at_columns(df: pd.DataFrame) -> pd.DataFrame:
            # если есть строки с объектами, которые повторяются в колонке column
            for duplicate_io in df_where_duplicate_on_column[column][df_where_duplicate_on_column[column] != 0]:
                one_essence: pd.DataFrame = df[df.isin([duplicate_io]).any(1)]
                pseudonym = '/'.join(list(set('/'.join(one_essence.index).split('/'))))
                df.loc[pseudonym] = pd.Series(list(set(io for io in list(chain(*one_essence.values)) if io != 0)))
                df = df.drop(one_essence.index)
            return df.fillna(0)

        for column in df.columns:
        # duplicate_on_column - выделяем датафрейм дубликатов в каждой колонке
            df_where_duplicate_on_column: pd.DataFrame = df[df[column].duplicated(keep='first') & df[column] != 0].loc[:, (df != 0).any(axis=0)]
            if df_where_duplicate_on_column.empty:
                continue
            else:
                df = _clearing_duplicates_objects_at_columns(df)  
        return df    
    
    def __repr__(self) -> str:
        return "Объект содержит таблицы"