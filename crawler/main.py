import sqlite3
import json
import os
import logging
from bs4 import BeautifulSoup
import requests
from urllib.parse import unquote, urljoin
import re
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import concurrent.futures

# 設置日誌記錄
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 資料庫和 JSON 檔案路徑
db_path = 'data/inventory.db'
json_path = 'data/drug.json'

def create_database():
    try:
        # 創建資料庫連接
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 創建表格來存儲 barcode 和 location
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id TEXT PRIMARY KEY,
                barcode TEXT NOT NULL,
                location TEXT NOT NULL
            )
        ''')
        
        # 新增表格來存儲爬蟲結果
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drug_info (
                barcode TEXT PRIMARY KEY,
                chinese_name TEXT,
                english_name TEXT,
                ingredients TEXT,
                license_number TEXT,
                applicant TEXT,
                manufacturer TEXT,
                health_code TEXT,
                package_details TEXT,
                image_data TEXT
            )
        ''')
        
        conn.commit()
        logging.info("成功創建或連接到資料庫")
        return conn, cursor
    except Exception as e:
        logging.error(f"創建資料庫時發生錯誤: {str(e)}")
        return None, None

def insert_data_in_batches(conn, cursor, data, batch_size=1000):
    try:
        conn.execute('BEGIN TRANSACTION')  # 開始事務
        batch = []
        for item in data:
            batch.append((item["_id"]["$oid"], item["barcode"], item["location"]))
            
            # 當批次達到指定大小時插入數據
            if len(batch) == batch_size:
                cursor.executemany('''
                    INSERT OR REPLACE INTO inventory (id, barcode, location)
                    VALUES (?, ?, ?)
                ''', batch)
                batch = []  # 清空批次
        
        # 插入剩餘的數據
        if batch:
            cursor.executemany('''
                INSERT OR REPLACE INTO inventory (id, barcode, location)
                VALUES (?, ?, ?)
            ''', batch)
        
        conn.commit()  # 提交事務
        logging.info("所有數據成功插入到資料庫中")
    except Exception as e:
        conn.rollback()  # 如果發生錯誤，回滾事務
        logging.error(f"批量插入數據時發生錯誤: {str(e)}")

def load_and_insert_json_data():
    try:
        # 加載 JSON 檔案
        with open(json_path, 'r') as f:
            data = json.load(f)
        logging.info("成功加載 JSON 檔案")

        # 創建資料庫連接
        conn, cursor = create_database()
        if conn and cursor:
            # 插入數據到資料庫
            insert_data_in_batches(conn, cursor, data)
            conn.close()
        else:
            logging.error("無法創建資料庫連接")
    except Exception as e:
        logging.error(f"加載或插入 JSON 數據時發生錯誤: {str(e)}")

def b64encode(s):
    return base64.b64encode(s).decode('utf-8')

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
                all_data = {}
                for row in summary_card.find_all('div', class_='govuk-summary-list__row'):
                    key = row.find('dt', class_='govuk-summary-list__key').text.strip()
                    value = row.find('dd', class_='govuk-summary-list__value').text.strip()
                    all_data[key] = value
                
                # 提取並顯示指定的字段
                results['中文品名'] = all_data.get('中文品名', '')
                results['英文品名'] = all_data.get('英文品名', '')
                results['主成分略述'] = all_data.get('主成分略述', '')
                results['許可證字號'] = all_data.get('許可證字號', '')
                results['申請商名稱'] = all_data.get('申請商名稱', '')
                results['製造商名稱'] = all_data.get('製造商名稱', '')

                health_code = all_data.get('健保代碼', '')
                health_code_list = re.split(',\\s*', health_code)
                for i, code in enumerate(health_code_list, start=1):
                    results[f'健保代碼_{i}'] = code.strip()
                
                package_details = all_data.get('包裝', '').split(';;')
                results['包裝'] = package_details
                
                barcodes = re.findall(r'\d{10,}', all_data.get('包裝', ''))
                for i, barcode in enumerate(barcodes, start=1):
                    results[f'國際條碼_{i}'] = barcode
                
                logging.info("成功解析網頁內容")
                break  # 如果找到所需的資料，結束循環
            else:
                logging.warning(f"在連結 {link} 中未找到預期的govuk-summary-card__content區域")

        return results
    except Exception as e:
        logging.error(f"web_scraping 函數發生錯誤: {str(e)}")
        return {'Error': f"發生未預期的錯誤: {str(e)}"}

