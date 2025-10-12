<template>
  <Breadcrumbs :elements="breadcrumbsElements" />
  <q-card class="my-card" flat bordered>
    <q-parallax src="https://picsum.photos/800/600" :height="150" />

    <q-card-section>
      <q-avatar
        size="96px"
        class="absolute"
        style="top: 0; transform: translateY(-60%)"
      >
        <img :src="userIcon" />
      </q-avatar>
    </q-card-section>

    <q-card-section class="q-pt-none">
      <div class="row">
        <div class="col-11">
          <div class="text-h6 ellipsis">
            {{ fullName }}
          </div>
          <div class="text-caption">
            <q-icon :name="mdiEmail" color="grey" />
            {{ user.email }}
          </div>
          <div class="text-caption">
            <q-icon :name="mdiIdentifier" color="grey" />
            {{ user.nickname }}
          </div>
        </div>
        <div class="col-1">
          <q-btn class="q-pa-sm" flat @click="userStore.deleteUser(auth0)">
            <q-icon :name="mdiTrashCan" color="negative" />
          </q-btn>
        </div>
      </div>
    </q-card-section>

    <q-card-section>
      <UserForm :user="user" />
    </q-card-section>
  </q-card>
</template>
<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { userUserStore } from 'src/stores/userStore';
import {
  mdiAccount,
  mdiEmail,
  mdiHome,
  mdiIdentifier,
  mdiTrashCan,
} from '@quasar/extras/mdi-v7';
import Breadcrumbs from 'src/components/BreadCrumbs.vue';
import UserForm from 'src/components/UserForm.vue';
import { useAuth0 } from '@auth0/auth0-vue';

const userStore = userUserStore();
const auth0 = useAuth0();

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
});

const breadcrumbsElements = computed(() => [
  {
    label: 'Home',
    icon: mdiHome,
    to: '/',
  },
  {
    label: fullName.value,
    icon: mdiAccount,
  },
]);

onMounted(() => {
  userStore.getUser(props.userId);
});

const user = computed(() => userStore.appUser);
const fullName = computed(
  () => `${user.value.firstName} ${user.value.lastName}`
);
const userIcon = computed(() => {
  return user.value.picture || '';
});
</script>
