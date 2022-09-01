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
            result += (list(filter(lambda x: re.findall(_, x[3].lower()), speech)))
    else:
        for _ in speech_samples:
            result += (list(filter(lambda x: re.findall(_, x[3].lower()) if x[0] == index else None, speech)))
    return result


def greetings(sequence: list, dialogue_index: Optional[int | None]=None) -> list:
    """
    Извлекает список реплик с приветствием менеджера.
    :param sequence: Текстовая расшифровка речи менеджера.
    :param dialogue_index: Номер диалога.
    :return: Список вида [Номер диалога (int), Номер строки (int), Должность (str), Строка диалога (str)]
    или пустой список, если не найдено.
    """
    greetings_samples = [
        'здравствуйте',
        'добрый день',
        'добрый вечер',
        'доброе утро',
    ]
    return entry_check(greetings_samples, sequence, dialogue_index)


def introduction(sequence: list, dialogue_index: Optional[int | None]=None) -> list:
    """
    Извлекает список реплик, где менеджер представился.
    :param sequence: Текстовая расшифровка речи менеджера.
    :param dialogue_index: Номер диалога.
    :return: Список вида [Номер диалога (int), Номер строки (int), Должность (str), Строка диалога (str)]
    или пустой список, если не найдено.
    """
    introduction_samples = [
        'меня зовут',
        'моё имя',
        'меня \w+ зовут',
        'зовут \w+ меня',
        'да это \w+',
        'здравствуйте это \w+'
    ]
    return entry_check(introduction_samples, sequence, dialogue_index)


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
    string = introduction(sequence, dialogue_index)
    result = 'Не представился.'
    if string:
        name = introduction(sequence, dialogue_index)[0][3].lower()
        name = list(re.findall(f'{_}', name) for _ in sales_name_samples)
        name = list(filter(lambda x: len(x) > 0, name))
        if name:
            result = name[0][0].capitalize()
    return result


def company_name(sequence, dialogue_index=None):
    company_name_samples = [
        'компания \w+ бизнес',
        'компания \w+бизнес'
    ]
    return entry_check(company_name_samples, sequence, dialogue_index)


def goodbye(sequence: list, dialogue_index: Optional[int | None]=None) -> list:
    """
    Извлекает список реплик, где менеджер попрощался.
    :param sequence: Текстовая расшифровка речи менеджера.
    :param dialogue_index: Номер диалога.
    :return: Список вида [Номер диалога (int), Номер строки (int), Должность (str), Строка диалога (str)]
    или пустой список, если не найдено.
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
    return entry_check(goodbye_samples, sequence, dialogue_index)


def script_check(sequence: list, dialogue_index: int) -> bool:
    """
    Проверка исполнения менеджером скрипта, предусматривающего приветствие и прощание с клиентом.
    :param sequence: Текстовая расшифровка речи менеджера.
    :param dialogue_index: Номер диалога.
    :return: bool
    """
    result = False
    if greetings(sequence, dialogue_index) and goodbye(sequence, dialogue_index):
        result = True
    return result


with open('test_data.csv', 'r', encoding='utf8') as file:
    content = file.readlines()
content = list(map(lambda x: x.split(','), list(map(str.strip, content))))
salesman_speech = list(filter(lambda x: x[2] == 'manager', content))
for i in salesman_speech:
    i[0] = int(i[0])
    i[1] = int(i[1])
# print(greetings(salesman_speech, 10))
# print(goodbye(salesman_speech, 10))
# print(script_check(salesman_speech, 10))
# for i in range(6):
#     print(introduction(salesman_speech, i))
# for i in range(6):
#     print(sales_name(salesman_speech, i))
# print(*list(filter(lambda x: 'бизнес' in x[3], salesman_speech)), sep='\n')
print(*company_name(salesman_speech), sep='\n')
