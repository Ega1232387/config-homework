## 1. Общее описание
Данная программа представляет собой инструмент командной строки для визуализации графа зависимостей Alpine Package Keeper (APK) в формате Mermaid.

## 2. Описание всех функций и настроек
1. `read_config` - считывает данные из конфигурационного файла
2. `download_data` - загрузка APKINDEX
3. `parse_packages` - парсинг загруженных данных
4. `build_dependency_graph` - построение графа зависимостей
5. `generate_mermaid_graph` - генерация Mermaid-графа

## 3. Описание команд для сборки проекта
1. Загрузить необходимые зависимости:
```bash
pip install lxml
```
2. Запустить необходимый файл:
```bash
python visualizer.py
```

## 4. Примеры использования
![alt text](https://i.imgur.com/bljZc4N.png)

## 5. Результаты прогона тестов
1. `test_read_config` - успешно прочитана конфигурация
2. `test_download_data` - успешно загружены данные
3. `build_dependency_graph` - успешно построен граф зависимостей