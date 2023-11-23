class Market_ACP:
    """
    :code_assign: service
    :code_type: отрисовка графиков ф-ий блока Рынка
    :imports: Canvas, BarPlot
    :packages:
    import pandas as pd
    
    """

    def __init__(self, data, dataset_checks, code, company, time_start, time_end):
        """
        :param pd.DateFrame data: неотфильтрованный датасет
        :param str code: выбранной продукт
        :param str company: унп выбранной компании
        :param str time_start: начало временного интервала
        :param str time_end: конец временного интервала
        """
        self.time_start = time_start
        self.time_end = time_end
        self.data = data
        self.dataset_checks = dataset_checks
        self.code = int(code)
        self.company = int(company)
        self.canvass = list()

    def csv_options(self):
        """
            Функция настроек датасета
        """
        self.data = self.data[
            ['roster_item_code', 'general_date_transaction', 'provider_unp', 'recipient_unp', 'roster_item_count',
             'roster_item_cost', 'roster_item_price', 'document_type', 'status']]
        self.data['general_date_transaction'] = pd.to_datetime(self.data['general_date_transaction'])
        self.data['roster_item_code'] = self.data['roster_item_code'].astype(str)
        self.data["provider_unp"] = self.data["provider_unp"].astype(str)
        self.data['recipient_unp'] = self.data['recipient_unp'].fillna(0)
        self.data['recipient_unp'] = self.data['recipient_unp'].astype(int)
        self.data['recipient_unp'] = self.data['recipient_unp'].astype(str)
        self.data = self.data[self.data["document_type"].str.contains("ADDITIONAL") == False]
        self.data = self.data[((self.data["status"].str.contains("COMPLETED")) | (
            self.data["status"].str.contains(
                "COMPLETED_SIGNED"))) == True]  # удаляем строки, которые не подходят по условию
        self.time_start = pd.to_datetime(self.time_start).strftime('%Y-%m-%d')
        self.time_end = pd.to_datetime(self.time_end).strftime('%Y-%m-%d')

    # def search_code_all_company_sale_buy(self):
    #     """
    #         Функция выборки из датасета по коду товара по продажам и покупкам
    #         :return: выборка из pd.dataframe
    #     """
    #     data_sale_buy_all = self.data.loc[self.data['roster_item_code'] == str(self.code)]
    #
    #     data_sale_buy_all = data_sale_buy_all.loc[(data_sale_buy_all["general_date_transaction"] >= self.time_start) & (
    #             data_sale_buy_all["general_date_transaction"] <= self.time_end)]
    #
    #     data_sale_buy_all["year_month"] = data_sale_buy_all["general_date_transaction"].dt.to_period("M")
    #
    #     return data_sale_buy_all

    def search_code_and_company_sale(self):
        """
            Функция выборки из датасета по коду товара и компании по продажам
            :return: выборка из pd.dataframe
        """
        if len(str(self.code)) > 0:
            data_sale = self.data.loc[
                (self.data['roster_item_code'] == str(self.code)) & (self.data['provider_unp'] == str(self.company))]
        else:
            data_sale = self.data.loc[self.data['provider_unp'] == str(self.company)]

        data_sale = data_sale.loc[(data_sale["general_date_transaction"] >= self.time_start) & (
                data_sale["general_date_transaction"] <= self.time_end)]

        data_sale["year_month"] = data_sale["general_date_transaction"].dt.to_period("M")

        return data_sale

    def search_code_and_company_buy(self):
        """
            Функция выборки из датасета по коду товара и компании по покупкам
            :return: выборка из pd.dataframe
        """
        if len(str(self.code)) > 0:
            data_buy = self.data.loc[
                (self.data['roster_item_code'] == str(self.code)) & (self.data['recipient_unp'] == str(self.company))]
        else:
            data_buy = self.data.loc[self.data['recipient_unp'] == str(self.company)]

        data_buy = data_buy.loc[(data_buy["general_date_transaction"] >= self.time_start) & (
                data_buy["general_date_transaction"] <= self.time_end)]

        data_buy["year_month"] = data_buy["general_date_transaction"].dt.to_period("M")

        return data_buy

    """
    Чтение файла по ДТ и Чекам
    """

    def read_data_dt(self):
        """
        Функция чтения файла по ДТ
        """
        self.data['dt_date'] = pd.to_datetime(self.data['dt_date'])
        self.data['total_amount'] = self.data['g38netweightquantity'] * self.data['ТС/кг, бел руб']
        time_start = pd.to_datetime(self.time_start)
        time_end = pd.to_datetime(self.time_end)
        data = self.data[(self.data['dt_date'] >= time_start) & (self.data['dt_date'] <= time_end)]
        data_nw = data[(data['g331goodstnvedcode'] == self.code) & (data['g14rbunp'] == self.company)]
        return data_nw


    def read_data_ch(self):
        """
        Функция чтения файла по Чекам
        """
        self.dataset_checks['issued_at'] = pd.to_datetime(self.dataset_checks['issued_at'])
        time_start = pd.to_datetime(self.time_start)
        time_end = pd.to_datetime(self.time_end)
        data = self.dataset_checks[
            (self.dataset_checks['issued_at'] >= time_start) & (self.dataset_checks['issued_at'] <= time_end)]
        data_nw = data[(data['tnved_code'] == self.code) & (data['unp'] == self.company)]
        return data_nw

    """
    2.5 Показ объёма в количественном и стоимостном выражении, ориентируясь отдельно на
     ДТ и на чеки - столбч. диаграмма 
    """

    def show_sells_by_dt(self):

        sorted_data = self.read_data_dt()

        grouped_df = sorted_data.groupby('dt_date')['total_amount'].sum().reset_index()
        if grouped_df.empty:
            pass
        else:
            self.canvass.append(Canvas(title=f'Объём импорта компании {self.company} по коду: {self.code} в стоимостном выражении'
                                             f'',
                                       showlegend=False,
                                       x_title='Дата',
                                       y_title='Стоимость в бел. руб. BYN',
                                       plots=[BarPlot(x=grouped_df['dt_date'].values,
                                                      y=grouped_df['total_amount'].values
                                                      )]
                                       )
                                )

    def show_quantity_by_dt(self):
        """
        Функция показа объема рынка в количиественном выражении по ДТ
        """

        # Выборка
        sorted_data = self.read_data_dt()
        grouped_df = sorted_data.groupby('dt_date')['g38netweightquantity'].sum().reset_index()
        if grouped_df.empty:
            pass
        else:
            self.canvass.append(Canvas(title=f'Объём импорта компании {self.company}  по коду: {self.code} в количественном выражении',
                                       showlegend=False,
                                       x_title='Дата',
                                       y_title='Кол-во в КГ',
                                       plots=[BarPlot(x=grouped_df['dt_date'].values,
                                                      y=grouped_df['g38netweightquantity'].values
                                                      )]
                                       )
                                )

    def show_sells_by_check(self):
        """
        Функция показа объема рынка в стоимостном выражении по Чекам
        """

        # Получение выборки
        sorted_data = self.read_data_ch()

        grouped_df = sorted_data.groupby('issued_at')['total_amount'].sum().reset_index()
        if grouped_df.empty:
            pass
        else:
            self.canvass.append(Canvas(title=f'Объем продаж компании {self.company} по коду: {self.code} в стоимостном выражении',
                                       showlegend=False,
                                       x_title='Дата',
                                       y_title='Стоимость в бел. руб. BYN',
                                       plots=[BarPlot(x=grouped_df['issued_at'].values,
                                                      y=grouped_df['total_amount'].values
                                                      )]
                                       )
                                )

    def show_quantity_by_check(self):
        """
        Функция показа объема рынка в количиественном выражении по Чекам
        """

        sorted_data = self.read_data_ch()

        grouped_df = sorted_data.groupby('issued_at')['position_count'].sum().reset_index()
        if grouped_df.empty:
            pass
        else:
            self.canvass.append(Canvas(title=f'Объем продаж компании {self.company} по коду: {self.code} в количественном выражении',
                                       showlegend=False,
                                       x_title='Дата',
                                       y_title='Кол-во в КГ',
                                       plots=[BarPlot(x=grouped_df['issued_at'].values,
                                                      y=grouped_df['position_count'].values
                                                      )]
                                       )
                                )


