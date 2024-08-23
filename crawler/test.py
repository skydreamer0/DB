import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, urljoin
import logging
import re

# 設置日誌
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def web_scraping(query_value, domain):
    try:
        # 構建 Google 搜索 URL
        url = f"https://www.google.com/search?q=site:{domain}+{query_value}"
        logging.info(f"開始搜索 URL: {url}")
        
        # 發送 HTTP 請求到 Google 搜索
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = {}
        
        # 尋找搜索結果中的所有連結
        links = soup.find_all('a')
        matching_links = []
        
        for link in links:
            href = link.get('href')
            if href and href.startswith('/url?q='):
                actual_url = unquote(href.split('/url?q=')[1].split('&')[0])
                # 排除掉無關的鏈接
                if domain in actual_url and "maps.google.com" not in actual_url and "accounts.google.com" not in actual_url:
                    matching_links.append(actual_url)
                    logging.info(f"找到匹配的連結: {actual_url}")
        
        if not matching_links:
            logging.warning(f"未找到與 {domain} 匹配的連結")
            results['Error'] = f"未找到與 {domain} 匹配的連結"
            return results
        
        # 如果找到匹配的連結，繼續處理
        for link in matching_links:
            logging.info(f"正在處理連結: {link}")
            if not link.startswith("http"):
                link = urljoin("https://www.google.com", link)

            page_response = requests.get(link)
            page_soup = BeautifulSoup(page_response.text, 'html.parser')
            
            # 提取所需的信息
            summary_card = page_soup.find('div', class_='govuk-summary-card__content')
            if summary_card:
                for row in summary_card.find_all('div', class_='govuk-summary-list__row'):
                    key = row.find('dt', class_='govuk-summary-list__key').text.strip()
                    value = row.find('dd', class_='govuk-summary-list__value').text.strip()
                    results[key] = value
            else:
                logging.warning(f"在連結 {link} 中未找到預期的govuk-summary-card__content區域")
            
            # 如果找到了所需的數據，結束循環
            if results:
                break

        return results
    except Exception as e:
        logging.error(f"web_scraping 函數發生錯誤: {str(e)}")
        return {'Error': f"發生未預期的錯誤: {str(e)}"}

# 測試用的主函數
if __name__ == "__main__":
    # 測試參數
    domain = "drugs.olc.tw"
    query_value = "4711916005145"  # 這裡輸入你想要測試的條碼或其他查詢內容

    # 調用 web_scraping 函數進行測試
    results = web_scraping(query_value, domain)

    # 打印測試結果
    print("測試結果:")
    for key, value in results.items():
        print(f"{key}: {value}")
