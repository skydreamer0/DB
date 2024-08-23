<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <header class="bg-white shadow-md">
      <nav class="container mx-auto px-4 py-6 flex justify-between items-center">
        <div class="text-3xl font-bold text-blue-500">
          <router-link to="/" class="hover:text-blue-600 transition duration-300">藥品管理系統</router-link>
        </div>
        <ul class="hidden md:flex space-x-4">
          <li v-for="(item, index) in navItems" :key="index">
            <router-link :to="item.path" class="text-gray-700 hover:text-blue-500 font-medium transition duration-300 px-3 py-2 rounded-md">{{ item.name }}</router-link>
          </li>
        </ul>
        <div class="md:hidden">
          <button @click="toggleMobileMenu" class="text-gray-700 hover:text-blue-500 transition duration-300">
            <i class="fas fa-bars text-2xl"></i>
          </button>
        </div>
      </nav>
    </header>
    <main class="container mx-auto px-4 py-8 flex-grow">
      <transition name="fade" mode="out-in">
        <router-view/>
      </transition>
    </main>
    <footer class="bg-gray-800 text-white py-8">
      <div class="container mx-auto px-4 text-center">
        <p>&copy; 2024 藥品管理系統. 版權所有.</p>
      </div>
    </footer>
    <MobileMenu :isActive="isMobileMenuActive" @close="closeMobileMenu" />
  </div>
</template>

<script>
import MobileMenu from './components/MobileMenu.vue';

export default {
  name: 'App',
  components: {
    MobileMenu
  },
  data() {
    return {
      isMobileMenuActive: false,
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
    toggleMobileMenu() {
      this.isMobileMenuActive = !this.isMobileMenuActive;
    },
    closeMobileMenu() {
      this.isMobileMenuActive = false;
    }
  }
};
</script>