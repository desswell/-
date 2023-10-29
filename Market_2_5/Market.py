class Market_ACP:
    """
    :code_assign: service
    :code_type: отрисовка графиков ф-ий блока Рынка
    :packages:
    """
    def __init__(self, data, input_code, company, time_start, time_end):
        """
        :param pd.DateFrame data: неотфильтрованный датасет
        :param str input_code: выбранной продукт
        :param str company: унп выбранной компании
        :param str time_start: начало временного интервала
        :param str time_end: конец временного интервала
        """
        self.time_start = time_start
        self.time_end = time_end
        self.data = data
        self.code = int(input_code)
        self.company = int(company)
        self.canvass = list()


    """
    Чтение файла по ДТ и Чекам
    """
    def read_data_dt(self):
        """
        Функция чтения файла по ДТ
        """
        self.data['dt_date'] = pd.to_datetime(self.data['dt_date'])
        self.data['total_sum'] = self.data['g38netweightquantity'] * self.data['ТС/кг, бел руб']
        # Convert object type to datetime
        time_start = pd.to_datetime(self.time_start)
        time_end = pd.to_datetime(self.time_end)
        # Sampling by interval
        data = self.data[(self.data['dt_date'] >= time_start) & (self.data['dt_date'] <= time_end)]
        # sampling by code and company
        data_nw = data[(data['g32goodsnumeric'] == self.code) & (data['g14rbunp'] == self.company)]
        return data_nw


    def read_data_ch(self):
        """
        Функция чтения файла по Чекам
        """
        self.data['issued_at'] = pd.to_datetime(self.data['issued_at'])
        time_start = pd.to_datetime(self.time_start)
        time_end = pd.to_datetime(self.time_end)
        data = self.data[(self.data['issued_at'] >= time_start) & (self.data['issued_at'] <= time_end)]
        data_nw = data[(data['unp'] == self.company)]
        return data_nw




    """
    2.5 Показ объёма в количественном и стоимостном выражении, ориентируясь отдельно на
     ДТ и на чеки - столбч. диаграмма 
    """
    def show_dt(self):

        sorted_data = self.read_data_dt()

        grouped_df_sum = sorted_data.groupby('dt_date')['total_sum'].sum().reset_index()
        grouped_df_count = sorted_data.groupby('dt_date')['g38netweightquantity'].sum().reset_index()
        self.canvass.append(Canvas(title=f'Объем рынка по ДТ по коду товара: {self.code}, по УНП компании: {self.company}',
                                   showlegend=False,
                                   x_title='Дата',
                                   y_title='Cумма по ДТ в бел. руб.',
                                   plots=[BarPlot(x=grouped_df_sum['dt_date'].values,
                                                  y=grouped_df_sum['total_sum'].values),
                                          BarPlot(x=grouped_df_count['dt_date'].values,
                                                  y=grouped_df_count['g38netweightquantity'].values
                                                  )]
                                   )
                            )



    def show_check(self):
        """
        Функция показа объема рынка в стоимостном выражении по Чекам
        """

        #Получение выборки
        sorted_data = self.read_data_ch()

        grouped_df_sum = sorted_data.groupby('issued_at')['total_amount'].sum().reset_index()
        grouped_df_count = sorted_data.groupby('issued_at')['position_count'].sum().reset_index()
        self.canvass.append(Canvas(title=f'Объем рынка по Чекам по коду товара: {self.code}, по УНП компании: {self.company}',
                                   showlegend=False,
                                   x_title='Дата',
                                   y_title='Сумма в бел. руб.',
                                   plots=[BarPlot(x=grouped_df['issued_at'].values,
                                                  y=grouped_df['total_amount'].values),
                                          BarPlot(x=grouped_df['issued_at'].values,
                                                  y=grouped_df['position_count'].values
                                                  )]
                                   )
                            )




def market_acp(dataset: pd.DataFrame,
               input_code: str,
               company: str,
               time_start: str,
               time_end: str,
               selected_plot: str):
    """
    :code_assign: users
    :code_type: Пользовательские функции
    :imports: init_gui_dict, Canvas, BarPlot, Market_ACP, Window
    :packages:
    import datetime
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    :param_block pd.DataFrame dataset: датасет
    :param str input_code: выбранный код товара
    :param str company: выбранная компания
    :param str time_start: начало интервала
    :param str time_end: конец интервал
    :param str selected_plot: выбранный тип графика
    :returns: gui_dict, error
    :rtype: dict, str
    :semrtype: ,
    """
    market = Market_ACP(dataset, input_code, company, time_start, time_end)
    # Выбор пользователем нужного графика
    gui_dict = init_gui_dict()
    error = ""
    if selected_plot == '1':
        market.show_dt()
    else:
        market.show_check()
    gui_dict['plot'].append(
        Window(
            window_title='Столбчатые диаграммы',
            canvases=market.canvass
        ).to_dict()
    )
    return gui_dict, error
