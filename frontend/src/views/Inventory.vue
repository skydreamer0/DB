<template>
  <div class="space-y-6">
    <h1 class="text-3xl font-bold text-gray-800">產品清單</h1>
    
    <div class="flex space-x-4">
      <input v-model="searchBarcode" placeholder="輸入條碼查詢" class="flex-grow px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
      <button @click="searchByBarcode" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">查詢</button>
    </div>

    <ul class="space-y-2">
      <li v-for="item in filteredInventory" :key="item.barcode" class="bg-white p-4 rounded-lg shadow">
        <router-link :to="{ name: 'ProductDetails', params: { id: item.barcode } }" class="text-blue-600 hover:underline">
          條碼: {{ item.barcode }} - 位置: {{ item.location }}
        </router-link>
      </li>
    </ul>
    
    <div v-if="selectedImage" class="mt-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">產品圖片</h2>
      <img :src="selectedImage" alt="產品圖片" class="max-w-full h-auto rounded-lg shadow-lg" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'InventoryPage',
  data() {
    return {
      inventory: [],
      selectedImage: null,
      searchBarcode: ''
    };
  },
  created() {
    this.fetchInventory();
  },
  methods: {
    fetchInventory() {
      axios.get('/api/inventory')
        .then(response => {
          this.inventory = response.data.data;
        })
        .catch(error => {
          console.error('無法獲取產品清單資料:', error);
        });
    },
    fetchImage(barcode) {
      axios.get(`/api/drug-image/${barcode}`)
        .then(response => {
          if (response.data.images) {
            this.selectedImage = `data:image/png;base64,${response.data.images}`;
          } else {
            this.selectedImage = null;
          }
        })
        .catch(error => {
          console.error('無法獲取圖片資料:', error);
        });
    },
    searchByBarcode() {
      if (this.searchBarcode) {
        this.fetchImage(this.searchBarcode);
      } else {
        this.selectedImage = null;
      }
    }
  },
  computed: {
    filteredInventory() {
      if (this.searchBarcode) {
        return this.inventory.filter(item => item.barcode.includes(this.searchBarcode));
      }
      return this.inventory;
    }
  },
  watch: {
    $route(to) {
      if (to.params.id) {
        this.fetchImage(to.params.id);
      } else {
        this.selectedImage = null;
      }
    }
  }
};
</script>
