{
    'market_esf':
        {
            'hint':
                {
                    'rus': 'Рынок',
                },
            'blocks': 'Process',
            'gui_name':
                {
                    'rus': 'Рынок',
                },
            'in_params':
                {
                    'dataset_dt':
                        {
                            'gui_name':
                                {
                                    'rus': 'Датасет ДТ',
                                },
                        },
                    'dataset_esf':
                        {
                            'gui_name':
                                {
                                    'rus': 'Датасет всех ЭСЧФ',
                                },
                        },
                    'dataset_last_esf':
                        {
                            'gui_name':
                                {
                                    'rus': 'Датасет последних ЭСЧФ',
                                },
                        },
                    'dataset_check':
                        {
                            'gui_name':
                                {
                                    'rus': 'Датасет чеков',
                                },
                        },
                    'product_code':
                        {
                            'gui_name':
                                {
                                    'rus': 'Код товара',
                                },
                            'gui_type': 'select',
                            'gui_select_values':
                                {
                                    'rus': ['0702000001', '0702000002', '0702000003', '0702000004', '0702000005', '0702000006', '0702000007', '0702000009', '0803901000', '080390100', '08039010', '0803901', '080390', '08039', '0803', '0805501000', '080550100', '08055010', '0805501', '080550', '08055', '0805']
                                },
                            'ds_values':
                                {
                                    'rus': ['702000001', '702000002', '702000003', '702000004', '702000005', '702000006', '702000007', '702000009', '803901000', '80390100', '8039010', '803901', '80390', '8039', '803', '805501000', '80550100', '8055010', '805501', '80550', '8055', '805']
                                },
                            'gui_default_values':
                                {
                                    'rus': '803901000'
                                }
                        },
                    'start_date':
                        {
                            'gui_name':
                                {
                                    'rus': 'Дата начала (YYYY-MM-DD)',
                                },
                            'gui_type': 'input',
                            'gui_type_value': 'string',
                            'gui_default_values':
                                {
                                    'rus': '2021-01-01'
                                }
                        },
                    'end_date':
                        {
                            'gui_name':
                                {
                                    'rus': 'Дата конца (YYYY-MM-DD)',
                                },
                            'gui_type': 'input',
                            'gui_type_value': 'string',
                            'gui_default_values':
                                {
                                    'rus': '2023-12-31'
                                }
                        },
                    'daily_data':
                        {
                            'gui_name':
                                {
                                    'rus': 'Данные по дням',
                                },
                            'gui_type': 'checkbox',
                            'gui_default_values':
                                {
                                    'rus': False
                                }
                        },
                    'build_chain':
                        {
                            'gui_name':
                                {
                                    'rus': 'Построение цепочек ЭСЧФ',
                                },
                            'gui_type': 'checkbox',
                            'gui_default_values':
                                {
                                    'rus': False
                                }
                        },
                    'start_date_to_chain':
                        {
                            'gui_name':
                                {
                                    'rus': 'Дата начала для цепочек ЭСЧФ (YYYY-MM-DD)',
                                },
                            'gui_type': 'input',
                            'gui_type_value': 'string',
                            'gui_default_values':
                                {
                                    'rus': '2021-01-01'
                                },
                            'gui_visible':
                                {
                                    'build_chain':
                                        {
                                            1: True,
                                        },
                                },
                        },
                    'interval':
                        {
                            'gui_name':
                                {
                                    'rus': 'Интервал в днях',
                                },
                            'gui_type': 'input',
                            'gui_type_value': 'int',
                            'gui_default_values':
                                {
                                    'rus': 30
                                },
                            'gui_visible':
                                {
                                    'build_chain':
                                        {
                                            1: True,
                                        },
                                },
                        },
                    'tracing_goods':
                        {
                            'gui_name':
                                {
                                    'rus': 'Наименование товара для цепочек',
                                },
                            'gui_type': 'input',
                            'gui_type_value': 'str',
                            'gui_default_values':
                                {
                                    'rus': 'БАНАН 1КГ'
                                },
                            'gui_visible':
                                {
                                    'build_chain':
                                        {
                                            1: True,
                                        },
                                },
                        },
                }
        }
}
