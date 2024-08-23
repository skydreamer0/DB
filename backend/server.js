const express = require('express');
const cors = require('cors'); // 引入 cors 套件
const sqlite3 = require('sqlite3').verbose();
const path = require('path'); 
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(cors()); // 使用 cors 中介軟體

// 使用 path 模組構建資料庫路徑
const dbPath = path.resolve(__dirname, '../shared_data/inventory.db');
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('無法連接到資料庫:', err.message);
    } else {
        console.log('成功連接到 SQLite 資料庫');
    }
});

// API 端點來獲取所有產品清單
app.get('/api/inventory', (req, res) => {
    db.all('SELECT * FROM inventory', [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json({ data: rows });
    });
});
// 取得所有藥品資訊的 API
app.get('/api/all-drugs', (req, res) => {
    db.all('SELECT * FROM drug_info', [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json({ data: rows });
    });
});

// 新增 API 端點來獲取藥品擺放位置
app.get('/api/inventory-map', (req, res) => {
    db.all('SELECT barcode, location, chinese_name FROM drug_info', [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json({ data: rows });
    });
});


app.get('/', (req, res) => {
    res.send('Welcome to the API');
});

// API 端點來獲取指定條碼的圖片
app.get('/api/drug-info/:barcode', (req, res) => {
    const barcode = req.params.barcode;
    db.get('SELECT * FROM drug_info WHERE barcode = ?', [barcode], (err, row) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        if (row) {
            if (row.image_data) {
                row.image_data = JSON.parse(row.image_data);
            }
            res.json(row);
        } else {
            res.status(404).json({ error: '未找到產品資訊' });
        }
    });
});

app.listen(PORT, () => {
    console.log(`伺服器運行在 http://localhost:${PORT}`);
});