# 任務要求

1. 使用 [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/README.md) Helm Chart，在 K8s 中安裝 Prometheus 與 Grafana。
2. 使用 Prometheus SDK（任何語言），在自己的 image 中加入 `/metrics` endpoint，並暴露任何一個 custom metrics。
3. 在 Grafana 與 Prometheus 後台分別查看 Custom Metrics。
4. 創建 K8s CronJob 運行自己 Build 的 image，說明非常駐行程情況下 Prometheus 如何獲取 metrics（例如執行 duration）。
5. 創建 Alert，在 Container CPU 達 80% 時發送訊息至 Discord。
6. 總結以上，使用 Prometheus Operator（CRD）完成所有設定。

# 實作回答

## 實作步驟

### 1. 安裝 kube-prometheus-stack

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack -n task15 --create-namespace
```

---

### 2. 建立 custom metrics app 並打包成 Docker image

`app.py` 透過 Prometheus Python SDK `prometheus_client`，定義 custom metrics 並自動產生 `/metrics` endpoint 供 Prometheus pull

```
啟動
  └─ start_http_server(8080)  ← 在背景等待 Prometheus 來抓
  └─ while True
       ├─ REQUEST_COUNT +1    ← 模擬請求發生
       └─ sleep 10s           ← 避免 CPU 空轉
```

```bash
docker build -t vup4k0806/my-metrics-app:v1 .
docker push vup4k0806/my-metrics-app:v1
```

---

### 3. 部署至 K8s 並建立 ServiceMonitor

部署 Deployment 與 Service：

```bash
kubectl apply -f monitor/deployment.yaml
```

建立 ServiceMonitor（CRD），讓 Prometheus Operator 自動將此服務加入 scrape target：

```bash
kubectl apply -f monitor/service-monitor.yaml
```

**Prometheus Operator 運作流程：**

```
建立 ServiceMonitor
       ↓
Operator 偵測到，翻譯成 Prometheus scrape 設定
       ↓
Prometheus 多了一個 scrape target（my-metrics-app）
       ↓
Prometheus 定期 GET Pod:8080/metrics
```

> 注意：ServiceMonitor 的 `spec.selector` 對應 Service 的 `metadata.labels`，而非 `spec.selector`。兩者用途不同，前者是給外部（ServiceMonitor）找 Service 用，後者是 Service 用來選 Pod 用

---

### 4. 在 Prometheus 查看 Custom Metrics

```bash
kubectl port-forward -n task15 svc/kube-prometheus-stack-prometheus 9090:9090
```

打開 `http://localhost:9090`，在 **Status → Targets** 可以看到 `my-metrics-app` 狀態為 UP。

![Prometheus Targets](imgs/task15-1.png)

在搜尋欄輸入 PromQL 查詢 custom metric：

```
my_app_requests_total
```

`my_app_requests_total` 是在 `app.py` 定義的 Counter，代表模擬的 GET 請求累計次數。

![Custom Metrics 查詢結果](imgs/task15-2.png)

---

### 5. 在 Grafana 查看 Custom Metrics

```bash
kubectl port-forward -n task15 svc/kube-prometheus-stack-grafana 3000:80
```

打開 `http://localhost:3000`

- 帳號：`admin`
- 密碼：透過以下指令取得

```bash
kubectl get secret -n task15 kube-prometheus-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

進入後：**Explore → 右上角切換為 Code 模式 → 輸入 PromQL**

```
my_app_requests_total
```

![explore my_app_requests_total的數據](imgs/task15-3.png)

也可以建立 Dashboard查詢
![my_app_requests_total 的 Dashboard](imgs/task15-4.png)


Grafana 本身不儲存資料，它透過 PromQL（打 API） 向 Prometheus（的資料庫） 查詢後畫成圖表，`kube-prometheus-stack` 安裝時已自動設定好 Prometheus 作為 Data Source，不需要手動設定。

--------

### 6. 設計一個 CronJob（定時任務），使用 Pushgateway 讓 Prometheus 定時來抓取資料

設定一個非常駐任務 `/cronjob/app.py`，靠該任務執行時推到 Pushgateway。
Pushgateway 為一個中間站，app 推進去，Prometheus 再定期 GET。

```
CronJob 執行
    │
    │  HTTP POST /metrics/job/cronjob_metrics
    ▼
Pushgateway（如同一般 Deployment，只是用官方 image）
    │  資料存在這裡，即使 CronJob Pod 消失也還在
    │
    │  Prometheus 定期 GET :9091/metrics
    ▼
Prometheus
    │
    │  PromQL 查詢
    ▼
Grafana
```

並建立 `ServiceMonitor` 指向 `pushgateway` 的 Pod ，讓 Prometheus 定時去抓資料

同時，另外將 `cronjob` 部署至 K8s，性質為 `CronJob`，設定時間定期執行

執行
```bash
kubectl get pod -n task15
kubectl get cronjob -n task15
```

查看 pushgateway 和 cronjob 是否都成功部署

![查看 pushgateway 和 cronjob 是否都成功部署](imgs/task15-5.png)


### 7. 分別在 Prometheus 和 Grafana 查看

在 `cronjob`設定的 metric為`cronjob_duration_seconds`

查看 Prometheus
![查看 Prometheus 關於 cronjob的 metric](imgs/task15-6.png)

查看 Grafana
![查看 Grafana 關於 cronjob的 metric](imgs/task15-7.png)