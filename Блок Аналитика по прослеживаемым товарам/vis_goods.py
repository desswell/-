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
        Добавляем записи по товарам без учета кода
        """
        # flattened_month_arr = []
        # flattened_year_arr = []
        # flattened_price_arr = []
        # flattened_count_arr = []
        # for sublist in month_arr:
        #     flattened_month_arr.extend(sublist)
        # for sublist in year_arr:
        #     flattened_year_arr.extend(sublist)
        # for sublist in price_arr:
        #     flattened_price_arr.extend(sublist)
        # for sublist in count_arr:
        #     flattened_count_arr.extend(sublist)
        #
        # code_arr.append('All_' + self.name)
        # month_arr.append(flattened_month_arr)
        # year_arr.append(flattened_year_arr)
        # price_arr.append(flattened_price_arr)
        # count_arr.append(flattened_count_arr)

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

        if len(av_price_arr) > 0:
            if len(av_price_arr[0]) > 0:
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

                # Поиск минимального года
                min_year = sorted_year_arr[0][0]
                for i in range(len(sorted_year_arr)):
                    for j in range(len(sorted_year_arr[i])):
                        if sorted_year_arr[i][j] < min_year:
                            min_year = sorted_year_arr[i][j]

                # Замена значений месяцев в соответствии с годом
                for i in range(len(sorted_months_arr)):
                    for j in range(len(sorted_months_arr[i])):
                        if sorted_year_arr[i][j] > min_year:
                            sorted_months_arr[i][j] = sorted_months_arr[i][j] + 12 * (sorted_year_arr[i][j] - min_year)

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

    def __init__(self, dataset, include_company, company_unp):
        """
        :param pd.DateFrame: датасет
        :param bool: фильтрация по УНП конкретной компании
        :param str: УНП компании
        """
        self.data = dataset
        self.in_company = include_company
        self.target_unp = company_unp

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

    def read_etn_nums(self):
        """
        Функция чтения цепочек номеров ЕТН
        """
        result = []

        for index, row in self.data.iterrows():
            nums = row['etns']
            etns = re.findall(r'\{([^\}]+)\}', nums)
            etns_array = etns[0].split(',')
            etns_array = [str(etn) for etn in etns_array]
            result.append(etns_array)

        return result

    def read_etn_unps(self):
        """
        Функция чтения цепочек унп ЕТН
        """
        result = []

        for index, row in self.data.iterrows():
            unps = row['unps_shippers']
            etns = re.findall(r'\d+\.\d+|\d+', unps)
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

    def read_dt_nums(self):
        """
        Функция чтения номеров dt
        """
        dts = self.data['nom_reg'].tolist()
        dts = [str(dt) for dt in dts]
        return dts

    def read_dt_unps(self):
        """
        Функция чтения унп dt
        """
        dts = self.data['g14rbunp'].tolist()
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

    def read_check_nums(self):
        """
        Функция чтения номеров check
        """
        checks = self.data['numbers'].tolist()
        checks = [str(check) for check in checks]
        return checks

    def read_check_unps(self):
        """
        Функция чтения унп check
        """
        checks = self.data['unp'].tolist()
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

    def filter_chains(self, icc, months, prices, nums, unps, target_codes, target_size):
        """
        Функция фильтрации цепочек по размеру и коду
        """
        filtered_months = []
        filtered_prices = []
        filtered_nums = []
        filtered_unps = []

        for i, code in enumerate(icc):
            if str(code) in target_codes and len(months[i]) == target_size + 2:
                print(0)
                filtered_months.append(months[i])
                filtered_prices.append(prices[i])
                filtered_nums.append(nums[i])
                filtered_unps.append(unps[i])

        return filtered_months, filtered_prices, filtered_nums, filtered_unps

    def get_average_chains(self, target_codes, target_size):
        """
        Функция вычисления средневзвешенных значений цен для всех цепочек
        """
        # ЧТЕНИЕ ЕТН
        prices = self.read_etn_prices()  # Все цены
        months = self.read_etn_months()  # Все месяцы
        years = self.read_etn_years()  # Все года
        counts = self.read_etn_counts()  # Все количества
        nums = self.read_etn_nums()  # Все номера
        unps = self.read_etn_unps() # Все УНП

        # ЧТЕНИЕ DT
        dt_prices = self.read_dt_prices()
        dt_months = self.read_dt_months()
        dt_years = self.read_dt_years()
        dt_counts = self.read_dt_counts()
        dt_nums = self.read_dt_nums()
        dt_unps = self.read_dt_unps()

        # ЧТЕНИЕ CHECK
        check_prices = self.read_check_prices()
        check_months = self.read_check_months()
        check_years = self.read_check_years()
        check_counts = self.read_check_counts()
        check_nums = self.read_check_nums()
        check_unps = self.read_check_unps()

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
            nums[i].insert(0, dt_nums[i])
            nums[i].append(check_nums[i])
            unps[i].insert(0, dt_unps[i])
            unps[i].append(check_unps[i])

        correct_unp_months = []
        correct_unp_prices = []
        correct_unp_counts = []
        correct_unp_nums = []
        correct_unp_unps = []
        correct_unp_icc = []
        correct_unp_lid = []

        # Сохраняем только цепочки, содержащие код определенной компании
        if self.in_company:
            for i in range(len(unps)):
                save_chain = False
                for company in unps[i]:
                    if str(company) == self.target_unp:
                        save_chain = True
                if save_chain:
                    correct_unp_months.append(months[i])
                    correct_unp_prices.append(prices[i])
                    correct_unp_counts.append(counts[i])
                    correct_unp_nums.append(nums[i])
                    correct_unp_unps.append(unps[i])
                    correct_unp_icc.append(icc[i])
                    correct_unp_lid.append(lid[i])
        else:
            for i in range(len(unps)):
                correct_unp_months.append(months[i])
                correct_unp_prices.append(prices[i])
                correct_unp_counts.append(counts[i])
                correct_unp_nums.append(nums[i])
                correct_unp_unps.append(unps[i])
                correct_unp_icc.append(icc[i])
                correct_unp_lid.append(lid[i])

        """
        Удаляем цепочки, в которых CHECK стоит раньше последней ETN
        """
        # Создаем новый список, в который будем добавлять только нужные подсписки
        filtered_months = []
        filtered_prices = []
        filtered_counts = []
        filtered_nums = []
        filtered_unps = []
        filtered_icc = []
        filtered_lid = []

        for i in range(len(correct_unp_months)):
            if correct_unp_months[i][-1] >= correct_unp_months[i][-2]:
                filtered_months.append(correct_unp_months[i])
                filtered_prices.append(correct_unp_prices[i])
                filtered_counts.append(correct_unp_counts[i])
                filtered_nums.append(correct_unp_nums[i])
                filtered_unps.append(correct_unp_unps[i])
                filtered_icc.append(correct_unp_icc[i])
                filtered_lid.append(correct_unp_lid[i])

        """
        Подсчет средневзвешенных значений по всем подходящим цепочкам
        """
        # Создаем словарь для хранения сумм и весов
        agg_data = {}

        for i in range(len(filtered_icc)):
            key = (tuple(filtered_months[i]), filtered_icc[i], filtered_lid[i], tuple(filtered_nums[i]), tuple(filtered_unps[i]))  # создаем ключ для идентификации уникальной цепочки и кода icc
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
        nums_result = [] # Массив значений номеров
        unps_result = []  # Массив значений УНП компаний

        for key, val in agg_data.items():
            icc_result.append(key[1])
            lid_result.append(key[2])
            months_result.append(list(key[0]))
            prices_result.append(np.round(val['prices_avg'], 2))
            nums_result.append(list(key[3]))
            unps_result.append(list(key[4]))


        # Преобразование выходных данных в нужный формат
        months_result = np.array(months_result, dtype='object')
        prices_result = np.array(prices_result, dtype='object')
        nums_result = np.array(nums_result, dtype='object')
        unps_result = np.array(unps_result, dtype='object')


        # Фильтрация выходных данных по длине цепочки и по коду
        filtered_months_result, filtered_prices_result, filtered_nums_result, filtered_unps_result = self.filter_chains(icc_result,
                                                                                                  months_result,
                                                                                                  prices_result,
                                                                                                  nums_result,
                                                                                                  unps_result,
                                                                                                  target_codes,
                                                                                                  target_size)

        return filtered_months_result, filtered_prices_result, filtered_nums_result, filtered_unps_result


def monthly_prices_visualise(
        dataset: pd.DataFrame,
        input_code: str = '',
        chain_flag: bool = False,
        date_dt: str = '',
        date_check: str = '',
        all_interval: bool = False,
        include_company: bool = False,
        company_unp: str = '',
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
    :param str date_dt: дата ДТ
    :param str date_check: дата чека
    :param bool all_interval: все цепочки внутри интервала дат
    :param bool include_company: цепочки по коду определенной компании
    :param str company_unp: унп компании
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

    canvases = []
    if not dataset.empty:
        code_arr_t, sorted_months_arr_t, sorted_year_arr_t, sorted_prices_arr_t = MP.get_monthly_prices(dataset,
                                                                                                        codes)
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
                       x_title='Месяц',
                       y_title='Цена, бел. руб',
                       showlegend=True,
                       plots=plots
                       )
            )
    else:
        plots = []
        canvases.append(
            Canvas(title='Все коды',
                   x_title='Месяц',
                   y_title='Цена, бел. руб',
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

    # Фильтрация цепочек по интервалу времени
    dataset['dt_date'] = pd.to_datetime(dataset['dt_date'])
    dataset['issued_at'] = pd.to_datetime(dataset['issued_at'])
    if all_interval:
        data_right_dates = dataset[(dataset['dt_date'] >= date_dt) & (dataset['issued_at'] <= date_check)]
    else:
        data_right_dates = dataset[(dataset['dt_date'] == date_dt) & (dataset['issued_at'] == date_check)]

    if chain_flag:
        plots = []
        if not data_right_dates.empty:
            CH = Chain(data_right_dates, include_company, company_unp)
            x_points_arr, y_points_arr, nums_arr, unps_arr = CH.get_average_chains(codes, size_chain)
            if len(x_points_arr) != 0 and len(y_points_arr) != 0 and len(nums_arr) != 0:

                text = [[f"DT"] + ["ETN" + str(i) for i in range(1, size_chain + 1)] + [f"Check"]]

                for x, y, n, u in zip(x_points_arr, y_points_arr, nums_arr, unps_arr):
                    plots.append(LinePlot(x=np.array(x), y=y, names=[f'Месяц: {"-".join(map(str, x))}']))
                    plots.append(Scatter2DPlot(x=np.array(x), y=y, names=[f'Месяц: {"-".join(map(str, x))}'], text=[[text[0][i]+'\n'+n[i]+'\n'+str(u[i]) for i in range(len(text[0]))]],
                                               marker=[dict(color="black")]))

        gui_dict['plot'].append(
            Window(
                window_title='Цепочка продаж - линейный график',
                canvases=[Canvas(
                    title=f'Цепочка продаж по категории {input_code} размерностью {size_chain}',
                    x_title='Цепочка',
                    y_title='Цена, бел. руб',
                    showlegend=True,
                    plots=plots)]
            ).to_dict()
        )

    return gui_dict, error


# Чтение файла
filename = 'test_view_10000.csv'

dataset = pd.read_csv(filename)
input_code = 'Холодильники'    # Код itemcustomcode
chain_flag = True
date_dt = '2022-08-01'
date_check = '2022-11-12'
all_interval = False
include_company = True
company_unp = '700474487'
size_chain = 2             # Длина цепочки

error = monthly_prices_visualise(dataset, input_code, chain_flag, date_dt, date_check, all_interval, include_company, company_unp, size_chain)
