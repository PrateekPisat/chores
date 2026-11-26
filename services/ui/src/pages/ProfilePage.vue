<template>
  <q-page class="q-pa-md">
    <div class="page-wrap">
      <q-card flat bordered>
        <q-card-section class="row items-center">
          <q-avatar size="96px">
            <img v-if="userIcon" :src="userIcon" alt="" />
            <q-icon v-else :name="mdiAccount" />
          </q-avatar>
          <div class="q-ml-md">
            <div class="text-h5">{{ fullName }}</div>
          </div>
        </q-card-section>
        <q-list>
          <q-item>
            <q-item-section avatar>
              <q-icon :name="mdiEmail" color="grey" />
            </q-item-section>
            <q-item-section>{{ user.email }}</q-item-section>
          </q-item>
          <q-item v-if="user.nickname">
            <q-item-section avatar>
              <q-icon :name="mdiIdentifier" color="grey" />
            </q-item-section>
            <q-item-section>{{ user.nickname }}</q-item-section>
          </q-item>
        </q-list>
        <q-card-actions align="right">
          <q-btn flat color="negative" label="Delete account" @click="confirmDelete" />
        </q-card-actions>
        <q-card-section>
          <UserForm :user="user" />
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { userUserStore } from 'src/stores/userStore';
import { mdiAccount, mdiEmail, mdiIdentifier } from '@quasar/extras/mdi-v7';
import UserForm from 'src/components/UserForm.vue';
import { useAuth0 } from '@auth0/auth0-vue';
import { useQuasar } from 'quasar';

const userStore = userUserStore();
const auth0 = useAuth0();
const $q = useQuasar();

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
});

onMounted(() => {
  void userStore.getUser(props.userId);
});

const user = computed(() => userStore.appUser);
const fullName = computed(() => `${user.value.firstName || ''} ${user.value.lastName || ''}`.trim());
const userIcon = computed(() => user.value.picture || '');

function confirmDelete() {
  $q.dialog({
    title: 'Delete account',
    message: 'Delete your account? This cannot be undone.',
    cancel: true,
    persistent: true,
    ok: { label: 'Delete', color: 'negative' },
  }).onOk(() => {
    void userStore.deleteUser(auth0);
  });
}
</script>
