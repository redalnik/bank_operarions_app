```
project_root/
├── data/                    
│   ├── operations.xlsx     # Excel файл с данными операций
│   └── user_settings.json  # Настройки пользователя
├── src/                    # Основной код программы
│   ├── __init__.py        
│   ├── main.py            # Запуск программы
│   ├── reports.py         # Создание отчетов
│   ├── services.py        # Сервисы
│   ├── utils.py           # Вспомогательные функции
│   └── views.py           # Основная логика отображения
├── tests/                  # Тестовый набор
│   ├── __init__.py
│   ├── test_reports.py
│   ├── test_services.py
│   ├── test_utils.py
│   └── test_views.py
├── env_template           # Шаблон переменных окружения
└── flake8                # Конфигурация Flake8
```