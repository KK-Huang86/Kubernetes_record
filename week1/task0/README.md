# 任務要求

以下為一份 TypeScript 的 Dockerfile，請說明有哪些方向可以優化此 Dockerfile。
```
FROM node:20
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY tsconfig.json ./
COPY src ./src
RUN npm run build
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

嘗試使用 buildx 將 dockerfile（不需要是這一份，可以請 AI 根據你的習慣語言生一個範例） 編譯成多架構的 image，Image 需要可以分別在 x86 跟 ARM 上執行。
完成後請嘗試驗證是否有成功執行（可以開雲端 VM 執行看看）。 

# Dockerfile優化方向
1. node抓取的版本應鎖定，而且最好使用 alpine的版本
2. 使用多階段構建 (Multi-stage builds)的概念，bulid 環境 和 run環境分開，確保image 只保留執行需要的東西。每當程式碼進行更動時，除非增加新的套件，否則直接取快取層的資料，無需重跑 build image
3. 將不常變動的（安裝依賴）放前面，常變動的（源代碼）放後面
4. 盡量不以 root來執行，而是建立 USER 的方式執行

# 使用 buildx

1. 為什麼要使用 buildx? 同一個 docker pull myapp:latest，x86 機器拿到 x86 版，ARM 機器拿到 ARM 版，自動對應，不需做另外處理；如果只單純 build 後推上 Docker Hub後，不同機器版本可能會報錯

2. 相關指令
建立一個新的 builder，取名 buildx
```docker buildx create --name task0```

切換到這個 builder
```docker buildx use task0```

啟動 builder 並確認支援哪些架構
應該會看到 linux/amd64, linux/arm64 等

```docker buildx inspect --bootstrap```

同時 build x86 + ARM，直接推上 Docker Hub
```docker buildx build --platform linux/amd64,linux/arm64 -t <username>/<image>:<tag> --push .```
