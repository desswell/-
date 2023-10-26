class Total_sold:
    """
        :code_assign: service
        :code_type: отрисовка LinePlot
        :packages:
        import pandas as pd
    """
    def __init__(self, data, code, time_start, time_end, company):
        """
        :param pd.DateFrame data: датасет
        :param str code: выбраный товар
        :param str company: выбраная компания
        :param str time_start: введенное начало интервала
        :param str time_end: введенный конец интервала
        """
        self.data = data
        self.code = code
        self.company = company
        self.time_start = time_start
        self.time_end = time_end


    def csv_options(self):
        """
            Функция настроек датасета
        """
        self.data = self.data[['roster_item_code', 'general_date_transaction', 'provider_unp', 'recipient_unp', 'roster_item_count', 'roster_item_cost', 'roster_item_price', 'document_type', 'status']]
        self.data['general_date_transaction'] = pd.to_datetime(self.data['general_date_transaction'])
        self.data['roster_item_code'] = self.data['roster_item_code'].astype(str)
        self.data["provider_unp"] = self.data["provider_unp"].astype(str)
        self.data["recipient_unp"] = self.data["recipient_unp"].astype(str)
        self.data = self.data[self.data["document_type"].str.contains("ADDITIONAL") == False ]
        self.data = self.data[((self.data["status"].str.contains("COMPLETED")) | (
            self.data["status"].str.contains("COMPLETED_SIGNED"))) == True]  # удаляем строки, которые не подходят по условию
        self.time_start = pd.to_datetime(self.time_start).strftime('%Y-%m-%d')
        self.time_end = pd.to_datetime(self.time_end).strftime('%Y-%m-%d')


    def search_code_and_company_sale(self):
        """
            Функция выборки из датасета по коду товара и компании по продажам
            :return: выборка из pd.dataframe
        """
        if len(str(self.code)) > 0:
            data_sale = self.data.loc[(self.data['roster_item_code'] == self.code) & (self.data['provider_unp'] == self.company)]
        else:
            data_sale = self.data.loc[self.data['provider_unp'] == self.company]

        data_sale = data_sale.loc[(data_sale["general_date_transaction"] >= self.time_start) & (data_sale["general_date_transaction"] <= self.time_end)]

        data_sale["year_month"] = data_sale["general_date_transaction"].dt.to_period("M")

        return data_sale

    def search_code_and_company_buy(self):
        """
            Функция выборки из датасета по коду товара и компании по покупкам
            :return: выборка из pd.dataframe
        """
        if len(str(self.code)) > 0:
            data_buy = self.data.loc[
                (self.data['roster_item_code'] == self.code) & (self.data['recipient_unp'] == self.company)]
        else:
            data_buy = self.data.loc[self.data['recipient_unp'] == self.company]

        data_buy = data_buy.loc[(data_buy["general_date_transaction"] >= self.time_start) & (
                    data_buy["general_date_transaction"] <= self.time_end)]

        data_buy["year_month"] = data_buy["general_date_transaction"].dt.to_period("M")

        return data_buy


def total_price(
        dataset: pd.DataFrame,
        code: str = '',
        company: str = '',
        time_start: str = '',
        time_end: str = ''
):
    """
    :code_assign: users
    :code_type: Пользовательские функции
    :imports: init_gui_dict, Window, Canvas, LinePlot, Total_sold
    :packages:
    import pandas as pd
    import numpy as np
    :param_block pd.DataFrame dataset: датасет
    :param str code: выбранный товар
    :param str company: выбранная компания
    :param str time_start: начало временного интервала
    :param str time_end: конец временного интервала
    :returns: gui_dict, error
    :rtype: dict, str
    :semrtype: ,
    """
    error = ""
    gui_dict = init_gui_dict()
    total = Total_sold(dataset, code, time_start, time_end, company)
    total.csv_options()
    sale = total.search_code_and_company_sale()
    buy = total.search_code_and_company_buy()
    sale = sale.groupby('year_month')['roster_item_price'].sum().reset_index(name='roster_item_price')
    buy = buy.groupby('year_month')['roster_item_price'].sum().reset_index(name='roster_item_price')
    gui_dict['plot'].append(
        Window(
            window_title='Объем закупок и продаж',
            canvases=[Canvas(
                title=f'Объем закупок и продаж у компании с кодом {company} по товару {code} в интервале от {time_start} до {time_end}',
                x_title='Количество',
                y_title='Месяц',
                showlegend=True,
                plots=[LinePlot(x=np.array(sale['year_month']), y=sale['roster_item_price'], names=['Количество проданных товаров']),
                 LinePlot(x=np.array(buy['year_month']), y=buy['roster_item_price'], names=['Количество закупленных товаров'])])]
        ).to_dict()
    )
    return gui_dict, error

