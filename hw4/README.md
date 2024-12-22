## 1. Общее описание
Данная программа представляет собой ассемблер и интерпретатор для учебной виртуальной машины (УВМ).

## 2. Описание всех функций и настроек
УВМ поддерживает 4 команды:
1. `LOAD` - загружает предоставленный операнда (19 бит) в регистр-аккумулятор
2. `READ` - читает данные по адресу-сумме регистра-аккумулятора  и операнда (15 бит) в регистр-аккумулятор
3. `WRITE` - записывает данные из регистра-аккумулятора по адресу-операнду (24 бита)
4. `REV` - переворачивает бит-регистр-аккумулятор по адресу-операнду (24 бита)

## 3. Описание команд для сборки проекта
1. Запустить необходимый файл:
```bash
python assebler.py -i программа -o итоговый байт-код -l лог
```
```bash
python assebler.py -i программа -r результат-лог --range диапазон записываемых в лог адресов
```

## 4. Примеры использования
![alt text](https://i.imgur.com/475hg7c.png)
![alt text](https://i.imgur.com/07qG54S.png)

## 5. Результаты прогона тестов
1. `test_XXX_command` - тесты каждой команды
2. `test_invalid_command` - тест неверного выполнения команды
3. `test_invalid_operands_count` - тест неверного кол-ва операндов
4. `main_test` - тестовое задание