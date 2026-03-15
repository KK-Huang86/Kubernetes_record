# 任務要求

使用 IaC 工具在雲端建立 K8s Cluster，將步驟留存成可重複使用及 cleanup 的形式。
建立 Task1 的資源，但將 Service 改成 LoadBalancer，驗證雲端 Load Balancer 是否成功建立，並透過它存取 Nginx 頁面。

# 實作與回答

使用 **Terraform + Linode LKE** 建立 Cluster。
Linode 在建立 LoadBalancer type 的 Service 時會自動對應到 Linode NodeBalancer，驗證直觀。

## 檔案說明

```
task5/
├── main.tf                    ← Linode provider + LKE cluster 資源
├── variables.tf               ← 所有變數定義
├── outputs.tf                 ← 輸出 cluster id 和 kubeconfig
├── terraform.tfvars.example   ← 設定範本（複製後填入真實值）
└── k8s/
    ├── deployment.yml         ← nginx deployment（沿用 task1）
    └── service.yml            ← LoadBalancer service
```

## 前置需求

- [Terraform](https://developer.hashicorp.com/terraform/install) 已安裝
- Linode 帳號 + API token（Personal Access Tokens → Read/Write）

## 流程

### 1. 準備設定檔

```bash
cp terraform.tfvars.example terraform.tfvars
# 編輯 terraform.tfvars，填入真實的 linode_token
```

### 2. 建立 Cluster

```bash
terraform init
terraform plan
terraform apply
```

apply 完成後大約等 3-5 分鐘讓 cluster 就緒。

### 3. 取得 kubeconfig

```bash
terraform output -raw kubeconfig > kubeconfig.yaml
export KUBECONFIG=$(pwd)/kubeconfig.yaml
kubectl get nodes
```

![cluster nodes ready](imgs/task5-1.png)

### 4. 部署 K8s 資源

```bash
kubectl apply -f k8s/deployment.yml
kubectl apply -f k8s/service.yml
```

### 5. 確認 LoadBalancer 建立

```bash
kubectl get svc -n task1
```

`EXTERNAL-IP` 欄位從 `<pending>` 變成 IP 後，代表 Linode NodeBalancer 已建立。

![LoadBalancer EXTERNAL-IP](imgs/task5-2.png)

在 Linode 後台 NodeBalancers 頁面也可以看到自動建立的 NodeBalancer：

![Linode NodeBalancer 後台](imgs/task5-3.png)

### 6. 透過 LoadBalancer 存取 Nginx

```bash
curl http://<EXTERNAL-IP>
```

或直接在瀏覽器開啟。

![Nginx 頁面](imgs/task5-4.png)

### 7. Cleanup

```bash
kubectl delete -f k8s/
terraform destroy
```

`terraform destroy` 會一併刪除 LKE cluster 和 Linode 自動建立的 NodeBalancer，不會有殘留計費資源。

## 整體流程

```
terraform apply
└── 建立 Linode LKE cluster（managed control plane + worker nodes）
    │
kubectl apply -f k8s/
└── Deployment: 3 個 nginx pods
└── Service (LoadBalancer)
    └── Linode 自動建立 NodeBalancer
    └── EXTERNAL-IP 分配完成
    └── 流量進來 → NodeBalancer → nginx pods
```
