{
    'lineplot_esf':
        {
            'hint':
                {
                    'rus': 'Визуализация средневзвешенных цен продаж ЭСЧФ',
                },
            'blocks': 'Process',
            'gui_name':
                {
                    'rus': 'Визуализация средневзвешенных цен продаж ЭСЧФ',
                },
            'in_params':
                {
                    'dataset_dt':
                        {
                            'gui_name':
                                {
                                    'rus': 'Датасет ДТ со сзязанными ЭСЧФ',
                                },
                        },
                    'dataset_esf':
                        {
                            'gui_name':
                                {
                                    'rus': 'Датасет ЭСЧФ',
                                },
                        },
                    'dataset_check':
                        {
                            'gui_name':
                                {
                                    'rus': 'Датасет чеков со связанными ЭСЧФ',
                                },
                        },
                    'monthly':
                        {
                            'gui_name':
                                {
                                    'rus': 'Разбивка по месяцам'
                                },
                            'gui_type': 'checkbox',
                            'gui_default_values':
                                {
                                    'rus': False
                                },
                        },
                    'linear_regression':
                        {
                            'gui_name':
                                {
                                    'rus': 'Линейная регрессия'
                                },
                            'gui_type': 'checkbox',
                            'gui_default_values':
                                {
                                    'rus': False
                                },
                        },
                    'step_regression':
                        {
                            'gui_name':
                                {
                                    'rus': 'Шаг регрессии'
                                },
                            'gui_type': 'input',
                            'gui_default_values':
                                {
                                    'rus': 1
                                },
                            'gui_visible':
                                {
                                    'linear_regression':
                                        {
                                            1: True,
                                        },
                                },
                        },
                    'product_code':
                        {
                            'gui_name':
                                {
                                    'rus': 'Код товара',
                                },
                            'gui_type': 'input',
                            'gui_default_values':
                                {
                                    'rus': "803901000"
                                }
                        },
                    'start_date':
                        {
                            'gui_name':
                                {
                                    'rus': 'Период: от',
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
                                    'rus': 'Период: до',
                                },
                            'gui_type': 'input',
                            'gui_type_value': 'string',
                            'gui_default_values':
                                {
                                    'rus': '2023-12-31'
                                }
                        }
                }
        }
}
