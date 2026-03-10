# 任務要求

## 實作題

1.  撰寫一個名為 deployment.yaml 的檔案，並用 kubectl 在本地 cluster 創建以下服務。
    類型： Deployment
    名稱： web-server
    副本數 (Replicas)： 3
    標籤 (Labels)： app: nginx
    映像檔： nginx:1.14.2
    容器埠號： 80

![三個pod](imgs/task1-1.png)

2.  使用 kubectl get pods -o wide 獲得這 3 個 Pod 的 IP 地址。

![三個pod的IP](imgs/task1-2.png)

3.  嘗試用 jsonpath 抓出所有 Label 為 app: nginx 的 pod name，並用逗點分隔。

![抓到符合條件的pod](imgs/task1-3.png)

4.  使用 kubectl exec 進入其中一個 Pod，使用指令驗證網路互通。

進入某一個 Pod 後，打同一個 cluster 的其他 Pod IP，使用 bash 內建的 `/dev/tcp` 發送 HTTP 請求：

```bash
exec 3<>/dev/tcp/<ip>/80; echo -e "GET / HTTP/1.0\r\nHost: <ip>\r\n\r\n" >&3; cat <&3
```

nginx:1.14.2 預設不包含 curl 或 wget，因此使用 bash 內建的 tcp 連線方式驗證。

![進入其中一個pod，使用指令驗證網路互通](imgs/task1-11.png)

5.  手動刪除其中一個 Pod (kubectl delete pod <pod-name>)，觀察 Deployment 如何自動建立新 Pod。

Deployment 底層由 ReplicaSet 管理副本數量。當手動刪除一個 Pod 後，ReplicaSet 偵測到實際 Pod 數量低於期望值（3），會自動建立一個新的 Pod 補足，確保副本數維持在設定值。

這與 Rolling Update 不同：Rolling Update 是更新 Pod spec 時的替換策略，而此處是 ReplicaSet 的自動修復機制。

![deployment自動補充pod](imgs/task1-9.png)

6.  嘗試創建 service.yaml，套用並建立 service 負責該 pods 的服務轉發，使用 NodePort type 的 Service，創建完成後，嘗試另外創建 pod 去 curl ClusterIp 來驗證該 Service 有正確轉發流量以及觀察 Nginx Pods 上的 logs。

建立 Service 並設定為 NodePort，使用以下指令臨時建立一個 curl pod 打 Service 的 ClusterIP：

```bash
kubectl run curl-test --image=curlimages/curl -it --rm -n task1 -- curl <service-ip>
```

再以以下指令查看 Nginx Pods 上的 access log，確認有流量進來：

```bash
kubectl logs -l app=nginx -n task1
```

![pods之間打service](imgs/task1-19.png)

7.  嘗試分別使用 NodePort 及 port forward 的方式，嘗試在本機網路去 curl 該 Service，並且說明兩者的差異以及如果我們希望做到 Service 分流的效果，我們該用兩者之中哪個方法？

**NodePort 方式：**

透過 minikube 建立 tunnel，把本機 port 對應到 minikube Node 的 NodePort：

```bash
minikube service <service-name> -n task1 --url
curl http://127.0.0.1:xxxxx
```

![透過minikube 從本機curl](imgs/task1-13.png)

**Port Forward 方式：**

```bash
kubectl port-forward svc/web-server-service 8080:80 -n task1
curl http://localhost:8080
```

**兩者差異：**

| | NodePort | Port Forward |
|---|---|---|
| 流量路徑 | 本機 → Node → Service → Pod | 本機 → kubectl 程序 → Pod |
| 經過 Service | 有 | 無（直接到單一 Pod） |
| Load balancing | 有 | 無 |
| 用途 | 正式對外暴露 | 本機 debug |

如果希望做到 Service 分流 → 使用 **NodePort**。Port Forward 繞過了 Service 的 load balancing，流量只會到固定的一個 Pod，無法分流。

8.  嘗試使用 kubectl edit 更新 deployment 後，觀察 pod 的變化，並嘗試使用 rollback 退版及查看版本變化。

使用 `kubectl edit` 修改 Deployment 的 nginx image 版本，觸發 Rolling Update，產生新的 revision：

![產生新的版本](imgs/task1-16.png)

退回指定版本：

```bash
kubectl rollout undo deployment/<appname> -n task1 --to-revision=1
```

![產生新版本](imgs/task1-18.png)

Rollback 後，原本的 revision 1 會消失，產生新的 revision 3，因為 rollback 本身也是一次變更紀錄。

9.  嘗試自己 build 一個新的 nginx image，用它創建一個新的 deployment "web-server-new"，以及與之對應的 service，嘗試在 dockerfile 中，加入 nginx 設定檔的設定，讓其可以將流量轉發至 web-server。
    並且提供您如何驗證是否有成功的做法。

**流量順序：**
```
client -> web-server-service-new -> web-server-new -> web-server-service -> web-server
```

`web-server-new` 作為中間代理人（reverse proxy），自身不提供內容，只負責將流量轉發至原有的 `web-server-service`。

**實作步驟：**

1. 新增 `nginx.conf`，透過 `proxy_pass` 將流量導向 `web-server-service`
2. 新增 `Dockerfile`，將 `nginx.conf` 覆蓋進 nginx image
3. 使用 minikube 的 docker 環境 build image，確保 cluster 可以使用：
```bash
eval $(minikube docker-env)
docker build -t my-nginx-proxy:v1 .
```
4. 建立 `deployment-new.yml` 及 `service-new.yml` 並套用

**驗證方式：**

從 cluster 內打 `web-server-service-new`，觀察流量是否經過兩層：

```bash
kubectl run curl-test --image=curlimages/curl -it --rm -n task1 -- curl web-server-service-new.task1.svc.cluster.local
```

同時觀察原本 `web-server` 的 log 有沒有收到請求：

```bash
kubectl logs -l app=nginx -n task1
```

若原本的 `web-server` pods 有新增 access log，代表流量確實經過兩層轉發，驗證成功。

![多一筆紀錄](imgs/task1-20.png)
