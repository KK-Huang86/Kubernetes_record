# Kubernetes 學習記錄

記錄學習 Kubernetes 的實作練習，包含 Docker、kubectl、k9s 等工具的操作。

## 目錄結構

### Week 1

| 任務                 | 主題                           | 說明                                                                                     |
| -------------------- | ------------------------------ | ---------------------------------------------------------------------------------------- |
| [task0](week1/task0) | Dockerfile 優化 & 多架構 build | Dockerfile 最佳化方向、使用 buildx 編譯 x86/ARM 多架構 image                             |
| [task1](week1/task1) | Kubernetes 基礎操作            | Deployment/Service 建立、kubectl 常用指令、Rolling Update、Rollback、Nginx Reverse Proxy |
| [task2](week1/task2) | K9s 操作                       | 使用 K9s 查看 namespace、pod logs、exec shell、編輯 deployment、xray 資源關係圖          |
| [task3](week1/task3) | Probe 探針                     | Liveness/Readiness/Startup Probe 原理，使用 Probe 停止 Pod 流量而不刪除 Pod              |
| [task4](week1/task4) | ServiceAccount & K8s API       | 使用 SA + Projected Volume 掛載 token，透過程式呼叫 K8s API 取得 Pod 列表                |
| [task5](week1/task5) | IaC 雲端 K8s Cluster           | Terraform + Linode LKE 建立 Cluster，LoadBalancer Service 對應 Linode NodeBalancer       |

### Week 2

| 任務                 | 主題                              | 說明                                                                                          |
| -------------------- | --------------------------------- | --------------------------------------------------------------------------------------------- |
| [task6](week2/task6) | ConfigMap / StatefulSet / Secret  | Nginx ConfigMap 掛載設定、Redis StatefulSet + PV、Headless Service DNS 解析、Secret 注入 ENV  |
| [task7](week2/task7) | 自製 Helm Chart & 推送至 Registry | 建立 Helm Chart（Nginx Deployment + values.yaml），推送至 hosted registry 並 install          |
| [task8](week2/task8) | Nginx Ingress & Grafana           | Helm 安裝 Grafana、ingress-nginx Controller、Ingress hostname 路由、LoadBalancer 對外流量路徑 |
| [task9](week2/task9) | 集中式日誌收集（Loki + Grafana）  | Helm 安裝 Loki + Grafana、Nginx log 寫入 HostPath、Promtail DaemonSet 收集 log 推送至 Loki   |

### Week 3

| 任務                   | 主題                        | 說明                                                                                                          |
| ---------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------- |
| [task10](week3/task10) | GitOps with ArgoCD & GitLab | 部署 GitLab + Harbor + ArgoCD、Helm Chart 推上 Harbor、ArgoCD 追蹤 GitLab repo 自動部署、Application CRD 管理 |

### Week 4

| 任務                   | 主題                        | 說明                                                                                                          |
| ---------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------- |
| [task15](week4/task15) | Prometheus & Grafana 監控   | kube-prometheus-stack 安裝、Custom Metrics、CronJob + Pushgateway、PrometheusRule CPU alert、AlertmanagerConfig 通知 Discord |
| [task17](week4/task17) | HPA 水平自動擴縮容          | 啟用 metrics-server、建立 HPA 規則、模擬 CPU 負載觀察 Pod 自動擴容與縮容行為                                  |

## 環境

- Kubernetes: minikube / Linode LKE
- 容器工具: Docker / buildx
- 管理工具: kubectl、k9s、Helm
- 監控工具: Prometheus、Grafana、Alertmanager（kube-prometheus-stack）
- IaC: Terraform
