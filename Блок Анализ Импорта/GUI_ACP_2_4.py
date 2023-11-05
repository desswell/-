{
    'diagram_visualise_acp':
        {
            'hint':
                {
                    'rus': 'Анализ импорта',
                },
            'blocks': 'Process',
            'gui_name':
                {
                    'rus': 'Анализ импорта',
                },
            'in_params':
                {
                    'dataset_import':
                        {
                            'gui_name':
                                {
                                    'rus': 'Датасет импорта',
                                },
                        },
                    'dataset_dt':
                        {
                            'gui_name':
                                {
                                    'rus': 'Датасет деклараций',
                                },
                        },
                    'input_code':
                        {
                            'hint':
                                {
                                    'rus': 'Вводить код ТНВЭД, либо наименование товара в единственном числе, если это '
                                           'дистрибутивное слово (т.е например, банан (ед. ч.) — бананы (мн. ч.),'
                                           'либо до расхождениях в собирательных словах (например, огурец (ед. ч.) — '
                                           'огурцы (мн. ч.)) в буквах в ед. и мн. числах (например, огур)'
                                },
                            'gui_name':
                                {
                                    'rus': 'Товар',
                                },
                            'gui_type': 'input',
                            'gui_default_values': 
                                {
                                    'rus': "803901000"
                                },
                        },
                    'threshold_value':
                        {
                            'gui_name':
                                {
                                    'rus': 'Пороговое значение в %',
                                },
                            'gui_type': 'input',
                            'gui_default_values':
                                {
                                    'rus': 2
                                },
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
                },
        },
}
