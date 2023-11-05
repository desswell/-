{
    'monthly_prices_visualise':
        {
            'hint':
                {
                    'rus': 'Аналитика по прослеживаемым товарам',
                },
            'blocks': 'Process',
            'gui_name':
                {
                    'rus': 'Аналитика по прослеживаемым товарам',
                },
            'in_params':
                {
                    'dataset':
                        {
                            'gui_name':
                                {
                                    'rus': 'Датасет',
                                },
                        },
                    'input_code':
                        {
                            'gui_name':
                                {
                                    'rus': 'Категория',
                                },
                            'gui_type': 'input',
                            'gui_default_values': 
                                {
                                    'rus': "8418102001"
                                }
                        },
                    'chain_flag':
                        {
                            'gui_name':
                                {
                                    'rus': 'Построение цепочек'
                                },
                            'gui_type': 'checkbox',
                            'gui_default_values':
                                {
                                    'rus': False
                                },
                        },
                    'size_chain':
                        {
                            'gui_name':
                                {
                                    'rus': 'Размерность цепочки',
                                },
                            'gui_type': 'input',
                            'gui_type_value': 'number',
                            'gui_default_values':
                                {
                                    'rus': 2
                                },
                            'gui_visible':
                                {
                                    'chain_flag':
                                        {
                                            1: True,
                                        },
                                },
                        },
                    'date_dt':
                        {
                            'gui_name':
                                {
                                    'rus': 'Дата ДТ (YYYY-MM-DD)',
                                },
                            'gui_type': 'input',
                            'gui_type_value': 'string',
                            'gui_default_values':
                                {
                                    'rus': '2022-08-01'
                                }
                        },
                    'date_check':
                        {
                            'gui_name':
                                {
                                    'rus': 'Дата чека (YYYY-MM-DD)',
                                },
                            'gui_type': 'input',
                            'gui_type_value': 'string',
                            'gui_default_values':
                                {
                                    'rus': '2022-11-12'
                                }
                        },
                    'all_interval':
                        {
                            'gui_name':
                                {
                                    'rus': 'Все цепочки из интервала',
                                },
                            'gui_type': 'checkbox',
                            'gui_default_values':
                                {
                                    'rus': False
                                }
                        },
                    'include_company':
                        {
                            'gui_name':
                                {
                                    'rus': 'Цепочки по определенной компании',
                                },
                            'gui_type': 'checkbox',
                            'gui_default_values':
                                {
                                    'rus': False
                                }
                        },
                    'company_unp':
                        {
                            'gui_name':
                                {
                                    'rus': 'УНП компании',
                                },
                            'gui_type': 'input',
                            'gui_type_value': 'string',
                            'gui_default_values':
                                {
                                    'rus': '700474487'
                                }
                        }
                }
        }
}
