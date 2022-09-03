from __future__ import annotations

import re
from typing import Optional


def entry_check(speech_samples: list, speech: list, index: Optional[int | None]) -> list:
    """
    Проверка вхождения искомой последовательности слов в речь оператора.
    :param speech_samples: Образцы искомых последовательностей.
    :param speech: Текстовая расшифровка речи менеджера.
    :param index: Номер диалога.
    :return: Список вида [Номер диалога (int), Номер строки (int), Должность (str), Строка диалога (str)]
    или пустой список, если не найдено.
    """
    result = []
    if index is None:
        for _ in speech_samples:
            result += list(filter(lambda x: re.findall(_, x[3].lower()), speech))
    else:
        for _ in speech_samples:
            result += list(filter(lambda x: re.findall(_, x[3].lower()) if x[0] == index else None, speech))
    return result


def extract_sample(possible_string: list, name_samples: list) -> str:
    """
    Извлекает всякие названия и имена (последовательности), согласуясь со списком примеров.
    :param possible_string: Список содержащий строку, содержащую извлекаемую последовательность.
    :param name_samples: Список примеров возможных последовательностей.
    :return: Последовательность(str)
    """

    name = possible_string[0][3].lower()
    name = list(re.findall(f'{_}', name) for _ in name_samples)
    name = list(filter(lambda x: len(x) > 0, name))
    if name:
        return name[0][0].capitalize()


def checks(result: list, dialogue_index: Optional[int | None], internal: bool, message: str) -> Optional[str | list]:
    """
    Обработка результата выполнения функции.
    :param result: Список сформированный из строки файла.
    :param dialogue_index: Индекс соответствующий номеру строки из файла.
    :param internal: Флаг, что надо вернуть необработанный список для внутренней обработки.
    :param message: Сообщение при несоблюдении условий.
    :return: Строку, если обработка внутри функции, список, если вне.
    """
    if internal:
        return result
    if result:
        if dialogue_index is not None:
            return f'Диалог: {result[0][0]}, строка: {result[0][1]}, реплика: {result[0][3]}'
        else:
            return [f'Диалог: {result[_][0]}, строка: {result[_][1]}, реплика: {result[_][3]}'
                    for _ in range(len(result))]
    else:
        return message


def greetings(sequence: list, dialogue_index: Optional[int | None] = None, internal: bool = False)\
        -> Optional[list | str]:
    """
    Извлекает список реплик с приветствием менеджера.
    :param internal: Флаг, что надо вернуть необработанный список для внутренней обработки.
    :param sequence: Текстовая расшифровка речи менеджера.
    :param dialogue_index: Номер диалога.
    :return:Строку с указанием диалога и строки с приветствием или список строк содержащих приветствие,
    если индекс не задан. Если по индексу нет приветствия, возвращается соответствующее сообщение.
    """
    greetings_samples = [
        'здравствуйте',
        'добрый день',
        'добрый вечер',
        'доброе утро',
    ]
    result = entry_check(greetings_samples, sequence, dialogue_index)
    message = 'Нет приветствия.'
    return checks(result, dialogue_index, internal, message)


def introduction(sequence: list, dialogue_index: Optional[int | None] = None, internal: bool = False)\
        -> Optional[list | str]:
    """
    Извлекает список реплик, где менеджер представился.
    :param internal: Флаг, что надо вернуть необработанный список для внутренней обработки.
    :param sequence: Текстовая расшифровка речи менеджера.
    :param dialogue_index: Номер диалога.
    :return:Строку с указанием диалога и строки и приветствием или список строк содержащих представление,
    если индекс не задан. Если по индексу нет представления, возвращается соответствующее сообщение.
    """
    introduction_samples = [
        'меня зовут',
        'моё имя',
        'меня \w+ зовут',
        'зовут \w+ меня',
        'да это \w+',
        'здравствуйте это \w+'
    ]
    result = entry_check(introduction_samples, sequence, dialogue_index)
    message = 'Не представился.'
    return checks(result, dialogue_index, internal, message)


