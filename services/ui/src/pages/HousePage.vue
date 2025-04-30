<template>
  <Breadcrumbs :elements="breadcrumbsElements" />

  <div class="q-pa-md">
    <q-toolbar>
      <q-toolbar-title>Your Houses</q-toolbar-title>
    </q-toolbar>
    <q-list separator padding>
      <q-item
        v-for="house in houseStore.houses"
        :key="house.id"
        class="q-my-sm"
        clickable
        v-ripple
      >
        <q-item-section avatar>
          <q-avatar color="primary" text-color="white" :icon="mdiHome" />
        </q-item-section>

        <q-item-section>
          <q-item-label>{{ house.name }}</q-item-label>
        </q-item-section>

        <q-item-section side>
          <q-icon :name="mdiHomeEdit" color="black" />
        </q-item-section>
      </q-item>
    </q-list>
  </div>

  <q-page-sticky position="bottom-right" :offset="[18, 18]">
    <q-btn @click="showCard = true" fab icon="add" color="accent" />
  </q-page-sticky>
  <NewHouseDialog
    :card="showCard"
    :user-id="props.userId"
    @close="showCard = false"
  />
</template>
<script setup lang="ts">
import { mdiHome, mdiAccount, mdiHomeEdit } from '@quasar/extras/mdi-v7';
import { userHouseStore } from 'src/stores/houseStore';
import { computed, onMounted, ref } from 'vue';
import Breadcrumbs from 'src/components/BreadCrumbs.vue';
import { userUserStore } from 'src/stores/userStore';
import NewHouseDialog from 'src/components/NewHouseDialog.vue';

const houseStore = userHouseStore();
const userStore = userUserStore();
const showCard = ref(false);

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
});

onMounted(async () => {
  await houseStore.listUserHouses(props.userId);
});

const breadcrumbsElements = computed(() => [
  {
    label: 'Home',
    icon: mdiHome,
    to: '/',
  },
  {
    label: `${userStore.appUser.firstName}'s Houses`,
    icon: mdiAccount,
  },
]);
</script>
