class monthlyPrices:
    """
    :code_assign: service
    :code_type: отрисовка LinePlot средневзвешенной цены
    :packages:
    import pandas as pd
    import numpy as np
    import re
    """

    def __init__(self, name):
        self.tires_codes = ['4011100003',
                            '4011100009',
                            '4011201000',
                            '4011209000',
                            '4011400000',
                            '4011700000',
                            '4011800000',
                            '4011900000']

        self.fridges_codes = ['8418108001',
                              '8418102001',
                              '8418211000',
                              '8418215100',
                              '8418215900',
                              '8418219100',
                              '8418219900',
                              '8418302001',
                              '8418308001',
                              '8418402001',
                              '8418408001']
        self.name = name
    def get_monthly_prices(self, dataset, codes):
        """
        Функция подсчета средневзвешенного
        """
        np.set_printoptions(linewidth=np.inf)

        # Чтение всех значений кодов из CSV
        code_arr_all = dataset['itemcustomcode'].tolist()
        month_arr_all = []
        year_arr_all = []
        price_arr_all = []
        count_arr_all = []

        # Чтение всех значений year из CSV
        for index, row in dataset.iterrows():
            year = row['year']
            numbers = re.findall(r'\d+', year)
            numbers = [int(num) for num in numbers]
            year_arr_all.append(numbers)

        # Чтение всех значений month из CSV
        for index, row in dataset.iterrows():
            month = row['month']
            numbers = re.findall(r'\d+', month)
            numbers = [int(num) for num in numbers]
            month_arr_all.append(numbers)

        # Чтение всех значений цен из CSV
        for index, row in dataset.iterrows():
            lineitempricespt = row['lineitempricespt']
            numbers = re.findall(r'\d+\.\d+|\d+', lineitempricespt)
            numbers = [float(num) if '.' in num else int(num) for num in numbers]
            price_arr_all.append(numbers)

        # Чтение всех значений количества продаж из CSV
        for index, row in dataset.iterrows():
            quantitydespatchedspt = row['quantitydespatchedspt']
            numbers = re.findall(r'\d+\.\d+|\d+', quantitydespatchedspt)
            numbers = [float(num) if '.' in num else int(num) for num in numbers]
            count_arr_all.append(numbers)

        """
        Объединение данных по кодам
        """

        # Создаем словарь для хранения данных
        combined_data = {}

        for i in range(len(code_arr_all)):
            code = code_arr_all[i]
            month = month_arr_all[i]
            year = year_arr_all[i]
            price = price_arr_all[i]
            count = count_arr_all[i]

            if code not in combined_data:
                combined_data[code] = {'month': [], 'year': [], 'price': [], 'count': []}

            combined_data[code]['month'].extend(month)
            combined_data[code]['year'].extend(year)
            combined_data[code]['price'].extend(price)
            combined_data[code]['count'].extend(count)

        # Преобразуем словарь обратно в списки
        code_arr_all = list(combined_data.keys())
        month_arr_all = [combined_data[code]['month'] for code in code_arr_all]
        year_arr_all = [combined_data[code]['year'] for code in code_arr_all]
        price_arr_all = [combined_data[code]['price'] for code in code_arr_all]
        count_arr_all = [combined_data[code]['count'] for code in code_arr_all]

        code_arr = []
        month_arr = []
        year_arr = []
        price_arr = []
        count_arr = []

        for i in range(len(code_arr_all)):
            if (str(code_arr_all[i]) in codes):
                code_arr.append(str(code_arr_all[i]))
                month_arr.append(month_arr_all[i])
                year_arr.append(year_arr_all[i])
                price_arr.append(price_arr_all[i])
                count_arr.append(count_arr_all[i])

        """
        Добавляем записи по всем шинам без учета кода
        """
        flattened_month_arr = []
        flattened_year_arr = []
        flattened_price_arr = []
        flattened_count_arr = []
        for sublist in month_arr:
            flattened_month_arr.extend(sublist)
        for sublist in year_arr:
            flattened_year_arr.extend(sublist)
        for sublist in price_arr:
            flattened_price_arr.extend(sublist)
        for sublist in count_arr:
            flattened_count_arr.extend(sublist)

        code_arr.append('All_' + self.name)
        month_arr.append(flattened_month_arr)
        year_arr.append(flattened_year_arr)
        price_arr.append(flattened_price_arr)
        count_arr.append(flattened_count_arr)

        # Вывод данных до подсчета средневзвешенного значения
        # print("\n\nИСХОДНЫЕ ДАННЫЕ")
        # print("\ncode")
        # print(len(code_arr))
        # print(code_arr)
        # print("\nmonth")
        # print(len(month_arr))
        # print(month_arr)
        # print("\nyear")
        # print(len(year_arr))
        # print(year_arr)
        # print("\nprice")
        # print(len(price_arr))
        # print(price_arr)
        # print("\ncount")
        # print(len(count_arr))
        # print(count_arr)

        """
        Подсчет средневзвешенного значения
        """
        av_price_arr = []
        av_year_arr = []
        av_month_arr = []

        # Подсчет средневзвешенных значений по месяцам
        for i in range(len(year_arr)):
            # Создаем словарь для хранения данных
            sales_data = {}

            for j in range(len(year_arr[i])):
                year = year_arr[i][j]
                month = month_arr[i][j]
                price = price_arr[i][j]
                count = count_arr[i][j]

                if (year, month) not in sales_data:
                    sales_data[(year, month)] = {'total_price': 0, 'count': 0}

                sales_data[(year, month)]['total_price'] += price * count
                sales_data[(year, month)]['count'] += count

            # Вычисляем средние значения
            av_price = []
            av_year = []
            av_month = []

            for (year, month), dataset in sales_data.items():
                avg_price = dataset['total_price'] / dataset['count']
                av_price.append(round(avg_price, 4))
                av_year.append(year)
                av_month.append(month)

            av_price_arr.append(av_price)
            av_year_arr.append(av_year)
            av_month_arr.append(av_month)

        """
        Сортировка значений в хронологическом порядке
        """
        sorted_year_arr = []
        sorted_months_arr = []
        sorted_prices_arr = []

        for i in range(len(code_arr)):
            # Объединяем все данные в один список кортежей
            combined_data = list(zip(av_year_arr[i], av_month_arr[i], av_price_arr[i]))

            # Сортируем данные по году и месяцу
            sorted_data = sorted(combined_data, key=lambda x: (x[0], x[1]))

            # Разделяем данные обратно в списки
            sorted_years, sorted_months, sorted_prices = zip(*sorted_data)

            sorted_year_arr.append(sorted_years)
            sorted_months_arr.append(sorted_months)
            sorted_prices_arr.append(sorted_prices)

        # Преобразуем данные в NumPy Array
        for i in range(len(sorted_months_arr)):
            sorted_months_arr[i] = np.array(sorted_months_arr[i])
            sorted_year_arr[i] = np.array(sorted_year_arr[i])
            sorted_prices_arr[i] = np.array(sorted_prices_arr[i])


        # Замена значений месяцев в соответствии с годом
        for i in range(len(sorted_months_arr)):
            for j in range(len(sorted_months_arr[i])):
                if sorted_year_arr[i][j] == 2023:
                    sorted_months_arr[i][j] += 12


        return code_arr, sorted_months_arr, sorted_year_arr, sorted_prices_arr


