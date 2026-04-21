import time
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

PUSHGATEWAY_URL = "http://pushgateway:9091"
JOB_NAME = "cronjob_metrics"

def main():
    start = time.time()
    print("CronJob started")

    # 模擬工作（等待 3 秒）
    time.sleep(3)

    duration = time.time() - start
    print(f"CronJob finished, duration: {duration:.2f}s")

    # Push metrics 到 Pushgateway
    registry = CollectorRegistry()
    g = Gauge('cronjob_duration_seconds', 'CronJob execution duration', registry=registry)
    g.set(duration)

    push_to_gateway(PUSHGATEWAY_URL, job=JOB_NAME, registry=registry)
    print("Metrics pushed to Pushgateway")

if __name__ == '__main__':
    main()
