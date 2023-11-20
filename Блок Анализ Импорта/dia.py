class PrintGraphByCode_visulise:
    """
    :code_assign: service
    :code_type: отрисовка PiePlot и HistPlot
    :packages:
    import pandas as pd
    """

    def __init__(self, selected_data, input_code, threshold_value):
        """
        :param pd.DateFrame selected_data: отфильтрованный датасет для выбранной категории
        :param str input_code: выбранная категория
        :param pd.DateFrame summeryCountry: датасет отфильтрован по средним суммам по странам
        """
        self.SelectedData = selected_data
        self.input_code = input_code
        self.summeryCountry = pd.DataFrame
        self.threshold_value = threshold_value / 100

    def selected_data(self):
        if self.input_code.isdigit():
            self.summeryCountry = self.SelectedData.sort_values(by='price', ascending=False)
            unit = self.summeryCountry.groupby(['g15_name'])['price'].mean().reset_index()
            if unit.shape[0] > 5:
                unit = unit.sort_values(by='price', ascending=False).reset_index()
                top_five = unit.head(min(5, len(unit)))[['g15_name', 'price']]
                other_contry = unit[5:]['price'].mean()
                other_data = pd.DataFrame({'g15_name': ['OTHER'], 'price': [other_contry]})
                self.summeryCountry = pd.concat([top_five, other_data], ignore_index=True)
            else:
                self.summeryCountry = unit
        self.SelectedData.loc[
            self.SelectedData['g15_name'].isna(), 'g15_name'
        ] = 'NaN'
        self.SelectedData = self.SelectedData.groupby(['g15_name']).agg({
            'quantity': 'sum',
            'cost': 'sum',
        }).reset_index()
        self.SelectedData.loc[
            self.SelectedData['cost'] / self.SelectedData['cost'].sum() <= self.threshold_value, 'g15_name'] \
            = 'OTHER'
        self.SelectedData.loc[
            self.SelectedData['quantity'] / self.SelectedData['quantity'].sum() <= self.threshold_value, 'g15_name'] \
            = 'OTHER'


