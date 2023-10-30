import pandas as pd


class PricesESF:
    """
    :code_assign: service
    :code_type: отрисовка LinePlot
    :packages:
    import pandas as pd
    """

    def __init__(self,
                 dt_data: pd.DataFrame = None,
                 first_esf_data: pd.DataFrame = None,
                 esf_data: pd.DataFrame = None,
                 last_esf_data: pd.DataFrame = None,
                 check_data: pd.DataFrame = None):
        """
        :param pd.DateFrame dt_data: датасет DT
        :param pd.DateFrame first_esf_data: связанных с DT ЭСЧФ
        :param pd.DateFrame esf_data: датасет ЭСЧФ
        :param pd.DateFrame last_esf_data: связанных с CHECK ЭСЧФ
        :param pd.DateFrame check_data: датасет CHECK
        """
        self.data_dt = dt_data
        self.data_first_esf = first_esf_data
        self.data_esf = esf_data
        self.data_last_esf = last_esf_data
        self.data_check = check_data

    def get_dt_means_daily(self):
        """
        Функция подсчета средневзвешенного значения по всем ДТ по дням
        """
        df = self.data_dt
        # Преобразуем поле dt_date в формат даты
        df['dt_date'] = pd.to_datetime(df['dt_date'])

        # Извлекаем год, месяц и день из даты
        df['year'] = df['dt_date'].dt.year
        df['month'] = df['dt_date'].dt.month
        df['day'] = df['dt_date'].dt.day

        # Рассчитываем сумму (продажи * цена) для каждой строки
        df['total_sales'] = df['g38netweightquantity'] * df['ТС/кг, бел руб']

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = df.groupby(['year', 'month', 'day']).apply(
            lambda x: (x['total_sales']).sum() / x['g38netweightquantity'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'day', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        days = grouped['day'].tolist()
        dt_means = grouped['weighted_average_price'].tolist()

        first_date = str(days[0]) + '-' + str(months[0]) + '-' + str(years[0])

        dt_dates = self.dates_to_days(years, months, days)

        return dt_dates, dt_means

    def get_dt_means_monthly(self):
        """
        Функция подсчета средневзвешенного значения по всем ДТ по месяцам
        """
        df = self.data_dt
        # Преобразуем поле dt_date в формат даты
        df['dt_date'] = pd.to_datetime(df['dt_date'])

        # Извлекаем год, месяц и день из даты
        df['year'] = df['dt_date'].dt.year
        df['month'] = df['dt_date'].dt.month

        # Рассчитываем сумму (продажи * цена) для каждой строки
        df['total_sales'] = df['g38netweightquantity'] * df['ТС/кг, бел руб']

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = df.groupby(['year', 'month']).apply(
            lambda x: (x['total_sales']).sum() / x['g38netweightquantity'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'weighted_average_price']
        grouped_weight = df.groupby(['year', 'month'])['g38netweightquantity'].sum().reset_index()
        grouped_weight = grouped_weight.sort_values(['year', 'month'])

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        dt_means = grouped['weighted_average_price'].tolist()

        first_date = str(months[0]) + '-' + str(years[0])

        dt_dates = self.dates_to_months(years, months)

        return dt_dates, dt_means, grouped_weight['g38netweightquantity'].tolist()

    def get_first_esf_means_daily(self):
        """
        Функция подсчета средневзвешенного значения по всем ЭСЧФ по дням
        """
        df = self.data_first_esf
        # Преобразуем поле general_date_transaction в формат даты
        df['general_date_transaction'] = pd.to_datetime(df['general_date_transaction'])

        # Извлекаем год, месяц и день из даты
        df['year'] = df['general_date_transaction'].dt.year
        df['month'] = df['general_date_transaction'].dt.month
        df['day'] = df['general_date_transaction'].dt.day

        # Рассчитываем значение roster_item_price
        new_roster_item_price = (df['roster_item_cost'].sum() / df['roster_item_count'].sum())

        # Добавляем новый столбец new_roster_item_price к DataFrame
        df['new_roster_item_price'] = new_roster_item_price

        # Рассчитываем сумму (продажи * цена) для каждой строки
        df['total_sales'] = df['roster_item_count'] * df['new_roster_item_price']

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = df.groupby(['year', 'month', 'day']).apply(
            lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'day', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        days = grouped['day'].tolist()
        esf_means = grouped['weighted_average_price'].tolist()

        first_date = str(days[0]) + '-' + str(months[0]) + '-' + str(years[0])

        first_esf_dates = self.dates_to_days(years, months, days)

        return first_esf_dates, esf_means

    def get_first_esf_means_monthly(self):
        """
        Функция подсчета средневзвешенного значения по всем ЭСЧФ по месяцам
        """
        df = self.data_first_esf
        # Преобразуем поле general_date_transaction в формат даты
        df['general_date_transaction'] = pd.to_datetime(df['general_date_transaction'])

        # Извлекаем год, месяц и день из даты
        df['year'] = df['general_date_transaction'].dt.year
        df['month'] = df['general_date_transaction'].dt.month

        # Рассчитываем значение roster_item_price
        new_roster_item_price = (df['roster_item_cost'].sum() / df['roster_item_count'].sum())

        # Добавляем новый столбец new_roster_item_price к DataFrame
        df['new_roster_item_price'] = new_roster_item_price

        # Рассчитываем сумму (продажи * цена) для каждой строки
        df['total_sales'] = df['roster_item_count'] * df['new_roster_item_price']

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = df.groupby(['year', 'month']).apply(
            lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        esf_means = grouped['weighted_average_price'].tolist()

        first_date = str(months[0]) + '-' + str(years[0])

        first_esf_dates = self.dates_to_months(years, months)

        return first_esf_dates, esf_means

    def get_esf_means_daily(self):
        """
        Функция подсчета средневзвешенного значения по всем ЭСЧФ по дням
        """
        df = self.data_esf
        # Преобразуем поле general_date_transaction в формат даты
        df['general_date_transaction'] = pd.to_datetime(df['general_date_transaction'])

        # Извлекаем год, месяц и день из даты
        df['year'] = df['general_date_transaction'].dt.year
        df['month'] = df['general_date_transaction'].dt.month
        df['day'] = df['general_date_transaction'].dt.day

        # Рассчитываем сумму (продажи * цена) для каждой строки
        df['total_sales'] = df['roster_item_count'] * df['roster_item_price']

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = df.groupby(['year', 'month', 'day']).apply(
            lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'day', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        days = grouped['day'].tolist()
        esf_means = grouped['weighted_average_price'].tolist()

        first_date = str(days[0]) + '-' + str(months[0]) + '-' + str(years[0])

        esf_dates = self.dates_to_days(years, months, days)

        return esf_dates, esf_means

    def get_esf_means_monthly(self):
        """
        Функция подсчета средневзвешенного значения по всем ЭСЧФ по месяцам
        """
        df = self.data_esf
        # Преобразуем поле general_date_transaction в формат даты
        df['general_date_transaction'] = pd.to_datetime(df['general_date_transaction'])

        # Извлекаем год, месяц и день из даты
        df['year'] = df['general_date_transaction'].dt.year
        df['month'] = df['general_date_transaction'].dt.month

        # Рассчитываем сумму (продажи * цена) для каждой строки
        df['total_sales'] = df['roster_item_count'] * df['roster_item_price']

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = df.groupby(['year', 'month']).apply(
            lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        esf_means = grouped['weighted_average_price'].tolist()

        first_date = str(months[0]) + '-' + str(years[0])

        esf_dates = self.dates_to_months(years, months)

        return esf_dates, esf_means

    def get_last_esf_means_daily(self):
        """
        Функция подсчета средневзвешенного значения по последнему ЭСЧФ по дням
        """
        df = self.data_last_esf
        # Преобразуем поле general_date_transaction в формат даты
        df['general_date_transaction'] = pd.to_datetime(df['general_date_transaction'])

        # Извлекаем год, месяц и день из даты
        df['year'] = df['general_date_transaction'].dt.year
        df['month'] = df['general_date_transaction'].dt.month
        df['day'] = df['general_date_transaction'].dt.day

        # Рассчитываем сумму (продажи * цена) для каждой строки
        df['total_sales'] = df['roster_item_count'] * df['roster_item_price']

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = df.groupby(['year', 'month', 'day']).apply(
            lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'day', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        days = grouped['day'].tolist()
        last_esf_means = grouped['weighted_average_price'].tolist()

        first_date = str(days[0]) + '-' + str(months[0]) + '-' + str(years[0])

        last_esf_dates = self.dates_to_days(years, months, days)

        return last_esf_dates, last_esf_means

    def get_last_esf_means_monthly(self):
        """
        Функция подсчета средневзвешенного значения по последнему ЭСЧФ по месяцам
        """
        df = self.data_last_esf
        # Преобразуем поле general_date_transaction в формат даты
        df['general_date_transaction'] = pd.to_datetime(df['general_date_transaction'])

        # Извлекаем год, месяц и день из даты
        df['year'] = df['general_date_transaction'].dt.year
        df['month'] = df['general_date_transaction'].dt.month

        # Рассчитываем сумму (продажи * цена) для каждой строки
        df['total_sales'] = df['roster_item_count'] * df['roster_item_price']

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = df.groupby(['year', 'month']).apply(
            lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        last_esf_means = grouped['weighted_average_price'].tolist()

        first_date = str(months[0]) + '-' + str(years[0])

        last_esf_dates = self.dates_to_months(years, months)

        return last_esf_dates, last_esf_means

    def get_check_means_daily(self):
        """
        Функция подсчета средневзвешенного значения по всем ЧЕКам по дням
        """
        df = self.data_check
        # Рассчитываем общую сумму (продажи * цена) для каждой строки
        df['total_sales'] = df['position_count'] * df['price']

        # Группируем данные по году, месяцу и дню, а затем рассчитываем средневзвешенное значение
        grouped = df.groupby(['year_check', 'month_check', 'day_check']).apply(
            lambda x: (x['total_sales']).sum() / x['position_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'day', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        days = grouped['day'].tolist()
        check_means = grouped['weighted_average_price'].tolist()

        first_date = str(days[0]) + '-' + str(months[0]) + '-' + str(years[0])

        check_dates = self.dates_to_days(years, months, days)

        return check_dates, check_means

    def get_check_means_monthly(self):
        """
        Функция подсчета средневзвешенного значения по всем Чекам по месяцам
        """
        df = self.data_check
        # Рассчитываем общую сумму (продажи * цена) для каждой строки
        df['total_sales'] = df['position_count'] * df['price']

        # Группируем данные по году, месяцу и дню, а затем рассчитываем средневзвешенное значение
        grouped = df.groupby(['year_check', 'month_check']).apply(
            lambda x: (x['total_sales']).sum() / x['position_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        check_means = grouped['weighted_average_price'].tolist()

        first_date = str(months[0]) + '-' + str(years[0])

        check_dates = self.dates_to_months(years, months)

        return check_dates, check_means

    def dates_to_days(self, years, months, days):
        """
        Функция преобразования дат в дни
        """
        # Замена значений дней в соответствии с месяцем
        for i in range(len(months)):
            match months[i]:
                case 1:
                    days[i] += 0
                case 2:
                    days[i] += 31
                case 3:
                    days[i] += 59
                case 4:
                    days[i] += 90
                case 5:
                    days[i] += 120
                case 6:
                    days[i] += 151
                case 7:
                    days[i] += 181
                case 8:
                    days[i] += 212
                case 9:
                    days[i] += 243
                case 10:
                    days[i] += 273
                case 11:
                    days[i] += 304
                case 12:
                    days[i] += 334

        # Поиск минимального года
        min_year = years[0]
        for i in range(len(years)):
            if years[i] < min_year:
                min_year = years[i]

        # Замена значений дней в соответствии с годом
        for i in range(len(days)):
            if years[i] > min_year:
                days[i] = days[i] + 365 * (years[i] - min_year)

        return days

    def dates_to_months(self, years, months):
        """
        Функция преобразования дат в месяцы
        """
        # Поиск минимального года
        min_year = years[0]
        for i in range(len(years)):
            if years[i] < min_year:
                min_year = years[i]

        # Замена значений дней в соответствии с годом
        for i in range(len(months)):
            if years[i] > min_year:
                months[i] = months[i] + 12 * (years[i] - min_year)

        return months


class ACPLinearRegression:
    """
    :code_assign: service
    :code_type: Линейная регрессия АСР
    :imports: LinePlot, Scatter2DPlot
    :packages:
    import numpy as np
    from sklearn.linear_model import LinearRegression
    """

    def __init__(self,
                 x: list = [None],
                 y: list = [None],
                 step: int = 1,
                 names: list = [None],
                 weights: list = []
                 ):
        """
        :param list y: list[np.array] координаты x
        :param int step: шаг регрессии
        :param list names: имена прямых
        :param list weight: веса
        """
        self.x = x
        self.y = y
        self.step = step
        self.names = names
        self.weights = weights

    def train_regression(self):
        """
        Обучение модели
        :return: list plots: полотна
        """
        plots = list()

        for x, y, name, weight in zip(self.x, self.y, self.names, self.weights):
            x_reshaped = np.array(x).reshape((-1, 1))
            model = LinearRegression()
            model_weight = LinearRegression()
            model.fit(x_reshaped, y)
            model_weight.fit(x_reshaped, np.array(weight))
            xy_pred = model.predict(x_reshaped)
            intercept = model.intercept_
            coefficient = model.coef_
            intercept_weight = model_weight.intercept_
            coefficient_weight = model_weight.coef_
            x_range = list(range(max(x) + 1, max(x) + 1 + self.step))
            x_pred = np.array(x_range).reshape((-1, 1))
            y_pred = np.array([intercept + coefficient * i for i in x_range])
            y_pred_weight = np.array([intercept_weight + coefficient_weight * i for i in x_range])
            weight = [f'Объем: {i // 1000} т' for i in weight]
            weight_predicted = [f'Объем: {i // 1000} т' for i in y_pred_weight]
            plots.append(
                LinePlot(x=np.append(x_reshaped, x_pred), y=np.append(xy_pred, y_pred), names=['Тренд ' + name]))
            plots.append(Scatter2DPlot(x=x_reshaped, y=xy_pred, names=['Тренд ' + name],
                                       marker=[dict(color="black")],
                                       text=[weight],
                                       ))
            plots.append(Scatter2DPlot(x=x_pred, y=y_pred, names=['Тренд ' + name],
                                       marker=[dict(color="red")],
                                       text=[weight_predicted]
                                       ))
        return plots


def lineplot_esf(
        dataset_dt: pd.DataFrame,
        dataset_esf: pd.DataFrame,
        dataset_check: pd.DataFrame,
        monthly: bool = False,
        linear_regression: bool = False,
        product_code: int = 803901000,
        start_date: str = '',
        end_date: str = '',
        step_regression: int = 1,
):
    """
    :code_assign: users
    :code_type: Пользовательские функции
    :imports: init_gui_dict, Window, Canvas, LinePlot, Scatter2DPlot, PricesESF, ACPLinearRegression
    :packages:
    import pandas as pd
    import numpy as np
    :param_block pd.DataFrame dataset_dt: датасет DT и связанных ЭСЧФ
    :param_block pd.DataFrame dataset_esf: датасет ЭСЧФ
    :param_block pd.DataFrame dataset_check: датасет CHECK и связанных ЭСЧФ
    :param bool monthly: флаг разбивки на месяца
    :param bool linear_regression: флаг для линейной регрессии
    :param int product_code: код товара
    :param str start_date: дата начала
    :param str end_date: дата конца
    :param int step_regression: шаг регрессии
    :returns: gui_dict, error
    :rtype: dict, str
    :semrtype: ,
    """
    error = ""
    gui_dict = init_gui_dict()
    pd.options.mode.chained_assignment = None

    # Фильтрация датасета по коду товара
    dataset_dt_filtered = dataset_dt[(dataset_dt['roster_item_code'] == product_code)]
    dataset_esf_filtered = dataset_esf[(dataset_esf['roster_item_code'] == product_code)]
    dataset_check_filtered = dataset_check[(dataset_check['roster_item_code'] == product_code)]

    if dataset_dt_filtered.empty or dataset_esf_filtered.empty or dataset_check_filtered.empty:
        raise Exception(f'Нет записей по коду {product_code}')

    # Фильтрация датасета по дате
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    dataset_dt_filtered['dt_date'] = pd.to_datetime(dataset_dt_filtered['dt_date'])
    dataset_dt_filtered['general_date_transaction'] = pd.to_datetime(dataset_dt_filtered['general_date_transaction'])
    dataset_esf_filtered['general_date_transaction'] = pd.to_datetime(dataset_esf_filtered['general_date_transaction'])
    dataset_check_filtered['general_date_transaction'] = pd.to_datetime(
        dataset_check_filtered['general_date_transaction'])
    dataset_check_filtered['issued_at'] = pd.to_datetime(dataset_check_filtered['issued_at'])

    dt_data = dataset_dt_filtered.loc[
        (dataset_dt_filtered['dt_date'] >= start_date) & (dataset_dt_filtered['dt_date'] <= end_date)]
    first_esf_data = dataset_dt_filtered.loc[(dataset_dt_filtered['general_date_transaction'] >= start_date) & (
            dataset_dt_filtered['general_date_transaction'] <= end_date)]
    esf_data = dataset_esf_filtered.loc[(dataset_esf_filtered['general_date_transaction'] >= start_date) & (
            dataset_esf_filtered['general_date_transaction'] <= end_date)]
    last_esf_data = dataset_check_filtered.loc[(dataset_check_filtered['general_date_transaction'] >= start_date) & (
            dataset_check_filtered['general_date_transaction'] <= end_date)]
    check_data = dataset_check_filtered.loc[
        (dataset_check_filtered['issued_at'] >= start_date) & (dataset_check_filtered['issued_at'] <= end_date)]

    pe = PricesESF(dt_data, first_esf_data, esf_data, last_esf_data, check_data)
    weights = ['ДТ']
    if monthly:
        sorted_dt_dates, dt_means, weights = pe.get_dt_means_monthly()
        sorted_first_esf_dates, first_esf_means = pe.get_first_esf_means_monthly()
        sorted_esf_dates, esf_means = pe.get_esf_means_monthly()
        sorted_last_esf_dates, last_esf_means = pe.get_last_esf_means_monthly()
        sorted_check_dates, check_means = pe.get_check_means_monthly()
    else:
        sorted_dt_dates, dt_means = pe.get_dt_means_daily()
        sorted_first_esf_dates, first_esf_means = pe.get_first_esf_means_daily()
        sorted_esf_dates, esf_means = pe.get_esf_means_daily()
        sorted_last_esf_dates, last_esf_means = pe.get_last_esf_means_daily()
        sorted_check_dates, check_means = pe.get_last_esf_means_daily()

    x_list = [np.array(arr) for arr in [sorted_dt_dates, sorted_first_esf_dates,
                                        sorted_esf_dates, sorted_last_esf_dates, sorted_check_dates]]
    y_list = [np.array(arr) for arr in [dt_means, first_esf_means, esf_means, last_esf_means, check_means]]
    names = ['ДТ', 'ЭСЧФ1', 'Все ЭСЧФ', 'Последняя ЭСЧФ', 'Чек']
    plots = []

    if linear_regression and monthly:
        lr = ACPLinearRegression(x_list, y_list, step_regression, names, weights)
        plots = lr.train_regression()
    for x, y, name in zip(x_list, y_list, names):
        plots.append(LinePlot(x=x, y=y, names=[name]))
        plots.append(Scatter2DPlot(x=x, y=y, names=[name], marker=[dict(color="black")], text=[weights]))

    gui_dict['plot'].append(
        Window(
            window_title='Цепочка продаж - линейный график',
            canvases=[Canvas(
                title=f'Средневзвешенные цены продаж по товару {product_code} с {start_date} по {end_date}',
                x_title=f'{"Месяц" if monthly else "День"}',
                y_title='Цена',
                showlegend=True,
                plots=plots)]
        ).to_dict()
    )

    return gui_dict, error
