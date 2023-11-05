import pandas as pd
import matplotlib

matplotlib.use('TkAgg')
from tqdm import tqdm

data_last_esf = pd.read_csv('last_esf.csv')
data_check = pd.read_csv('checks_all.csv')



def get_top3(tnv_code, item_name):
    data_sorted = data_dt_esf[(data_dt_esf['g331goodstnvedcode'].astype(str) == tnv_code)
                              & (data_dt_esf['roster_item_name'] == item_name)]
    data_sorted = data_sorted.groupby('provider_unp')['roster_item_units'].sum().reset_index()
    data_ans = data_sorted.sort_values(by='roster_item_units', ascending=False)
    data_ans_to_list = data_ans.head(3)[['provider_unp', 'roster_item_units']].values.tolist()
    return data_ans_to_list



def interval_esf(last_esf, start, end, name_prod):
    last_esf['general_date_transaction'] = pd.to_datetime(last_esf['general_date_transaction'])
    last_esf = last_esf.loc[(last_esf["general_date_transaction"] >= start) & (
            last_esf["general_date_transaction"] <= end) & (
            last_esf["roster_item_name"] == name_prod)
                            ].reset_index()
    return last_esf



def interval_check(check, start, end, name_prod):
    check['issued_at'] = pd.to_datetime(check['issued_at'])
    check = check.loc[(check["issued_at"] >= start) & (data_check["issued_at"] <= end)
                      & (data_check["name"] <= name_prod)].reset_index()
    check['unp'] = check['unp'].astype(str)
    return check


def group(check):
    check = check.groupby(['unp', 'name']).agg(
        {'total_amount': 'sum', 'position_count': 'sum'}).reset_index()
    return check


def two_tables(last_esf, check):
    cost = 0
    count = 0
    for j in range(len(check['unp'])):
        for i in range(len(last_esf['roster_item_name'])):
            if (last_esf['recipient_unp'][i] == check['unp'][j]) and (
                    last_esf['roster_item_name'][i] == check['name'][j]):
                count = count + check['position_count'][j]
                cost = cost + check['total_amount'][j]
    if count != 0:
        return cost / count


def calculate_weighted_average_price(count_price):
    total_weight = 0.0
    weighted_sum = 0.0

    for item in count_price:
        weight, price = item
        total_weight += weight
        weighted_sum += weight * price

    if total_weight == 0:
        return 0  # Избегаем деления на ноль

    weighted_avg = weighted_sum / total_weight
    return weighted_avg


def get_next_unp(before_unp, tnv_code, item_name):
    data_esf_filtered = data_esf.copy()
    data_esf_filtered = data_esf_filtered.loc[(data_esf_filtered['provider_unp'].astype(str) == before_unp)
                                              & (data_esf_filtered['roster_item_name'] == item_name)
                                              & (data_esf_filtered['roster_item_code'].astype(str) == tnv_code)
                                              ]
    data_esf_filtered['roster_item_price'].fillna(data_esf_filtered['roster_item_cost']
                                                  / data_esf_filtered['roster_item_count'], inplace=True)
    data_esf_filtered = data_esf_filtered.sort_values(by='roster_item_count', ascending=False)
    data_esf_filtered['recipient_unp'] = data_esf_filtered['recipient_unp'].astype(str)
    data_esf_filtered['recipient_unp'] = data_esf_filtered['recipient_unp'].apply(lambda x: x.rstrip('0').rstrip('.'))
    data_esf_filtered = data_esf_filtered.groupby('recipient_unp').agg(
        {'roster_item_count': 'sum', 'roster_item_price': 'sum'}).reset_index()
    count_price = data_esf_filtered[['roster_item_count', 'roster_item_price']].values.tolist()

    return data_esf_filtered['recipient_unp'].astype(str).tolist(), count_price


time_start = '2021-12-15'
time_start = pd.to_datetime(time_start)
# time_end = time_start + pd.DateOffset(days=30)
time_end = '2023-01-01'
time_end = pd.to_datetime(time_end)
time_start = time_start.strftime('%Y-%m-%d')
time_end = time_end.strftime('%Y-%m-%d')
# company = ['400099778', '400460407', '997474486']
# name = 'Томат'
item_name = 'ЛИМОН 1КГ'

esf_last_int = interval_esf(data_last_esf, time_start, time_end, item_name)
check_int = interval_check(data_check, time_start, time_end, item_name)
check_int_group = group(check_int)
data = two_tables(esf_last_int, check_int_group)
last_esf = set()

data_dt_esf = pd.read_csv('dt_esf_newdate.csv')
data_esf = pd.read_csv('esf_all.csv')
tnv_code = '805501000'
top_3 = get_top3(tnv_code, item_name)
data_esf = data_esf[(data_esf['document_type'] == "ORIGINAL")]
data_esf = data_esf.loc[(data_esf["general_date_transaction"] >= time_start) & (
        data_esf["general_date_transaction"] <= time_end)
                        & (data_esf["roster_item_code"].astype(str) == tnv_code)
                        & (data_esf["roster_item_name"] == item_name)
                        ].reset_index()
data_esf = data_esf.sort_values(by='general_date_transaction')
chain_size = 3
data_esf['roster_item_price'].fillna(data_esf['roster_item_cost']
                                     / data_esf['roster_item_count'], inplace=True)
