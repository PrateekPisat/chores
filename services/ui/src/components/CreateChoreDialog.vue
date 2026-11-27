<template>
  <q-dialog
    :model-value="props.card"
    @hide="closeDialog"
    @before-show="beforeShow"
  >
    <q-card style="width: 100%; max-width: 420px">
      <div class="q-pa-md">
        <q-form class="q-gutter-md">
          <div class="text-h6 q-mb-sm">Create a New Chore</div>
          <q-select
            filled
            v-model="tasksStore.newChore.houseId"
            :options="userHouses"
            option-value="id"
            option-label="name"
            label="House"
            map-options
            emit-value
            :error-message="tasksStore.getErrors('houseId')"
            :error="!!tasksStore.getErrors('houseId')"
            @blur="tasksStore.checkCreateChore()"
          />
          <q-input
            filled
            placeholder="Chore Name"
            v-model="tasksStore.newChore.name"
            :error-message="tasksStore.getErrors('name')"
            :error="!!tasksStore.getErrors('name')"
            @blur="tasksStore.checkCreateChore()"
          />
          <q-input
            filled
            placeholder="Description"
            v-model="tasksStore.newChore.description"
            type="textarea"
            @blur="tasksStore.checkCreateChore()"
            :error-message="tasksStore.getErrors('description')"
            :error="!!tasksStore.getErrors('description')"
          />
          <q-select
            filled
            v-model="tasksStore.newChore.cadence"
            :options="options"
            label="Cadence"
            @blur="tasksStore.checkCreateChore()"
            :error-message="tasksStore.getErrors('cadence')"
            :error="!!tasksStore.getErrors('cadence')"
          />
          <q-input
            filled
            v-model="tasksStore.newChore.startDate"
            @blur="tasksStore.checkCreateChore()"
            placeholder="Start Date"
            :error-message="tasksStore.getErrors('startDate')"
            :error="!!tasksStore.getErrors('startDate')"
          >
            <template v-slot:append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy cover>
                  <q-date
                    v-model="tasksStore.newChore.startDate"
                    mask="YYYY-MM-DD"
                  />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>

          <q-input
            filled
            placeholder="End Date"
            v-model="tasksStore.newChore.endDate"
            @blur="tasksStore.checkCreateChore()"
            :error-message="tasksStore.getErrors('endDate')"
            :error="!!tasksStore.getErrors('endDate')"
          >
            <template v-slot:append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy cover>
                  <q-date
                    v-model="tasksStore.newChore.endDate"
                    mask="YYYY-MM-DD"
                  />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>

          <div class="row items-center">
            <q-btn flat label="Close" @click="closeDialog" />
            <q-space />
            <q-btn color="primary" label="Create chore" @click="createChore" />
          </div>
        </q-form>
      </div>
    </q-card>
  </q-dialog>
</template>
<script setup lang="ts">
import { userHouseStore } from 'src/stores/houseStore';
import { taskStore } from 'src/stores/taskStore';
import { computed } from 'vue';

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
const emit = defineEmits(['close']);
const tasksStore = taskStore();
const houseStore = userHouseStore();
const options = ['DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY'];

async function beforeShow() {
  await houseStore.listUserHouses(props.userId);
}

async function createChore() {
  await tasksStore.createChore();
  if (tasksStore.errors) {
    return;
  }
  closeDialog();
}

function closeDialog() {
  tasksStore.resetForm();
  emit('close');
}

const userHouses = computed(() => {
  return houseStore.houses;
});
</script>
