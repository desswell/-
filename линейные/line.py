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


def lineplot_acp(
        dataset: pd.DataFrame,
        input_code: str = '',
        size: Union[int] = 3
):
    """
    :code_assign: users
    :code_type: Пользовательские функции
    :imports: init_gui_dict, Window, Canvas, LinePlot, Chain, Scatter2DPlot
    :packages:
    import numpy as np
    :param_block pd.DataFrame dataset: датасет
    :param str input_code: код для цепочки продаж
    :param Union[int] size: размер цепочки
    :returns: gui_dict, error
    :rtype: dict, str
    :semrtype: ,
    """
    error = ""
    gui_dict = init_gui_dict()
    CH = Chain(dataset)
    x_points_arr, y_points_arr = CH.get_average_chains(int(input_code), int(size))
    plots = []
    text = [["DT"] + ["ETN" + str(i) for i in range(1, size + 1)] + ["Check"]]
    for x, y in zip(x_points_arr, y_points_arr):
        plots.append(LinePlot(x=np.array(x), y=y, names=[f'Месяц: {"-".join(map(str, x))}']))
        plots.append(Scatter2DPlot(x=np.array(x), y=y, names=[f'Месяц: {"-".join(map(str, x))}'], text=text))
    gui_dict['plot'].append(
        Window(
            window_title='Цепочка продаж - линейный график',
            canvases=[Canvas(
                title=f'Цепочка продаж {input_code} размерностью {size}',
                x_title='Цепочка',
                y_title='Цена',
                showlegend=True,
                plots=plots)]
        ).to_dict()
    )
    return gui_dict, error
