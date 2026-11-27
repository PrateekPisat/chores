<template>
  <q-btn flat round aria-label="Account">
    <q-avatar size="32px">
      <img v-if="userIcon" :src="userIcon" alt="" />
      <q-icon v-else :name="mdiAccount" />
    </q-avatar>
    <q-menu anchor="bottom right" self="top right">
      <div class="q-pa-md column items-center" style="min-width: 180px">
        <div class="text-subtitle1 q-mb-sm">{{ userName }}</div>
        <q-btn
          flat
          :icon="mdiLogout"
          label="Logout"
          v-close-popup
          @click="emit('logout')"
        />
      </div>
    </q-menu>
  </q-btn>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { mdiAccount, mdiLogout } from '@quasar/extras/mdi-v7';
import { AppUser } from 'src/stores/userStore';

const props = defineProps<{
  user: AppUser;
}>();

const emit = defineEmits(['logout']);

const userIcon = computed(() => props.user?.picture || '');
const userName = computed(() => {
  if (!props.user) {
    return '';
  }
  return `${props.user.firstName || ''} ${props.user.lastName || ''}`.trim();
});
</script>
