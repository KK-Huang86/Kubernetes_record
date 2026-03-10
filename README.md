# Kubernetes 學習記錄

記錄學習 Kubernetes 的實作練習，包含 Docker、kubectl、k9s 等工具的操作。

## 目錄結構

### Week 1

| 任務 | 主題 | 說明 |
|------|------|------|
| [task0](week1/task0/README.md) | Dockerfile 優化 & 多架構 build | Dockerfile 最佳化方向、使用 buildx 編譯 x86/ARM 多架構 image |
| [task1](week1/task1/README.md) | Kubernetes 基礎操作 | Deployment/Service 建立、kubectl 常用指令、Rolling Update、Rollback、Nginx Reverse Proxy |
| [task2](week1/task2/README.md) | K9s 操作 | 使用 K9s 查看 namespace、pod logs、exec shell、編輯 deployment、xray 資源關係圖 |

## 環境

- Kubernetes: minikube
- 容器工具: Docker / buildx
- 管理工具: kubectl、k9s
