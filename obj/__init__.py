from threading import Thread

from obj.intelligent import IntelligentObject

def get_all_obj(tensors: list) -> dict[str, list[IntelligentObject]]:
    """
    Возвращает множество интеллектуальных объектов из всех текстов.
    Соответствие 'набор_символов': [список_из_объектов]
    Внутри каждого объекта хранится информация о местах, где этот ИО находится и в каких текстах
    """

    objects_of_words: dict[str, list[IntelligentObject]] = {} # все объекты которые созданы для набора из русских символов
    
    def watch_all_rows(rows_list: list, root_path: str):
        "К каждой строке применяем алгоритм check_symbols_in_the_row()"

        def check_symbols_in_the_row(row: str, row_number: int):
            "Выделяем объект из символов, ограниченных' 'пробелами' '"

            def create_IO(symbols_set, row_number, word_number_in_row):
                "Превращаю слово в интеллектуальный объект"
                io = IntelligentObject(root_path, symbols_set, row_number, word_number_in_row)
                
                if io.symbols in objects_of_words.keys():
                    objects_of_words[io.symbols].append(io)
                else:
                    objects_of_words[io.symbols] = [io]
            
            # разбиваем строку на список слов по пробелам
            symbols_list = row.split(' ')
            # для всех слов в строке
            thread_list = []
            for word_number_in_row, symbols_set in enumerate(symbols_list):
                # ''.join(e for e in symbols_set if e.isalnum())
                thread = Thread(target=create_IO, args=[symbols_set, row_number, word_number_in_row], name=f'thread_for_word-{word_number_in_row}')
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