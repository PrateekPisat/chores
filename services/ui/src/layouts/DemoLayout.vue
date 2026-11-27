<template>
  <q-layout view="lHh LpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="drawer = !drawer"
        />
        <q-toolbar-title>
          <q-icon :name="mdiBroom" size="sm" class="q-mr-sm" />
          Chores
        </q-toolbar-title>
        <q-space />
        <q-btn
          flat
          dense
          label="Exit Demo"
          icon="exit_to_app"
          @click="router.push('/')"
        />
      </q-toolbar>
    </q-header>

    <AppDrawer v-model="drawer" :links="links" />

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import AppDrawer, { DrawerLink } from 'src/components/AppDrawer.vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { mdiBroom, mdiHome } from '@quasar/extras/mdi-v7';

const router = useRouter();
const drawer = ref(false);
const links: DrawerLink[] = [
  { label: 'Home', icon: mdiHome, to: { name: 'demo' }, exact: true },
];
</script>
