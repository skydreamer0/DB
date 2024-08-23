<template>
  <div>
    <h1>藥品擺放位置圖</h1>
    <div v-if="loading" class="loading">加載中...</div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div class="inventory-map" v-if="!loading && !errorMessage">
      <table>
        <thead>
          <tr>
            <th></th>
            <th v-for="col in columns" :key="col">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in formattedMap" :key="rowIndex">
            <th>{{ rowIndex + 1 }}</th>
            <td v-for="(cell, colIndex) in row" :key="colIndex" @click="showDrugInfo(cell)">
              <div v-if="cell && cell.length">
                <span v-for="drug in cell" :key="drug.barcode">{{ drug.name }}</span>
              </div>
              <div v-else>
                空位
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="selectedDrug && selectedDrug.length">
      <h2>藥品詳情</h2>
      <ul>
        <li v-for="drug in selectedDrug" :key="drug.barcode">
          <p>名稱: {{ drug.name }}</p>
          <p>位置: {{ drug.location }}</p>
          <p>條碼: {{ drug.barcode }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      inventoryData: [],
      selectedDrug: null,
      formattedMap: [],
      columns: [],
      loading: true,
      errorMessage: ''
    };
  },
  async mounted() {
    try {
      const response = await axios.get('/api/inventory-map');
      this.inventoryData = response.data.data.map(item => ({
        name: item.chinese_name,
        location: item.location,
        barcode: item.barcode
      }));
      this.buildMap();
      this.loading = false;
    } catch (error) {
      console.error('Failed to fetch data:', error);
      this.errorMessage = '無法加載數據，請稍後再試';
      this.loading = false;
    }
  },
  methods: {
    buildMap() {
      const map = {};
      let maxRow = 0;
      let maxCol = 0;

      // 找出最大的行和列
      this.inventoryData.forEach(item => {
        const [letter, ...rest] = item.location.split('');
        const col = letter.charCodeAt(0) - 65; // 'A' 的 ASCII 碼是 65
        const row = parseInt(rest.join('')) - 1; // 假設行號從 1 開始
        maxRow = Math.max(maxRow, row);
        maxCol = Math.max(maxCol, col);
        if (!map[row]) map[row] = {};
        if (!map[row][col]) map[row][col] = [];
        map[row][col].push(item); // 將藥品加入對應的列表中
      });

      // 創建二維數組
      this.formattedMap = Array(maxRow + 1).fill(null).map(() => Array(maxCol + 1).fill(null));
      
      // 填充二維數組
      for (let row in map) {
        for (let col in map[row]) {
          this.formattedMap[row][col] = map[row][col];
        }
      }

      // 設置列標題（字母）
      this.columns = Array(maxCol + 1).fill(0).map((_, i) => String.fromCharCode(65 + i));
    },
    showDrugInfo(cell) {
      this.selectedDrug = cell || [];
    }
  }
};

</script>

<style>
.inventory-map table {
  width: 100%;
  border-collapse: collapse;
}

.inventory-map th, .inventory-map td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

.inventory-map td {
  cursor: pointer;
}

.inventory-map td:hover {
  background-color: #f0f0f0;
}

.loading, .error-message {
  text-align: center;
  margin: 20px 0;
}

.error-message {
  color: red;
}

</style>