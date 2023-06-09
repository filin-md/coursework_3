import json
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(current_dir, "..", "history", "operations.json")


def encode_from(from_str):
    """Функция получает строку с названием и номером карты.
    Возвращает обратно строку с названием и закодированным номером карты"""
    items = from_str.split()
    number = items[-1]

    if len(number) == 16:
        encode = number[:4] + " " + number[4:6] + "**" + " " + "****" + " " + number[-4:]
    else:
        encode = number[:4] + " " + number[4:6] + "**" + " " + "**** ****" + " " + number[-4:]

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



def last_five(data):
    """Функция, которая берёт исходный список словарей json
    и по нему создаёт новый список из 5 последних выполненных клиентом операций
    """
    with open(data, encoding="UTF-8") as file:
        history = json.load(file)
        formatted_list = []

        for operation in history:
            #Проверяем не пустой ли словарь
            if operation:
                if operation["state"] == "CANCELED":
                    continue

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

            result = sorted(formatted_list, key=lambda x: datetime.strptime(x["date"], "%d.%m.%Y"))[-5:]

        return result

for operation in last_five(DATA):
    if 'from' not in operation:
        print(f"""{operation['date']} {operation['description']}
-> {operation['to']}
{operation['amount']}
""")
    elif 'to' not in operation:
        print(f"""{operation['date']} {operation['description']}
{operation['from']}  -> 
{operation['amount']}
""")
    else:
        print(f"""{operation['date']} {operation['description']}
{operation['from']} -> {operation['to']}
{operation['amount']}
""")




