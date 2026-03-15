# 任務要求

使用 ConfigMap 掛載 Volume 的方式，將 Nginx 設定檔掛載進 Container 當中，如此一來，你不需要自己 Build image 便可以調整 Nginx 的設定。

請部署一個 Nginx deployment，Nginx 將請求轉發至你自己寫的 Web Service Pod（Deployment）。

另外，使用 Redis Image 部署一個 Redis StatefulSet(2 replicas)，並且掛載 PV 確保其狀態持久性。

您需要驗證你的 Web Service 能夠使用 Headless Service 連線到 Redis 上（例如 redis-0 pod），並存取資料。

你可以嘗試在 Cluster 內做 DNS 解析的測試，說明你要怎麼確保你可以存取第一個 Pod，以及 Headless 跟 ClusterIP 有何差別，請說明。

嘗試使用 Secret 定義 redis 使用者資料，讓 Web Service Pod 可以透過掛載 ENV 去取得連線資訊。

# 實作與回答

## 任務架構圖

```

外部流量
    │
    ▼
┌─────────────────────────────────┐
│  Nginx Deployment               │
│  (nginx pod)                    │◄── ConfigMap
│  nginx.conf 透過 Volume 掛載     │    (nginx.conf 內容)
└──────────────┬──────────────────┘
               │ proxy_pass to web-service
               ▼
┌─────────────────────────────────┐
│  Web Service Deployment         │
│  (app pod)                      │◄── Secret
│  ENV: REDIS_HOST, REDIS_PASS    │    (redis 帳號密碼)
└──────────────┬──────────────────┘
               │ 連線 redis-0.redis-headless
               ▼
┌─────────────────────────────────┐
│  Redis StatefulSet              │
│  ┌──────────┐  ┌──────────┐    │
│  │ redis-0  │  │ redis-1  │    │◄── Headless Service
│  │  PVC/PV  │  │  PVC/PV  │    │    (穩定 DNS 名稱)
│  └──────────┘  └──────────┘    │
└─────────────────────────────────┘
```

### 需要建立的相關檔案

Dockerfile + Web Server 程式碼 → build & push image
ConfigMap — 存 nginx.conf 內容
Deployment — web-server
Service — web-server-service（ClusterIP，給 Nginx proxy_pass 用）
Deployment — nginx（掛載 ConfigMap 為 Volume）
Service — nginx-service（對外暴露，可用 NodePort 或 LoadBalancer）
