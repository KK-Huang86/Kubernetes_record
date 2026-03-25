嘗試根據此教學（https://grafana.com/docs/loki/latest/setup/install/helm/install-monolithic/）
使用 Helm 安裝 Loki 及 Grafana（不一定要 monolithic 也沒關係，但 monolithic 應該提供了驗證可行性的最簡單方式，應該足以完成這一題的要求），

完成後，我們現在應該有 Loki（日誌搜集工具）跟 Grafana（圖像化的監控介面）

請部署一個 Nginx Deployment/Pod，將 log 存到 HostPath，

並且以 DaemonSet 的方式，部署任一個日誌搜集工具（例如 fluentd, fluentbit, promtail, logstash 等），抓取該 hostpath，將 Log 上報到 Loki。

此題概念圖如下：
![任務概念圖](imgs/task9-1.png)