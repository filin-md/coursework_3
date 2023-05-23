import json
from datetime import datetime

DATA = "../history/operations.json"

def last_operations():
    """Функция, которая выводит на экран список
    из 5 последних выполненных клиентом операций в формате:
    <дата перевода> <описание перевода>
    <откуда> -> <куда>
    <сумма перевода> <валюта>"""
    # with open('../history/operations.json', encoding='utf8') as file:
    #     history = json.load(file)
    #     sorted_date = []
    #     for i in range(len(history)):
    #         if "date" in history[i]:
    #             sorted_date.append(history[i]["date"][:10])
    #     print(sorted(sorted_date)[-5:])


def encode_from(from_str):
    """Функция получает строку с названием и номером карты.
    Возвращает обратно строку с названием и закодированным номером карты"""
    items = from_str.split()
    number = items[-1]
    encode = number[:4] + " " + number[4:6] + "**" + " " + "****" + " " + number[-4:]
    items[-1] = encode
    result = " ".join(items)
    return result

def encode_to(to_str):
    """Функция получает строку с названием и номером счет.
        Возвращает обратно строку с названием и закодированным номером счета"""
    items = to_str.split()
    number = items[-1]
    encode = "**" + number[-4:]
    items[-1] = encode
    result = " ".join(items)
    return result



def new_list():
    """Функция, которая берёт исходный список словарей json
    и по нему создаёт новый с необходимыми полями в нужном формате"""
    with open(DATA, encoding="UTF-8") as file:
        history = json.load(file)
        formatted_list = []

        for operation in history:
            #Проверяем не пустой ли словарь
            if operation:
                #Создаём пустой словарь для одной операции
                entity = {}

                #Берём дату из исходного списка, форматируем и передаём в новый
                input_date = operation["date"]
                datetime_object = datetime.strptime(input_date, "%Y-%m-%dT%H:%M:%S.%f")
                output_date = datetime_object.strftime("%d.%m.%Y")
                entity["date"] = output_date

                #Переносим описание
                entity["description"] = operation["description"]

                #Если поле from есть в операции - берём, кодируем и заносим в словарь
                if "from" in operation:
                    entity["from"] = encode_from(operation["from"])

                #Если поле to есть в операции - берём, кодируем и заносим в словарь
                if "to" in operation:
                    entity["to"] = encode_to(operation["to"])

                #Берём сумму и валюту, объединяем в одну строку и заносим в словарь по ключу amount
                entity["amount"] = operation["operationAmount"]["amount"] + " " + operation["operationAmount"]["currency"]["name"]

            formatted_list.append(entity)

        return formatted_list

for i in new_list():
    print(i)