def market_acp(
        dataset_dt: pd.DataFrame,
        dataset_checks: pd.DataFrame,
        dataset_esf: pd.DataFrame,
        code: str,
        company: str,
        time_start: str,
        time_end: str,
):
    """
    :code_assign: users
    :code_type: Пользовательские функции
    :imports: init_gui_dict, Canvas, BarPlot, Market_ACP, Window, LinePlot
    :packages:
    import datetime
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    :param_block pd.DataFrame dataset_dt: датасет дт
    :param_block pd.DataFrame dataset_checks: датасет чеков
    :param_block pd.DataFrame dataset_esf: датасет эсчф
    :param str code: выбранный код товара
    :param str company: выбранная компания
    :param str time_start: начало интервала
    :param str time_end: конец интервал
    :returns: gui_dict, error
    :rtype: dict, str
    :semrtype: ,
    """

    # Выбор пользователем нужного графика
    gui_dict = init_gui_dict()
    error = ""
    market = Market_ACP(dataset_dt, dataset_checks, code, company, time_start, time_end)
    market.show_sells_by_dt()
    market.show_quantity_by_dt()
    market.show_sells_by_check()
    market.show_quantity_by_check()
    if market.canvass:
        gui_dict['plot'].append(
            Window(
                window_title='Столбчатые диаграммы',
                canvases=market.canvass
            ).to_dict()
        )
    """
    Вызывается ф-ия 2_6
    """
    avg = Market_ACP(dataset_esf, dataset_checks, code, company, time_start, time_end)
    avg.csv_options()
    # sale_buy_all = avg.search_code_all_company_sale_buy()
    sale = avg.search_code_and_company_sale()
    buy = avg.search_code_and_company_buy()

    min_date = time_start
    min_date = pd.to_datetime(min_date)

    # Функция для вычисления разницы в месяцах
    def months_since_min_date_sale(date):
        months_diff_sale = (date.year - min_date.year) * 12 + (date.month - min_date.month) + 1
        return months_diff_sale

    # Примените функцию к столбцу datetime и создайте новый столбец с месяцами
    # sale_buy_all['months'] = sale_buy_all['general_date_transaction'].apply(months_since_min_date_sale)

    # Примените функцию к столбцу datetime и создайте новый столбец с месяцами
    sale['months'] = sale['general_date_transaction'].apply(months_since_min_date_sale)

    # Примените функцию к столбцу datetime и создайте новый столбец с месяцами
    buy['months'] = buy['general_date_transaction'].apply(months_since_min_date_sale)

    # sale_buy_all = sale_buy_all.groupby('months')['roster_item_price'].mean().reset_index(name='roster_item_price')
    sale = sale.groupby('months')['roster_item_price'].mean().reset_index(name='roster_item_price')
    buy = buy.groupby('months')['roster_item_price'].mean().reset_index(name='roster_item_price')

    plots = list()
    if not sale.empty:
        plots.append(LinePlot(x=np.array(sale['months']), y=sale['roster_item_price'],
                              names=['Средняя продажная цена компании']))
    if not buy.empty:
        plots.append(LinePlot(x=np.array(buy['months']), y=buy['roster_item_price'],
                              names=['Средняя закупочная цена компании']))
    # if not sale_buy_all.empty:
    #     plots.append(LinePlot(x=np.array(sale_buy_all['months']), y=sale_buy_all['roster_item_price'],
    #                           names=['Средняя закупочная/продажная цена по рынку']))
    if sale.empty and buy.empty and sale_buy_all.empty:
        pass
    else:
        gui_dict['plot'].append(
            Window(
                window_title='Смена средней продажной цены',
                canvases=[Canvas(
                    title=f'Цена продажи и закупки товара {code} компанией {company} в интервале от {time_start} до {time_end}',
                    x_title='Месяц',
                    y_title='Цена (бел руб)',
                    showlegend=True,
                    plots=plots)]
            ).to_dict()
        )
    total = Market_ACP(dataset_esf, dataset_checks, code, company, time_start, time_end)
    total.csv_options()
    sale = total.search_code_and_company_sale()
    buy = total.search_code_and_company_buy()


    min_date = time_start
    min_date = pd.to_datetime(min_date)

    # Функция для вычисления разницы в месяцах
    def months_since_min_date(date):
        months_diff = (date.year - min_date.year) * 12 + (date.month - min_date.month) + 1
        return months_diff

        # Примените функцию к столбцу datetime и создайте новый столбец с месяцами

    sale['months'] = sale['general_date_transaction'].apply(months_since_min_date)

    buy['months'] = buy['general_date_transaction'].apply(months_since_min_date)

    sale = sale.groupby('months')['roster_item_count'].sum().reset_index(name='roster_item_count')
    buy = buy.groupby('months')['roster_item_count'].sum().reset_index(name='roster_item_count')
    plots = []
    if not sale.empty:
        plots.append(LinePlot(x=np.array(sale['months']), y=sale['roster_item_count'],
                              names=['Количество проданных товаров']))
    if not buy.empty:
        plots.append(LinePlot(x=np.array(buy['months']), y=buy['roster_item_count'],
                              names=['Количество закупленных товаров']))
    if sale.empty and buy.empty:
        pass
    else:
        gui_dict['plot'].append(
            Window(
                window_title='Объем закупок и продаж',
                canvases=[Canvas(
                    title=f'Объем закупок и продаж у компании с кодом {company} по товару {code} в интервале от {time_start} до {time_end}',
                    x_title='Месяц',
                    y_title='Количество кг',
                    showlegend=True,
                    plots=plots)]
            ).to_dict()
        )
    return gui_dict, error
