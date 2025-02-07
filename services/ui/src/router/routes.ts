import { RouteRecordRaw } from 'vue-router';
import { authGuard } from '@auth0/auth0-vue';


const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('pages/IndexPage.vue'),
        name: 'home',
        beforeEnter: authGuard,
      },
      {
        path: 'profile/:userId',
        component: () => import('pages/ProfilePage.vue'),
        name: 'profile',
        beforeEnter: authGuard,
        props: true,
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
    beforeEnter: authGuard,
  },
];

export default routes;
