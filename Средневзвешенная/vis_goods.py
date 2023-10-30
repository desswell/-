import copy


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


class Chain:
    """
    :code_assign: service
    :code_type: отрисовка LinePlot
    :packages:
    import pandas as pd
    import numpy as np
    import re
    """

    def __init__(self, dataset):
        """
        :param pd.DateFrame: датасет
        """
        self.data = dataset

    def read_etn_prices(self):
        """
        Функция чтения цепочек цен ЕТН
        """
        result = []

        for index, row in self.data.iterrows():
            prices = row['lineitempricespt']
            etns = re.findall(r'\d+\.\d+|\d+', prices)
            etns = [float(etn) if '.' in etn else int(etn) for etn in etns]
            result.append(etns)

        return result

    def read_etn_counts(self):
        """
        Функция чтения цепочек количества ЕТН
        """
        result = []

        for index, row in self.data.iterrows():
            counts = row['quantitydespatchedspt']
            etns = re.findall(r'\d+\.\d+|\d+', counts)
            etns = [int(float(etn)) if '.' in etn else int(etn) for etn in etns]
            result.append(etns)

        return result

    def read_etn_months(self):
        """
        Функция чтения цепочек месяцев ЕТН
        """
        result = []

        for index, row in self.data.iterrows():
            months = row['month']
            etns = re.findall(r'\d+\.\d+|\d+', months)
            etns = [int(etn) for etn in etns]
            result.append(etns)

        return result

    def read_etn_years(self):
        """
        Функция чтения цепочек годов ЕТН
        """
        result = []

        for index, row in self.data.iterrows():
            years = row['year']
            etns = re.findall(r'\d+\.\d+|\d+', years)
            etns = [int(etn) for etn in etns]
            result.append(etns)

        return result

    def read_dt_prices(self):
        """
        Функция чтения цен dt
        """
        dts = self.data['ТС/доп, бел руб'].tolist()

        return dts

    def read_dt_counts(self):
        """
        Функция чтения количества dt
        """
        dts = self.data['g41goodsquantity'].tolist()
        dts = [int(dt) for dt in dts]

        return dts

    def read_dt_months(self):
        """
        Функция чтения месяцев dt
        """
        dts = self.data['МЕСЯЦ'].tolist()
        dts = [int(dt) for dt in dts]

        return dts

    def read_dt_years(self):
        """
        Функция чтения годов dt
        """
        dts = self.data['ГОД'].tolist()
        dts = [int(dt) for dt in dts]
        return dts

    def read_check_prices(self):
        """
        Функция чтения цен check
        """
        checks = self.data['price'].tolist()

        return checks

    def read_check_counts(self):
        """
        Функция чтения количества check
        """
        checks = self.data['position_count'].tolist()
        checks = [int(check) for check in checks]

        return checks

    def read_check_months(self):
        """
        Функция чтения месяцев check
        """
        checks = self.data['month_check'].tolist()
        checks = [int(check) for check in checks]

        return checks

    def read_check_years(self):
        """
        Функция чтения годов check
        """
        checks = self.data['year_check'].tolist()
        checks = [int(check) for check in checks]
        return checks

    def read_itemcustomcodes(self):
        """
        Функция чтения значений itemcustomcode
        """
        itemcustomcodes = self.data['itemcustomcode'].tolist()

        return itemcustomcodes

    def read_lineitemids(self):
        """
        Функция чтения значений gtin
        """
        lineitemids = self.data['lineitemid'].tolist()

        return lineitemids

    def filter_chains(self, icc, months, prices, target_code, target_size):
        """
        Функция фильтрации цепочек по размеру и коду
        """
        filtered_months = []
        filtered_prices = []

        for i, code in enumerate(icc):
            if code == target_code and len(months[i]) == target_size + 2:
                filtered_months.append(months[i])
                filtered_prices.append(prices[i])

        return filtered_months, filtered_prices

    def get_average_chains(self, target_code, target_size):
        """
        Функция вычисления средневзвешенных значений цен для всех цепочек
        """
        # ЧТЕНИЕ ЕТН
        prices = self.read_etn_prices()  # Все цены
        months = self.read_etn_months()  # Все месяцы
        years = self.read_etn_years()  # Все года
        counts = self.read_etn_counts()  # Все количества

        # ЧТЕНИЕ DT
        dt_prices = self.read_dt_prices()
        dt_months = self.read_dt_months()
        dt_years = self.read_dt_years()
        dt_counts = self.read_dt_counts()

        # ЧТЕНИЕ CHECK
        check_prices = self.read_check_prices()
        check_months = self.read_check_months()
        check_years = self.read_check_years()
        check_counts = self.read_check_counts()

        # ЧТЕНИЕ КОДОВ И GTIN
        icc = self.read_itemcustomcodes()  # коды
        lid = self.read_lineitemids()  # gtin

        """
        Замена значений месяцев в соответствии с годом
        """
        # Определяем минимальный год
        min_year = dt_years[0]
        for i in range(len(dt_months)):
            if dt_years[i] < min_year:
                min_year = dt_years[i]

        # Заменяем значения
        for i in range(len(months)):
            for j in range(len(months[i])):
                if years[i][j] > min_year:
                    months[i][j] = months[i][j] + 12 * (years[i][j] - min_year)
        for i in range(len(dt_months)):
            if dt_years[i] > min_year:
                dt_months[i] = dt_months[i] + 12 * (dt_years[i] - min_year)
        for i in range(len(check_months)):
            if check_years[i] > min_year:
                check_months[i] = check_months[i] + 12 * (check_years[i] - min_year)

        # Добавляем DT и CHECK в одну цепочку с ETN
        for i in range(len(prices)):
            months[i].insert(0, dt_months[i])
            months[i].append(check_months[i])
            prices[i].insert(0, dt_prices[i])
            prices[i].append(check_prices[i])
            counts[i].insert(0, dt_counts[i])
            counts[i].append(check_counts[i])

        """
        Удаляем цепочки, в которых CHECK стоит раньше последней ETN
        """
        # Создаем новый список, в который будем добавлять только нужные подсписки
        filtered_months = []
        filtered_prices = []
        filtered_counts = []
        filtered_icc = []
        filtered_lid = []

        for i in range(len(months)):
            if months[i][-1] >= months[i][-2]:
                filtered_months.append(months[i])
                filtered_prices.append(prices[i])
                filtered_counts.append(counts[i])
                filtered_icc.append(icc[i])
                filtered_lid.append(lid[i])

        """
        Подсчет средневзвешенных значений по всем подходящим цепочкам
        """
        # Создаем словарь для хранения сумм и весов
        agg_data = {}

        for i in range(len(filtered_icc)):
            key = (tuple(filtered_months[i]), filtered_icc[i],
                   filtered_lid[i])  # создаем ключ для идентификации уникальной цепочки и кода icc
            if key not in agg_data:
                agg_data[key] = {'prices_sum': np.array(filtered_prices[i]),
                                 'counts_sum': np.array(filtered_counts[i]),
                                 'n': 1}
            else:
                agg_data[key]['prices_sum'] += np.array(filtered_prices[i]) * np.array(filtered_counts[i])
                agg_data[key]['n'] += np.array(filtered_counts[i])

        # Рассчитываем средневзвешенные значения
        for key, val in agg_data.items():
            y_sum = val['prices_sum']
            n = val['n']
            y_avg = y_sum / n
            val['prices_avg'] = y_avg

        # Формируем итоговые массивы
        icc_result = []  # Массив значений itemcustomcode
        lid_result = []  # Массив значений gtin
        months_result = []  # Массив значений оси X
        prices_result = []  # Массив значений оси Y

        for key, val in agg_data.items():
            icc_result.append(key[1])
            lid_result.append(key[2])
            months_result.append(list(key[0]))
            prices_result.append(np.round(val['prices_avg'], 2))

        # Преобразование выходных данных в нужный формат
        months_result = np.array(months_result, dtype='object')
        prices_result = np.array(prices_result, dtype='object')

        # Фильтрация выходных данных по длине цепочки и по коду
        filtered_months_result, filtered_prices_result = self.filter_chains(icc_result,
                                                                       months_result,
                                                                       prices_result,
                                                                       target_code,
                                                                       target_size)

        return filtered_months_result, filtered_prices_result


