<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title> Chores </q-toolbar-title>

        <q-space />
        <q-btn flat :icon="mdiLogout" :to="{ name: 'login' }" label="Logout" />
      </q-toolbar>
    </q-header>

    <q-drawer show-if-above v-model="leftDrawerOpen" side="left" elevated>
      <!-- drawer content -->
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { mdiLogout } from '@quasar/extras/mdi-v7';
import { ref } from 'vue';

const leftDrawerOpen = ref(false);
</script>
