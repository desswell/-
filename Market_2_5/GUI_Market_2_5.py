{
    'market_acp':
        {
            'hint':
                {
                    'rus': 'Показ объёма рынка на ДТ и на чеки',
                },
            'blocks': 'Process',
            'gui_name':
                {
                    'rus': 'Показ объёма рынка на ДТ и на чеки',
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
                                    'rus': 'Код товара',
                                },
                            'gui_type': 'input',
                            'gui_default_values':
                                {
                                    'rus': ''
                                },
                        },
                    'company':
                        {
                            'gui_name':
                                {
                                    'rus': 'УНП-код компании',
                                },
                            'gui_type': 'input',
                            'gui_default_values':
                                {
                                    'rus': ''
                                },
                        },
                    'time_start':
                        {
                            'gui_name':
                                {
                                    'rus': 'Дата начала (YYYY-MM-DD)',
                                },
                            'gui_type': 'input',
                            'gui_default_values':
                                {
                                    'rus': ''
                                },
                        },
                    'time_end':
                        {
                            'gui_name':
                                {
                                    'rus': 'Дата окончания (YYYY-MM-DD)',
                                },
                            'gui_type': 'input',
                            'gui_default_values':
                                {
                                    'rus': ''
                                },
                        },
                    'selected_plot':
                        {
                            'gui_name':
                                {
                                    'rus': 'Требуемая выборка',
                                },
                            'gui_type': 'select',
                            'gui_select_values':
                                {
                                    'rus': ['График по ДТ', 'График по Чекам'
                                            ]
                                },
                            'ds_values':
                                {
                                    'rus': ['1', '2'
                                            ]
                                },
                        }
                },
        },
}