def monthly_prices_visualise(
        dataset: pd.DataFrame,
        input_code: str = '',
        chain_flag: bool = False,
        size_chain: int = 1
):
    """
    :code_assign: users
    :code_type: Пользовательские функции
    :imports: init_gui_dict, Window, Canvas, LinePlot, Scatter2DPlot, monthlyPrices, Chain
    :packages:
    import pandas as pd
    import numpy as np
    import copy
    :param_block pd.DataFrame dataset: датасет
    :param str input_code: выбранная категория
    :param bool chain_flag: флаг для построения цепочек
    :param int size_chain: размер цепочки
    :returns: gui_dict, error
    :rtype: dict, str
    :semrtype: ,
    """
    error = ""
    gui_dict = init_gui_dict()
    MP = monthlyPrices(input_code)
    if input_code == 'Шины':
        codes = MP.tires_codes
    elif input_code == 'Холодильники':
        codes = MP.fridges_codes
    else:
        codes = [input_code]
    
    code_arr_t, sorted_months_arr_t, sorted_year_arr_t, sorted_prices_arr_t = MP.get_monthly_prices(dataset,
                                                                                                    codes)
    canvases = []
    for price, month, code, years in zip(sorted_prices_arr_t, sorted_months_arr_t, code_arr_t, sorted_year_arr_t):
        plots = []
        x = []
        y = []
        for year in sorted(list(set(years))):
            if plots:
                x = [x[-1]]
                y = [y[-1]]
            else:
                x = []
                y = []
            for i in [j for j in range(len(years)) if years[j] == year]:
                x.append(month[i])
                y.append(price[i])
            plots.append(LinePlot(x=np.array(x), y=np.array(y), names=[f'Год {year}']))
        canvases.append(
            Canvas(title=f'Код {code}',
                   showlegend=True,
                   plots=plots
                   )
        )
    gui_dict['plot'].append(
        Window(
            window_title='Средневзвещанные цены',
            canvases=canvases
        ).to_dict()
    )

    if chain_flag:
        CH = Chain(dataset)
        x_points_arr, y_points_arr = CH.get_average_chains(int(input_code), int(size_chain))
        plots = []
        text = [[f"DT"] + ["ETN" + str(i) for i in range(1, size_chain + 1)] + [f"Check"]]
        for x, y in zip(x_points_arr, y_points_arr):
            plots.append(LinePlot(x=np.array(x), y=y, names=[f'Месяц: {"-".join(map(str, x))}']))
            plots.append(Scatter2DPlot(x=np.array(x), y=y, names=[f'Месяц: {"-".join(map(str, x))}'], text=text,
                                       marker=[dict(color="black")]))
        gui_dict['plot'].append(
            Window(
                window_title='Цепочка продаж - линейный график',
                canvases=[Canvas(
                    title=f'Цепочка продаж {input_code} размерностью {size_chain}',
                    x_title='Цепочка',
                    y_title='Цена',
                    showlegend=True,
                    plots=plots)]
            ).to_dict()
        )

    return gui_dict, error
