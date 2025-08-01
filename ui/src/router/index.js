import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import Home from '@/views/HomeView.vue'
import Cropper from '@/views/CropperPage.vue'
import About from '@/views/AboutView.vue'
import TrainModel from '@/views/TrainModel.vue'

const routes = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      { path: ' ', component: Cropper },
      { path: 'train-model', component: TrainModel },
      // { path: 'about', component: About },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
