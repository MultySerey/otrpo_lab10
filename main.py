import psutil
import time
from prometheus_client import (
    CollectorRegistry,
    Gauge,
    push_to_gateway
)

registry = CollectorRegistry()

cpu_usage = Gauge(
    'system_cpu_usage',
    'Процент использования ЦПУ',
    registry=registry
)
mem_total = Gauge(
    'system_mem_total',
    'Общее количество оперативной памяти',
    registry=registry
)
mem_used = Gauge(
    'system_mem_used',
    'Используемое количество оперативной памяти',
    registry=registry
)
disk_total = Gauge(
    'system_disk_total',
    'Объем диска',
    registry=registry
)
disk_used = Gauge(
    'system_disk_used',
    'Используемый объем диска',
    registry=registry
)


def collect_system_metrics():
    cpu_usage.set(psutil.cpu_percent())

    mem = psutil.virtual_memory()
    mem_total.set(mem.total / 1024 / 1024 / 1024)
    mem_used.set(mem.used / 1024 / 1024 / 1024)

    disk = psutil.disk_usage('/')
    disk_total.set(disk.total / 1024 / 1024 / 1024)
    disk_used.set(disk.used / 1024 / 1024 / 1024)


def main():
    pushgateway_url = "localhost:9090"  # URL сервера PushGateway
    job_name = "system_metrics"  # Имя задачи

    while True:
        collect_system_metrics()  # Сбор метрик каждую секунду
        push_to_gateway(pushgateway_url, job=job_name, registry=registry)
        time.sleep(1)


if __name__ == '__main__':
    main()
