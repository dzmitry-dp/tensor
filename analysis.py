import pandas as pd

from intel_obj import get_all_obj # собрать объекты всех наборов символов, которые буду считать словом

class FramesData:
    def __init__(self, tensors) -> None:
        self.all_obj: dict[str, list] = get_all_obj(tensors)
        self._symbols = None # таблица соответствия символов и объекту который был создан по этим символам

    @property
    def symbols(self):
        if self._symbols is None:
            self._symbols = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in self.all_obj.items()]))
        return self._symbols

    def __repr__(self) -> str:
        return "Объект содержит таблицы и средства анализа полученных данных"