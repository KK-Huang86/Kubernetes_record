# 任務要求

1. 嘗試在 K8s 部署 Gitlab，並測試將 local repo 推上去成功。
2. 嘗試部署 ArgoCD，在 Gitlab 中新增一個 Repo，用以存放你要部署的 Helm，將 Task6 的作業成品透過 Argocd 部署上去。並且嘗試 Argocd 上的相關部署設定。（如果是 Helm，可嘗試將 Chart 推到 harbor [https://github.com/goharbor/harbor] 上）
3. 嘗試手動使用 ArgoCD 部署第三方 Helm Chart 服務。
4. 嘗試將 2 & 3 創建出來的兩個 Applications，改成用 YAML（Custom Resource） 管理。
5. （進階題）承 4，近一步考慮 App of Apps [https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/#app-of-apps-pattern] 的方式進行管理。

# 實作回答

## 實作步驟
1. 創建 Namespace(可做可不做)
```bash
kubectl create namespace gitlab
kubectl create namespace argocd
kubectl create namespace task10
```

2. 需要先在 本機 minikube 安裝 ```Gitlab```，為的是後續 ArgoCD 追蹤的標的

```bash
helm repo add gitlab https://charts.gitlab.io/
```

```bash
helm repo update
```

```bash
helm install gitlab gitlab/gitlab \
  -n gitlab \
  --set global.hosts.domain=127.0.0.1.nip.io \
  --set global.edition=ce \
  --set certmanager-issuer.install=false \
  --set global.ingress.configureCertmanager=false \
  --set gitlab-runner.install=false \
  --set prometheus.install=false \
  --set global.ingress.class=nginx
```

不確定 helm 的 values要填入哪些時，可以先下該指令進行查詢
```bash
helm show values gitlab/gitlab > gitlab-values.yaml
```

注意：在 macOS Docker driver 下，`minikube ip`（e.g. `192.168.49.2`）從 host 無法直接連到，因此 domain 必須使用 `127.0.0.1.nip.io`，讓 DNS 解析到 `127.0.0.1`。

3. 查看 ```Gitlab```的 pod 以及 ingress 設置

確保 ```Gitlab```的 pod 都跑完並且執行中
```bash
kubectl get pods -n gitlab
```

查看 ingress 設置
```bash
kubectl get ingress -n gitlab
```

GitLab Helm Chart 自帶一個 nginx-ingress-controller，其 Service 類型為 LoadBalancer
查看 ingress ADDRESS 是否有值：
![address 有值的](imgs/)



4. 使用 ```kubectl port-forward``` 進行轉發

在 macOS Docker driver 上，有兩種方式可以連到 GitLab：

| 方式 | 說明 |
|------|------|
| `minikube tunnel` | 讓 LoadBalancer Service 拿到外部 IP，走完整的 LoadBalancer → Ingress 路徑，但 macOS 上 port 80/443 需要 root 權限，實際上無法直接連線 |
| `kubectl port-forward` | 直接將 Mac 本機 port 接到 K8s Service，繞過 LoadBalancer，是 macOS 上最簡單直接的解法 |

因此採用 `kubectl port-forward`，**不需要另外開** `minikube tunnel`。

GitLab 預設會將所有 HTTP 請求強制 redirect 到 HTTPS（308），因此要 port-forward HTTPS 的 port：
```bash
kubectl port-forward svc/gitlab-nginx-ingress-controller 8443:443 -n gitlab
```

打開瀏覽器輸入 ```https://gitlab.127.0.0.1.nip.io:8443```

會出現自簽憑證警告，點「進階」→「繼續前往」即可。
![Gitlab登入畫面]()





-----

遇到問題

在安裝 Gitlab 時，有一個 pod一直裝不起來

查看原因

```bash
kubectl describe pod gitlab-webservice-default-758f497bcf-6t7jv -n gitlab
```

一開始給的 ```minikube```的資源太少