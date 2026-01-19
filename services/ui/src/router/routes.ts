import { RouteRecordRaw } from 'vue-router';
import { authGuard } from '@auth0/auth0-vue';


const routes: RouteRecordRaw[] = [
  // Authenticated routes
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
      {
        path: 'houses/:userId',
        component: () => import('pages/HousePage.vue'),
        name: 'houses',
        beforeEnter: authGuard,
        props: true,
      },
      {
        path: 'tasks/:userId',
        component: () => import('pages/TaskPage.vue'),
        name: 'tasks',
        beforeEnter: authGuard,
        props: true,
      },
    ],
  },

  // Public routes (no auth required)
  {
    path: '/demo',
    component: () => import('layouts/DemoLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('pages/DemoPage.vue'),
        name: 'demo',
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
