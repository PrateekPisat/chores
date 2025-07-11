<template>
  <q-card class="my-card" bordered style="">
    <q-card-section horizontal>
      <q-card-section class="q-pt-xs">
        <div class="text-h5 q-mt-sm q-mb-xs">{{ props.task.chore.name }}</div>
        <div class="text-caption text-grey">
          {{ props.task.chore.description }}
        </div>
      </q-card-section>
    </q-card-section>

    <q-separator />

    <q-card-actions>
      <span>Complete By: {{ fluentFormatDatetime(task.dueDate) }} </span>
      <q-checkbox
        :model-value="completed"
        label="Mark as Completed"
        @update:model-value="(value: boolean) => updateTask(value, props.task.dueDate)"
      />
      <q-btn flat @click="deleteTask" class="q-ml-xs">
        <q-icon color="negative" :name="mdiTrashCan" />
      </q-btn>
    </q-card-actions>
  </q-card>
</template>
<script setup lang="ts">
import { mdiTrashCan } from '@quasar/extras/mdi-v7';
import { format, parseISO } from 'date-fns';
import { Task, taskStore } from 'src/stores/taskStore';
import { onMounted, PropType, ref } from 'vue';
const props = defineProps({
  task: {
    type: Object as PropType<Task>,
    required: true,
  },
});
const completed = ref(false);
const tasksStore = taskStore();
const emit = defineEmits(['update']);

onMounted(() => {
  completed.value = !!props.task.completedAt ? true : false;
});

async function deleteTask() {
  await tasksStore.deleteTask(props.task.id);
  emit('update');
}

async function updateTask(completed: boolean, dueDate: string) {
  await tasksStore.updateTask(props.task.id, completed, dueDate);
  emit('update');
}

function datetimeFormat(
  date: string | Date | null,
  formatString: string
): string {
  if (!date) {
    return 'Invalid';
  }

  if (typeof date === 'string') {
    date = parseISO(date);
  }
  return format(date, formatString);
}

function fluentFormatDatetime(date: string | Date | null): string {
  return datetimeFormat(date, 'PPPP');
}
</script>
