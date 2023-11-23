class Market_esf:
    """
    :code_assign: service
    :code_type: отрисовка BarPlot
    :packages:
    import pandas as pd
    import numpy as np
    """

    def __init__(self, dt_data, first_esf_data, esf_data, last_esf_data, check_data, dt_esf, esf, checks):
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
        self.dt_esf = dt_esf
        self.esf = esf
        self.checks = checks

    def get_active_companies(self, esf_data):
        """
        Функция поиска списка активных компаний за временной промежуток
        """
        # Получаем уникальные названия компаний из полей provider_unp и recipient_unp
        unique_companies = pd.concat([esf_data['provider_unp'], esf_data['recipient_unp']]).unique()

        df_active_companies = pd.DataFrame(unique_companies, columns=['УНП'])

        return df_active_companies

    def count_interval(self, left, right):
        """
        Функция вычисления дельты - размерности временного интервала
        """
        left = pd.to_datetime(left)
        right = pd.to_datetime(right)

        return int((right - left).days)

    def get_name_of_companies(self, codes):
        df = self.esf.copy()
        df['provider_name'] = df['provider_name'].astype(str)
        df['provider_unp'] = df['provider_unp'].astype(str)
        df['provider_unp'] = df['provider_unp'].apply(lambda x: x.rstrip('0').rstrip('.'))
        df['provider_name'] = df['provider_name'].fillna('')
        unique_combinations = df.groupby('provider_unp')['provider_name'].unique().reset_index()
        names = unique_combinations[(unique_combinations['provider_unp'].isin(codes))].copy()
        names['короткое'] = names['provider_name'].astype(str).apply(
            lambda x: x.split('"')[-2] if '"' in str(x) else ' '.join(x.split("'")[-2].split()[-2:]) if "'" in x
            else x.split()[-2:] if x else '')
        names = names.sort_values(by=['provider_unp'],
                                  key=lambda x: x.map({v: i for i, v in enumerate(codes)})).reset_index(drop=True)
        names['УНП_names'] = names['короткое'].astype(str) + ' (' + names['provider_unp'].astype(str) + ')'
        return names

    def get_statistics(self, esf_data, date_start, date_end):
        """
        Функция подсчета статистики для каждой компании
        """
        active_companies = self.get_active_companies(esf_data)

        company_arr = active_companies['УНП'].tolist()
        buy_price_arr = [0 for x in range(len(company_arr))]
        delta_buy_arr = [0 for x in range(len(company_arr))]
        sell_price_arr = [0 for x in range(len(company_arr))]
        delta_sell_arr = [0 for x in range(len(company_arr))]
        sell_buy_arr = [0 for x in range(len(company_arr))]

        # Группируем данные по поставщику и рассчитываем среднюю цену покупки
        avg_buy_price = esf_data.groupby('recipient_unp')['roster_item_price'].mean().reset_index()
        avg_buy_price.columns = ['recipient_unp', 'average_buy_price']
        # Возвращаем результаты в виде массивов
        buy_company = avg_buy_price['recipient_unp'].tolist()
        buy_price = avg_buy_price['average_buy_price'].tolist()

        # Средняя цена покупки и продажи по рынку
        avg_price_all = esf_data['roster_item_price'].mean()

        # Группируем данные по поставщику и рассчитываем среднюю цену продажи
        avg_sell_price = esf_data.groupby('provider_unp')['roster_item_price'].mean().reset_index()
        avg_sell_price.columns = ['provider_unp', 'average_sell_price']
        # Возвращаем результаты в виде массивов
        sell_company = avg_sell_price['provider_unp'].tolist()
        sell_price = avg_sell_price['average_sell_price'].tolist()

        for i in range(len(company_arr)):
            for j in range(len(sell_company)):
                if company_arr[i] == sell_company[j]:
                    sell_price_arr[i] = sell_price[j]

        for i in range(len(company_arr)):
            for j in range(len(buy_company)):
                if company_arr[i] == buy_company[j]:
                    buy_price_arr[i] = buy_price[j]

        # Отношение sell - buy
        for i in range(len(company_arr)):
            if sell_price_arr[i] != 0 and buy_price_arr[i] != 0:
                sell_buy_arr[i] = sell_price_arr[i] - buy_price_arr[i]

        # Подсчет дельты от средней цены по рынку
        for i in range(len(company_arr)):
            delta_buy_arr[i] = buy_price_arr[i] - avg_price_all
            delta_sell_arr[i] = sell_price_arr[i] - avg_price_all

        df_statistics = pd.DataFrame(
            list(zip(company_arr, buy_price_arr, delta_buy_arr, sell_price_arr, delta_sell_arr, sell_buy_arr)),
            columns=['УНП', 'Ср.вз. цена покупки', 'Дельта от ср. цены покупки по рынку', 'Ср.вз. цена продажи',
                     'Дельта от ср. цены продажи по рынку', 'Отношение'])
        df_statistics = df_statistics.fillna(0)

        # Добавление количества продаж и закупок и стоимости продаж и закупок
        df_statistics['Количество продаж'] = 0
        df_statistics['Количество закупок'] = 0
        df_statistics['% от рынка по кол-ву продаж'] = 0
        df_statistics['% от рынка по кол-ву закупок'] = 0
        df_statistics['Стоимость продаж'] = 0
        df_statistics['Стоимость закупок'] = 0
        df_statistics['% от рынка по стоимости продаж'] = 0
        df_statistics['% от рынка по стоимости закупок'] = 0

        grouped_sale = esf_data.groupby(['provider_unp']).agg(
            {'roster_item_cost': 'sum', 'roster_item_count': 'sum'}).reset_index()
        grouped_buy = esf_data.groupby(['recipient_unp']).agg(
            {'roster_item_cost': 'sum', 'roster_item_count': 'sum'}).reset_index()

        grouped_sale = grouped_sale.dropna()
        for i in range(len(df_statistics['УНП'])):
            for j in range(len(grouped_sale['provider_unp'])):
                if df_statistics['УНП'][i] == grouped_sale['provider_unp'][j]:
                    df_statistics['Количество продаж'][i] = df_statistics['Количество продаж'][i] + \
                                                            grouped_sale['roster_item_count'][j]
                    df_statistics['Стоимость продаж'][i] = df_statistics['Стоимость продаж'][i] + \
                                                           grouped_sale['roster_item_cost'][j]
                else:
                    pass

        grouped_buy = grouped_buy.dropna()
        for i in range(len(df_statistics['УНП'])):
            for j in range(len(grouped_buy['recipient_unp'])):
                if df_statistics['УНП'][i] == grouped_buy['recipient_unp'][j]:
                    df_statistics['Количество закупок'][i] = df_statistics['Количество закупок'][i] + \
                                                             grouped_buy['roster_item_count'][j]
                    df_statistics['Стоимость закупок'][i] = df_statistics['Стоимость закупок'][i] + \
                                                            grouped_buy['roster_item_cost'][j]
                else:
                    pass

        # Добавление процентов покупки и продажи от рынка
        interval = self.count_interval(date_start, date_end)
        df_statistics['% актив продаж'] = 0
        df_statistics['% актив покупок'] = 0
        for i in range(len(df_statistics['УНП'])):
            df_statistics['% от рынка по кол-ву продаж'][i] = (df_statistics['Количество продаж'][i] / df_statistics[
                'Количество продаж'].sum()) * 100
            df_statistics['% от рынка по кол-ву закупок'][i] = (df_statistics['Количество закупок'][i] / df_statistics[
                'Количество закупок'].sum()) * 100
            df_statistics['% от рынка по стоимости продаж'][i] = (df_statistics['Стоимость продаж'][i] / df_statistics[
                'Стоимость продаж'].sum()) * 100
            df_statistics['% от рынка по стоимости закупок'][i] = (df_statistics['Стоимость закупок'][i] /
                                                                   df_statistics['Стоимость закупок'].sum()) * 100
            company_number = df_statistics.at[i, 'УНП']
            count_days_seller = esf_data[esf_data['provider_unp'] == company_number][
                'general_date_transaction'].nunique()
            count_days_buyer = esf_data[esf_data['recipient_unp'] == company_number][
                'general_date_transaction'].nunique()
            percentages_sellers = (count_days_seller / interval) * 100
            percentages_buyers = (count_days_buyer / interval) * 100
            df_statistics.at[i, '% актив продаж'] = percentages_sellers
            df_statistics.at[i, '% актив покупок'] = percentages_buyers
        return df_statistics, avg_price_all

    def get_dt_means_daily(self):
        """
        Функция подсчета средневзвешенного значения по всем ДТ по дням
        """
        # Преобразуем поле dt_date в формат даты
        self.data_dt['dt_date'] = pd.to_datetime(self.data_dt['dt_date'])

        # Извлекаем год, месяц и день из даты
        self.data_dt['year'] = self.data_dt['dt_date'].dt.year
        self.data_dt['month'] = self.data_dt['dt_date'].dt.month
        self.data_dt['day'] = self.data_dt['dt_date'].dt.day

        # Рассчитываем сумму (продажи * цена) для каждой строки
        self.data_dt['total_sales'] = self.data_dt['g38netweightquantity'] * self.data_dt['ТС/кг, бел руб']

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = self.data_dt.groupby(['year', 'month', 'day']).apply(
            lambda x: (x['total_sales']).sum() / x['g38netweightquantity'].sum()).reset_index()

        # grouped = grouped.rename(columns={grouped.columns[-1]: 'weighted_average_price'})
        grouped.columns = ['year', 'month', 'day', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        days = grouped['day'].tolist()
        dt_means = grouped['weighted_average_price'].tolist()

        dt_days = self.dates_to_days(years, months, days)

        return dt_days, dt_means

    def get_dt_means_monthly(self):
        """
        Функция подсчета средневзвешенного значения по всем ДТ по месяцам
        """
        # Преобразуем поле dt_date в формат даты
        self.data_dt['dt_date'] = pd.to_datetime(self.data_dt['dt_date'])

        # Извлекаем год и месяц из даты
        self.data_dt['year'] = self.data_dt['dt_date'].dt.year
        self.data_dt['month'] = self.data_dt['dt_date'].dt.month

        # Рассчитываем сумму (продажи * цена) для каждой строки
        self.data_dt['total_sales'] = self.data_dt['g38netweightquantity'] * self.data_dt['ТС/кг, бел руб']

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = self.data_dt.groupby(['year', 'month']).apply(
            lambda x: (x['total_sales']).sum() / x['g38netweightquantity'].sum()).reset_index()

        # grouped = grouped.rename(columns={grouped.columns[-1]: 'weighted_average_price'})
        grouped.columns = ['year', 'month', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        dt_means = grouped['weighted_average_price'].tolist()

        dt_months = self.dates_to_months(years, months)

        return dt_months, dt_means

    def get_first_esf_means_daily(self):
        """
        Функция подсчета средневзвешенного значения по первым ЭСЧФ по дням
        """

        # Преобразуем поле general_date_transaction в формат даты
        self.data_first_esf['general_date_transaction'] = pd.to_datetime(
            self.data_first_esf['general_date_transaction'])

        # Извлекаем год, месяц и день из даты
        self.data_first_esf['year'] = self.data_first_esf['general_date_transaction'].dt.year
        self.data_first_esf['month'] = self.data_first_esf['general_date_transaction'].dt.month
        self.data_first_esf['day'] = self.data_first_esf['general_date_transaction'].dt.day

        # Рассчитываем значение roster_item_price
        # new_roster_item_price = (
        #         self.data_first_esf['roster_item_cost'].sum() / self.data_first_esf['roster_item_count'].sum())
        #
        # # Добавляем новый столбец new_roster_item_price к DataFrame
        # self.data_first_esf['new_roster_item_price'] = new_roster_item_price

        # Рассчитываем сумму (продажи * цена) для каждой строки
        # self.data_first_esf['total_sales'] = self.data_first_esf['roster_item_count'] * self.data_first_esf[
        #     'new_roster_item_price']

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = self.data_first_esf.groupby(['year', 'month', 'day']).apply(
            lambda x: (x['roster_item_cost']).sum() / x['roster_item_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'day', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        days = grouped['day'].tolist()
        esf_means = grouped['weighted_average_price'].tolist()

        esf_days = self.dates_to_days(years, months, days)

        return esf_days, esf_means

    def get_first_esf_means_monthly(self):
        """
        Функция подсчета средневзвешенного значения по первым ЭСЧФ по месяцам
        """

        # Преобразуем поле general_date_transaction в формат даты
        self.data_first_esf['general_date_transaction'] = pd.to_datetime(
            self.data_first_esf['general_date_transaction'])

        # Извлекаем год и месяц из даты
        self.data_first_esf['year'] = self.data_first_esf['general_date_transaction'].dt.year
        self.data_first_esf['month'] = self.data_first_esf['general_date_transaction'].dt.month

        # Рассчитываем значение roster_item_price
        # new_roster_item_price = (
        #         self.data_first_esf['roster_item_cost'].sum() / self.data_first_esf['roster_item_count'].sum())
        #
        # # Добавляем новый столбец new_roster_item_price к DataFrame
        # self.data_first_esf['new_roster_item_price'] = new_roster_item_price

        # # Рассчитываем сумму (продажи * цена) для каждой строки
        # self.data_first_esf['total_sales'] = self.data_first_esf['roster_item_count'] * self.data_first_esf[
        #     'new_roster_item_price']

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = self.data_first_esf.groupby(['year', 'month']).apply(
            lambda x: (x['roster_item_cost']).sum() / x['roster_item_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        esf_means = grouped['weighted_average_price'].tolist()

        esf_months = self.dates_to_months(years, months)

        return esf_months, esf_means

    def get_second_esf_means_daily(self):
        """
        Функция подсчета средневзвешенного значения по ЭСЧФ2 по дням
        """

        # Преобразуем поле general_date_transaction в формат даты
        self.data_esf['general_date_transaction'] = pd.to_datetime(
            self.data_esf['general_date_transaction'])

        # Извлекаем год, месяц и день из даты
        self.data_esf['year'] = self.data_esf['general_date_transaction'].dt.year
        self.data_esf['month'] = self.data_esf['general_date_transaction'].dt.month
        self.data_esf['day'] = self.data_esf['general_date_transaction'].dt.day
        df_first = self.data_first_esf.copy()
        first_esf = df_first['recipient_unp'].astype(str).unique().tolist()
        second_esf = self.data_esf[(self.data_esf['provider_unp'].astype(str).isin(first_esf))]

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = second_esf.groupby(['year', 'month', 'day']).apply(
            lambda x: (x['roster_item_cost']).sum() / x['roster_item_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'day', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        days = grouped['day'].tolist()
        esf_means = grouped['weighted_average_price'].tolist()

        esf_days = self.dates_to_days(years, months, days)

        return esf_days, esf_means

    def get_second_esf_means_monthly(self):
        """
        Функция подсчета средневзвешенного значения по ЭСЧФ2 по месяцам
        """

        # Преобразуем поле general_date_transaction в формат даты
        self.data_esf['general_date_transaction'] = pd.to_datetime(
            self.data_esf['general_date_transaction'])

        # Извлекаем год и месяц из даты
        self.data_esf['year'] = self.data_esf['general_date_transaction'].dt.year
        self.data_esf['month'] = self.data_esf['general_date_transaction'].dt.month
        df_first = self.data_first_esf.copy()
        first_esf = df_first['recipient_unp'].astype(str).unique().tolist()
        second_esf = self.data_esf[(self.data_esf['provider_unp'].astype(str).isin(first_esf))]

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = second_esf.groupby(['year', 'month']).apply(
            lambda x: (x['roster_item_cost']).sum() / x['roster_item_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'weighted_average_price']
        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        esf_means = grouped['weighted_average_price'].tolist()

        esf_months = self.dates_to_months(years, months)

        return esf_months, esf_means

    # def get_esf_means_daily(self):
    #     """
    #     Функция подсчета средневзвешенного значения по всем ЭСЧФ по дням
    #     """
    #
    #     # Преобразуем поле general_date_transaction в формат даты
    #     self.data_esf['general_date_transaction'] = pd.to_datetime(self.data_esf['general_date_transaction'])
    #
    #     # Извлекаем год, месяц и день из даты
    #     self.data_esf['year'] = self.data_esf['general_date_transaction'].dt.year
    #     self.data_esf['month'] = self.data_esf['general_date_transaction'].dt.month
    #     self.data_esf['day'] = self.data_esf['general_date_transaction'].dt.day
    #
    #     # Рассчитываем сумму (продажи * цена) для каждой строки
    #     self.data_esf['total_sales'] = self.data_esf['roster_item_count'] * self.data_esf['roster_item_price']
    #
    #     # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
    #     grouped = self.data_esf.groupby(['year', 'month', 'day']).apply(
    #         lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
    #     grouped.columns = ['year', 'month', 'day', 'weighted_average_price']
    #
    #     # Возвращаем результаты в виде массивов
    #     years = grouped['year'].tolist()
    #     months = grouped['month'].tolist()
    #     days = grouped['day'].tolist()
    #     esf_means = grouped['weighted_average_price'].tolist()
    #
    #     esf_days = self.dates_to_days(years, months, days)
    #
    #     return esf_days, esf_means

    # def get_esf_means_monthly(self):
    #     """
    #     Функция подсчета средневзвешенного значения по всем ЭСЧФ по месяцам
    #     """
    #
    #     # Преобразуем поле general_date_transaction в формат даты
    #     self.data_esf['general_date_transaction'] = pd.to_datetime(self.data_esf['general_date_transaction'])
    #
    #     # Извлекаем год и месяц из даты
    #     self.data_esf['year'] = self.data_esf['general_date_transaction'].dt.year
    #     self.data_esf['month'] = self.data_esf['general_date_transaction'].dt.month
    #
    #     # Рассчитываем сумму (продажи * цена) для каждой строки
    #     self.data_esf['total_sales'] = self.data_esf['roster_item_count'] * self.data_esf['roster_item_price']
    #
    #     # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
    #     grouped = self.data_esf.groupby(['year', 'month']).apply(
    #         lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
    #     grouped.columns = ['year', 'month', 'weighted_average_price']
    #
    #     # Возвращаем результаты в виде массивов
    #     years = grouped['year'].tolist()
    #     months = grouped['month'].tolist()
    #     esf_means = grouped['weighted_average_price'].tolist()
    #
    #     esf_months = self.dates_to_months(years, months)
    #
    #     return esf_months, esf_means
    #
    def get_last_esf_means_daily(self):
        """
        Функция подсчета средневзвешенного значения по последнему ЭСЧФ по дням
        """

        # Преобразуем поле general_date_transaction в формат даты
        self.data_last_esf['general_date_transaction'] = pd.to_datetime(self.data_last_esf['general_date_transaction'])

        # Извлекаем год, месяц и день из даты
        self.data_last_esf['year'] = self.data_last_esf['general_date_transaction'].dt.year
        self.data_last_esf['month'] = self.data_last_esf['general_date_transaction'].dt.month
        self.data_last_esf['day'] = self.data_last_esf['general_date_transaction'].dt.day

        # Рассчитываем сумму (продажи * цена) для каждой строки
        self.data_last_esf['total_sales'] = self.data_last_esf['roster_item_count'] * self.data_last_esf[
            'roster_item_price']

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = self.data_last_esf.groupby(['year', 'month', 'day']).apply(
            lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'day', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        days = grouped['day'].tolist()
        esf_means = grouped['weighted_average_price'].tolist()

        esf_days = self.dates_to_days(years, months, days)

        return esf_days, esf_means

    def get_last_esf_means_monthly(self):
        """
        Функция подсчета средневзвешенного значения по последнему ЭСЧФ по месяцам
        """

        # Преобразуем поле general_date_transaction в формат даты
        self.data_last_esf['general_date_transaction'] = pd.to_datetime(self.data_last_esf['general_date_transaction'])

        # Извлекаем год и месяц из даты
        self.data_last_esf['year'] = self.data_last_esf['general_date_transaction'].dt.year
        self.data_last_esf['month'] = self.data_last_esf['general_date_transaction'].dt.month

        # Рассчитываем сумму (продажи * цена) для каждой строки
        self.data_last_esf['total_sales'] = self.data_last_esf['roster_item_count'] * self.data_last_esf[
            'roster_item_price']

        # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
        grouped = self.data_last_esf.groupby(['year', 'month']).apply(
            lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        esf_means = grouped['weighted_average_price'].tolist()

        esf_months = self.dates_to_months(years, months)

        return esf_months, esf_means

    def get_check_means_daily(self):
        """
        Функция подсчета средневзвешенного значения по всем Чекам по дням
        """
        # Преобразуем поле general_date_transaction в формат даты
        self.data_check['issued_at'] = pd.to_datetime(self.data_check['issued_at'])

        # Извлекаем год, месяц и день из даты
        self.data_check['year'] = self.data_check['issued_at'].dt.year
        self.data_check['month'] = self.data_check['issued_at'].dt.month
        self.data_check['day'] = self.data_check['issued_at'].dt.day

        # Рассчитываем общую сумму (продажи * цена) для каждой строки
        self.data_check['total_sales'] = self.data_check['position_count'] * self.data_check['price']

        # Группируем данные по году, месяцу и дню, а затем рассчитываем средневзвешенное значение
        grouped = self.data_check.groupby(['year', 'month', 'day']).apply(
            lambda x: (x['total_sales']).sum() / x['position_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'day', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        days = grouped['day'].tolist()
        check_means = grouped['weighted_average_price'].tolist()

        check_days = self.dates_to_days(years, months, days)

        return check_days, check_means

    def get_check_means_monthly(self):
        """
        Функция подсчета средневзвешенного значения по всем Чекам по месяцам
        """
        # Преобразуем поле general_date_transaction в формат даты
        self.data_check['issued_at'] = pd.to_datetime(self.data_check['issued_at'])

        # Извлекаем год, месяц и день из даты
        self.data_check['year'] = self.data_check['issued_at'].dt.year
        self.data_check['month'] = self.data_check['issued_at'].dt.month

        # Рассчитываем общую сумму (продажи * цена) для каждой строки
        self.data_check['total_sales'] = self.data_check['position_count'] * self.data_check['price']

        # Группируем данные по году, месяцу и дню, а затем рассчитываем средневзвешенное значение
        grouped = self.data_check.groupby(['year', 'month']).apply(
            lambda x: (x['total_sales']).sum() / x['position_count'].sum()).reset_index()
        grouped.columns = ['year', 'month', 'weighted_average_price']

        # Возвращаем результаты в виде массивов
        years = grouped['year'].tolist()
        months = grouped['month'].tolist()
        check_means = grouped['weighted_average_price'].tolist()

        check_months = self.dates_to_months(years, months)

        return check_months, check_means

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

    def get_weighted_check(self, last_unp, top_3):
        weighted_price = {}
        for top in top_3:
            copy_check = self.checks.copy()
            copy_check = copy_check[(copy_check['unp'].astype(str).isin(last_unp[top]))]
            ch, zn = 0, 0
            for index, item in copy_check.iterrows():
                ch += item['price'] * item['position_count']
                zn += item['position_count']
            if zn:
                weighted_price[top] = ch / zn
            else:
                weighted_price[top] = 0
        return weighted_price

    def get_next_unp(self, df, provider_unp):
        df_local = df.copy()
        df_local = df_local.loc[(df_local['provider_unp'].astype(str) == provider_unp)].reset_index()
        df_local = df_local.sort_values(by='roster_item_count', ascending=False)
        df_local['recipient_unp'] = df_local['recipient_unp'].astype(str)
        df_local['recipient_unp'] = df_local['recipient_unp'].apply(lambda x: x.rstrip('0').rstrip('.'))
        df_local = df_local.groupby('recipient_unp').agg({
            'roster_item_count': 'sum',
            'roster_item_price': 'sum',
            'roster_item_cost': 'sum'
        }).reset_index()

        return df_local[['recipient_unp', 'roster_item_count', 'roster_item_price', 'roster_item_cost']]

    def get_top_3(self, code, name):
        data_sorted = self.dt_esf.copy()
        data_sorted = data_sorted.loc[(data_sorted['roster_item_code'].astype(str) == code)
                                      & (data_sorted['roster_item_name'].astype(str) == name)].reset_index()
        data_sorted = data_sorted.groupby('provider_unp').agg({
            'roster_item_count': 'sum',
            'roster_item_cost': 'sum'
        }).reset_index()
        data_sorted.sort_values(by='roster_item_count', ascending=False)
        return data_sorted['provider_unp'].astype(str).head(3).tolist()

    def get_dt_weighted(self, code, name, unp):
        df_local = self.dt_esf.copy()
        df_local['recipient_unp'] = df_local['recipient_unp'].astype(str)
        df_local['recipient_unp'] = df_local['recipient_unp'].apply(lambda x: x.rstrip('0').rstrip('.'))
        df_local = df_local.loc[(df_local['roster_item_code'].astype(str) == code)
                                & (df_local['roster_item_name'].astype(str) == name)
                                & (df_local['provider_unp'].astype(str) == unp)].reset_index()
        price = sum([i * j for i, j in zip(df_local['ТС/кг, бел руб'], df_local['g38netweightquantity'])]) \
                / sum(df_local['g38netweightquantity'])
        return price

    def filter_data(self, tnved_code, goods_name, time_start, delta_time):
        time_start = pd.to_datetime(time_start)
        time_end = time_start + pd.DateOffset(days=delta_time)
        self.esf = self.esf[(self.esf['document_type'] == "ORIGINAL")]
        self.esf["general_date_transaction"] = pd.to_datetime(self.esf["general_date_transaction"])
        self.esf = self.esf[(self.esf["general_date_transaction"] >= time_start) & (
                self.esf["general_date_transaction"] <= time_end)
                            & (self.esf["roster_item_code"].astype(str) == tnved_code)
                            & (self.esf["roster_item_name"] == goods_name)
                            ].reset_index()
        self.dt_esf['dt_date'] = pd.to_datetime(self.dt_esf['dt_date'])
        self.dt_esf = self.dt_esf[(self.dt_esf['g331goodstnvedcode'].astype(str) == tnved_code)
                                  & (self.dt_esf['roster_item_name'] == goods_name)
                                  & (self.dt_esf['dt_date'] >= time_start)
                                  & (self.dt_esf['dt_date'] <= time_end)].reset_index()
        self.checks['issued_at'] = pd.to_datetime(self.checks['issued_at'])
        self.checks = self.checks[(self.checks['name'] == goods_name)
                                  & (self.checks['tnved_code'].astype(str) == tnved_code)
                                  & (self.checks['issued_at'] >= time_start)
                                  & (self.checks['issued_at'] <= time_end)].reset_index()

    def print_result(self, unp):
        if type(unp) == list:
            return unp
        else:
            return unp['recipient_unp'].tolist()

    def erase_weight(self, df, max_weight):
        copy_df = df.copy()
        copy_df = copy_df.sort_values(by='roster_item_count', ascending=False)
        local_weights = 0
        local_index = None
        for index, item in copy_df.iterrows():
            if item['roster_item_count'] > max_weight:
                copy_df.drop(index, inplace=True)
                continue
            if local_weights <= max_weight:
                local_weights += item['roster_item_count']
            else:
                local_index = index
                break
        if local_index:
            return copy_df.reset_index()[:local_index]
        return df


def market_esf(
        dataset_dt: pd.DataFrame,
        dataset_esf: pd.DataFrame,
        dataset_last_esf: pd.DataFrame,
        dataset_check: pd.DataFrame,
        product_code: str = '',
        start_date: str = '',
        end_date: str = '',
        daily_data: bool = False,
        build_chain: bool = False,
        start_date_to_chain: str = '',
        interval: int = 30,
        tracing_goods: str = '',
        size_chain: int = 2,
):
    """
    :code_assign: users
    :code_type: Пользовательские функции
    :imports: init_gui_dict, Window, Canvas, BarPlot, LinePlot, PiePlot, Market_esf, Scatter2DPlot
    :packages:
    import pandas as pd
    import datetime
    :param_block pd.DataFrame dataset_dt: датасет DT и связанных ЭСЧФ
    :param_block pd.DataFrame dataset_esf: датасет ЭСЧФ
    :param_block pd.DataFrame dataset_last_esf: датасет последних ЭСЧФ
    :param_block pd.DataFrame dataset_check: датасет CHECK и связанных ЭСЧФ
    :param str product_code: код товара
    :param str start_date: дата начала
    :param str end_date: дата конца
    :param bool daily_data: данные по дням
    :param bool build_chain: флаг построение цепочек
    :param str start_date_to_chain: дата
    :param int interval: интервал дней для цепочек
    :param str tracing_goods: продукт по которому идет поиск
    :param int size_chain: размер цепочки
    :returns: gui_dict, error
    :rtype: dict, str
    :semrtype: ,
    """
    error = ""
    gui_dict = init_gui_dict()
    pd.options.mode.chained_assignment = None

    # Фильтрация датасета по временному диапазону и коду товара
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Преобразуем поля
    dataset_dt['dt_date'] = pd.to_datetime(dataset_dt['dt_date'])
    dataset_dt['general_date_transaction'] = pd.to_datetime(dataset_dt['general_date_transaction'])
    dataset_esf['general_date_transaction'] = pd.to_datetime(dataset_esf['general_date_transaction'])
    dataset_last_esf['general_date_transaction'] = pd.to_datetime(dataset_last_esf['general_date_transaction'])
    dataset_check['issued_at'] = pd.to_datetime(dataset_check['issued_at'])

    # Фильтруем данные по указанному промежутку времени
    dt_data = dataset_dt[(dataset_dt['dt_date'] >= start_date) & (dataset_dt['dt_date'] <= end_date)]
    first_esf_data = dataset_dt[
        (dataset_dt['general_date_transaction'] >= start_date) & (dataset_dt['general_date_transaction'] <= end_date)]
    esf_data = dataset_esf[
        (dataset_esf['general_date_transaction'] >= start_date) & (dataset_esf['general_date_transaction'] <= end_date)]
    last_esf_data = dataset_last_esf[(dataset_last_esf['general_date_transaction'] >= start_date) & (
            dataset_last_esf['general_date_transaction'] <= end_date)]
    check_data = dataset_check[(dataset_check['issued_at'] >= start_date) & (dataset_check['issued_at'] <= end_date)]

    # Для статистики по компаниям не учитываем данные неизвестных компаний
    esf_data = esf_data.dropna(subset=['provider_unp', 'recipient_unp'])

    # Фильтрация по коду товара
    df_dt_filtered = dt_data[(dt_data['roster_item_code'] == int(product_code))]
    df_first_esf_filtered = first_esf_data[(first_esf_data['roster_item_code'] == int(product_code))]
    df_esf_filtered = esf_data[(esf_data['roster_item_code'] == int(product_code))]
    df_last_esf_filtered = last_esf_data[(last_esf_data['roster_item_code'] == int(product_code))]
    df_check_filtered = check_data[(check_data['tnved_code'] == int(product_code))]

    # Приводим все УНП компаний к одному типу
    df_esf_filtered['recipient_unp'] = pd.to_numeric(df_esf_filtered['recipient_unp'], downcast='signed')
    df_esf_filtered['recipient_unp'] = df_esf_filtered['recipient_unp'].astype(str)

    if df_esf_filtered.empty:
        raise Exception(f'Нет записей по коду {product_code} за период с {start_date} по {end_date}')

    Market = Market_esf(df_dt_filtered, df_first_esf_filtered, df_esf_filtered, df_last_esf_filtered, df_check_filtered,
                        dataset_dt, dataset_esf, dataset_check)

    # Получение статистики по компаниям
    company_stat, avg_price = Market.get_statistics(df_esf_filtered, start_date, end_date)

    company_unp = company_stat['УНП'].tolist()
    mean_buy_price = company_stat['Ср.вз. цена покупки'].tolist()
    delta_buy = company_stat['Дельта от ср. цены покупки по рынку'].tolist()
    mean_sell_price = company_stat['Ср.вз. цена продажи'].tolist()
    delta_sell = company_stat['Дельта от ср. цены продажи по рынку'].tolist()
    sell_count = company_stat['Количество продаж'].tolist()
    buy_count = company_stat['Количество закупок'].tolist()
    sell_count_percent = company_stat['% от рынка по кол-ву продаж'].tolist()
    buy_count_percent = company_stat['% от рынка по кол-ву закупок'].tolist()
    sell_cost = company_stat['Стоимость продаж'].tolist()
    buy_cost = company_stat['Стоимость закупок'].tolist()
    sell_cost_percent = company_stat['% от рынка по стоимости продаж'].tolist()
    buy_cost_percent = company_stat['% от рынка по стоимости закупок'].tolist()
    active_sell_percent = company_stat['% актив продаж'].tolist()
    active_buy_percent = company_stat['% актив покупок'].tolist()

    gui_dict['table'].append({
        'title': "Статистика по компаниям",
        'value': {
            'УНП': [str(value) for value in company_unp],
            'Ср.вз. цена покупки': [str(value) for value in mean_buy_price],
            'Дельта от ср. цены покупки по рынку': [str(value) for value in delta_buy],
            'Ср.вз. цена продажи': [str(value) for value in mean_sell_price],
            'Дельта от ср. цены продажи по рынку': [str(value) for value in delta_sell],
            'Количество продаж': [str(value) for value in sell_count],
            'Количество закупок': [str(value) for value in buy_count],
            '% от рынка по кол-ву продаж': [str(value) for value in sell_count_percent],
            '% от рынка по кол-ву закупок': [str(value) for value in buy_count_percent],
            'Стоимость продаж': [str(value) for value in sell_cost],
            'Стоимость закупок': [str(value) for value in buy_cost],
            '% от рынка по стоимости продаж': [str(value) for value in sell_cost_percent],
            '% от рынка по стоимости закупок': [str(value) for value in buy_cost_percent],
            '% актив продаж': [str(value) for value in active_sell_percent],
            '% актив покупок': [str(value) for value in active_buy_percent]
        }
    })

    avg_price_arr = []
    for i in range(len(company_unp)):
        avg_price_arr.append(avg_price)

    datetime_start = datetime.datetime.strptime(str(start_date), "%Y-%m-%d %H:%M:%S")
    datetime_end = datetime.datetime.strptime(str(end_date), "%Y-%m-%d %H:%M:%S")
    start_date_graph = datetime_start.strftime("%Y-%m-%d")
    end_date_graph = datetime_end.strftime("%Y-%m-%d")

    gui_dict['plot'].append(
        Window(
            window_title='Средневзвешенные цены покупок и продаж',
            canvases=[Canvas(
                title=f'Средневзвешенные цены покупок и продаж {product_code} с {start_date_graph} по {end_date_graph}',
                x_title='УНП компании',
                y_title='Цена, бел. рубли',
                showlegend=True,
                plots=[
                    BarPlot(x=np.array(company_unp), y=np.array(mean_sell_price), names=['Цена продажи']),
                    BarPlot(x=np.array(company_unp), y=np.array(mean_buy_price), names=['Цена покупки']),
                    LinePlot(x=np.array(company_unp), y=np.array(avg_price_arr), names=['Ср.вз. цена продажи по рынку'])
                ])]
        ).to_dict()
    )

    # ТОП-5 компаний по разнице sell-buy
    top_five_sell_buy = company_stat.sort_values(by='Отношение', ascending=False).head(5)

    gui_dict['plot'].append(
        Window(
            window_title='Топ-5 фирм по наибольшей дельте цены продажи и покупки',
            canvases=[Canvas(
                title=f'Средневзвешенные цены покупок и продаж {product_code} с {start_date_graph} по {end_date_graph}',
                x_title='УНП компании',
                y_title='Цена, бел. рубли',
                showlegend=True,
                plots=[
                    BarPlot(x=np.array(top_five_sell_buy['УНП']), y=np.array(top_five_sell_buy['Ср.вз. цена продажи']),
                            names=['Цена продажи']),
                    BarPlot(x=np.array(top_five_sell_buy['УНП']), y=np.array(top_five_sell_buy['Ср.вз. цена покупки']),
                            names=['Цена покупки']),
                    LinePlot(x=np.array(top_five_sell_buy['УНП']), y=np.array(avg_price_arr),
                             names=['Ср.вз. цена продажи по рынку'])
                ])]
        ).to_dict()
    )

    # ТОП-5 компаний по объему продаж в количественном выражении
    top_five_sell_count = company_stat.sort_values(by='Количество продаж', ascending=False).head(5)
    # ТОП-5 компаний по объему продаж в стоимостном выражении
    top_five_sell_cost = company_stat.sort_values(by='Стоимость продаж', ascending=False).head(5)
    # ТОП-5 компаний по объему покупок в количественном выражении
    top_five_buy_count = company_stat.sort_values(by='Количество закупок', ascending=False).head(5)
    # ТОП-5 компаний по объему покупок в стоимостном выражении
    top_five_buy_cost = company_stat.sort_values(by='Стоимость закупок', ascending=False).head(5)
    names_1 = Market.get_name_of_companies(top_five_sell_count['УНП'].astype('str').tolist())
    names_2 = Market.get_name_of_companies(top_five_sell_cost['УНП'].astype('str').tolist())
    names_3 = Market.get_name_of_companies(top_five_buy_count['УНП'].astype('str').tolist())
    names_4 = Market.get_name_of_companies(top_five_buy_cost['УНП'].astype('str').tolist())


    gui_dict['plot'].append(
        Window(
            window_title='Круговые диаграммы',
            canvases=[Canvas(
                title=f'Топ 5 компаний по объёму продаж в количественном выражении по товару с кодом: {product_code} в '
                      f'интервале от {start_date_graph} до {end_date_graph}',
                showlegend=True,
                plots=[PiePlot(labels=names_1['УНП_names'].astype('str'),
                               values=top_five_sell_count['Количество продаж'].astype('int'))]
            ),
                Canvas(
                    title=f'Топ 5 компаний по объёму продаж в стоимостном выражении по товару с кодом: {product_code} в '
                          f'интервале от {start_date_graph} до {end_date_graph}',
                    showlegend=True,
                    plots=[PiePlot(labels=names_2['УНП_names'].astype('str'),
                                   values=top_five_sell_cost['Стоимость продаж'].astype('int'))]
                ),
                Canvas(
                    title=f'Топ 5 компаний по объёму покупок в количественном выражении по товару с кодом: {product_code} в '
                          f'интервале от {start_date_graph} до {end_date_graph}',
                    showlegend=True,
                    plots=[PiePlot(labels=names_3['УНП_names'].astype('str'),
                                   values=top_five_buy_count['Количество закупок'].astype('int'))]
                ),
                Canvas(
                    title=f'Топ 5 компаний по объёму покупок в стоимостном выражении по товару с кодом: {product_code} в '
                          f'интервале от {start_date_graph} до {end_date_graph}',
                    showlegend=True,
                    plots=[PiePlot(labels=names_4['УНП_names'].astype('str'),
                                   values=top_five_buy_cost['Стоимость закупок'].astype('int'))]
                )
            ]
        ).to_dict()
    )

    if daily_data:
        dt_x_points, dt_y_points = Market.get_dt_means_daily()
        first_esf_x_points, first_esf_y_points = Market.get_first_esf_means_daily()
        # esf_x_points, esf_y_points = Market.get_esf_means_daily()
        second_esf_x, second_esf_y = Market.get_second_esf_means_daily()
        last_esf_x_points, last_esf_y_points = Market.get_last_esf_means_daily()
        check_x_points, check_y_points = Market.get_check_means_daily()
        caption = 'День'
    else:
        dt_x_points, dt_y_points = Market.get_dt_means_monthly()
        first_esf_x_points, first_esf_y_points = Market.get_first_esf_means_monthly()
        # esf_x_points, esf_y_points = Market.get_esf_means_monthly()
        second_esf_x, second_esf_y = Market.get_second_esf_means_monthly()
        last_esf_x_points, last_esf_y_points = Market.get_last_esf_means_monthly()
        check_x_points, check_y_points = Market.get_check_means_monthly()
        caption = 'Месяц'

    gui_dict['plot'].append(
        Window(
            window_title='Сравнение цен по ДТ, ЭСЧФ, Чеки',
            canvases=[Canvas(
                title=f'Средневзвешенные цены продаж по товару {product_code} с {start_date_graph} по {end_date_graph}',
                x_title=caption,
                y_title='Цена, бел. руб',
                showlegend=True,
                plots=[
                    LinePlot(x=np.array(dt_x_points), y=np.array(dt_y_points), names=['ДТ']),
                    LinePlot(x=np.array(first_esf_x_points), y=np.array(first_esf_y_points), names=['ЭСЧФ1']),
                    LinePlot(x=np.array(second_esf_x), y=np.array(second_esf_y), names=['ЭСЧФ2']),
                    # LinePlot(x=np.array(esf_x_points), y=np.array(esf_y_points), names=['Все ЭСЧФ']),
                    LinePlot(x=np.array(last_esf_x_points), y=np.array(last_esf_y_points), names=['Последняя ЭСЧФ']),
                    LinePlot(x=np.array(check_x_points), y=np.array(check_y_points), names=['Чек']),
                ])]
        ).to_dict()
    )
    if build_chain:
        top_3 = Market.get_top_3(product_code, tracing_goods)
        dt_weighted_points = {}
        for top in top_3:
            dt_weighted_points[top] = Market.get_dt_weighted(product_code, tracing_goods, top)
        Market.filter_data(product_code, tracing_goods, start_date_to_chain, interval)
        chain_len = size_chain + 1
        structure = {
            0: {'dt': top_3}
        }
        structure_price = {}
        weighted_points = {}

        for idx_chain in range(chain_len - 1):
            structure[idx_chain + 1] = dict()
            for company in structure[idx_chain]:
                if type(structure[idx_chain][company]) == list:
                    for recipient in structure[idx_chain][company]:
                        next_chain = Market.get_next_unp(Market.dt_esf, recipient)
                        structure[idx_chain + 1][recipient] = next_chain
                else:
                    for index, recipient in structure[idx_chain][company].iterrows():
                        next_chain = Market.get_next_unp(Market.esf, recipient['recipient_unp'])
                        next_chain = Market.erase_weight(next_chain, recipient['roster_item_count'])
                        # print(next_chain)
                        structure[idx_chain + 1][company + '_' + recipient['recipient_unp']] = next_chain
        check = {}
        for top in top_3:
            check[top] = []
            weighted_points[top] = {}
            for size in range(1, chain_len):
                weighted_points[top][size] = [0, 0]
        for chain in structure:
            # print('УЗЕЛ', chain)
            count = 0
            for index, provider in enumerate(structure[chain]):
                if len(structure[chain][provider]) != 0:
                    if chain != 0:
                        price = structure[chain][provider]['roster_item_cost'].sum() / structure[chain][provider][
                            'roster_item_count'].sum()
                        if weighted_points[provider.split("_")[0]][chain][0] == 0:
                            weighted_points[provider.split("_")[0]][chain] = [price, structure[chain][provider][
                                'roster_item_count'].sum()]
                        else:
                            chain_price = weighted_points[provider.split("_")[0]][chain][0]
                            chain_weight = weighted_points[provider.split("_")[0]][chain][1]
                            current_weight = structure[chain][provider]['roster_item_count'].sum()
                            weighted_points[provider.split("_")[0]][chain] = [
                                (chain_price * chain_weight + price * current_weight) / (current_weight + chain_weight),
                                chain_weight + current_weight]
                        check[provider.split("_")[0]].extend(Market.print_result(structure[chain][provider]))
                        # print(f'Цепочка: {provider} Поставщик: {provider.split("_")[-1]}, Получатели ({len(structure[chain][provider])}): {print_result(structure[chain][provider])}, Цена: {price:.3f}')
                    else:
                        pass
                        # print(f'Цепочка: {provider} Поставщик: {provider.split("_")[-1]}, Получатели: {print_result(structure[chain][provider])}')

                    count += 1

            # print(f'{count} / {len(structure[chain])}')
        weighted_checks = Market.get_weighted_check(check, top_3)
        plots = []
        for top in top_3:
            if weighted_checks[top]:
                node_list = ['ДТ'] + [f"Узел {i}" for i in range(1, size_chain + 1)] + ['Чек']
                y = np.array([dt_weighted_points[top]] + [value[0] for key, value in weighted_points[top].items()] + [
                    weighted_checks[top]])
            else:
                node_list = ['ДТ'] + [f"Узел {i}" for i in range(1, size_chain + 1)]
                y = np.array([dt_weighted_points[top]] + [value[0] for key, value in weighted_points[top].items()])
            x = np.arange(len(y))
            plots.append(LinePlot(x=x, y=y, names=[f'Цепочка ЭСЧФ для компании: {top}']))
            plots.append(Scatter2DPlot(x=x, y=y, names=[f'Цепочка ЭСЧФ для компании: {top}'],
                                       text=[node_list], marker=[dict(color="black")]))
        gui_dict['plot'].append(
            Window(
                window_title='Цепочка ЭСЧФ',
                canvases=[Canvas(
                    title=f'Цепочка ЭСЧФ по товару {tracing_goods}',
                    x_title='Узел',
                    y_title='Среднезвешенная цена, бел. руб',
                    showlegend=True,
                    plots=plots)]
            ).to_dict()
        )

    return gui_dict, error