def sales_name(sequence: list, dialogue_index: int) -> str:
    """
    Извлекает имя менеджера.
    :param sequence: Текстовая расшифровка речи менеджера.
    :param dialogue_index: Номер диалога.
    :return: Имя (str)
    """
    sales_name_samples = [
        'меня зовут (\w+)',
        'моё имя (\w+)',
        'меня (\w+) зовут',
        'зовут (\w+) меня',
        'да это (\w+)',
        'здравствуйте это (\w+)',
    ]
    string = introduction(sequence, dialogue_index, internal=True)
    result = 'Не представился.'
    if string:
        result = extract_sample(string, sales_name_samples)
    return result


def company_name(sequence: list, dialogue_index: int) -> str:
    """
    Извлекает название компании.
    :param sequence: Текстовая расшифровка речи менеджера.
    :param dialogue_index: Номер диалога.
    :return: Название (str)
    """
    company_name_samples = [
        'компания (\w+ бизнес) ',
        'компания (\w+бизнес) '
    ]
    string = entry_check(company_name_samples, sequence, dialogue_index)
    result = 'Компания не названа'
    if string:
        result = extract_sample(string, company_name_samples)
    return result


def goodbye(sequence: list, dialogue_index: Optional[int | None] = None, internal: bool = False) -> Optional[list | str]:
    """
    Извлекает список реплик, где менеджер попрощался.
    :param internal: Флаг, что надо вернуть необработанный список для внутренней обработки.
    :param sequence: Текстовая расшифровка речи менеджера.
    :param dialogue_index: Номер диалога.
    :return: Строку с указанием диалога и строки с прощанием или список строк содержащих прощание,
    если индекс не задан. Если по индексу нет прощания, возвращается соответствующее сообщение.
    """
    goodbye_samples = [
        'до свидания',
        'до скорой встречи',
        'приятного вечера',
        'прощайте',
        'позвольте попрощаться',
        'всего хорошего',
        'хорошего вечера',
    ]
    result = entry_check(goodbye_samples, sequence, dialogue_index)
    message = 'Нет прощания.'
    return checks(result, dialogue_index, internal, message)


def script_check(sequence: list, dialogue_index: int) -> bool:
    """
    Проверка исполнения менеджером скрипта, предусматривающего приветствие и прощание с клиентом.
    :param sequence: Текстовая расшифровка речи менеджера.
    :param dialogue_index: Номер диалога.
    :return: bool
    """
    result = False
    if greetings(sequence, dialogue_index, internal=True) and goodbye(sequence, dialogue_index, internal=True):
        result = True
    return result


with open('test_data.csv', 'r', encoding='utf8') as file:
    content = file.readlines()
content = list(map(lambda x: x.split(','), list(map(str.strip, content))))
salesman_speech = list(filter(lambda x: x[2] == 'manager', content))
for i in salesman_speech:
    i[0] = int(i[0])
    i[1] = int(i[1])
# 1. Извлекать реплики с приветствием – где менеджер поздоровался.

# for i in range(6):
#     print(greetings(salesman_speech, i))
# print(*greetings(salesman_speech), sep='\n')

#2. Извлекать реплики, где менеджер представил себя.
# for i in range(6):
#     print(introduction(salesman_speech, i))
# print(*introduction(salesman_speech), sep='\n')

# 3. Извлекать имя менеджера.

# for i in range(6):
#     print(sales_name(salesman_speech, i))

# 4. Извлекать название компании.

# for i in range(6):
#     print(company_name(salesman_speech, i), sep='\n')

# 5. Извлекать реплики, где менеджер попрощался.

# for i in range(6):
#     print(goodbye(salesman_speech, i))

# 6. Проверять требование к менеджеру: «В каждом диалоге обязательно необходимо поздороваться и попрощаться с клиентом»

# for i in range(6):
#     print(script_check(salesman_speech, i))
# print(*goodbye(salesman_speech), sep='\n')
