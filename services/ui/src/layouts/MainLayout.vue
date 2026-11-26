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
        <ProfileDropdown :user="userStore.user" @logout="logout" />
      </q-toolbar>
    </q-header>

    <AppDrawer v-model="drawer" :links="links" />

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import ProfileDropdown from 'src/components/ProfileDropdown.vue';
import AppDrawer, { DrawerLink } from 'src/components/AppDrawer.vue';
import { computed, onMounted, ref } from 'vue';
import { userUserStore } from 'src/stores/userStore';
import { logout, auth0 } from 'src/boot/auth0';
import { mdiAccount, mdiBroom, mdiHome, mdiHomeGroup, mdiListBox } from '@quasar/extras/mdi-v7';

const userStore = userUserStore();
const drawer = ref(false);

onMounted(async () => {
  await userStore.syncUser(auth0.user.value);
});

const links = computed((): DrawerLink[] => {
  const userId = userStore.appUser.userId;
  const needsUser = !userId;
  return [
    { label: 'Home', icon: mdiHome, to: { name: 'home' }, exact: true },
    {
      label: 'Houses',
      icon: mdiHomeGroup,
      to: needsUser ? { name: 'home' } : { name: 'houses', params: { userId } },
      disable: needsUser,
    },
    {
      label: 'Tasks',
      icon: mdiListBox,
      to: needsUser ? { name: 'home' } : { name: 'tasks', params: { userId } },
      disable: needsUser,
    },
    {
      label: 'Profile',
      icon: mdiAccount,
      to: needsUser ? { name: 'home' } : { name: 'profile', params: { userId } },
      disable: needsUser,
    },
  ];
});
</script>
