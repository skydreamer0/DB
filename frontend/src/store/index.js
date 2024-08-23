import { createRouter, createWebHistory } from 'vue-router';
import InventoryPage from '../views/Inventory.vue';
import AllDataPage from '../views/AllData.vue'; 

const routes = [
  {
    path: '/',
    name: 'Inventory',
    component: InventoryPage
  },
  {
    path: '/all-data',
    name: 'AllData',
    component: AllDataPage  
  },
  {
    path: '/product/:id',
    name: 'ProductDetails',
    component: () => import('../views/ProductDetails.vue')
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
