import numpy as np
import pandas as pd
import csv
import re

def read_json_from_csv(file_name):
    """
    Функция чтения всех json из файла csv
    """
    line = 0
    json_text_arr = []

    # Считывание всех json из файла
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Преобразование списка в строку
            text = ' '.join(row)

            # Ищем участки текста между "[" и "]"
            json_text = re.findall(r'\[(.*?)\]', text)

            if (line > 0):
                json_text_arr.append(json_text)
            line += 1

        return json_text_arr

def find_lineitempricespt(json_text):
    """
    Функция поиска значений lineitempricespt
    """
    # Поиск значений после "lineitempricespt:"
    pattern = r'lineitempricespt:(\d+\.\d+)'
    matches = re.findall(pattern, json_text)

    # Преобразуем найденные строки в числа с плавающей точкой и вернем в виде массива
    lipspt_arr = [float(match) for match in matches]

    return lipspt_arr

def find_n(json_text):
    """
    Функция поиска значений n
    """
    # Поиск значений после "n:"
    pattern = r'n":(\d+)'
    matches = re.findall(pattern, json_text)

    # Преобразуем найденные строки в числа с плавающей точкой и вернем в виде массива
    n_arr = [int(match) for match in matches]

    return n_arr

def find_delivery_note_id(json_text):
    """
    Функция поиска значений delivery_note_id
    """
    # Поиск значений после "delivery_note_id:"
    pattern = r'delivery_note_id:"(.*?)"'
    matches = re.findall(pattern, json_text)

    # Преобразуем найденные строки в числа с плавающей точкой и вернем в виде массива
    delivery_note_id_arr = [match for match in matches]

    return delivery_note_id_arr

def find_deliverynoteprev(json_text):
    """
    Функция поиска значений deliverynoteprev
    """
    # Поиск значений после "deliverynoteprev:"
    pattern = r'deliverynoteprev:"(.*?)"'
    matches = re.findall(pattern, json_text)

    # Преобразуем найденные строки в числа с плавающей точкой и вернем в виде массива
    deliverynoteprev_arr = [match for match in matches]

    return deliverynoteprev_arr


def build_chains(sales_data):
    chains = {}
    for price, n, sale_id, prev_sale_id in sales_data:
        if sale_id not in chains:
            chains[sale_id] = []
        if prev_sale_id in chains:
            chains[sale_id] = chains[prev_sale_id] + [sale_id] + [n] + [price]
        else:
            chains[sale_id] = [sale_id] + [n] + [price]
    return chains

def remove_subchains(chain_data):
    chains_to_remove = set()

    for chain_id, chain in chain_data.items():
        for other_chain_id, other_chain in chain_data.items():
            if chain_id != other_chain_id and all(item in other_chain for item in chain):
                chains_to_remove.add(chain_id)

    return {chain_id: chain for chain_id, chain in chain_data.items() if chain_id not in chains_to_remove}


def find_end_of_chain(sales_data):
    sale_dict = {}
    for lipspt, n, dni, dnp in sales_data:
        sale_dict[dni] = (lipspt, n, dnp)

    end_of_chains = set(sale_dict.keys()) - set(dnp for _, _, dnp in sale_dict.values())

    return [(sale_dict[dni][0], dni) for dni in end_of_chains]


def find_previous_in_chain(sales_data, end_of_chains):
    sale_dict = {}
    for lipspt, n, dni, dnp in sales_data:
        sale_dict[dni] = (lipspt, n, dnp)

    previous_in_chain = []
    for lipspt, dni in end_of_chains:
        prev_dni = sale_dict[dni][2]
        previous_in_chain.append((sale_dict[prev_dni][0], prev_dni))

    return previous_in_chain

def read_prices(filename):
    """
    Функция чтения цен по цепочкам продаж из нового формата данных
    """
    # Загружаем файл CSV
    df = pd.read_csv(filename)

    # Сохраняем значения из столбца lineitempricespt и преобразовывваем в np.array
    lineitem_prices = df['lineitempricespt'].apply(lambda x: np.array(re.findall(r'\d+\.\d+', x), dtype=float))

    return lineitem_prices


# file_name = 'test_20.csv'
filename = 'chain_etn.csv'

# Массивы точек для графиков
x_arr = []
y_arr = []

# Чтение всех json с файла
json_text_arr = read_json_from_csv(file_name)

"""
Извлечение всех нужных значений из JSON
"""
original = []
lipspt = find_lineitempricespt(str(json_text_arr[0]))
n = find_n(str(json_text_arr[0]))
dni = find_delivery_note_id(str(json_text_arr[0]))
dnp = find_deliverynoteprev(str(json_text_arr[0]))

original.append(lipspt)
original.append(n)
original.append(dni)
original.append(dnp)

sales_data = tuple(zip(*original[::]))

# print(lipspt)
# print(n)
# print(dni)
# print(dnp)


# Строим цепочки продаж
chains = build_chains(sales_data)
cleaned_chains = remove_subchains(chains)

'''
# Выводим цепочки продаж
for sale_id, chain in cleaned_chains.items():
    print(f"Цепочка продаж с id '{sale_id}':")
    for sale in chain:
        print(sale)
    print('-' * 20)
'''

lineitem_prices = read_prices(filename)
print(lineitem_prices)

'''
# Для каждой строки из исходного CSV
for json_text in json_text_arr:
    """
    Добавление значений DT и Check и подписей для оси X
    """

    x_values = ['DT']
    for i in range(len(lipspt_arr)):
        x_values.append('ETN' + str(i+1))
    lipspt_arr.insert(0, round(lipspt_arr[0]*0.95, 7))
    lipspt_arr.append(round(lipspt_arr[-1]*1.05, 7))
    x_values.append('Check')
    x_arr.append(x_values)
    y_arr.append(lipspt_arr)
    '''


'''
# Точки на графике по оси Y
y_points = []

for i in range(len(lipspt)):
    if n[i] == 0:
        zeros_arr = []
        zeros_arr.append(lipspt[i])
        zero_count = dnp.count(dni[i])

        for j in range(zero_count):
            y_points.append(zeros_arr)

'''