def perform_search(query_value):
    driver = None
    try:
        logging.info(f"開始處理查詢: {query_value}")
        web_scraping_result = web_scraping(query_value, "drugs.olc.tw")

        if web_scraping_result and '中文品名' in web_scraping_result:
            chinese_name = web_scraping_result.get('中文品名', '')
            logging.info(f"中文品名: {chinese_name}")

            driver = webdriver.Chrome()
            image_query_string = f"{chinese_name} 圖片 "
            image_url = f"https://www.google.com/search?q={image_query_string}&tbm=isch"
            logging.info(f"圖片搜索 URL: {image_url}")

            driver.get(image_url)
            driver.implicitly_wait(10)
            img_elements = driver.find_elements(By.CSS_SELECTOR, 'img')
            logging.info(f"找到 {len(img_elements)} 個圖片元素")

            images = []
            max_images = 3  # 設定最多下載的圖片數量

            def download_image(img_element):
                try:
                    img_src = img_element.get_attribute('src')
                    logging.debug(f"圖片元素 src: {img_src}")  # 新增日誌以顯示 src 屬性
                    if img_src:
                        img_height = int(img_element.get_attribute('height'))
                        img_width = int(img_element.get_attribute('width'))
                        logging.debug(f"圖片尺寸: {img_height}x{img_width}")  # 新增日誌以顯示圖片尺寸
                        if img_src.startswith('data:image') and img_height >= 50 and img_width >= 50:  # 放寬條件
                            base64_data = img_src.split(",")[1]
                            images.append(base64_data)
                            logging.debug(f"成功下載圖片: {img_height}x{img_width}")
                            if len(images) >= max_images:
                                return True  # 找到足夠的圖片後退出
                    return False
                except StaleElementReferenceException:
                    logging.warning("遇到 StaleElementReferenceException，嘗試重新定位元素")
                    img_element = driver.find_element(By.CSS_SELECTOR, 'img')
                    return download_image(img_element)
                except Exception as e:
                    logging.error(f"下載圖片時發生錯誤: {str(e)}")
                    return False

            # 限制只下載前三張圖片
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for img_element in img_elements:
                    if download_image(img_element):
                        break

            logging.info(f"成功下載 {len(images)} 張圖片")
            web_scraping_result['圖片'] = images

            return web_scraping_result
        else:
            logging.warning("web_scraping 未返回有效結果，跳過圖片搜索")
            return web_scraping_result
    except Exception as e:
        logging.error(f"perform_search 函數發生錯誤: {str(e)}")
        return None
    finally:
        if driver:
            driver.quit()
            logging.info("WebDriver 已關閉")

def update_database_with_scraping_results(conn, cursor, barcode, results):
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO drug_info
            (barcode, chinese_name, english_name, ingredients, license_number,
            applicant, manufacturer, health_code, package_details, image_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            barcode,
            results.get('中文品名', ''),
            results.get('英文品名', ''),
            results.get('主成分略述', ''),
            results.get('許可證字號', ''),
            results.get('申請商名稱', ''),
            results.get('製造商名稱', ''),
            ', '.join([results.get(f'健保代碼_{i}', '') for i in range(1, 6)]),
            '; '.join(results.get('包裝', [])),
            json.dumps(results.get('圖片', []))
        ))
        conn.commit()
        logging.info(f"成功更新資料庫中 barcode {barcode} 的資料")
    except Exception as e:
        logging.error(f"更新資料庫時發生錯誤: {str(e)}")

def process_all_barcodes():
    conn, cursor = create_database()
    if not conn or not cursor:
        logging.error("無法連接到資料庫")
        return

    try:
        cursor.execute("SELECT barcode FROM inventory")
        barcodes = cursor.fetchall()

        for barcode in barcodes:
            barcode = barcode[0]
            logging.info(f"正在處理 barcode: {barcode}")
            results = perform_search(barcode)
            if results:
                update_database_with_scraping_results(conn, cursor, barcode, results)
            else:
                logging.warning(f"未能獲取 barcode {barcode} 的資料")
    except Exception as e:
        logging.error(f"處理所有條碼時發生錯誤: {str(e)}")
    finally:
        conn.close()
        logging.info("資料庫連接已關閉")

# 加載 JSON 數據並插入到資料庫
load_and_insert_json_data()

# 處理所有條碼
process_all_barcodes()
