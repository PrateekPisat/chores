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
              <q-item-label>Profile</q-item-label>
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
            @click="logout"
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
import { useAuth0 } from '@auth0/auth0-vue';
import { computed } from 'vue';
import { mdiLogout, mdiFaceManProfile } from '@quasar/extras/mdi-v7';

const auth0 = useAuth0();

const userIcon = computed(() => {
  return auth0.user.value?.picture;
});
const userName = computed(() => {
  return auth0.user.value?.name;
});

function logout() {
  auth0.logout({
    logoutParams: {
      returnTo: window.location.origin,
    },
  });
}
</script>
