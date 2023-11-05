import pandas as pd


class Top_Company_Cost_Count:
    """
    :code_assign: service
    :code_type: отрисовка PiePlot
    :packages:
    import pandas as pd
    """

    def __init__(self, data, code, time_start, time_end):
        """
        :param pd.DateFrame data: датасет
        :param str code: выбраный товар
        :param str time_start: введенное начало интервала
        :param str time_end: введенный конец интервала
        """
        self.data = data
        self.code = int(code)
        self.time_start = time_start
        self.time_end = time_end

    def sort_cost_sale(self):
        """
        Функция группировки и сортировки компаний по продажам в стоимостном выражении
        """
        # продажа
        data_cost_sale = self.data.groupby('provider_unp')['roster_item_cost'].sum().reset_index(
            name='roster_item_cost')
        data_cost_sale = data_cost_sale.sort_values(by=['roster_item_cost'], ascending=False)
        data_cost_sale = data_cost_sale.head(5)

        return data_cost_sale

    def sort_count_sale(self):
        """
        Функция группировки и сортировки компаний по продажам в количественном выражении
        """
        # продажа
        data_count_sale = self.data.groupby('provider_unp')['roster_item_count'].sum().reset_index(
            name='roster_item_count')
        data_count_sale = data_count_sale.sort_values(by=['roster_item_count'], ascending=False)
        data_count_sale = data_count_sale.head(5)

        return data_count_sale

    def sort_cost_buy(self):
        """
        Функция группировки и сортировки компаний по покупкам в стоимостном выражении
        """
        # покупка
        data_cost_buy = self.data.groupby('recipient_unp')['roster_item_cost'].sum().reset_index(
            name='roster_item_cost')
        data_cost_buy = data_cost_buy.sort_values(by=['roster_item_cost'], ascending=False)
        data_cost_buy = data_cost_buy.head(5)

        return data_cost_buy

    def sort_count_buy(self):
        """
        Функция группировки и сортировки компаний по покупкам в количественном выражении
        """
        # покупка
        data_count_buy = self.data.groupby('recipient_unp')['roster_item_count'].sum().reset_index(
            name='roster_item_count')
        data_count_buy = data_count_buy.sort_values(by=['roster_item_count'], ascending=False)
        data_count_buy = data_count_buy.head(5)

        return data_count_buy

    def csv_options(self):
        """
        Функция настроек датасета
        :return: выборка из pd.dataframe
        """

        data = self.data[
            ['roster_item_code', 'general_date_transaction', 'provider_unp', 'recipient_unp', 'roster_item_count',
             'roster_item_cost', 'document_type', 'status']]  # выбираем нужные столбцы
        data = data[
            data["document_type"].str.contains("ADDITIONAL") == False]  # удаляем строки, которые не подходят по условию
        data = data[data["status"].str.contains("CANCELLED") == False]  # удаляем строки, которые не подходят по условию
        data['general_date_transaction'] = pd.to_datetime(data['general_date_transaction'])
        data['roster_item_code'] = data['roster_item_code'].astype(str)
        data = data.loc[
            (data["general_date_transaction"] >= self.time_start) & (data["general_date_transaction"] <= self.time_end)]
        data = data.loc[data['roster_item_code'] == self.code]

        return data


def diagram_acp(
        dataset: pd.DataFrame,
        code: str = '',
        time_start: str = '',
        time_end: str = ''
):
    """
    :code_assign: users
    :code_type: Пользовательские функции
    :imports: init_gui_dict, Window, Canvas, PiePlot, Top_Company_Cost_Count
    :packages:
    :param_block pd.DataFrame dataset: датасет
    :param str code: выбранный товар
    :param str time_start: начало временного интервала
    :param str time_end: конец временного интервала
    :returns: gui_dict, error
    :rtype: dict, str
    :semrtype: ,
    """
    error = ""
    gui_dict = init_gui_dict()
    Com = Top_Company_Cost_Count(dataset, code, time_start, time_end)
    Com.csv_options()
    count_sale = Com.sort_count_sale()
    count_buy = Com.sort_count_buy()
    cost_sale = Com.sort_cost_sale()
    cost_buy = Com.sort_cost_buy()
    gui_dict['plot'].append(
        Window(
            window_title='Круговые диаграммы',
            canvases=[Canvas(
                title=f'Топ 5 компаний по объёму продаж в количественном выражении по товару с кодом: {code} в '
                      f'интервале от {time_start} до {time_end}',
                showlegend=True,
                plots=[PiePlot(labels=count_sale['provider_unp'].astype('str'),
                               values=count_sale['roster_item_count'].astype('int'))]
            ),
                Canvas(
                    title=f'Топ 5 компаний по объёму продаж в стоимостном выражении по товару с кодом: {code} в '
                          f'интервале от {time_start} до {time_end}',
                    showlegend=True,
                    plots=[PiePlot(labels=cost_sale['provider_unp'].astype('str'),
                                   values=cost_sale['roster_item_cost'].astype('int'))]
                ),
                Canvas(
                    title=f'Топ 5 компаний по объёму покупок в количественном выражении по товару с кодом: {code} в '
                          f'интервале от {time_start} до {time_end}',
                    showlegend=True,
                    plots=[PiePlot(labels=count_buy['recipient_unp'].astype('str'),
                                   values=count_buy['roster_item_count'].astype('int'))]
                ),
                Canvas(
                    title=f'Топ 5 компаний по объёму покупок в стоимостном выражении по товару с кодом: {code} в '
                          f'интервале от {time_start} до {time_end}',
                    showlegend=True,
                    plots=[PiePlot(labels=cost_buy['recipient_unp'].astype('str'),
                                   values=cost_buy['roster_item_cost'].astype('int'))]
                ),
            ]
        ).to_dict()
    )

    return gui_dict, error
