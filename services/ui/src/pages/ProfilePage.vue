<template>
  <div class="q-pa-md q-gutter-sm">
    <q-breadcrumbs>
      <template v-slot:separator>
        <q-icon size="1.25em" :name="mdiChevronRight" color="primary" />
      </template>
      <q-breadcrumbs-el :icon="mdiHome" to="/" label="Home" />
      <q-breadcrumbs-el :label="fullName" :icon="mdiAccount" />
    </q-breadcrumbs>
  </div>
  <q-card class="my-card" flat bordered>
    <q-parallax src="https://picsum.photos/800/600" :height="150" />

    <q-card-section>
      <q-avatar
        size="96px"
        class="absolute"
        style="top: 0; transform: translateY(-60%)"
      >
        <img :src="userIcon" />
        <q-badge color="primary" align="top" floating>
          <q-icon :name="mdiCheckDecagram" />
        </q-badge>
      </q-avatar>
    </q-card-section>

    <q-card-section class="q-pt-none">
      <div class="col text-h6 ellipsis">
        <span>
          {{ fullName }}
        </span>
      </div>
      <div class="text-caption text-grey">
        <span>
          {{ user.email }}
        </span>
      </div>
    </q-card-section>

    <q-tabs v-model="tab" align="left">
      <q-tab label="Account Details" name="one" />
      <q-tab label="Houses" name="two" />
      <q-tab label="Roommates" name="three" />
    </q-tabs>

    <q-separator />
    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="one">
        <div class="text-h4">
          Title
          <q-badge align="bottom">docs v1.0.0</q-badge>
        </div>
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
  mdiChevronRight,
  mdiHome,
  mdiCheckDecagram,
} from '@quasar/extras/mdi-v7';

const tab = ref('one');
const userStore = userUserStore();

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
});

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
