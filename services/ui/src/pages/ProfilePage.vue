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
      <div class="col text-h6 ellipsis">
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
    </q-card-section>

    <q-tabs v-model="tab" align="left">
      <q-tab label="Details" name="details" />
      <q-tab label="Houses" name="one" />
      <q-tab label="Roommates" name="two" />
    </q-tabs>

    <q-separator />
    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="details">
        <UserForm :user="user" />
      </q-tab-panel>
      <q-tab-panel name="one">
        With so much content to display at once, and often so little screen
        real-estate, Cards have fast become the design pattern of choice for
        many companies, including the likes of Google and Twitter.
      </q-tab-panel>
      <q-tab-panel name="two">
        With so much content to display at once, and often so little screen
        real-estate, Cards have fast become the design pattern of choice for
        many companies, including the likes of Google and Twitter.
      </q-tab-panel>
    </q-tab-panels>
  </q-card>
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { userUserStore } from 'src/stores/userStore';
import {
  mdiAccount,
  mdiEmail,
  mdiHome,
  mdiIdentifier,
} from '@quasar/extras/mdi-v7';
import Breadcrumbs from 'src/components/Breadcrumbs.vue';
import UserForm from 'src/components/UserForm.vue';

const tab = ref('one');
const userStore = userUserStore();

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
  () => `${user.value.first_name} ${user.value.last_name}`
);
const userIcon = computed(() => {
  return user.value.picture || '';
});
</script>
