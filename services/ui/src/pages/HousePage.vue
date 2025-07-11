<template>
  <Breadcrumbs :elements="breadcrumbsElements" />

  <div class="q-pa-sm">
    <q-toolbar>
      <q-toolbar-title>Your Houses</q-toolbar-title>
    </q-toolbar>
    <q-list separator padding>
      <q-item v-for="house in houses" :key="house.id" class="q-my-sm">
        <q-item-section avatar>
          <q-avatar color="primary" text-color="white" :icon="mdiHome" />
        </q-item-section>

        <q-item-section>
          <q-item-label>{{ house.name }}</q-item-label>
        </q-item-section>

        <q-item-section side>
          <q-btn
            class="q-ml-sm"
            flat
            dense
            :icon="mdiPlus"
            color="black"
            @click="showAddMembersDialog.set(house.id, true)"
          />
        </q-item-section>
        <q-item-section side>
          <q-btn
            class="q-ml-sm"
            dense
            flat
            :icon="mdiHomeEdit"
            color="black"
            @click="showHouseEditDialogs.set(house.id, true)"
          />
        </q-item-section>
        <q-item-section side>
          <q-btn
            class="q-ml-sm"
            dense
            flat
            :icon="mdiTrashCan"
            color="negative"
            @click="deleteHouse(house.id)"
          />
        </q-item-section>
      </q-item>
    </q-list>
  </div>

  <q-page-sticky position="top-right" :offset="[18, 18]">
    <q-btn @click="showCard = true" fab icon="add" color="accent" />
  </q-page-sticky>
  <NewHouseDialog
    :card="showCard"
    :user-id="props.userId"
    @close="showCard = false"
  />
  <EditHouseDialog
    v-for="house in houses"
    :key="house.id"
    :card="showHouseEditDialogs.get(house.id)"
    :house="house"
    :user-id="props.userId"
    @close="showHouseEditDialogs.set(house.id, false)"
    @update="houseStore.listUserHouses(props.userId)"
  />
  <AddMembersDialog
    v-for="house in houses"
    :key="house.id"
    :card="showAddMembersDialog.get(house.id)"
    :house="house"
    :user-id="props.userId"
    @close="showAddMembersDialog.set(house.id, false)"
    @update="houseStore.listUserHouses(props.userId)"
  />
</template>
<script setup lang="ts">
import {
  mdiHome,
  mdiAccount,
  mdiHomeEdit,
  mdiPlus,
  mdiTrashCan,
} from '@quasar/extras/mdi-v7';
import { userHouseStore } from 'src/stores/houseStore';
import { computed, onMounted, Ref, ref } from 'vue';
import Breadcrumbs from 'src/components/BreadCrumbs.vue';
import { userUserStore } from 'src/stores/userStore';
import NewHouseDialog from 'src/components/NewHouseDialog.vue';
import EditHouseDialog from 'src/components/EditHouseDialog.vue';
import AddMembersDialog from 'src/components/AddMembersDialog.vue';

const houseStore = userHouseStore();
const userStore = userUserStore();
const showCard = ref(false);
const showHouseEditDialogs: Ref<Map<string, boolean>> = ref(
  new Map<string, boolean>()
);
const showAddMembersDialog: Ref<Map<string, boolean>> = ref(
  new Map<string, boolean>()
);

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
});

onMounted(async () => {
  await houseStore.listUserHouses(props.userId).then(() => {
    for (const house of houseStore.houses) {
      showHouseEditDialogs.value.set(house.id, false);
      showAddMembersDialog.value.set(house.id, false);
    }
  });
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

const houses = computed(() => {
  return houseStore.houses;
});

async function deleteHouse(houseId: string) {
  await houseStore.deleteHouse(houseId);
  await houseStore.listUserHouses(props.userId);
}
</script>
