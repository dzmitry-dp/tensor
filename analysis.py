import pandas as pd

from obj import get_all_obj # собрать объекты всех наборов символов, которые буду считать словом
from obj.intelligent import IntelligentObject

class Frame:
    """.df - таблица где название колонок - это набор символов str. 
            А в ячейках находятся объекты IntelligentObject
            В каждой строке объект из конкретного файла
    """
    def __init__(self, tensors) -> None:
        self.all_obj: dict[str, list] = get_all_obj(tensors)
        self._df: pd.DataFrame = None # таблица соответствия символов и интеллектуальному объекту который был создан по этим символам
        self._essences: pd.DataFrame = None # таблица в которой учтены формы слова о объеденены в одну колонку

    @property
    def df(self) -> pd.DataFrame:
        """Предоставляю pd.DataFrame где строки это символы, по которым составлен объект,
        А столбцы - файлы в которых этот набор символов встречался"""
        if self._df is None:
            self._df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in self.all_obj.items()])).fillna(0).T
        return self._df
    
    @property
    def essences(self) -> pd.DataFrame:
        if self._essences is None:
            _essences = self._get_essences_df(self.df)
            self._essences = self._clear_essences(_essences)
        return self._essences
    
    def _get_essences_df(self, df):
        "Собираю одни и те же сущности в одну колонку. Отслеживаю формы одного и того же слова"
        def _save_one_of_two_obj():
            essensce_pseudonym = ''.join(e for e in essence_2.symbols if e.isalnum())
            if essensce_pseudonym not in d.keys():
                # если раньше не сохранял под ключом 2й сущности
                d[essensce_pseudonym] = df.iloc[j][df.iloc[j] != 0]

        def _save_objects():
            title_es_1: str = essence_1.__str__()  # символы приведенные к верхнему регистру
            title_es_2: str = essence_2.__str__() # символы в объекте с которым сравниваем
            # разные символы
            l1 = list(title_es_1) # для удобства сравнения переводим строку в список букв
            l2 = list(title_es_2) # для удобства сравнения переводим строку в список букв
            a = int(len(l1) * 0.8) # 80% совпадений списков
            b = int(len(l2) * 0.8) # 80% совпадений списков
            c = int((a + b)/2)
            
            pseudonym = ''.join(e for e in essence_2.symbols if e.isalnum())
            if l1[:c] == l2[:c] and len(l1[:c]) > 1 and len(l2[:c]) >1: # если совпадает 80% букв
                if pseudonym not in d.keys():
                    # если еще не сохранялись общие строки
                    d[pseudonym] = pd.concat([df.iloc[j][df.iloc[j] != 0], df.iloc[i][df.iloc[i] != 0]], ignore_index=True)
                else:
                    # pseudonym in d.keys()
                    for _ in pd.concat([df.iloc[i][df.iloc[i] != 0], df.iloc[j][df.iloc[j] != 0]], ignore_index=True).values:
                        if _ not in d[pseudonym].values:
                                d[pseudonym] = pd.concat([d.pop(pseudonym), pd.Series([_])], ignore_index=True)
                    
        i = 0 # фиксируем номер строки для списка всех объектов
        d = {} # создаем словарь для нового df
        # значения первой колонки в типе данных list (т.к. она всегда будет максимально заполнена данными)
        values_first_column: list = df[0].values.tolist()
        while len(values_first_column) != 0:
            # пока список со всеми уникальными объектами не пустой
            essence_1: IntelligentObject = values_first_column.pop(0)  # берем всегда первый элемент из списка
            
            for j, essence_2 in enumerate(df[0].values):
                j: int # нумерация строк для серии табличных данных
                essence_2: IntelligentObject
                # symbols - набор символов для которого был создан объект IntelligentObject
                if essence_1 == essence_2: 
                    # если одинаковые сущности
                    _save_one_of_two_obj()
                else: 
                    # если сущности разные
                    _save_objects()
            i += 1
        
        return pd.DataFrame(d).fillna(0).T

    def _clear_essences(self, df) -> pd.DataFrame:
        return df

    def __repr__(self) -> str:
        return "Объект содержит таблицы"