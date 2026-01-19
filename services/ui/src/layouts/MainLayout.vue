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
import { userUserStore } from 'src/stores/userStore';
import { logout, auth0 } from 'src/boot/auth0';
const userStore = userUserStore();

onMounted(async () => {
  await userStore.syncUser(auth0.user.value);
});
</script>
