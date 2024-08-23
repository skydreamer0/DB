# app.py
from flask import Flask, request, render_template
import logging
from main import perform_search  # 從 main.py 導入 perform_search 函數

# 設置日誌
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query_value = request.form['query_value']
    logging.info(f"收到查詢值: {query_value}")
    results = perform_search(query_value)
    logging.debug(f"搜索結果: {results}")
    return render_template('results.html', web_scraping_result=results['web_scraping_result'])

if __name__ == '__main__':
    logging.info("正在啟動 Flask 應用程序...")
    app.run(host='localhost', port=14000, debug=True)
