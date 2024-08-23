<template>
  <transition name="slide-fade">
    <div v-if="isActive" class="fixed inset-0 bg-gray-800 bg-opacity-75 z-50">
      <div class="flex justify-end p-4">
        <button @click="close" class="text-white hover:text-blue-300 transition duration-300">
          <i class="fas fa-times text-3xl"></i>
        </button>
      </div>
      <nav class="flex flex-col items-center mt-16">
        <router-link 
          v-for="(item, index) in navItems" 
          :key="index" 
          :to="item.path" 
          @click="close" 
          class="text-white text-2xl py-4 hover:text-blue-300 transition duration-300"
        >
          {{ item.name }}
        </router-link>
      </nav>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'MobileMenu',
  props: {
    isActive: Boolean
  },
  data() {
    return {
      navItems: [
        { name: '首頁', path: '/' },
        { name: '產品清單', path: '/inventory' },
        { name: '庫存資料', path: '/alldata' },     
        { name: '藥品擺放位置圖', path: '/inventory-map' },
        { name: '關於我們 & 聯絡我們', path: '/about-contact' }
      ]
    };
  },
  methods: {
    close() {
      this.$emit('close');
    }
  }
}
</script>

<style scoped>
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>