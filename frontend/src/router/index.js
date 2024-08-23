import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Inventory from '../views/Inventory.vue';
import ProductDetails from '../views/ProductDetails.vue';
import AboutContact from '../views/AboutContact.vue';
import AllData from '../views/AllData.vue';
import InventoryMap from '../views/InventoryMap.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/inventory',
    name: 'Inventory',
    component: Inventory
  },
  {
    path: '/product/:id',
    name: 'ProductDetails',
    component: ProductDetails
  },
  {
    path: '/about-contact',
    name: 'AboutContact',
    component: AboutContact
  },
  {
    path: '/alldata',
    name: 'AllData',
    component: AllData
  },
  {
    path: '/inventory-map',
    name: 'InventoryMap',
    component: InventoryMap
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;