# chains = [
#     # [{'Узел1': ['вес и цена'], 'Узел2': ['вес и цена'], 'Узел3': ['вес и цена']}], # одна цепочка
# ]
iterator = 0
chains = []

start_companies = [i[0] for i in top_3]
initial_weights = [i[1] for i in top_3]
checks_company = set()


def empty_check(unp):
    df = data_check.copy()
    df = df.loc[(df['unp']).astype(str) == str(unp)]
    return df.empty


# Функция для поиска цепочек
def find_chains(current_chain, remaining_data, current_input_weight_sum, iterr):
    if len(current_chain) == chain_size:
        if empty_check(list(current_chain[-1].values())[0][-1]):
            return
        chains.append(current_chain)
        checks_company.add(list(current_chain[-1].values())[0][-1])
        return
    remaining_data = remaining_data.loc[(remaining_data['roster_item_name'] == item_name)]
    for idx, row in tqdm(remaining_data.iterrows(), total=len(remaining_data)):
        if (current_input_weight_sum >= remaining_data['roster_item_count'].get(idx, 0)) \
                and (remaining_data['roster_item_name'].get(idx, 0) == item_name) \
                and (str(remaining_data['roster_item_code'].get(idx, 0)) == str(tnv_code)):
            next_chain = current_chain.copy()
            next_chain.append({f"Узел{len(current_chain) + 1}": [row['roster_item_count'],
                                                                 row['roster_item_price'],
                                                                 row['recipient_unp']]})
            find_chains(next_chain, remaining_data[remaining_data.index != idx],
                        current_input_weight_sum + remaining_data['roster_item_count'].get(idx, 0), iterr)


data_esf_filtered = data_esf.copy()
data_esf_filtered['recipient_unp'] = data_esf_filtered['recipient_unp'].astype(str)
data_esf_filtered['recipient_unp'] = data_esf_filtered['recipient_unp'].apply(lambda x: x.rstrip('0').rstrip('.'))
data_esf_filtered = data_esf_filtered.groupby(
    ['recipient_unp', 'provider_unp', 'roster_item_name', 'roster_item_code']).agg(
    {'roster_item_count': 'sum', 'roster_item_price': 'sum'}).reset_index()
iterr = 0
# Начните поиск цепочек с каждой указанной компании
print(top_3)
for start_company in start_companies:
    start_data = data_esf_filtered.loc[(data_esf_filtered['provider_unp'].astype(str) == (str(start_company))) &
                                       (data_esf_filtered['roster_item_name'].astype(str) == (str(item_name))) &
                                       (data_esf["roster_item_code"].astype(str) == tnv_code)
                                       ]
    print(start_data)
    unps = start_data['recipient_unp'].tolist()
    weights = start_data['roster_item_count'].tolist()
    for unp, weight in zip(unps, weights):
        new_select_data = data_esf_filtered.loc[
            (data_esf_filtered['provider_unp'].astype(str) == (str(unp))) &
            (data_esf_filtered['roster_item_name'].astype(str) == (str(item_name))) &
            (data_esf["roster_item_code"].astype(str) == tnv_code)].reset_index()
        new_select_data = new_select_data.sort_values(by='roster_item_count', ascending=False)
        print(new_select_data)

        while new_select_data['roster_item_count'].sum() > weight:
            min_weight_index = new_select_data['roster_item_count'].idxmin()
            max_weight_index = new_select_data['roster_item_count'].idxmax()
            if new_select_data.loc[max_weight_index]['roster_item_count'] > weight:
                new_select_data = new_select_data.drop(max_weight_index)
            else:
                new_select_data = new_select_data.drop(min_weight_index)
        weighted_average_price = new_select_data['roster_item_cost'].sum() / new_select_data[
            'roster_item_count'].sum()
        chains.append(weighted_average_price)
print(chains)
    # for idx, row in tqdm(start_data.iterrows(), total=len(start_data)):
    #     current_chain = []
    #     current_chain.append({f"Узел1": [row['roster_item_count'], row['roster_item_price'], row['recipient_unp']]})
    #     find_chains(current_chain, data_esf_filtered[data_esf_filtered.index != idx], initial_weights[iterr], iterr)
    #     print(chains)
    #
    # if chains:
    #     weighted_prices = {'Узел1': 0, 'Узел2': 0, 'Узел3': 0}
    #     weights = {'Узел1': 0, 'Узел2': 0, 'Узел3': 0}
    #
    #     for item in chains:
    #         for i in range(chain_size):
    #             node = f'Узел{i + 1}'
    #             if node in item[i]:
    #                 weight, price, comp = item[i][node]
    #                 weighted_prices[node] += weight * price
    #                 weights[node] += weight
    #
    #     for node in weighted_prices:
    #         if weights[node] > 0:
    #             average_price = weighted_prices[node] / weights[node]
    #             print(f'Средневзвешенная цена для {node}: {average_price:.2f}')
    #
    #     esf_last_int = interval_esf(data_last_esf, time_start, time_end, item_name, list(checks_company))
    #     check_int = interval_check(data_check, time_start, time_end, item_name)
    #     check_int_group = group(check_int)
    #     data = two_tables(esf_last_int, check_int_group)
    #     print(f'Средневзвешенная цена чека: {data}')

