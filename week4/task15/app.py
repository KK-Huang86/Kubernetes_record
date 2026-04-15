from prometheus_client import start_http_server, Counter
import time

REQUEST_COUNT = Counter('my_app_requests_total', 'Total requests', ['method'])

if __name__ == '__main__':
    start_http_server(8080)
    print("Metrics server started on :8080")

    while True:
        REQUEST_COUNT.labels(method='GET').inc()
        time.sleep(10)
