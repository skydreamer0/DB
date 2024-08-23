# 使用 Python 官方的基礎映像
FROM python:3.11-slim

# 設置工作目錄
WORKDIR /app

# 複製當前目錄下的所有內容到工作目錄
COPY . .

# 安裝 Python 依賴項
RUN pip install --no-cache-dir -r requirements.txt

# 指定運行爬蟲的命令
CMD ["python", "crawler.py"]
