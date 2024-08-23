<template>
  <div class="product-details">
    <h1>產品詳情</h1>
    <div v-if="product" class="product-info">
      <table class="info-table">
        <tr>
          <th>項目</th>
          <th>內容</th>
          <th>操作</th>
        </tr>
        <tr v-for="(value, key) in productInfo" :key="key">
          <td>{{ labels[key] }}</td>
          <td>{{ value }}</td>
          <td>
            <button @click="copyToClipboard(value)">複製</button>
          </td>
        </tr>
      </table>
      <div class="image-gallery">
        <h2>產品圖片</h2>
        <div v-if="product.image_data && product.image_data.length > 0" class="images">
          <img v-for="(image, index) in product.image_data" :key="index" :src="'data:image/jpeg;base64,' + image" alt="產品圖片" />
        </div>
        <p v-else>暫無圖片</p>
      </div>
    </div>
    <div v-else>
      <p>載入中...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProductDetailsPage',
  data() {
    return {
      product: null,
      labels: {
        barcode: '條碼',
        chinese_name: '中文品名',
        english_name: '英文品名',
        ingredients: '主成分',
        license_number: '許可證字號',
        applicant: '申請商',
        manufacturer: '製造商',
        health_code: '健保代碼',
        package_details: '包裝詳情',
        location: '位置'
      }
    };
  },
  computed: {
    productInfo() {
      if (!this.product) return {};
      return {
        barcode: this.product.barcode,
        chinese_name: this.product.chinese_name,
        english_name: this.product.english_name,
        ingredients: this.product.ingredients,
        license_number: this.product.license_number,
        applicant: this.product.applicant,
        manufacturer: this.product.manufacturer,
        health_code: this.product.health_code,
        package_details: this.product.package_details,
        location: this.product.location
      };
    }
  },
  created() {
    this.fetchProductDetails();
  },
  methods: {
    fetchProductDetails() {
      const barcode = this.$route.params.id;
      axios.get(`/api/drug-info/${barcode}`)
        .then(response => {
          this.product = response.data;
          
        })
        .catch(error => {
          console.error('無法獲取產品詳情:', error);
        });
    },
    copyToClipboard(text) {
      navigator.clipboard.writeText(text).then(() => {
        alert('已複製到剪貼簿');
      }).catch(err => {
        console.error('複製失敗:', err);
      });
    }
  }
};
</script>

<style scoped>
.product-details {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-table {
  width: 100%;
  border-collapse: collapse;
}

.info-table th, .info-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.info-table th {
  background-color: #f2f2f2;
}

.info-table button {
  padding: 5px 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

.info-table button:hover {
  background-color: #45a049;
}

.image-gallery {
  margin-top: 20px;
}

.images {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.images img {
  max-width: 200px;
  max-height: 200px;
  object-fit: cover;
}
</style>