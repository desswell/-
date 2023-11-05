import pandas as pd

def process_data(df, product_code):
    """
    Функция фильтрации датасета по коду товара
    """
    df_filtered = df[(df['roster_item_code'] == product_code)]

    return df_filtered

def get_dt_means_daily(df):
    """
    Функция подсчета средневзвешенного значения по всем ДТ по дням
    """
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

    dt_dates = dates_to_days(years, months, days)

    return dt_dates, dt_means

def get_dt_means_monthly(df):
    """
    Функция подсчета средневзвешенного значения по всем ДТ по месяцам
    """
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

    # Возвращаем результаты в виде массивов
    years = grouped['year'].tolist()
    months = grouped['month'].tolist()
    dt_means = grouped['weighted_average_price'].tolist()

    first_date = str(months[0]) + '-' + str(years[0])

    dt_dates = dates_to_months(years, months)

    return dt_dates, dt_means

def get_first_esf_means_daily(df):
    """
    Функция подсчета средневзвешенного значения по всем ЭСЧФ по дням
    """

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
    grouped = df.groupby(['year', 'month', 'day']).apply(lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
    grouped.columns = ['year', 'month', 'day', 'weighted_average_price']

    # Возвращаем результаты в виде массивов
    years = grouped['year'].tolist()
    months = grouped['month'].tolist()
    days = grouped['day'].tolist()
    esf_means = grouped['weighted_average_price'].tolist()

    first_date = str(days[0]) + '-' + str(months[0]) + '-' + str(years[0])

    first_esf_dates = dates_to_days(years, months, days)

    return first_esf_dates, esf_means

def get_first_esf_means_monthly(df):
    """
    Функция подсчета средневзвешенного значения по всем ЭСЧФ по месяцам
    """

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
    grouped = df.groupby(['year', 'month']).apply(lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
    grouped.columns = ['year', 'month', 'weighted_average_price']

    # Возвращаем результаты в виде массивов
    years = grouped['year'].tolist()
    months = grouped['month'].tolist()
    esf_means = grouped['weighted_average_price'].tolist()

    first_date = str(months[0]) + '-' + str(years[0])

    first_esf_dates = dates_to_months(years, months)

    return first_esf_dates, esf_means

def get_esf_means_daily(df):
    """
    Функция подсчета средневзвешенного значения по всем ЭСЧФ по дням
    """

    # Преобразуем поле general_date_transaction в формат даты
    df['general_date_transaction'] = pd.to_datetime(df['general_date_transaction'])

    # Извлекаем год, месяц и день из даты
    df['year'] = df['general_date_transaction'].dt.year
    df['month'] = df['general_date_transaction'].dt.month
    df['day'] = df['general_date_transaction'].dt.day

    # Рассчитываем сумму (продажи * цена) для каждой строки
    df['total_sales'] = df['roster_item_count'] * df['roster_item_price']

    # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
    grouped = df.groupby(['year', 'month', 'day']).apply(lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
    grouped.columns = ['year', 'month', 'day', 'weighted_average_price']

    # Возвращаем результаты в виде массивов
    years = grouped['year'].tolist()
    months = grouped['month'].tolist()
    days = grouped['day'].tolist()
    esf_means = grouped['weighted_average_price'].tolist()

    first_date = str(days[0]) + '-' + str(months[0]) + '-' + str(years[0])

    esf_dates = dates_to_days(years, months, days)

    return esf_dates, esf_means

def get_esf_means_monthly(df):
    """
    Функция подсчета средневзвешенного значения по всем ЭСЧФ по месяцам
    """

    # Преобразуем поле general_date_transaction в формат даты
    df['general_date_transaction'] = pd.to_datetime(df['general_date_transaction'])

    # Извлекаем год, месяц и день из даты
    df['year'] = df['general_date_transaction'].dt.year
    df['month'] = df['general_date_transaction'].dt.month

    # Рассчитываем сумму (продажи * цена) для каждой строки
    df['total_sales'] = df['roster_item_count'] * df['roster_item_price']

    # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
    grouped = df.groupby(['year', 'month']).apply(lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
    grouped.columns = ['year', 'month', 'weighted_average_price']

    # Возвращаем результаты в виде массивов
    years = grouped['year'].tolist()
    months = grouped['month'].tolist()
    esf_means = grouped['weighted_average_price'].tolist()

    first_date = str(months[0]) + '-' + str(years[0])

    esf_dates = dates_to_months(years, months)

    return esf_dates, esf_means

def get_last_esf_means_daily(df):
    """
    Функция подсчета средневзвешенного значения по последнему ЭСЧФ по дням
    """

    # Преобразуем поле general_date_transaction в формат даты
    df['general_date_transaction'] = pd.to_datetime(df['general_date_transaction'])

    # Извлекаем год, месяц и день из даты
    df['year'] = df['general_date_transaction'].dt.year
    df['month'] = df['general_date_transaction'].dt.month
    df['day'] = df['general_date_transaction'].dt.day

    # Рассчитываем сумму (продажи * цена) для каждой строки
    df['total_sales'] = df['roster_item_count'] * df['roster_item_price']

    # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
    grouped = df.groupby(['year', 'month', 'day']).apply(lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
    grouped.columns = ['year', 'month', 'day', 'weighted_average_price']

    # Возвращаем результаты в виде массивов
    years = grouped['year'].tolist()
    months = grouped['month'].tolist()
    days = grouped['day'].tolist()
    last_esf_means = grouped['weighted_average_price'].tolist()

    first_date = str(days[0]) + '-' + str(months[0]) + '-' + str(years[0])

    last_esf_dates = dates_to_days(years, months, days)

    return last_esf_dates, last_esf_means

def get_last_esf_means_monthly(df):
    """
    Функция подсчета средневзвешенного значения по последнему ЭСЧФ по месяцам
    """

    # Преобразуем поле general_date_transaction в формат даты
    df['general_date_transaction'] = pd.to_datetime(df['general_date_transaction'])

    # Извлекаем год, месяц и день из даты
    df['year'] = df['general_date_transaction'].dt.year
    df['month'] = df['general_date_transaction'].dt.month

    # Рассчитываем сумму (продажи * цена) для каждой строки
    df['total_sales'] = df['roster_item_count'] * df['roster_item_price']

    # Группируем данные по году и месяцу, а затем рассчитываем средневзвешенное значение
    grouped = df.groupby(['year', 'month']).apply(lambda x: (x['total_sales']).sum() / x['roster_item_count'].sum()).reset_index()
    grouped.columns = ['year', 'month', 'weighted_average_price']

    # Возвращаем результаты в виде массивов
    years = grouped['year'].tolist()
    months = grouped['month'].tolist()
    last_esf_means = grouped['weighted_average_price'].tolist()

    first_date = str(months[0]) + '-' + str(years[0])

    last_esf_dates = dates_to_months(years, months)

    return last_esf_dates, last_esf_means

def get_check_means_daily(df):
    """
    Функция подсчета средневзвешенного значения по всем ЧЕКам по дням
    """

    # Рассчитываем общую сумму (продажи * цена) для каждой строки
    df['total_sales'] = df['position_count'] * df['price']

    # Группируем данные по году, месяцу и дню, а затем рассчитываем средневзвешенное значение
    grouped = df.groupby(['year_check', 'month_check', 'day_check']).apply(lambda x: (x['total_sales']).sum() / x['position_count'].sum()).reset_index()
    grouped.columns = ['year', 'month', 'day', 'weighted_average_price']

    # Возвращаем результаты в виде массивов
    years = grouped['year'].tolist()
    months = grouped['month'].tolist()
    days = grouped['day'].tolist()
    check_means = grouped['weighted_average_price'].tolist()

    first_date = str(days[0]) + '-' + str(months[0]) + '-' + str(years[0])

    check_dates = dates_to_days(years, months, days)

    return check_dates, check_means

def get_check_means_monthly(df):
    """
    Функция подсчета средневзвешенного значения по всем Чекам по месяцам
    """

    # Рассчитываем общую сумму (продажи * цена) для каждой строки
    df['total_sales'] = df['position_count'] * df['price']

    # Группируем данные по году, месяцу и дню, а затем рассчитываем средневзвешенное значение
    grouped = df.groupby(['year_check', 'month_check']).apply(lambda x: (x['total_sales']).sum() / x['position_count'].sum()).reset_index()
    grouped.columns = ['year', 'month', 'weighted_average_price']

    # Возвращаем результаты в виде массивов
    years = grouped['year'].tolist()
    months = grouped['month'].tolist()
    check_means = grouped['weighted_average_price'].tolist()

    first_date = str(months[0]) + '-' + str(years[0])

    check_dates = dates_to_months(years, months)

    return check_dates, check_means

def dates_to_days(years, months, days):
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

def dates_to_months(years, months):
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

# Чтение файлов
dt_filename = 'dt_esf.csv'
esf_filename = 'esf.csv'
check_filename = 'esf_check.csv'
product_code = 803901000
start_date = '2021-01-01'
end_date = '2023-12-31'
daily_data = 0

dt_df = pd.read_csv('..\\' + dt_filename)
esf_df = pd.read_csv('..\\' + esf_filename)
check_df = pd.read_csv('..\\' + check_filename)
pd.options.mode.chained_assignment = None

# Фильтрация по коду товара
dataset_dt_filtered = process_data(dt_df, product_code)
dataset_esf_filtered = process_data(esf_df, product_code)
dataset_check_filtered = process_data(check_df, product_code)

# Фильтрация по дате
dataset_dt_filtered['dt_date'] = pd.to_datetime(dataset_dt_filtered['dt_date'])
dataset_dt_filtered['general_date_transaction'] = pd.to_datetime(dataset_dt_filtered['general_date_transaction'])
dataset_esf_filtered['general_date_transaction'] = pd.to_datetime(dataset_esf_filtered['general_date_transaction'])
dataset_check_filtered['general_date_transaction'] = pd.to_datetime(dataset_check_filtered['general_date_transaction'])
dataset_check_filtered['issued_at'] = pd.to_datetime(dataset_check_filtered['issued_at'])

dt_data = dataset_dt_filtered[(dataset_dt_filtered['dt_date'] >= start_date) & (dataset_dt_filtered['dt_date'] <= end_date)]
first_esf_data = dataset_dt_filtered[(dataset_dt_filtered['general_date_transaction'] >= start_date) & (dataset_dt_filtered['general_date_transaction'] <= end_date)]
esf_data = dataset_esf_filtered[(dataset_esf_filtered['general_date_transaction'] >= start_date) & (dataset_esf_filtered['general_date_transaction'] <= end_date)]
last_esf_data = dataset_check_filtered[(dataset_check_filtered['general_date_transaction'] >= start_date) & (dataset_check_filtered['general_date_transaction'] <= end_date)]
check_data = dataset_check_filtered[(dataset_check_filtered['issued_at'] >= start_date) & (dataset_check_filtered['issued_at'] <= end_date)]

if daily_data:
    sorted_dt_dates, dt_means = get_dt_means_daily(dt_data)
else:
    sorted_dt_dates, dt_means = get_dt_means_monthly(dt_data)

print('\nСредневзвешенные значения по всем ДТ')
for i in range(len(dt_means)):
    print(sorted_dt_dates[i], end=' ')
    print(dt_means[i])
print('\n'+'-'*40)

if daily_data:
    sorted_first_esf_dates, first_esf_means = get_first_esf_means_daily(first_esf_data)
else:
    sorted_first_esf_dates, first_esf_means = get_first_esf_means_monthly(first_esf_data)

print('\nСредневзвешенные значения по первым ЭСЧФ')
for i in range(len(first_esf_means)):
    print(sorted_first_esf_dates[i], end=' ')
    print(first_esf_means[i])
print('\n'+'-'*40)

if daily_data:
    sorted_esf_dates, esf_means = get_esf_means_daily(esf_data)
else:
    sorted_esf_dates, esf_means = get_esf_means_monthly(esf_data)

print('\nСредневзвешенные значения по всем ЭСЧФ')
for i in range(len(esf_means)):
    print(sorted_esf_dates[i], end=' ')
    print(esf_means[i])
print('\n'+'-'*40)

if daily_data:
    sorted_last_esf_dates, last_esf_means = get_last_esf_means_daily(last_esf_data)
else:
    sorted_last_esf_dates, last_esf_means = get_last_esf_means_monthly(last_esf_data)

print('\nСредневзвешенные значения по последнему ЭСЧФ')
for i in range(len(last_esf_means)):
    print(sorted_last_esf_dates[i], end=' ')
    print(last_esf_means[i])
print('\n'+'-'*40)

if daily_data:
    sorted_check_dates, check_means = get_last_esf_means_daily(check_data)
else:
    sorted_check_dates, check_means = get_check_means_monthly(check_data)

print('\nСредневзвешенные значения по всем чекам')
for i in range(len(check_means)):
    print(sorted_check_dates[i], end=' ')
    print(check_means[i])
print('\n'+'-'*40)





