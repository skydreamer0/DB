<template>
  <div>
    <h1>所有資料</h1>
    <table>
      <thead>
        <tr>
          <th>位置</th>
          <th>條碼</th>
          <th>中文名</th>
          <th>英文名</th>
          
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in sortedInventory" :key="item.id">
          <td>{{ item.location }}</td>
          <td>{{ item.barcode }}</td>
          <td>{{ item.chinese_name }}</td>
          <td>{{ item.english_name }}</td>
     
        </tr>
      </tbody>
    </table>
  </div>
</template>

  
  <script>
  import axios from 'axios';

export default {
  name: 'AllDataPage',
  data() {
    return {
      inventory: []
    };
  },
  created() {
    this.fetchInventory();
  },
  methods: {
    fetchInventory() {
      axios.get('/api/all-drugs')
        .then(response => {
          this.inventory = response.data.data;
        })
        .catch(error => {
          console.error('無法獲取所有藥品資料:', error);
        });
    }
  },
  computed: {
  sortedInventory() {
    // 使用 slice() 複製數組，再進行排序，這樣就不會有副作用
    return [...this.inventory].sort((a, b) => {
      if (a.location < b.location) return -1;
      if (a.location > b.location) return 1;
      return 0;
    });
  }
}
};

  </script>
<style>
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

tbody tr:hover {
  background-color: #f0f0f0;
}
</style>
