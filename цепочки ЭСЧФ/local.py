import pandas as pd


def get_weighted_check(last_unp):
    weighted_price = {}
    for top in top_3:
        copy_check = checks.copy()
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


def get_next_unp(df, provider_unp):
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


def get_top_3(code, name):
    data_sorted = dt_esf.copy()
    data_sorted = data_sorted.loc[(data_sorted['roster_item_code'].astype(str) == code)
                                  & (data_sorted['roster_item_name'].astype(str) == name)].reset_index()
    data_sorted = data_sorted.groupby('provider_unp').agg({
        'roster_item_count': 'sum',
        'roster_item_cost': 'sum'
    }).reset_index()
    data_sorted.sort_values(by='roster_item_count', ascending=False)
    return data_sorted['provider_unp'].astype(str).head(3).tolist()


def get_dt_weighted(df, code, name, unp):
    df_local = df.copy()
    df_local['recipient_unp'] = df_local['recipient_unp'].astype(str)
    df_local['recipient_unp'] = df_local['recipient_unp'].apply(lambda x: x.rstrip('0').rstrip('.'))
    df_local = df_local.loc[(df_local['roster_item_code'].astype(str) == code)
                            & (df_local['roster_item_name'].astype(str) == name)
                            & (df_local['provider_unp'].astype(str) == unp)].reset_index()
    price = sum([i * j for i, j in zip(df_local['ТС/кг, бел руб'], df_local['g38netweightquantity'])]) \
            / sum(df_local['g38netweightquantity'])
    return price


def filter_data(tnved_code, goods_name, time_start, delta_time):
    global dt_esf, esf, checks
    time_start = pd.to_datetime(time_start)
    time_end = time_start + pd.DateOffset(days=delta_time)
    esf = esf[(esf['document_type'] == "ORIGINAL")]
    esf["general_date_transaction"] = pd.to_datetime(esf["general_date_transaction"])
    esf = esf[(esf["general_date_transaction"] >= time_start) & (
            esf["general_date_transaction"] <= time_end)
              & (esf["roster_item_code"].astype(str) == tnved_code)
              & (esf["roster_item_name"] == goods_name)
              ].reset_index()
    dt_esf['dt_date'] = pd.to_datetime(dt_esf['dt_date'])
    dt_esf = dt_esf[(dt_esf['g331goodstnvedcode'].astype(str) == tnved_code)
                    & (dt_esf['roster_item_name'] == goods_name)
                    & (dt_esf['dt_date'] >= time_start)
                    & (dt_esf['dt_date'] <= time_end)].reset_index()
    checks['issued_at'] = pd.to_datetime(checks['issued_at'])
    checks = checks[(checks['name'] == goods_name)
                    & (checks['tnved_code'].astype(str) == tnved_code)
                    & (checks['issued_at'] >= time_start)
                    & (checks['issued_at'] <= time_end)].reset_index()


def print_result(unp):
    if type(unp) == list:
        return unp
    else:

        return unp['recipient_unp'].tolist()


def erase_weight(df, max_weight):
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


if __name__ == '__main__':
    dt_esf = pd.read_csv('dt_esf_newdate.csv')
    esf = pd.read_csv('esf_all.csv')
    checks = pd.read_csv('checks_all.csv')
    cop = checks.copy()
    time_start = '2021-01-01'
    item_name = 'ЛИМОН 1КГ'
    tnv_code = '805501000'
    delta = 3000
    top_3 = get_top_3(tnv_code, item_name)
    for top in top_3:
        print(get_dt_weighted(dt_esf, tnv_code, item_name, top))
    print(top_3)
    filter_data(tnv_code, item_name, time_start, delta)

    chain_len = 4

    structure = {
        0: {'dt': top_3},
    }

    structure_price = {}
    weighted_points = {}

    for idx_chain in range(chain_len - 1):
        structure[idx_chain + 1] = dict()
        for company in structure[idx_chain]:
            if type(structure[idx_chain][company]) == list:
                for recipient in structure[idx_chain][company]:
                    next_chain = get_next_unp(dt_esf, recipient)
                    structure[idx_chain + 1][recipient] = next_chain
            else:
                for index, recipient in structure[idx_chain][company].iterrows():
                    next_chain = get_next_unp(esf, recipient['recipient_unp'])
                    next_chain = erase_weight(next_chain, recipient['roster_item_count'])
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
                    if chain == 1:
                        price = structure[chain][provider]['roster_item_cost'].sum() / structure[chain][provider][
                            'roster_item_count'].sum()
                    else:
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
                    check[provider.split("_")[0]].extend(print_result(structure[chain][provider]))
                    # print(f'Цепочка: {provider} Поставщик: {provider.split("_")[-1]}, Получатели ({len(structure[chain][provider])}): {print_result(structure[chain][provider])}, Цена: {price:.3f}')
                else:
                    pass
                    # print(f'Цепочка: {provider} Поставщик: {provider.split("_")[-1]}, Получатели: {print_result(structure[chain][provider])}')

                count += 1

        # print(f'{count} / {len(structure[chain])}')

    print(weighted_points)
    weighted_checks = get_weighted_check(check)
    print(weighted_checks)
