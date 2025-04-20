<template>
  <Breadcrumbs :elements="breadcrumbsElements" />
  <q-page-sticky position="bottom-right" :offset="[18, 18]">
    <q-btn @click="showCard = true" fab icon="add" color="accent" />
  </q-page-sticky>
  <NewHouseDialog :card="showCard" @close="showCard = false" />
</template>
<script setup lang="ts">
import { mdiHome, mdiAccount } from '@quasar/extras/mdi-v7';
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
  console.log('HousePage mounted');
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
