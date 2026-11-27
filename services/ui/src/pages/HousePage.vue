<template>
  <q-page class="q-pa-md">
    <div class="page-wrap">
      <div class="text-h5 q-mb-md">Your houses</div>

      <div v-if="!houses.length" class="column items-center q-pa-xl text-center">
        <q-icon :name="mdiHome" size="48px" color="primary" />
        <div class="text-h6 q-mt-sm">No houses yet</div>
      </div>

      <q-card
        v-for="house in houses"
        :key="house.id"
        flat
        bordered
        class="q-mb-md"
      >
        <q-card-section class="row items-center no-wrap">
          <q-avatar color="primary" text-color="white" :icon="mdiHome" />
          <div class="text-subtitle1 q-ml-md">{{ house.name }}</div>
          <q-space />
          <q-btn-dropdown flat label="Actions">
            <q-list>
              <q-item clickable v-close-popup @click="showAddMembersDialog.set(house.id, true)">
                <q-item-section>Add members</q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="showHouseEditDialogs.set(house.id, true)">
                <q-item-section>Edit</q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="confirmDelete(house)">
                <q-item-section class="text-negative">Delete</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </q-card-section>
      </q-card>
    </div>

    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn
        fab
        icon="add"
        color="accent"
        aria-label="New house"
        @click="showCard = true"
      />
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
      :key="`${house.id}-members`"
      :card="showAddMembersDialog.get(house.id)"
      :house="house"
      :user-id="props.userId"
      @close="showAddMembersDialog.set(house.id, false)"
      @update="houseStore.listUserHouses(props.userId)"
    />
  </q-page>
</template>

<script setup lang="ts">
import { mdiHome } from '@quasar/extras/mdi-v7';
import { userHouseStore, House } from 'src/stores/houseStore';
import { computed, onMounted, Ref, ref } from 'vue';
import NewHouseDialog from 'src/components/NewHouseDialog.vue';
import EditHouseDialog from 'src/components/EditHouseDialog.vue';
import AddMembersDialog from 'src/components/AddMembersDialog.vue';
import { useQuasar } from 'quasar';

const houseStore = userHouseStore();
const $q = useQuasar();
const showCard = ref(false);
const showHouseEditDialogs: Ref<Map<string, boolean>> = ref(new Map());
const showAddMembersDialog: Ref<Map<string, boolean>> = ref(new Map());

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

const houses = computed(() => houseStore.houses);

function confirmDelete(house: House) {
  $q.dialog({
    title: 'Delete house',
    message: `Delete ${house.name}?`,
    cancel: true,
    persistent: true,
    ok: { label: 'Delete', color: 'negative' },
  }).onOk(() => {
    void deleteHouse(house.id);
  });
}

async function deleteHouse(houseId: string) {
  await houseStore.deleteHouse(houseId);
  await houseStore.listUserHouses(props.userId);
}
</script>
