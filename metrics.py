from prometheus_client import Counter, Gauge, Histogram
import psutil

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests"
)

ERROR_COUNT = Counter(
    "http_errors_total",
    "Total HTTP Errors"
)

RESPONSE_TIME = Histogram(
    "response_time_seconds",
    "Response Time"
)

CPU_USAGE = Gauge(
    "cpu_usage_percent",
    "CPU Usage Percent"
)

MEMORY_USAGE = Gauge(
    "memory_usage_percent",
    "Memory Usage Percent"
)


def update_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)