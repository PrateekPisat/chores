<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title> Chores </q-toolbar-title>

        <q-space />
        <ProfileDropdown :user="userStore.user" @logout="logout" />
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
import { ref } from 'vue';
import ProfileDropdown from 'src/components/ProfileDropdown.vue';
import { onMounted } from 'vue';
import { userUserStore } from 'src/stores/userStore';
const userStore = userUserStore();
const leftDrawerOpen = ref(false);

onMounted(() => {
  userStore.syncUser();
});

function logout() {
  userStore.auth0.logout({
    logoutParams: {
      returnTo: window.location.origin,
    },
  });
}
</script>
