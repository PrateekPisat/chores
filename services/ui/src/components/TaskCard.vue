<template>
  <div class="col-sm-12 col-md-4 q-pa-xs" style="width: 400px">
    <q-card class="my-card" bordered :class="{ 'bg-red-1': props.pastDue }">
      <q-card-section horizontal>
        <q-card-section class="q-pt-xs">
          <div class="text-h5 q-mt-sm q-mb-xs">{{ props.task.chore.name }}</div>
          <div class="text-caption text-grey">
            {{ props.task.chore.description }}
          </div>
        </q-card-section>
        <q-space />
        <q-btn flat color="negative" :icon="mdiTrashCan" @click="deleteTask" />
      </q-card-section>

      <q-separator />

      <q-card-actions>
        <span> {{ fluentFormatDatetime(task.dueDate) }} </span>
        <q-space />
        <q-checkbox
          :model-value="completed"
          :color="completed ? 'positive' : 'secondary'"
          @update:model-value="(value: boolean) => updateTask(value, props.task.dueDate)"
        >
          <span :class="completed ? 'text-green' : 'text-black'">{{
            completed ? 'Completed' : 'Mark as Completed'
          }}</span>
        </q-checkbox>
      </q-card-actions>
    </q-card>
  </div>
</template>
<script setup lang="ts">
import { mdiTrashCan } from '@quasar/extras/mdi-v7';
import { Task, taskStore } from 'src/stores/taskStore';
import { PropType } from 'vue';
import { fluentFormatDatetime } from 'src/utils';

const props = defineProps({
  task: {
    type: Object as PropType<Task>,
    required: true,
  },
  completed: {
    type: Boolean,
    required: true,
  },
  pastDue: {
    type: Boolean,
    default: false,
  },
  demoMode: {
    type: Boolean,
    default: false,
  },
});
const tasksStore = taskStore();
const emit = defineEmits(['refresh', 'update', 'delete']);

async function deleteTask() {
  if (props.demoMode) {
    emit('delete', props.task.id);
    emit('refresh');
  } else {
    await tasksStore.deleteTask(props.task.id);
    emit('refresh');
  }
}

async function updateTask(completed: boolean, dueDate: string) {
  if (props.demoMode) {
    emit('update', props.task.id, completed, dueDate);
    emit('refresh');
  } else {
    await tasksStore.updateTask(props.task.id, completed, dueDate);
    emit('refresh');
  }
}
</script>
