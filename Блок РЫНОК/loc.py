import pandas as pd

data_last_esf = pd.read_csv('last_esf.csv')
data_check = pd.read_csv('checks_all.csv')
data_dt_esf = pd.read_csv('dt_esf_newdate.csv')
data_esf = pd.read_csv('esf_all.csv')


def get_unp_first_esf(tnv_code, item_name, time_start, time_end):
    data_sorted = data_dt_esf[(data_dt_esf['g331goodstnvedcode'].astype(str) == tnv_code)
                              & (data_dt_esf['roster_item_name'] == item_name)
                              & (data_dt_esf['dt_date'] >= time_start)
                              & (data_dt_esf['dt_date'] <= time_end)].reset_index()
    data_ans = data_sorted.sort_values(by='roster_item_count', ascending=False)
    data_ans['recipient_unp'] = data_ans['recipient_unp'].astype(str)
    data_ans['recipient_unp'] = data_ans['recipient_unp'].apply(lambda x: x.rstrip('0').rstrip('.'))
    data_ans_to_list = data_ans[['recipient_unp', 'roster_item_count', 'roster_item_cost',
                                 'ТС/кг, бел руб', 'g38netweightquantity']].values.tolist()
    return data_ans_to_list


def get_unp_weight(unp_comp):
    df = data_esf.copy()
    df = df.loc[(df['provider_unp'].astype(str) == unp_comp)].reset_index()

    df = df.sort_values(by='roster_item_count', ascending=False)
    df['recipient_unp'] = df['recipient_unp'].astype(str)
    df['recipient_unp'] = df['recipient_unp'].apply(lambda x: x.rstrip('0').rstrip('.'))
    return df['recipient_unp'].astype(str).tolist(), df['roster_item_count'].tolist(), df['roster_item_price'].tolist()


time_start = '2021-01-01'
time_start = pd.to_datetime(time_start)
# time_end = time_start + pd.DateOffset(days=120)
time_end = '2024-01-01'

time_end = pd.to_datetime(time_end)
time_start = time_start.strftime('%Y-%m-%d')
time_end = time_end.strftime('%Y-%m-%d')
item_name = 'БАНАН 1КГ'
tnv_code = '803901000'
unpes = get_unp_first_esf(tnv_code, item_name, time_start, time_end)

data_esf = data_esf[(data_esf['document_type'] == "ORIGINAL")]
data_esf = data_esf.loc[(data_esf["general_date_transaction"] >= time_start) & (
        data_esf["general_date_transaction"] <= time_end)
                        & (data_esf["roster_item_code"].astype(str) == tnv_code)
                        & (data_esf["roster_item_name"] == item_name)
                        ].reset_index()

data_esf = data_esf.sort_values(by='general_date_transaction')
first_cost = []
first_weight = []
dt_costs = []
dt_weights = []
saved_cost = []
saved_weight = []

for unp, weight, esf_cost, dt_cost, dt_weight in unpes:
    new_unp, new_weight, new_cost = get_unp_weight(unp)
    dt_costs.append(dt_cost)
    dt_weights.append(dt_weight)
    saved_cost.extend(new_cost)
    saved_weight.extend(new_weight)
    first_cost.append(esf_cost)
    first_weight.append(weight)


print(f'weighted_dt = {sum([dt_costs[i] * dt_weights[i] for i in range(len(dt_weights))]) / sum(dt_weights)}')
print(f'weighted_cost1 = {sum(first_cost) / sum(first_weight)}')
print(f'weighted_cost2 = {sum([saved_cost[i] * saved_weight[i] for i in range(len(saved_weight))]) / sum(saved_weight)}')
