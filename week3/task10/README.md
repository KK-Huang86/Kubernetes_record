# 任務要求

1. 嘗試在 K8s 部署 Gitlab，並測試將 local repo 推上去成功。
2. 嘗試部署 ArgoCD，在 Gitlab 中新增一個 Repo，用以存放你要部署的 Helm，將 Task6 的作業成品透過 Argocd 部署上去。並且嘗試 Argocd 上的相關部署設定。（如果是 Helm，可嘗試將 Chart 推到 harbor [https://github.com/goharbor/harbor] 上）
3. 嘗試手動使用 ArgoCD 部署第三方 Helm Chart 服務。
4. 嘗試將 2 & 3 創建出來的兩個 Applications，改成用 YAML（Custom Resource） 管理。
5. （進階題）承 4，近一步考慮 App of Apps [https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/#app-of-apps-pattern] 的方式進行管理。

# 實作回答

## 實作步驟
