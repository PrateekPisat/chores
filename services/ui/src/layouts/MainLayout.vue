<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title> Chores </q-toolbar-title>

        <q-space />
        <ProfileDropdown :user="userStore.user" @logout="logout" />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import ProfileDropdown from 'src/components/ProfileDropdown.vue';
import { onMounted } from 'vue';
import { createAuth0 } from '@auth0/auth0-vue';
import { userUserStore } from 'src/stores/userStore';
const userStore = userUserStore();
const auth0 = createAuth0();

onMounted(() => {
  userStore.syncUser();
});

function logout() {
  auth0.logout({
    logoutParams: {
      returnTo: window.location.origin,
    },
  });
}
</script>
