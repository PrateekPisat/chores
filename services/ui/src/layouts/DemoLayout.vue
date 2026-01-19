<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>
          <q-icon :name="mdiBroom" size="sm" class="q-mr-sm" />
          Chores - Demo Mode
        </q-toolbar-title>

        <q-space />

        <!-- Demo User Info -->
        <div class="q-mr-md text-body2">
          <q-avatar size="32px" class="q-mr-sm">
            <img :src="demoUser.picture || ''" />
          </q-avatar>
          {{ demoUser.firstName }} {{ demoUser.lastName }}
        </div>

        <q-btn
          flat
          dense
          label="Exit Demo"
          icon="exit_to_app"
          @click="router.push('/')"
        />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { useDemoData } from 'src/composables/useDemoData';
import { useRouter } from 'vue-router';
import { mdiBroom } from '@quasar/extras/mdi-v7';

const { demoUser } = useDemoData();
const router = useRouter();
</script>