def diagram_visualise_acp(
        dataset_import: pd.DataFrame,
        dataset_dt: pd.DataFrame,
        input_code: str = '803901000',
        threshold_value: float = 2.0,
        start_date: str = '2021-01-01',
        end_date: str = '2023-12-31',
        linear_regression: bool = False,
        step_regression: int = 1,
        adding_code: bool = False,
        four_digit_code: str = ''
):
    """
    :code_assign: users
    :code_type: Пользовательские функции
    :imports: init_gui_dict, Window, Canvas, PiePlot, PrintGraphByCode_visulise, BarPlot, ACPLinearRegression, PricesESF, Top_OriginCountry_Cost_Count1
    :packages:
    import pandas as pd
    import numpy as np
    :param_block pd.DataFrame dataset_import: датасет
    :param_block pd.DataFrame dataset_dt: датасет
    :param str input_code: выбранная код ТН ВЭД или тип товара
    :param float threshold_value: пороговое значение
    :param str start_date: дата начала
    :param str end_date: дата конца
    :param bool linear_regression: флаг для линейной регрессии
    :param int step_regression: шаг регрессии
    :param bool adding_code: флаг для учета дополнительного кода
    :param str four_digit_code: дополнительный код
    :returns: gui_dict, error
    :rtype: dict, str
    :semrtype: ,
    """
    error = ""
    gui_dict = init_gui_dict()
    TNVED_codes = {
        'fridges': ['8418102001',
                    '8418108001',
                    '8418211000',
                    '8418215100',
                    '8418215900',
                    '8418219100',
                    '8418219900',
                    '8418302001',
                    '8418308001',
                    '8418402001',
                    '8418408001'],
        'tires': ['4011100003',
                  '4011100009',
                  '4011201000',
                  '4011209000',
                  '4011400000',
                  '4011700000',
                  '4011800000',
                  '4011900000'],
        'tomato': ['702000001',
                   '702000002',
                   '702000003',
                   '702000004',
                   '702000005',
                   '702000006',
                   '702000007',
                   '702000009'],
        'lemons': ['805501000',
                   '80550100',
                   '8055010',
                   '805501',
                   '80550',
                   '8055',
                   '805',
                   ],
        'banana': [
            '803901000',
            '80390100',
            '8039010',
            '803901',
            '80390',
            '8039',
            '803'
        ]
    }
    if dataset_dt.empty:
        raise Exception(f'Датасет ДТ пуст')
    if dataset_import.empty:
        raise Exception('Датасет импорта пуст')
    start_date_wo_day = start_date.split('-')
    end_date_wo_day = end_date.split('-')
    date_start = '-'.join(start_date_wo_day[:2])
    date_end = '-'.join(map(str, end_date_wo_day[:2]))
    date_start = pd.to_datetime(date_start)
    date_end = pd.to_datetime(date_end)
    if not input_code.isdigit():
        if input_code.lower() in 'холодильники fridges':
            input_codes = TNVED_codes['fridges']
            input_code = 'холодильник'
        elif input_code.lower() in 'шины шина tires':
            input_codes = TNVED_codes['tires']
            input_code = 'шины'
        elif input_code.lower() in 'томаты помидоры tomatoes':
            input_codes = TNVED_codes['tomato']
            input_code = 'томат'
        elif input_code.lower() in 'лимоны lemons плантайны':
            input_codes = TNVED_codes['lemons']
            input_code = 'лимон'
        elif input_code.lower() in 'bananas бананы':
            input_codes = TNVED_codes['banana']
            input_code = 'банан'
        else:
            raise Exception(f'Кодов ТН ВЭД по вашему товару нет')
    selectedData = dataset_import.loc[(dataset_import['g331goodstnvedcode'].astype(str) == input_code.lstrip('0')) |
                                      (dataset_import['type'].str.lower().str.contains(input_code.lower()))]
    if input_code.isdigit():
        if adding_code:
            selectedData = selectedData.loc[
                (selectedData['goodsaddtnvedcode'].astype(str) == four_digit_code.lstrip('0'))]
        else:
            four_digit_code = ''
    if selectedData.empty:
        raise Exception(f'Товаров по коду или типу выбранного товара нет')
    selectedData['import_date'] = pd.to_datetime(selectedData['import_date'])
    selected_data = selectedData.loc[
        (selectedData['import_date'] >= date_start) & (selectedData['import_date'] <= date_end)]
    if selected_data.empty:
        raise Exception(f'Товаров по коду или типу выбранного товара нет в заданном интервале нет')

    PG = PrintGraphByCode_visulise(selected_data, input_code, threshold_value)
    PG.selected_data()
    gui_dict['plot'].append(
        Window(
            window_title='Топ стран-импортеров',
            canvases=[
                Canvas(title=f'Топ стран-импортеров в количественной выборке по коду: {input_code} {four_digit_code}',
                       showlegend=True,
                       plots=[PiePlot(labels=PG.SelectedData['g15_name'].astype('str'),
                                      values=PG.SelectedData['quantity'].astype('int'))]
                       ),
                Canvas(title=f'Топ стран-импортеров в стоимостной выборке по коду: {input_code} {four_digit_code}',
                       showlegend=True,
                       plots=[PiePlot(labels=PG.SelectedData['g15_name'].astype('str'),
                                      values=PG.SelectedData['cost'].astype('int'))]
                       ),
                ]
        ).to_dict()
    )

    if input_code.isdigit():
        selectedDataOrigCountry = dataset_dt.loc[
            (dataset_dt['g331goodstnvedcode'].astype(str) == input_code.lstrip('0'))]
        if adding_code:
            selectedDataOrigCountry = selectedDataOrigCountry.loc[
                (selectedDataOrigCountry['goodsaddtnvedcode'].astype(str) == four_digit_code.lstrip('0'))]

        if selectedDataOrigCountry.empty:
            raise Exception(f'Товаров по коду или типу выбранного товара нет')

        selectedDataOrigCountry.loc[:, 'dt_date'] = pd.to_datetime(selectedDataOrigCountry['dt_date'])
        selected_data_orig_country = selectedDataOrigCountry.loc[
            (selectedDataOrigCountry["dt_date"] >= date_start) & (selectedDataOrigCountry["dt_date"] <= date_end)]
        if selected_data_orig_country.empty:
            raise Exception(f'Товаров по коду или типу выбранного товара нет в заданном интервале нет')
        Com = Top_OriginCountry_Cost_Count1(selected_data_orig_country, input_code, threshold_value)
        count_sale = Com.sort_count_sale()
        cost_sale = Com.sort_cost_sale()

        gui_dict['plot'].append(
            Window(
                window_title='Топ стран-производителей',
                canvases=[Canvas(
                    title=f'Топ стран-производителей в количественной выборке по коду: {input_code}',
                    showlegend=True,
                    plots=[PiePlot(labels=count_sale['g34origincountryname'].astype('str'),
                                   values=count_sale['count'].astype('int'))]
                ),
                    Canvas(
                        title=f'Топ стран-производителей в стоимостной выборке по коду: {input_code}',
                        showlegend=True,
                        plots=[PiePlot(labels=cost_sale['g34origincountryname'].astype('str'),
                                       values=cost_sale['cost'].astype('int'))]
                    ),
                ]
            ).to_dict()
        )
        price_sale = Com.sort_price_sell()
        gui_dict['plot'].append(
            Window(
                window_title='Гистограммы',
                canvases=[Canvas(title=f'Средняя цена по странам-импортерам по коду: {input_code}',
                                 showlegend=False,
                                 x_title='Страны',
                                 y_title='Цена, бел. руб',
                                 plots=[BarPlot(x=PG.summeryCountry['g15_name'].values,
                                                y=PG.summeryCountry['price'].values
                                                )]
                                 ),
                          Canvas(title=f'Средняя цена по странам-производителям по коду: {input_code}',
                                 showlegend=False,
                                 x_title='Страны',
                                 y_title='Цена, бел. руб',
                                 plots=[BarPlot(x=price_sale['g34origincountryname'].values,
                                                y=price_sale['price'].values
                                                )]
                                 ),
                          ]
            ).to_dict())

        pd.options.mode.chained_assignment = None
        dataset_dt_filtered = dataset_dt[(dataset_dt['g331goodstnvedcode'] == int(input_code.lstrip('0')))]
        if adding_code:
            dataset_dt_filtered = dataset_dt_filtered.loc[
                (dataset_dt_filtered['goodsaddtnvedcode'].astype(str) == four_digit_code.lstrip('0'))]

        if dataset_dt_filtered.empty:
            raise Exception(f'Нет записей по коду {input_code} в декларациях на товарах')

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        dataset_dt_filtered['dt_date'] = pd.to_datetime(dataset_dt_filtered['dt_date'])

        dt_data = dataset_dt_filtered.loc[
            (dataset_dt_filtered['dt_date'] >= start_date) & (dataset_dt_filtered['dt_date'] <= end_date)]

        pe = PricesESF(dt_data=dt_data)
        sorted_dt_dates, dt_means, weight = pe.get_dt_means_monthly(input_code)
        if input_code in TNVED_codes['fridges'] or input_code in TNVED_codes['tires']:
            weights = [f'Объем: {i} шт.' for i in weight]
            weight = ['штука'] + weight
        else:
            weights = [f'Объем: {i // 1000} т' for i in weight]
        x_list = [pd.array(sorted_dt_dates)]
        y_list = [pd.array(dt_means)]

    else:
        selectedDataOrigCountry = dataset_dt.loc[(dataset_dt['g331goodstnvedcode'].astype(str).str.lower().isin(
            [tnved_code.lower() for tnved_code in input_codes]))
        ]
        if selectedDataOrigCountry.empty:
            raise Exception(f'Товаров по коду или типу выбранного товара нет')

        selectedDataOrigCountry.loc[:, 'dt_date'] = pd.to_datetime(selectedDataOrigCountry['dt_date'])
        selected_data_orig_country = selectedDataOrigCountry.loc[
            (selectedDataOrigCountry["dt_date"] >= date_start) & (selectedDataOrigCountry["dt_date"] <= date_end)]
        if selected_data_orig_country.empty:
            raise Exception(f'Товаров по коду или типу выбранного товара нет в заданном интервале нет')
        Com = Top_OriginCountry_Cost_Count1(selected_data_orig_country, input_code, threshold_value)
        count_sale = Com.sort_count_sale()
        cost_sale = Com.sort_cost_sale()

        gui_dict['plot'].append(
            Window(
                window_title='Топ стран-производителей',
                canvases=[Canvas(
                    title=f'Топ стран-производителей в количественной выборке по типу товара: {input_code}',
                    showlegend=True,
                    plots=[PiePlot(labels=count_sale['g34origincountryname'].astype('str'),
                                   values=count_sale['count'].astype('int'))]
                ),
                    Canvas(
                        title=f'Топ стран-производителей в стоимостной выборке по типу товара: {input_code}',
                        showlegend=True,
                        plots=[PiePlot(labels=cost_sale['g34origincountryname'].astype('str'),
                                       values=cost_sale['cost'].astype('int'))]
                    ),
                ]
            ).to_dict()
        )

        df = selectedData

        df['weighted_cost'] = df['price'] * df['quantity']  # Взвешенная сумма

        grouped_df = df.groupby(['g15_name', 'type']).agg(
            {'weighted_cost': 'sum', 'quantity': 'sum'})  # Группировка по странам и типам + сумма стоимостей
        grouped_df['weighted_avg_cost'] = grouped_df['weighted_cost'] / grouped_df['quantity']  # Среднее взвешенное
        result_df = grouped_df.drop(columns=['weighted_cost', 'quantity']).reset_index()

        if result_df.empty:
            raise Exception(f'Пустая выборка')

        result_df = result_df.sort_values(by=['weighted_avg_cost'],
                                          ascending=False)  # Сортировка по средним значениям
        data_final = result_df.head(5)
        avg_other = result_df['weighted_avg_cost'][5:].mean()  # Топ 5 и остальное убирается в кучу
        data_final.loc[1] = ['OTHER', input_code, avg_other]

        price_sale = Com.sort_price_sell()
        gui_dict['plot'].append(
            Window(
                window_title='Гистограммы',
                canvases=[Canvas(title=f'Средняя цена по странам-импортерам по типу товара: {input_code}',
                                 showlegend=False,
                                 x_title='Страны',
                                 y_title='Цена, бел. руб',
                                 plots=[BarPlot(x=data_final['g15_name'].values,
                                                y=data_final['weighted_avg_cost'].values
                                                )]
                                 ),
                          Canvas(title=f'Средняя цена по странам-производителям по типу товара: {input_code}',
                                 showlegend=False,
                                 x_title='Страны',
                                 y_title='Цена, бел. руб',
                                 plots=[BarPlot(x=price_sale['g34origincountryname'].values,
                                                y=price_sale['price'].values
                                                )]
                                 ),

                          ]
            ).to_dict())

        pd.options.mode.chained_assignment = None
        dataset_dt_filtered = dataset_dt[
            (dataset_dt['g331goodstnvedcode'].astype(str).str.lower().isin([code.lower() for code in input_codes]))]
        if dataset_dt_filtered.empty:
            raise Exception(f'Нет записей по типу "{input_code}" в декларациях на товарах')

        dataset_dt_filtered['dt_date'] = pd.to_datetime(dataset_dt_filtered['dt_date'])

        dt_data = dataset_dt_filtered.loc[
            (dataset_dt_filtered['dt_date'] >= start_date) & (dataset_dt_filtered['dt_date'] <= end_date)]

        pe = PricesESF(dt_data=dt_data)
        sorted_dt_dates, dt_means, weight = pe.get_dt_means_monthly(input_code)
        if input_code.lower() in 'холодильники шина шины':
            weights = [f'Объем: {i} шт.' for i in weight]
            weight = ['штука'] + weight
        else:
            weights = [f'Объем: {i // 1000} т' for i in weight]

        x_list = [pd.array(sorted_dt_dates)]
        y_list = [pd.array(dt_means)]

    names = ['ДТ']
    plots = []
    if linear_regression:
        lr = ACPLinearRegression(x_list, y_list, step_regression, names, [weight])
        plots = lr.train_regression()

    for x, y in zip(x_list, y_list):
        plots.append(LinePlot(x=x, y=y, names=names))
        plots.append(Scatter2DPlot(x=x, y=y, names=names, text=[weights], marker=[dict(color="black")]))

    gui_dict['plot'].append(
        Window(
            window_title='Линейный график среднезвешенных цен',
            canvases=[Canvas(
                title=f'Средневзвешенные цены продаж по товару {input_code} с {start_date} по {end_date}',
                x_title="Месяц",
                y_title='Цена, бел. руб',
                showlegend=True,
                plots=plots)]
        ).to_dict()
    )

    return gui_dict, error
