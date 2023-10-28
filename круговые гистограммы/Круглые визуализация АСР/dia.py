class PrintGraphByCode_visulise:
    """
    :code_assign: service
    :code_type: отрисовка PiePlot и HistPlot
    :packages:
    import pandas as pd
    """

    def __init__(self, selected_data, input_code):
        """
        :param pd.DateFrame selected_data: отфильтрованный датасет для выбранной категории
        :param str input_code: выбранная категория
        :param pd.DateFrame summeryCountry: датасет отфильтрован по средним суммам по странам
        """
        self.SelectedData = selected_data
        self.input_code = input_code
        self.summeryCountry = pd.DataFrame

    def selected_data(self):
        if self.input_code.isdigit():
            self.summeryCountry = self.SelectedData.sort_values(by='price', ascending=False)
            top_five = self.summeryCountry.head(5)[['g15_name', 'price']]
            other_contry = self.summeryCountry[5:]['price'].mean()
            other_data = pd.DataFrame({'g15_name': ['OTHER'], 'price': [other_contry]})
            self.summeryCountry = pd.concat([top_five, other_data], ignore_index=True)
        self.SelectedData.loc[self.SelectedData['cost'] / self.SelectedData['cost'].sum() < 0.02, 'g15_name'] \
            = 'OTHER+NAN'
        self.SelectedData.loc[self.SelectedData['quantity'] / self.SelectedData['quantity'].sum() < 0.02, 'g15_name'] \
            = 'OTHER+NAN'


def diagram_visualise_acp(
        dataset: pd.DataFrame,
        input_code: str = '',
):
    """
    :code_assign: users
    :code_type: Пользовательские функции
    :imports: init_gui_dict, Window, Canvas, PiePlot, PrintGraphByCode_visulise, BarPlot
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
    selected_data = dataset.loc[(dataset['g331goodstnvedcode'].astype(str) == input_code) |
                                (dataset['type'].astype(str) == input_code)]
    PG = PrintGraphByCode_visulise(selected_data, input_code)
    PG.selected_data()
    gui_dict['plot'].append(
        Window(
            window_title='Круговые диаграммы',
            canvases=[Canvas(title=f'Количественная выборка по коду: {input_code}',
                             showlegend=True,
                             plots=[PiePlot(labels=PG.SelectedData['g15_name'].astype('str'),
                                            values=PG.SelectedData['quantity'].astype('int'))]
                             ),
                      Canvas(title=f'Ценовая выборка по коду: {input_code}',
                             showlegend=True,
                             plots=[PiePlot(labels=PG.SelectedData['g15_name'].astype('str'),
                                            values=PG.SelectedData['cost'].astype('int'))]
                             ),
                      ]
        ).to_dict()
    ) 
    if input_code.isdigit():
        gui_dict['plot'].append(
            Window(
                window_title='Гистограмма',
                canvases=[Canvas(title=f'Средняя цена по странам по коду: {input_code}',
                                 showlegend=False,
                                 x_title='Страны',
                                 y_title='Цена',
                                 plots=[BarPlot(x=PG.summeryCountry['g15_name'].values,
                                                 y=PG.summeryCountry['price'].values
                                                 )]
                                 ),
                          ]
            ).to_dict())
    else:
        df = dataset

        df['weighted_cost'] = df['price'] * df['quantity']  # Взвешенная сумма

        grouped_df = df.groupby(['g15_name', 'type']).agg(
            {'weighted_cost': 'sum', 'quantity': 'sum'})  # Группировка по странам и типам + сумма стоимостей
        grouped_df['weighted_avg_cost'] = grouped_df['weighted_cost'] / grouped_df['quantity']  # Среднее взвешенное
        result_df = grouped_df.drop(columns=['weighted_cost', 'quantity']).reset_index()

        selected_data = result_df.loc[(result_df['type'].astype(str) == input_code)]  # Поменять на выпадающую строку
        selected_data = selected_data.sort_values(by=['weighted_avg_cost'],
                                                  ascending=False)  # Сортировка по средним значениям
        data_final = selected_data.head(5)
        avg_other = selected_data['weighted_avg_cost'][5:].mean()  # Топ 5 и остальное убирается в кучу
        data_final.loc[1] = ['OTHER', input_code, avg_other]
        gui_dict['plot'].append(
            Window(
                window_title='Гистограмма',
                canvases=[Canvas(title=f'Средняя цена по странам по типу товара: {input_code}',
                                 showlegend=False,
                                 x_title='Страны',
                                 y_title='Цена',
                                 plots=[BarPlot(x=data_final['g15_name'].values,
                                                y=data_final['weighted_avg_cost'].values
                                                )]
                                 ),
                          ]
            ).to_dict())
    return gui_dict, error
