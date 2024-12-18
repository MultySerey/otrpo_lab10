# Лабораторная работа 10 по ОТРПО
## Требования
- Python >= 3.12.0
## Использованные библиотеки
- psutil
- prometheus-client
## Использование
1. Создаём Virtual Env
```shell
python -m venv .venv
```
2. Активируем Virtual Env
```shell
.venv\Scripts\Activate
```
3. Устанавливаем необходимые библиотеки
```shell
pip install -r requirements.txt
```
4. Запускаем экспортер
```shell
python main.py
```
## Запросы
### Запрос для вывода загрузки всех ядре процессора
```promql
system_cpu_usage
```
### Запрос для вывода сколько всего памяти и сколько используется
```promql
system_memory
```
### Запрос для вывода объёмов дисков и сколько занято
```promql
system_disk
```