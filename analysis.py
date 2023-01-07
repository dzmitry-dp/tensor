import pandas as pd

from obj import get_all_obj # собрать объекты всех наборов символов, которые буду считать словом

class FramesData:
    """.df - таблица где название колонок - это набор символов str. 
            А в ячейках находятся объекты IntelligentObject
            В каждой строке объект из конкретного файла
    """
    def __init__(self, tensors) -> None:
        self.all_obj: dict[str, list] = get_all_obj(tensors)
        self._df: pd.DataFrame = None # таблица соответствия символов и интеллектуальному объекту который был создан по этим символам

    @property
    def df(self):
        if self._df is None:
            self._df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in self.all_obj.items()])).T
            self._df = self._df.fillna(0)
        return self._df

    def __repr__(self) -> str:
        return "Объект содержит таблицы и средства анализа полученных данных"