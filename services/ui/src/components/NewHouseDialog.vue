<template>
  <q-dialog :model-value="props.card" @hide="emit('close')">
    <q-card class="my-card">
      <div class="q-pa-md" style="max-width: 400px">
        <q-form class="q-gutter-md">
          <div class="text-h6">Create A New House</div>
          <q-input
            filled
            v-model="houseStore.createHouseForm.name"
            label="House Name"
            hint="House Name"
            @blur="houseStore.checkCreate()"
            :error-message="houseStore.getErrors('name')"
            :error="!!houseStore.getErrors('name')"
          />

          <div>
            <q-btn
              label="Create House"
              type="button"
              color="primary"
              :disable="!!houseStore.getErrors('name')"
              @click="createHouse()"
            />
            <q-btn
              label="Close"
              type="reset"
              color="primary"
              flat
              class="q-ml-sm"
              @click="emit('close')"
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
  const houseId = await houseStore.createHouse();
  await houseStore.addMembers(houseId, [props.userId]);
  houseStore.listUserHouses(props.userId);
  houseStore.reset();
  emit('close');
}
</script>