def monthly_prices_visualise(
        dataset: pd.DataFrame,
        input_code: str = '',
):
    """
    :code_assign: users
    :code_type: Пользовательские функции
    :imports: init_gui_dict, Window, Canvas, LinePlot, monthlyPrices
    :packages:
    import pandas as pd
    import numpy as np
    :param_block pd.DataFrame dataset: датасет
    :param str input_code: выбранная категория
    :returns: gui_dict, error
    :rtype: dict, str
    :semrtype: ,
    """
    error = ""
    gui_dict = init_gui_dict()
    MP = monthlyPrices(input_code)
    if input_code == 'tires':
        codes = MP.tires_codes
    else:
        codes = MP.fridges_codes
    code_arr_t, sorted_months_arr_t, sorted_year_arr_t, sorted_prices_arr_t = MP.get_monthly_prices(dataset,
                                                                                                    codes)
    canvases = []
    for price, month, code, years in zip(sorted_prices_arr_t, sorted_months_arr_t, code_arr_t, sorted_year_arr_t):
        plots = []
        for year in sorted(list(set(years))):
            if plots:
                x = x[-1]
                y = y[-1]
            else:
                x = []
                y = []
            for i in [j for j in range(len(years)) if years[j] == year]:
                x.append(month[i])
                y.append(price[i])
            plots.append(LinePlot(x=x, y=y, names=[f'Год {year}']))
        canvases.append(
                    Canvas(title=f'Код {code}',
                           showlegend=True,
                           plots=[LinePlot(x=month, y=price, names=[f'Код {code}'])]
                           )
                )
    gui_dict['plot'].append(
        Window(
            window_title='Средневзвещанные цены',
            canvases=canvases
        ).to_dict()
    )
    return gui_dict, error
