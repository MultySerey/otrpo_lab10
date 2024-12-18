import psutil
import time
from prometheus_client import Gauge, start_http_server
from dotenv import dotenv_values

CONFIG = dotenv_values()

# Создание метрик
cpu_usage = Gauge(
    'system_cpu_usage',
    'Процент использования ядер процессора',
    ['core']
)
mem_info = Gauge(
    'system_memory',
    'Память: всего и используемая (ГБ)',
    ['type']
)

disk_info = Gauge(
    'system_disk',
    'Диски: общий объем и использованное пространство (ГБ)',
    ['disk', 'type']
)


def collect_system_metrics():
    # Сбор метрик по каждому ядру процессора
    for i, percent in enumerate(psutil.cpu_percent(percpu=True)):
        cpu_usage.labels(core=f'core_{i}').set(percent)

    mem = psutil.virtual_memory()
    mem_info.labels(type='total').set(mem.total / 1024 / 1024 / 1024)
    mem_info.labels(type='used').set(mem.used / 1024 / 1024 / 1024)

    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.labels(disk=partition.device, type='total').set(usage.total / 1024 / 1024 / 1024)
            disk_info.labels(disk=partition.device, type='used').set(usage.used / 1024 / 1024 / 1024)
        except PermissionError:
            # Игнорируем диски, к которым нет доступа
            continue


def main():
    # Чтение переменных окружения
    host = CONFIG["EXPORTER_HOST"]
    port = int(CONFIG["EXPORTER_PORT"])

    # Запуск HTTP-сервера
    start_http_server(port=port, addr=host)
    print(f"Экспортер запущен на {host}:{port}")

    # Сбор метрик
    while True:
        collect_system_metrics()
        time.sleep(1)


if __name__ == '__main__':
    main()
