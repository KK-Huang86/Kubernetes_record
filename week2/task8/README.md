# 任務要求

嘗試使用 Helm Chart 安裝任一開源服務，例如：
https://artifacthub.io/packages/helm/bitnami/ghost

並且，使用 Nginx Ingress（https://github.com/kubernetes/ingress-nginx），作為 Ingress 將外部流量導向該開源服務。

該 ingress 需根據 hostname(網址) 作為規則，去轉發該流量（可使用 Host Header 去驗證請求）。

並且你可以創建 Loadbalancer Service 允許外部流量進入 Ingress，流量路徑如下（亦可參考下圖）：
Client -> loadbalancer(created by "loadbalancer service") -> ClusterIP of "loadbalancer service" -> Service of Ingress -> Pods of Ingress(Nginx) -> Ghost Service -> Ghost Pod

（進階題）嘗試使用 Gateway API 取代 Ingress，Gateway API 實作部分，可以參考https://gateway.envoyproxy.io/

![任務架構圖](imgs/task8-1.png)

# 實作與回答

## 實作步驟

1. 安裝 ghost ， 透過 helm chart

```bash
helm install my-release oci://registry-1.docker.io/bitnamicharts/ghost
```
