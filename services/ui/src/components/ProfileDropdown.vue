<template>
  <div class="q-pa-sm">
    <q-btn-dropdown label="Options" flat>
      <div class="row no-wrap q-pa-sm">
        <q-list>
          <router-link :to="profileLink">
            <q-item clickable v-close-popup>
              <q-item-section avatar>
                <q-avatar
                  :icon="mdiFaceManProfile"
                  color="primary"
                  text-color="white"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label> Profile </q-item-label>
              </q-item-section>
            </q-item>
          </router-link>

          <router-link :to="houseLink">
            <q-item clickable v-close-popup>
              <q-item-section avatar>
                <q-avatar :icon="mdiHome" color="primary" text-color="white" />
              </q-item-section>
              <q-item-section>
                <q-item-label>House</q-item-label>
              </q-item-section>
            </q-item>
          </router-link>

          <router-link :to="taskLink">
            <q-item clickable v-close-popup>
              <q-item-section avatar>
                <q-avatar
                  :icon="mdiListBox"
                  color="primary"
                  text-color="white"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Tasks</q-item-label>
              </q-item-section>
            </q-item>
          </router-link>
        </q-list>

        <q-separator vertical inset class="q-mx-md" />

        <div class="column items-center">
          <q-avatar size="72px">
            <img :src="userIcon" />
          </q-avatar>

          <div class="text-subtitle1 q-mt-md q-mb-xs">{{ userName }}</div>

          <q-btn
            flat
            :icon="mdiLogout"
            @click="emit('logout')"
            label="Logout"
            push
            size="sm"
            v-close-popup
          />
        </div>
      </div>
    </q-btn-dropdown>
  </div>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import {
  mdiLogout,
  mdiFaceManProfile,
  mdiListBox,
  mdiHome,
} from '@quasar/extras/mdi-v7';
import { AppUser } from 'src/stores/userStore';

const props = defineProps<{
  user: AppUser;
}>();

const emit = defineEmits(['logout']);

const userIcon = computed(() => {
  return props.user.picture || '';
});
const userName = computed(() => {
  return props.user.firstName + props.user.lastName;
});

const profileLink = computed(() => {
  return { name: 'profile', params: { userId: props.user.userId } };
});

const houseLink = computed(() => {
  return { name: 'houses', params: { userId: props.user.userId } };
});

const taskLink = computed(() => {
  return { name: 'tasks', params: { userId: props.user.userId } };
});
</script>
