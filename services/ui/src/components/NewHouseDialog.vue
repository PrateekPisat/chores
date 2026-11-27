<template>
  <q-dialog :model-value="props.card" @hide="emit('close')">
    <q-card style="width: 100%; max-width: 420px">
      <div class="q-pa-md">
        <q-form class="q-gutter-md">
          <div class="text-h6">Create a house</div>
          <q-input
            filled
            v-model="houseStore.createHouseForm.name"
            label="House Name"
            hint="House Name"
            @blur="houseStore.checkCreate()"
            :error-message="houseStore.getErrors('name')"
            :error="!!houseStore.getErrors('name')"
          />

          <div class="row items-center">
            <q-btn label="Close" flat @click="emit('close')" />
            <q-space />
            <q-btn
              label="Create house"
              type="button"
              color="primary"
              :disable="!!houseStore.getErrors('name')"
              @click="createHouse()"
            />
          </div>
        </q-form>
      </div>
    </q-card>
  </q-dialog>
</template>
<script setup lang="ts">
import { userHouseStore } from 'src/stores/houseStore';

const props = defineProps({
  card: {
    type: Boolean,
    default: false,
  },
  userId: {
    type: String,
    required: true,
  },
});
const emit = defineEmits(['close', 'update']);
const houseStore = userHouseStore();

async function createHouse() {
  await houseStore.createHouse();
  houseStore.listUserHouses(props.userId);
  houseStore.reset();
  emit('close');
}
</script>
