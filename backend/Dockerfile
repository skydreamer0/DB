# 使用 Node.js 官方的基礎映像
FROM node:18-alpine

# 設置工作目錄
WORKDIR /app

# 複製 package.json 和 package-lock.json
COPY package*.json ./

# 安裝 Node.js 依賴項
RUN npm install

# 複製其餘的應用程式碼
COPY . .

# 暴露應用運行的端口
EXPOSE 3000

# 指定運行後端的命令
CMD ["node", "server.js"]
