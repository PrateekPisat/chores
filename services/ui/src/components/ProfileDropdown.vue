<template>
  <div class="q-pa-sm">
    <q-btn-dropdown label="Profile" flat>
      <div class="row no-wrap q-pa-sm">
        <q-list>
          <q-item clickable v-close-popup>
            <q-item-section avatar>
              <q-avatar
                :icon="mdiFaceManProfile"
                color="primary"
                text-color="white"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label>
                <router-link :to="profileLink">Profile</router-link>
              </q-item-label>
            </q-item-section>
          </q-item>

          <q-item clickable v-close-popup>
            <q-item-section avatar>
              <q-avatar
                icon="assignment"
                color="secondary"
                text-color="white"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label>Vacation</q-item-label>
            </q-item-section>
          </q-item>
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
import { mdiLogout, mdiFaceManProfile } from '@quasar/extras/mdi-v7';
import { AppUser } from 'src/stores/userStore';

const props = defineProps<{
  user: AppUser;
}>();

const emit = defineEmits(['logout']);

const userIcon = computed(() => {
  return props.user.picture || '';
});
const userName = computed(() => {
  return props.user.first_name + props.user.last_name;
});

const profileLink = computed(() => {
  return { name: 'profile', params: { userId: props.user.user_id } };
});
</script>
